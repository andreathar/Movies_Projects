"""Optional submission tracing. Receipts/ledger remain the cost authority.

No SDK import, credential-file read or network activity at module import. Only
allowlisted identifiers and typed credit observations cross the tracing boundary.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import uuid


def identifier(value):
    """Accept labels, never arbitrary prompts, URLs, paths or nested metadata."""
    if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}', value):
        return value
    return None


def context(film, job, payload_hash):
    try:
        metadata = json.loads(os.environ.get('RESPAN_METADATA', '{}'))
    except (TypeError, ValueError):
        metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    tags = {k: identifier(metadata.get(k)) for k in ('lane', 'role', 'task')}
    scene = identifier(os.environ.get('RESPAN_WORKFLOW_NAME')) or identifier(metadata.get('scene'))
    # Missing tags stay unassigned; a filename is not evidence of a scene/task.
    tags.update(project='Movies_Projects', script='kling_batch.py', episode=identifier(film.name),
                scene=scene, workflow=scene or 'kling_batch', job=identifier(job),
                execution_id=uuid.uuid4().hex,
                cost_event_id=hashlib.sha256(
                    json.dumps(['Kling', film.name, job, payload_hash]).encode()).hexdigest())
    return {k: v for k, v in tags.items() if v is not None}


def amount(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0)


def cost_attributes(envelope, result):
    """Read the validated release and reconcile result, not raw provider data."""
    attrs = {'cost_provider': 'Kling', 'cost_unit': 'Kling credits',
             'credit_quote_basis': 'unknown', 'credit_charge_basis': 'unknown',
             'cost_record_kind': 'submission', 'currency_conversion': 'none'}
    quote = envelope.get('quote') or {}
    if (quote.get('unit') == 'Kling credits' and amount(quote.get('credits'))
            and quote.get('basis') in {'official_panel', 'provider_quote'}):
        attrs.update(credit_quote=quote['credits'], credit_quote_basis=quote['basis'])
    if result is None:
        attrs['submission_state'] = 'local_error'
        return attrs
    attrs['submission_state'] = result['status'] if result.get('status') in {
        'SUBMITTED', 'SUBMISSION_UNKNOWN'} else 'unknown'
    generation = identifier(result.get('generationId'))
    if generation:
        attrs['generation_id'] = generation
    if result.get('chargeBasis') == 'provider_reported' and amount(result.get('creditsConsumed')):
        attrs.update(credit_charge=result['creditsConsumed'], credit_charge_basis='provider_reported')
    return attrs


def load_sdk():
    # Explicit instrumentations=[] prevents tracing other SDKs or request bodies.
    from respan import Respan, workflow, task
    from opentelemetry import trace
    client = Respan(app_name='kling_batch', instrumentations=[], is_auto_instrument=False,
                    customer_identifier='movies-projects', auto_flush='off')
    return client, workflow, task, trace.get_current_span


def warn():
    # Never stringify an SDK exception: it may contain headers, URLs or payloads.
    try:
        print('AVISO: Respan indisponível/incompleto; resultado e recibos Kling preservados; sem reenvio.',
              file=sys.stderr)
    except Exception:
        pass


def execute(tags, envelope, operation):
    """Execute exactly once, even when tracing fails before/after the callback.

    Decorated functions have no arguments and return None. Provider/local errors
    are held outside the decorator, then re-raised unchanged, so automatic SDK
    exception capture cannot export their potentially sensitive messages.
    """
    started = False
    result = None
    failure = None

    def once():
        nonlocal started, result, failure
        if started:
            return
        started = True  # Before all effects: never fall back to a second call.
        try:
            result = operation()
        except BaseException as error:
            failure = error

    enabled = (os.environ.get('MOVIES_KLING_RESPAN', '1').lower() not in {'0', 'false', 'no', 'off'}
               and bool(os.environ.get('RESPAN_API_KEY')))
    if not enabled:
        once()
    else:
        client = None
        try:
            client, workflow, task, current_span = load_sdk()

            def annotate(values):
                try:
                    span = current_span()
                    for key, value in values.items():
                        span.set_attribute('respan.metadata.' + key, value)
                except Exception:
                    warn()

            def submission():
                annotate(tags)
                once()
                try:
                    annotate(cost_attributes(envelope, result))
                except Exception:
                    warn()

            wrapped_submission = task(name='kling.submit')(submission)

            def execution():
                annotate(tags)  # No credit amounts on the parent: count once.
                try:
                    wrapped_submission()
                except Exception:
                    warn()

            workflow(name=tags['workflow'])(execution)()
        except Exception:
            warn()
        finally:
            if client is not None:
                try:
                    client.flush()
                except Exception:
                    warn()
        # Ordinary SDK failure can fall back before entry, cancellation cannot.
        once()
    if failure is not None:
        raise failure
    return result
