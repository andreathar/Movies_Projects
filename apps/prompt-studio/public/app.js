/* Prompt Studio UI — vanilla JS, talks to server.mjs. All prompt logic lives in engine.js. */
(function () {
  'use strict';
  const E = window.PromptEngine;
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const uid = () => Math.random().toString(36).slice(2, 9);

  const S = { projects: [], p: null, step: 'setup', integ: null, ui: { charId: null, comp: 'split-screen', outfitId: '', sceneKey: 'all' }, copy: [] };

  const STEPS = [
    { id: 'setup', t: 'Project setup', h: 'Name the project and choose the look, aspect ratio and platform models.' },
    { id: 'cast', t: 'Characters', h: 'Upload front and side headshots, describe each person, and add outfit references.' },
    { id: 'locations', t: 'Locations', h: 'Upload reference images for each scenario and describe the place.' },
    { id: 'script', t: 'Script', h: 'Paste the narrative. Scenes, cast and shots are detected automatically.' },
    { sep: 'Generate' },
    { id: 'sheets', t: 'Character sheets', h: 'Ready-to-paste sheet prompts for Higgsfield and Kling, plus Kling Element specs.' },
    { id: 'scenes', t: 'Scene references', h: 'Location plates and outfit sheets that anchor every shot.' },
    { id: 'shots', t: 'Shot prompts', h: 'Keyframe and video prompts per shot, with the exact platform tokens.' },
    { sep: 'Finish' },
    { id: 'naming', t: 'Naming guide', h: 'The tokens, tags and file names each platform expects.' },
    { id: 'export', t: 'Connect & export', h: 'Check your Kling / Higgsfield connections and export the full prompt pack.' },
  ];

  /* ------------------------------------------------------------ plumbing */
  async function api(path, opts = {}) {
    const r = await fetch('/api' + path, opts);
    const ct = r.headers.get('content-type') || '';
    const body = ct.includes('json') ? await r.json() : await r.text();
    if (!r.ok) throw new Error((body && body.error) || r.statusText);
    return body;
  }
  let saveTimer = null;
  function dirty() {
    $('#saveState').textContent = 'Saving…';
    clearTimeout(saveTimer);
    saveTimer = setTimeout(async () => {
      try { await api('/projects/' + S.p.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(S.p) }); $('#saveState').textContent = 'Saved'; }
      catch (e) { $('#saveState').textContent = 'Save failed: ' + e.message; }
    }, 450);
  }
  function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 1700); }
  const getPath = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
  function setPath(o, path, v) {
    const ks = path.split('.'); let cur = o;
    ks.slice(0, -1).forEach((k, i) => { if (cur[k] == null) cur[k] = /^\d+$/.test(ks[i + 1]) ? [] : {}; cur = cur[k]; });
    cur[ks[ks.length - 1]] = v;
  }
  const img = (rel) => `/api/projects/${S.p.id}/file?p=${encodeURIComponent(rel)}`;
  const regCopy = (text) => { S.copy.push(text); return S.copy.length - 1; };

  /* ----------------------------------------------------------- components */
  function field(label, path, { type = 'text', ph = '', rows = 0, rerender = false, opts = null } = {}) {
    const v = getPath(S.p, path);
    const rr = rerender ? ' data-rerender="1"' : '';
    let el;
    if (opts) el = `<select data-bind="${path}"${rr}>${opts.map(([val, lab]) => `<option value="${esc(val)}"${val === (v ?? '') ? ' selected' : ''}>${esc(lab)}</option>`).join('')}</select>`;
    else if (rows) el = `<textarea rows="${rows}" data-bind="${path}" placeholder="${esc(ph)}"${rr}>${esc(v || '')}</textarea>`;
    else el = `<input type="${type}" data-bind="${path}" value="${esc(v || '')}" placeholder="${esc(ph)}"${rr}>`;
    return `<div class="field"><label>${esc(label)}</label>${el}</div>`;
  }
  function dropSingle(label, path) {
    const v = getPath(S.p, path);
    return `<div class="field"><label>${esc(label)}</label><div class="drop" data-up="${path}">${v ? `<img src="${img(v)}" alt="${esc(label)}"><button class="rm" data-rm="${path}" title="Remove">✕</button>` : `<div>＋ Drop image or click<small>PNG · JPG · WEBP</small></div>`}</div></div>`;
  }
  function dropMulti(label, path, max = 6) {
    const arr = getPath(S.p, path) || [];
    return `<div class="field"><label>${esc(label)} <small>(${arr.length}/${max})</small></label><div class="thumbs">${arr.map((r, i) => `<div class="thumb"><img src="${img(r)}" alt=""><button class="rm" data-rmi="${path}:${i}">✕</button></div>`).join('')}${arr.length < max ? `<div class="add-thumb" data-upm="${path}" title="Add image">＋</div>` : ''}</div></div>`;
  }
  function lintHtml(list) {
    if (!list.length) return '<div class="lint"><span class="badge b-ok">✓ prompt checks passed</span></div>';
    return `<div class="lint">${list.map((x) => `<div><span class="badge ${x.level === 'error' ? 'b-err' : x.level === 'warn' ? 'b-warn' : 'b-info'}">${x.level}</span> ${esc(x.msg)}</div>`).join('')}</div>`;
  }
  function promptBlock(title, text, { lint = null, meta = [], extra = '' } = {}) {
    const i = regCopy(text);
    return `<div class="prompt"><div class="ph"><b>${esc(title)}</b><span class="badge b-info">${E.words(text)} words</span><span class="sp"></span><button class="btn ghost sm" data-copy="${i}">Copy</button></div><pre>${esc(text)}</pre>${meta.length ? `<div class="meta">${meta.join('')}</div>` : ''}${extra}${lint ? lintHtml(lint) : ''}</div>`;
  }
  const kv = (k, v) => `<span>${esc(k)}: <code>${esc(v)}</code></span>`;
  const empty = (msg, stepId, btn) => `<div class="card empty"><p>${msg}</p>${stepId ? `<button class="btn" data-go="${stepId}">${btn}</button>` : ''}</div>`;

  /* ------------------------------------------------------------ readiness */
  function readiness(p) {
    const r = [];
    if (!p.consent) r.push({ level: 'err', step: 'setup', msg: 'Confirm you have the right to use every face you upload (Project setup).' });
    if (!p.characters.length) r.push({ level: 'err', step: 'cast', msg: 'Add at least one character.' });
    p.characters.forEach((c) => {
      if (!c.images?.front) r.push({ level: 'warn', step: 'cast', msg: `${c.name || 'Character'}: front headshot missing.` });
      if (!c.images?.side) r.push({ level: 'warn', step: 'cast', msg: `${c.name || 'Character'}: side headshot missing.` });
      if (!(c.outfits || []).length) r.push({ level: 'warn', step: 'cast', msg: `${c.name || 'Character'}: no outfit defined.` });
      if (!c.klingElementId) r.push({ level: 'info', step: 'sheets', msg: `${c.name}: no Kling Element id yet — shot prompts show a placeholder until you create the Element and paste its id.` });
    });
    if (!p.locations.length) r.push({ level: 'warn', step: 'locations', msg: 'No locations added.' });
    p.locations.forEach((l) => { if (!(l.images || []).length) r.push({ level: 'warn', step: 'locations', msg: `${l.name || 'Location'}: no reference image.` }); });
    if (!p.script.trim()) r.push({ level: 'err', step: 'script', msg: 'Script is empty.' });
    return r;
  }
  function stepStatus(id) {
    const p = S.p; if (!p) return '';
    const bad = (x) => readiness(p).some((r) => r.step === id && r.level !== 'info');
    if (id === 'setup') return p.consent && p.title ? 'ok' : 'warn';
    if (id === 'cast') return p.characters.length && !bad('cast') ? 'ok' : 'warn';
    if (id === 'locations') return p.locations.length && !bad('locations') ? 'ok' : 'warn';
    if (id === 'script') return p.script.trim() ? 'ok' : 'warn';
    return '';
  }

  /* ---------------------------------------------------------------- steps */
  function viewSetup() {
    const p = S.p;
    const styles = Object.entries(E.STYLE_PRESETS).map(([k, v]) => `<div class="opt-card${p.style === k ? ' on' : ''}" data-style="${k}"><b>${esc(v.label)}</b><small>${esc(v.tail.split(',').slice(0, 2).join(','))}</small></div>`).join('');
    return `<div class="card"><h2>Project</h2><div class="grid g2">${field('Title', 'title', { rerender: false })}
      ${field('Dialogue language', 'dialogueLanguage', { ph: 'English' })}</div>
      <div class="grid g3">${field('Video aspect ratio', 'aspect', { opts: [['16:9', '16:9 landscape'], ['9:16', '9:16 vertical'], ['1:1', '1:1 square']] })}
      ${field('Default camera', 'defaultCamera', { opts: Object.keys(E.CAMERA).map((k) => [k, k]) })}</div>
      <div class="field"><label><input type="checkbox" data-bindc="consent" ${p.consent ? 'checked' : ''}> I own, or have written permission to use, every face and likeness I upload.</label>
      <small>Character-sheet and shot prompts stay locked until this is ticked.</small></div></div>
      <div class="card"><h2>Visual style</h2><div class="grid g3">${styles}</div></div>
      <div class="card"><h2>Platform models</h2><p class="muted">Defaults follow the live catalogues. Confirm what your account can use in <b>Connect &amp; export</b>.</p>
      <div class="grid g4">${field('Kling image model', 'kling.imageModel', { opts: E.KLING_IMAGE_MODELS.map((m) => [m, m]) })}
      ${field('Kling video model', 'kling.videoModel', { opts: E.KLING_VIDEO_MODELS.map((m) => [m, m]) })}
      ${field('Higgsfield image model', 'higgsfield.imageModel', { opts: E.HIGGS_IMAGE_MODELS.map((m) => [m, m]) })}
      ${field('Higgsfield video model', 'higgsfield.videoModel', { opts: Object.entries(E.HIGGS_VIDEO_MODELS).map(([m, v]) => [m, `${v.label}`]) })}</div></div>`;
  }

  function viewCast() {
    const p = S.p;
    const cards = p.characters.map((c, i) => {
      const b = `characters.${i}`;
      return `<div class="card"><div class="hdr"><h2>${esc(c.name || 'New character')}</h2><button class="btn danger sm" data-del="characters:${i}">Remove</button></div>
      <div class="grid g3">${dropSingle('Front headshot', b + '.images.front')}${dropSingle('Side headshot', b + '.images.side')}
        <div>${dropMulti('Extra angles (optional)', b + '.images.extra', 2)}<small>Kling Elements take a cover + 1–3 secondary images; extras raise identity accuracy.</small></div></div>
      <div class="grid g3">${field('Name', b + '.name')}${field('Role in story', b + '.role', { ph: 'protagonist' })}
        ${field('Pronouns used in prompts', b + '.pronouns', { opts: [['they', 'they/them'], ['he', 'he/him'], ['she', 'she/her']] })}</div>
      <div class="grid g3">${field('Age', b + '.age', { ph: 'man in his late thirties' })}${field('Skin tone', b + '.skin', { ph: 'olive skin' })}${field('Build', b + '.build', { ph: 'lean build' })}</div>
      <div class="grid g3">${field('Face', b + '.face', { ph: 'angular jaw, defined cheekbones' })}${field('Hair', b + '.hair', { ph: 'short dark wavy hair' })}${field('Eyes', b + '.eyes', { ph: 'dark brown, slightly deep-set' })}</div>
      <div class="grid g2">${field('Distinguishing features', b + '.distinct', { ph: 'small scar on left eyebrow' })}
        ${field('Kling Element id (paste after creating the Element)', b + '.klingElementId', { ph: '323525046658711' })}</div>
      <h3>Outfits</h3>
      ${(c.outfits || []).map((o, j) => `<div class="subcard"><div class="hdr"><b>${esc(o.name || 'Outfit')}</b><button class="btn danger sm" data-del="characters.${i}.outfits:${j}">Remove</button></div>
        <div class="grid g2">${field('Outfit name', `${b}.outfits.${j}.name`, { ph: 'Grey jacket' })}${field('Description (cut, material, colour, details, shoes, accessories)', `${b}.outfits.${j}.description`, { rows: 3, ph: 'grey pinstripe wool jacket over a white striped shirt, open collar, dark trousers, brown leather shoes' })}</div>
        ${dropMulti('Outfit reference images', `${b}.outfits.${j}.refs`, 6)}</div>`).join('')}
      <button class="btn ghost sm" style="margin-top:10px" data-addoutfit="${i}">＋ Add outfit</button></div>`;
    }).join('');
    return (cards || empty('No characters yet.')) + `<button class="btn" data-addchar>＋ Add character</button>`;
  }

  function viewLocations() {
    const p = S.p;
    const cards = p.locations.map((l, i) => {
      const b = `locations.${i}`;
      return `<div class="card"><div class="hdr"><h2>${esc(l.name || 'New location')}</h2><button class="btn danger sm" data-del="locations:${i}">Remove</button></div>
      <div class="grid g2"><div>${dropMulti('Reference images', b + '.images', 6)}</div><div>${field('Name (as in the script heading)', b + '.name', { ph: 'Oak Dining Room' })}${field('Description', b + '.description', { rows: 3, ph: 'pale oak table, tall arched window, plaster walls, wooden floor' })}</div></div>
      <div class="grid g3">${field('Time of day', b + '.time', { ph: 'dusk' })}${field('Mood', b + '.mood', { ph: 'quiet, intimate' })}${field('Palette', b + '.palette', { ph: 'warm ochre, grey-green' })}</div></div>`;
    }).join('');
    return (cards || empty('No locations yet.')) + `<button class="btn" data-addloc>＋ Add location</button>`;
  }

  const SAMPLE = `INT. OAK DINING ROOM - DUSK

Andre sits at the pale oak table and looks across it at an empty chair.

ANDRE (softly): Do you remember this table?

He lowers his eyes to the faint ring stain near the edge and rests two fingers on it.

ANDRE: It has waited a long time for us.

EXT. COURTYARD - NIGHT

Andre walks through the courtyard, stops at the fountain, and looks up at the lit window.
`;
  function viewScript() {
    const p = S.p;
    return `<div class="card"><div class="hdr"><h2>Script</h2><button class="btn ghost sm" data-sample>Load example</button></div>
      <p class="muted">Use scene headings (<code>INT. PLACE - TIME</code>), <code>NAME: line</code> or Fountain-style speaker lines, and plain action paragraphs. Each action or dialogue line becomes a shot.</p>
      ${field('', 'script', { rows: 14, ph: 'INT. KITCHEN - MORNING\n\nMARIA (softly): Good morning.' })}</div><div id="scriptPreview">${scriptPreview()}</div>`;
  }
  function scriptPreview() {
    const p = S.p;
    const { scenes, shots } = E.buildShots(p);
    if (!scenes.length) return '';
    const unknown = new Set();
    scenes.forEach((sc) => sc.beats.forEach((b) => { if (b.type === 'dialogue' && !p.characters.find((c) => c.name.toLowerCase() === b.character.toLowerCase())) unknown.add(b.character); }));
    return `<div class="card"><h2>Detected: ${scenes.length} scene(s) · ${shots.length} shot(s)</h2>
      ${unknown.size ? `<div class="banner warn">Speakers without a character card: <b>${[...unknown].map(esc).join(', ')}</b>. Add them in Characters (names must match).</div>` : ''}
      ${scenes.map((sc) => {
        const r = E.resolveScene(p, sc); const ss = (p.sceneSettings || {})['S' + E.pad(sc.index)] || {};
        return `<div class="subcard"><b>Scene ${sc.index} — ${esc(sc.heading)}</b> <small>${sc.beats.length} beats</small>
          <div class="grid g3" style="margin-top:8px"><div class="field"><label>Location</label><select data-scene="S${E.pad(sc.index)}.locationId"><option value="">${r.location && !ss.locationId ? 'Auto: ' + esc(r.location.name) : 'None'}</option>${p.locations.map((l) => `<option value="${l.id}"${ss.locationId === l.id ? ' selected' : ''}>${esc(l.name)}</option>`).join('')}</select></div>
          ${r.cast.map((c) => `<div class="field"><label>${esc(c.name)} outfit</label><select data-scene="S${E.pad(sc.index)}.outfits.${c.id}">${(c.outfits || []).length ? c.outfits.map((o) => `<option value="${o.id}"${(ss.outfits || {})[c.id] === o.id ? ' selected' : ''}>${esc(o.name)}</option>`).join('') : '<option value="">(no outfit)</option>'}</select></div>`).join('')}</div></div>`;
      }).join('')}</div>`;
  }

  function gate() {
    const p = S.p;
    if (!p.consent) return `<div class="banner err">Tick the likeness-rights confirmation in <b>Project setup</b> to unlock prompts that use uploaded faces. <button class="btn sm" data-go="setup">Go to setup</button></div>`;
    if (!p.characters.length) return empty('Add a character first.', 'cast', 'Add characters');
    return '';
  }

  function viewSheets() {
    const p = S.p; const g = gate(); if (g) return g;
    const c = p.characters.find((x) => x.id === S.ui.charId) || p.characters[0]; S.ui.charId = c.id;
    const outfit = (c.outfits || []).find((o) => o.id === S.ui.outfitId) || (c.outfits || [])[0] || null;
    const comp = S.ui.comp;
    const hs = E.higgsfieldCharacterSheet(p, c, outfit, comp);
    const ks = E.klingCharacterSheet(p, c, outfit, comp);
    const el = E.klingElementSpecCharacter(p, c);
    const lintH = E.lintPrompt(hs.prompt, { target: 'higgsfield', kind: 'sheet' });
    const lintK = E.lintPrompt(ks.promptCli, { target: 'kling-cli', kind: 'sheet', imageCount: ks.images.length });
    const lintA = E.lintPrompt(ks.promptApp, { target: 'kling-app', kind: 'sheet' });
    const warnImg = !c.images?.front || !c.images?.side ? `<div class="banner warn">Upload both front and side headshots on the Characters step — sheets are most faithful with both.</div>` : '';
    return `${warnImg}
      <div class="card tight"><div class="row">${p.characters.length > 1 ? p.characters.map((x) => `<span class="chip${x.id === c.id ? ' on' : ''}" data-char="${x.id}">${esc(x.name)}</span>`).join('') + '<span class="sep" style="width:1px;height:20px"></span>' : ''}
        ${Object.entries(E.COMPOSITIONS).map(([k, v]) => `<span class="chip${k === comp ? ' on' : ''}" data-comp="${k}">${esc(v.label)}</span>`).join('')}</div>
        ${(c.outfits || []).length ? `<div class="row" style="margin-top:10px"><label style="margin:0">Outfit</label><select style="max-width:260px" data-outfitpick>${c.outfits.map((o) => `<option value="${o.id}"${outfit && o.id === outfit.id ? ' selected' : ''}>${esc(o.name)}</option>`).join('')}</select></div>` : '<p class="muted" style="margin:10px 0 0">No outfit defined — sheets show the person without a costume description.</p>'}</div>
      <div class="grid g2"><div>
        <div class="card"><h2>Higgsfield</h2>
        ${promptBlock(`generate_image · ${hs.model}`, hs.prompt, { lint: lintH, meta: [kv('aspect_ratio', hs.aspect_ratio), kv('file', hs.fileName), kv('save element as', hs.elementName)] })}
        <h3>Attach as <code>image_references</code></h3><ul>${hs.references.map((r) => `<li>${esc(r.label)} — <code>${esc(r.file)}</code></li>`).join('') || '<li class="muted">No reference images uploaded.</li>'}</ul>
        <ul class="muted">${hs.notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul></div></div>
      <div>
        <div class="card"><h2>Kling</h2>
        ${promptBlock(`CLI prompt · ${ks.tool} · ${ks.model}`, ks.promptCli, { lint: lintK, meta: [kv('aspect_ratio', ks.aspect_ratio), kv('file', ks.fileName)] })}
        ${promptBlock('App / web prompt (@ handles)', ks.promptApp, { lint: lintA })}
        ${promptBlock('CLI command (copy to your terminal)', ks.cli)}
        <table><tr><th>CLI token</th><th>App token</th><th>Image</th></tr>${ks.tokenMap.map((t) => `<tr><td><code>${esc(t.cli)}</code></td><td><code>${esc(t.app)}</code></td><td>${esc(t.label)}</td></tr>`).join('') || '<tr><td colspan="3" class="muted">No images attached.</td></tr>'}</table>
        <ul class="muted">${ks.notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul></div></div></div>
      <div class="card"><h2>Kling Element for ${esc(c.name)}</h2>
        <div class="row"><span class="badge b-info">tag: ${el.tag}</span><span class="badge b-info">name: ${esc(el.name)}</span></div>
        ${el.problems.map((m) => `<div class="banner warn" style="margin-top:8px">${esc(m)}</div>`).join('')}
        <p class="muted">Cover: <code>${esc(el.cover || '—')}</code> · Secondary: ${el.secondary.map((s) => `<code>${esc(s)}</code>`).join(' ') || '—'}</p>
        ${el.cli ? promptBlock('element_create', el.cli) : ''}<p class="muted">${esc(el.note)} After creation, paste the returned id on the character card; shot prompts then switch from a placeholder to <code>&lt;&lt;&lt;id&gt;&gt;&gt;</code> and bind with <code>--elements</code>.</p></div>`;
  }

  function viewScenes() {
    const p = S.p; const g = gate(); if (g) return g;
    const locs = p.locations.map((l) => {
      const plates = E.locationPlates(p, l); const el = E.klingElementSpecScene(p, l);
      return `<div class="card"><h2>${esc(l.name)}</h2>${(l.images || []).length ? `<div class="thumbs">${l.images.map((r) => `<div class="thumb"><img src="${img(r)}" alt=""></div>`).join('')}</div>` : '<div class="banner warn">No reference image uploaded.</div>'}
        ${plates.map((pl, i) => `<details${i === 0 ? ' open' : ''} class="subcard"><summary><b>${esc(pl.label)}</b> <span class="badge b-info">${pl.aspect_ratio}</span> <small>${esc(pl.fileName)}</small></summary>
          <div class="grid g2"><div>${promptBlock(`Higgsfield · ${pl.higgsfield.model}`, pl.higgsfield.prompt, { lint: E.lintPrompt(pl.higgsfield.prompt, { target: 'higgsfield' }), meta: [kv('element', pl.higgsfield.elementName)] })}</div>
          <div>${promptBlock(`Kling CLI · ${pl.kling.tool}`, pl.kling.promptCli, { lint: E.lintPrompt(pl.kling.promptCli, { target: 'kling-cli', imageCount: pl.kling.images.length }) })}${promptBlock('Kling app', pl.kling.promptApp)}${promptBlock('CLI command', pl.kling.cli)}</div></div></details>`).join('')}
        <h3 style="margin-top:12px">Kling Element (Scenes)</h3>${el.problems.map((m) => `<div class="banner warn">${esc(m)}</div>`).join('')}${el.cli ? promptBlock('element_create', el.cli) : ''}</div>`;
    }).join('');
    const outs = p.characters.flatMap((c) => (c.outfits || []).map((o) => ({ c, o }))).map(({ c, o }) => {
      const sh = E.outfitSheet(p, c, o); const el = E.klingElementSpecCostume(p, c, o);
      return `<div class="card"><h2>Outfit — ${esc(c.name)} / ${esc(o.name)}</h2><div class="grid g2"><div>${promptBlock(`Higgsfield · ${sh.higgsfield.model}`, sh.higgsfield.prompt, { meta: [kv('file', sh.fileName), kv('element', sh.higgsfield.elementName)] })}</div>
        <div>${promptBlock(`Kling CLI · ${sh.kling.tool}`, sh.kling.promptCli)}${promptBlock('Kling app', sh.kling.promptApp)}</div></div>
        ${el.problems.map((m) => `<div class="banner warn">${esc(m)}</div>`).join('')}${el.cli ? promptBlock('Costumes element_create', el.cli) : ''}</div>`;
    }).join('');
    return (locs || empty('No locations yet.', 'locations', 'Add locations')) + outs;
  }

  function viewShots() {
    const p = S.p; const g = gate(); if (g) return g;
    const { scenes, shots } = E.buildShots(p);
    if (!shots.length) return empty('No shots yet — write or paste a script first.', 'script', 'Go to script');
    const sel = S.ui.sceneKey;
    const list = shots.filter((s) => sel === 'all' || s.sceneKey === sel);
    const elementIds = p.characters.map((c) => c.klingElementId).filter(Boolean);
    const chips = `<div class="card tight"><div class="row"><span class="chip${sel === 'all' ? ' on' : ''}" data-scenekey="all">All scenes</span>${scenes.map((sc) => `<span class="chip${sel === 'S' + E.pad(sc.index) ? ' on' : ''}" data-scenekey="S${E.pad(sc.index)}">Scene ${sc.index}</span>`).join('')}</div></div>`;
    return chips + list.map((s, idx) => {
      const sp = E.shotPrompts(p, s);
      const ov = (p.shotOverrides || {})[s.id] || {};
      const dl = s.type === 'dialogue' ? s.text : '';
      const lk = E.lintPrompt(sp.kling.video.promptCli, { target: 'kling-cli', kind: 'i2v', dialogue: dl, elementIds });
      const la = E.lintPrompt(sp.kling.video.promptApp, { target: 'kling-app', kind: 'i2v', dialogue: dl });
      const kk = E.lintPrompt(sp.kling.keyframe.promptCli, { target: 'kling-cli', kind: 'sheet', imageCount: sp.kling.keyframe.images.length });
      const errs = [...lk, ...kk].filter((x) => x.level === 'error').length;
      const hv = sp.higgsfield.video;
      return `<details class="card"${idx === 0 ? ' open' : ''}><summary><b>${s.id}</b> <span class="badge b-info">${s.type}</span> <span class="badge ${errs ? 'b-err' : 'b-ok'}">${errs ? errs + ' issue(s)' : 'checks ok'}</span> <small>${s.duration}s · ${esc((s.character ? s.character + ': ' : '') + s.text.slice(0, 90))}</small></summary>
        <div class="row" style="margin:10px 0"><div style="width:120px"><label>Duration (s)</label><input type="number" min="2" max="30" data-bind="shotOverrides.${s.id}.duration" data-num data-rerender value="${s.duration}"></div>
        <div style="width:220px"><label>Camera</label><select data-bind="shotOverrides.${s.id}.camera" data-rerender>${Object.keys(E.CAMERA).map((k) => `<option value="${k}"${(ov.camera || p.defaultCamera || 'locked') === k ? ' selected' : ''}>${k}</option>`).join('')}</select></div>
        <div><small>Files: <code>${esc(sp.fileNames.keyframe)}</code> → <code>${esc(sp.fileNames.video)}</code></small></div></div>
        <h3>1 · Keyframe (first frame)</h3><div class="grid g3">
          <div>${promptBlock(`Kling CLI · ${sp.kling.keyframe.tool}`, sp.kling.keyframe.promptCli, { lint: kk, meta: [kv('model', sp.kling.keyframe.model)], extra: sp.kling.keyframe.images.length ? `<div class="meta">${sp.kling.keyframe.images.map((r, i) => `<span>图片${i + 1} = <code>${esc(r.file)}</code></span>`).join('')}</div>` : '' })}</div>
          <div>${promptBlock('Kling app', sp.kling.keyframe.promptApp)}</div>
          <div>${promptBlock(`Higgsfield · ${sp.higgsfield.keyframe.model}`, sp.higgsfield.keyframe.prompt, { meta: [kv('aspect_ratio', sp.higgsfield.keyframe.aspect_ratio)], extra: `<div class="meta">${sp.higgsfield.keyframe.references.map((r) => `<span>image_references: <code>${esc(r.file)}</code></span>`).join('') || '<span>No reference images</span>'}</div>` })}</div></div>
        <h3>2 · Video</h3><div class="grid g3">
          <div>${promptBlock(`Kling CLI · ${sp.kling.video.args.model}`, sp.kling.video.promptCli, { lint: lk, meta: [kv('duration', sp.kling.video.args.duration), kv('enable_audio', sp.kling.video.args.enable_audio), kv('prefer_multi_shots', 'false')] })}${promptBlock('CLI command', sp.kling.video.cli)}</div>
          <div>${promptBlock('Kling app (native-audio syntax)', sp.kling.video.promptApp, { lint: la })}</div>
          <div>${promptBlock(`Higgsfield · ${hv.model}`, hv.prompt, { meta: [kv('duration', hv.duration), kv('aspect_ratio', hv.aspect_ratio), hv.audio ? kv(hv.audio.param, hv.audio.value) : ''], extra: `<div class="meta">${hv.references.map((r) => `<span>${r.role}: <code>${esc(r.file)}</code></span>`).join('')}</div>` })}</div></div></details>`;
    }).join('');
  }

  function viewNaming() {
    const p = S.p;
    const ex = p.characters[0] ? p.characters[0].name : 'Andre';
    return `<div class="card"><h2>Reference tokens — which syntax goes where</h2><table>
      <tr><th>What you reference</th><th>Kling CLI / MCP</th><th>Kling app / web</th><th>Higgsfield</th></tr>
      <tr><td>Input image N</td><td><code>图片1</code>, <code>图片2</code> … (literal, = image_N, in <code>--image</code> order)</td><td><code>@Image1</code></td><td>Attach with role <code>image_references</code> / <code>start_image</code> / <code>end_image</code>; describe by role in the prompt</td></tr>
      <tr><td>Saved character (Element)</td><td><code>&lt;&lt;&lt;ID&gt;&gt;&gt;</code> <b>and</b> <code>--elements '[{"id":"ID","bindName":"${esc(E.klingElementName(ex))}"}]'</code></td><td><code>@${esc(E.klingElementName(ex))}</code></td><td>Saved reference element <code>${esc(E.higgsElementName('char', ex, 1))}</code></td></tr>
      <tr><td>Reference video</td><td><code>视频1</code> (omni_ref_video only)</td><td><code>@video</code></td><td>role <code>video_references</code></td></tr>
      <tr><td>First / last frame</td><td><code>--input first_image=…</code> / <code>tail_image</code></td><td>Upload start / end frame</td><td>roles <code>start_image</code> / <code>end_image</code></td></tr>
      <tr><td>Dialogue (native audio)</td><td>Prose: <code>Name says: "line"</code>, set <code>enable_audio</code></td><td><code>Name (soft, in English): "line"</code></td><td>Model-dependent audio flag (<code>generate_audio</code> / <code>sound</code>)</td></tr>
      <tr><td>Exclusions</td><td>In the prompt body (<em>no negative_prompt</em> on v3/o1)</td><td>Same</td><td>Negative tail in the prompt; some models have a negative field</td></tr></table>
      <p class="muted">Never mix them: <code>@</code> handles in CLI prompts and <code>&lt;&lt;&lt;id&gt;&gt;&gt;</code> in app prompts do not bind anything. Prompts are written in English; only dialogue text uses the target language.</p></div>
      <div class="grid g2"><div class="card"><h2>Kling Element tags</h2><p>Exactly one or more of:</p><div class="row">${E.KLING_TAGS.map((t) => `<span class="badge b-info">${t}</span>`).join('')}</div>
      <ul><li>Image Element = <b>1 cover + 1–3 secondary</b> images. Video Element = one video, 3–60 s.</li><li>The cover cannot be changed later; secondary images are replaced as a list.</li><li>Elements only work in tools whose model lists an <code>elements</code> argument (not in text-to-image / text-to-video).</li><li>Characters → <code>Characters</code>, outfits → <code>Costumes</code>, locations → <code>Scenes</code>, props → <code>Items</code>.</li></ul></div>
      <div class="card"><h2>File &amp; element naming (used in every export)</h2>
      <p><code>&lt;project&gt;_&lt;kind&gt;_&lt;subject&gt;_&lt;variant&gt;_vNN.&lt;ext&gt;</code></p>
      <table><tr><th>kind</th><th>meaning</th><th>example</th></tr>
      <tr><td><code>char</code></td><td>character sheet / headshot</td><td><code>${esc(E.assetName({ project: p.title, kind: 'char', subject: ex, variant: 'split-screen', version: 1 }))}</code></td></tr>
      <tr><td><code>outfit</code></td><td>costume sheet</td><td><code>${esc(E.assetName({ project: p.title, kind: 'outfit', subject: ex, variant: 'grey-jacket', version: 1 }))}</code></td></tr>
      <tr><td><code>loc</code></td><td>location plate</td><td><code>${esc(E.assetName({ project: p.title, kind: 'loc', subject: 'oak room', variant: 'wide', version: 1 }))}</code></td></tr>
      <tr><td><code>shot</code></td><td>keyframe</td><td><code>${esc(E.assetName({ project: p.title, kind: 'shot', subject: 'S01_SH01', variant: 'keyframe', version: 1 }))}</code></td></tr>
      <tr><td><code>vid</code></td><td>video take</td><td><code>${esc(E.assetName({ project: p.title, kind: 'vid', subject: 'S01_SH01', variant: 'take', version: 1, ext: 'mp4' }))}</code></td></tr></table>
      <p class="muted">Higgsfield elements: <code>char_&lt;slug&gt;_vN</code>, <code>outfit_…</code>, <code>loc_…</code>, <code>prop_…</code>. Kling Elements: PascalCase, no spaces (<code>${esc(E.klingElementName(ex))}</code>).</p></div></div>
      <div class="card"><h2>Prompt rules baked into the generator</h2><ul>
      <li><b>Image-to-video:</b> the image is the engine — prompt = subject + one action + camera + preservation + exclusions. Never redescribe the scene.</li>
      <li><b>One action per shot with an end point</b> ("…then settles still") to avoid drift or stuck generations.</li>
      <li><b>Camera always explicit</b> (default: locked, one continuous shot, no cuts).</li>
      <li><b>Pin defaults:</b> <code>prefer_multi_shots=false</code>; <code>enable_audio</code> only for dialogue shots.</li>
      <li><b>Dialogue:</b> exact script line, 1–2 sentences; duration ≈ spoken seconds + 2; ask for "quiet room tone only, no music" unless you want music.</li>
      <li><b>Character sheets (Higgsfield):</b> composition → identity → face/eyes/hair → realism module → body → head-to-toe wardrobe → lighting → quality tail → negative tail; single subject, standing full body left, close-up right.</li>
      <li><b>Pronouns</b> come from the character card; if unset, prompts use they/them. Nothing is inferred from a name.</li></ul></div>`;
  }

  function viewExport() {
    const p = S.p; const rd = readiness(p); const i = S.integ;
    const klingOk = i && i.kling.installed;
    return `<div class="card"><h2>Readiness</h2>${rd.length ? rd.map((r) => `<div class="banner ${r.level === 'err' ? 'err' : 'warn'}" style="${r.level === 'info' ? 'background:var(--accent-soft);color:var(--accent)' : ''}">${esc(r.msg)} <button class="btn ghost sm" data-go="${r.step}">Fix</button></div>`).join('') : '<span class="badge b-ok">✓ Everything needed is in place</span>'}</div>
      <div class="grid g2"><div class="card"><h2>Kling connection</h2>
        ${i ? `<p>${klingOk ? `<span class="badge b-ok">CLI found</span> <code>${esc(i.kling.path)}</code> ${i.kling.version ? '· ' + esc(i.kling.version) : ''}` : '<span class="badge b-warn">kling CLI not found</span> Install the official CLI for your region (<code>npm i -g @klingai/cli-global</code> or <code>@klingai/cli-cn</code>) and run <code>kling login</code>.'}</p>` : '<p class="muted">Checking…</p>'}
        <div class="row">${['who_am_i', 'account', 'tool_list', 'element_list'].map((k) => `<button class="btn ghost sm" data-kling="${k}" ${klingOk ? '' : 'disabled'}>${k}</button>`).join('')}</div>
        <p class="muted">Read-only checks: confirm login, balance and the live model schemas before pasting any command. This app never runs generation, upload or delete.</p>
        <pre class="out" id="klingOut" hidden></pre>
        <a class="btn ghost sm" href="https://app.klingai.com/global" target="_blank" rel="noopener">Open Kling</a></div>
      <div class="card"><h2>Higgsfield connection</h2>
        <p>${i && i.higgsfield.cli ? '<span class="badge b-ok">CLI found</span>' : '<span class="badge b-info">via MCP / web</span>'} ${i ? esc(i.higgsfield.note) : ''}</p>
        <ul class="muted"><li>In Claude Code with the Higgsfield connector: paste a prompt, or load <code>higgsfield/requests-draft.json</code> and ask it to run item by item (it should check <code>balance</code> and quote first).</li><li>Character sheets: workflow <code>character-sheet</code>; then save the accepted sheet as a reference element with the suggested <code>char_…</code> name.</li></ul>
        <a class="btn ghost sm" href="https://higgsfield.ai" target="_blank" rel="noopener">Open Higgsfield</a></div></div>
      <div class="card"><h2>Export</h2><p>Creates a folder on this computer with the Markdown pack, JSON, Kling request drafts (blocked until you review them), Higgsfield request drafts, and your uploads renamed to the project convention.</p>
        <div class="row"><button class="btn" data-export>Export pack to disk</button><a class="btn ghost" href="/api/projects/${p.id}/markdown" download>Download Markdown</a></div><pre class="out" id="exportOut" hidden></pre></div>`;
  }

  const VIEWS = { setup: viewSetup, cast: viewCast, locations: viewLocations, script: viewScript, sheets: viewSheets, scenes: viewScenes, shots: viewShots, naming: viewNaming, export: viewExport };

  /* ---------------------------------------------------------------- render */
  function renderSide() {
    $('#steps').innerHTML = STEPS.map((s, i) => s.sep ? `<div class="sep"></div><small style="padding:0 10px">${s.sep}</small>` :
      `<button class="step${S.step === s.id ? ' on' : ''}" data-go="${s.id}"><span class="n">${STEPS.filter((x) => !x.sep).indexOf(s) + 1}</span>${esc(s.t)}<span class="dot ${stepStatus(s.id)}"></span></button>`).join('');
    $('#projectSelect').innerHTML = S.projects.map((p) => `<option value="${p.id}"${S.p && p.id === S.p.id ? ' selected' : ''}>${esc(p.title)}</option>`).join('');
  }
  function render() {
    S.copy = [];
    const st = STEPS.find((s) => s.id === S.step);
    $('#stepTitle').textContent = st.t; $('#stepHint').textContent = st.h;
    renderSide();
    const keepY = window.scrollY;
    $('#view').innerHTML = S.p ? VIEWS[S.step]() : '';
    const idx = STEPS.filter((s) => !s.sep).findIndex((s) => s.id === S.step);
    const order = STEPS.filter((s) => !s.sep);
    $('#topActions').innerHTML = `${idx > 0 ? `<button class="btn ghost" data-go="${order[idx - 1].id}">← Back</button>` : ''}${idx < order.length - 1 ? `<button class="btn" data-go="${order[idx + 1].id}">Next: ${esc(order[idx + 1].t)} →</button>` : ''}`;
    window.scrollTo(0, keepY);
  }
  function go(id) { S.step = id; render(); window.scrollTo(0, 0); }

  /* ---------------------------------------------------------------- events */
  document.addEventListener('input', (e) => {
    const t = e.target;
    if (t.dataset.bind) {
      let v = t.value; if (t.hasAttribute('data-num')) v = Number(v) || 0;
      setPath(S.p, t.dataset.bind, v); dirty();
      if (t.dataset.bind === 'script') $('#scriptPreview').innerHTML = scriptPreview();
      if (t.dataset.bind.endsWith('.name') || t.dataset.bind === 'title') renderSide();
    }
  });
  document.addEventListener('change', (e) => {
    const t = e.target;
    if (t.dataset.bindc) { setPath(S.p, t.dataset.bindc, t.checked); dirty(); render(); return; }
    if (t.dataset.rerender) { setPath(S.p, t.dataset.bind, t.hasAttribute('data-num') ? Number(t.value) || 0 : t.value); dirty(); render(); return; }
    if (t.dataset.bind && t.tagName === 'SELECT') { setPath(S.p, t.dataset.bind, t.value); dirty(); }
    if (t.dataset.scene) { setPath(S.p, 'sceneSettings.' + t.dataset.scene, t.value); dirty(); }
    if (t.dataset.outfitpick !== undefined) { S.ui.outfitId = t.value; render(); }
    if (t.id === 'projectSelect') loadProject(t.value);
    if (t.id === 'fileInput') handleFiles(t);
  });
  let pendingUpload = null;
  function pickFile(target) {
    pendingUpload = target;
    let fi = $('#fileInput'); if (!fi) { fi = document.createElement('input'); fi.type = 'file'; fi.id = 'fileInput'; fi.accept = 'image/png,image/jpeg,image/webp'; fi.multiple = true; fi.hidden = true; document.body.appendChild(fi); }
    fi.value = ''; fi.click();
  }
  async function uploadFile(file) {
    const r = await api(`/projects/${S.p.id}/upload`, { method: 'POST', body: file });
    return r.path;
  }
  async function placeFiles(target, files) {
    try {
      for (const f of files) {
        const rel = await uploadFile(f);
        if (target.multi) { const arr = getPath(S.p, target.path) || []; if (arr.length < target.max) { arr.push(rel); setPath(S.p, target.path, arr); } }
        else { setPath(S.p, target.path, rel); break; }
      }
      dirty(); render(); toast('Image added');
    } catch (err) { toast(err.message); }
  }
  async function handleFiles(input) { if (pendingUpload && input.files.length) await placeFiles(pendingUpload, [...input.files]); }

  document.addEventListener('click', async (e) => {
    const t = e.target.closest('[data-go],[data-copy],[data-up],[data-upm],[data-rm],[data-rmi],[data-del],[data-addchar],[data-addoutfit],[data-addloc],[data-style],[data-char],[data-comp],[data-scenekey],[data-sample],[data-kling],[data-export]');
    if (!t) return;
    const d = t.dataset;
    if (d.go) return go(d.go);
    if (d.copy !== undefined) { try { await navigator.clipboard.writeText(S.copy[+d.copy]); toast('Copied'); } catch { toast('Copy failed — select the text manually'); } return; }
    if (d.rm) { e.stopPropagation(); setPath(S.p, d.rm, ''); dirty(); return render(); }
    if (d.rmi) { const [path, i] = d.rmi.split(':'); const arr = getPath(S.p, path); arr.splice(+i, 1); dirty(); return render(); }
    if (d.up) { const max = 1; return pickFile({ path: d.up, multi: false, max }); }
    if (d.upm) { const max = d.upm.endsWith('extra') ? 2 : 6; return pickFile({ path: d.upm, multi: true, max }); }
    if (d.del) { const [path, i] = d.del.split(':'); if (!confirm('Remove this item?')) return; getPath(S.p, path).splice(+i, 1); dirty(); return render(); }
    if (d.addchar !== undefined) { S.p.characters.push({ id: uid(), name: 'New character', pronouns: 'they', images: { extra: [] }, outfits: [] }); dirty(); return render(); }
    if (d.addoutfit !== undefined) { const c = S.p.characters[+d.addoutfit]; (c.outfits = c.outfits || []).push({ id: uid(), name: 'Outfit ' + (c.outfits.length + 1), description: '', refs: [] }); dirty(); return render(); }
    if (d.addloc !== undefined) { S.p.locations.push({ id: uid(), name: 'New location', images: [] }); dirty(); return render(); }
    if (d.style) { S.p.style = d.style; dirty(); return render(); }
    if (d.char) { S.ui.charId = d.char; S.ui.outfitId = ''; return render(); }
    if (d.comp) { S.ui.comp = d.comp; return render(); }
    if (d.scenekey) { S.ui.sceneKey = d.scenekey; return render(); }
    if (d.sample !== undefined) { if (S.p.script.trim() && !confirm('Replace the current script with the example?')) return; S.p.script = SAMPLE; dirty(); return render(); }
    if (d.kling) {
      const out = $('#klingOut'); out.hidden = false; out.textContent = 'Running kling ' + d.kling + ' …';
      try { const r = await api('/integrations/kling/' + d.kling, { method: 'POST' }); out.textContent = (r.stdout || r.stderr || '(no output)').trim(); } catch (err) { out.textContent = err.message; }
      return;
    }
    if (d.export !== undefined) {
      const out = $('#exportOut'); out.hidden = false; out.textContent = 'Exporting…';
      try { const r = await api(`/projects/${S.p.id}/export`, { method: 'POST' }); out.textContent = `Saved to:\n${r.dir}\n\n${r.files.join('\n')}\n\n${r.copied} uploaded image(s) copied with project file names.`; } catch (err) { out.textContent = err.message; }
    }
  });
  // drag & drop
  document.addEventListener('dragover', (e) => { const z = e.target.closest('[data-up],[data-upm]'); if (z) { e.preventDefault(); z.classList.add('over'); } });
  document.addEventListener('dragleave', (e) => { const z = e.target.closest('[data-up],[data-upm]'); if (z) z.classList.remove('over'); });
  document.addEventListener('drop', (e) => {
    const z = e.target.closest('[data-up],[data-upm]'); if (!z) return; e.preventDefault(); z.classList.remove('over');
    const files = [...e.dataTransfer.files].filter((f) => f.type.startsWith('image/'));
    if (!files.length) return;
    const multi = !!z.dataset.upm; const path = z.dataset.up || z.dataset.upm;
    placeFiles({ path, multi, max: multi ? (path.endsWith('extra') ? 2 : 6) : 1 }, files);
  });

  /* ------------------------------------------------------------------ boot */
  async function loadProject(id) {
    S.p = await api('/projects/' + id); S.ui.charId = null; S.ui.outfitId = ''; S.ui.sceneKey = 'all';
    localStorage.setItem('ps.last', id); render();
  }
  async function refreshList() { S.projects = await api('/projects'); }
  async function newProject() {
    const title = prompt('Project title'); if (!title) return;
    const p = await api('/projects', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title }) });
    await refreshList(); await loadProject(p.id); go('setup');
  }
  $('#newProject').addEventListener('click', newProject);
  (async function boot() {
    try {
      await refreshList();
      if (!S.projects.length) { const p = await api('/projects', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: 'My first film' }) }); S.projects = await api('/projects'); await loadProject(p.id); }
      else { const last = localStorage.getItem('ps.last'); await loadProject(S.projects.find((p) => p.id === last) ? last : S.projects[0].id); }
      api('/integrations/status').then((r) => { S.integ = r; if (S.step === 'export') render(); }).catch(() => {});
    } catch (e) { $('#view').innerHTML = `<div class="banner err">Could not reach the local server: ${esc(e.message)}</div>`; }
  })();
})();
