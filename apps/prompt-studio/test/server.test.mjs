import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ps-test-'));
process.env.PROMPT_STUDIO_DATA = tmp;
const { server } = await import('../server.mjs');
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;
// The server validates Host against 127.0.0.1/localhost regardless of port.
const call = (p, o = {}) => fetch(base + p, o);
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');

test.after(() => { server.close(); fs.rmSync(tmp, { recursive: true, force: true }); });

test('project lifecycle, upload validation and file serving', async () => {
  const p = await (await call('/api/projects', { method: 'POST', body: JSON.stringify({ title: 'Test Film' }) })).json();
  assert.equal(p.id, 'test-film');
  const bad = await call(`/api/projects/${p.id}/upload`, { method: 'POST', body: 'not an image' });
  assert.equal(bad.status, 415);
  const ok = await (await call(`/api/projects/${p.id}/upload`, { method: 'POST', body: PNG })).json();
  assert.match(ok.path, /^uploads\/[0-9a-f]{16}\.png$/);
  const served = await call(`/api/projects/${p.id}/file?p=${encodeURIComponent(ok.path)}`);
  assert.equal(served.status, 200);
  assert.equal(served.headers.get('content-type'), 'image/png');
  const trav = await call(`/api/projects/${p.id}/file?p=${encodeURIComponent('../project.json')}`);
  assert.equal(trav.status, 404);
  const put = await call(`/api/projects/${p.id}`, { method: 'PUT', body: JSON.stringify({ ...p, title: 'Renamed' }) });
  assert.equal((await put.json()).title, 'Renamed');
});

test('invalid ids and non-local hosts are refused', async () => {
  assert.equal((await call('/api/projects/..%2F..%2Fetc')).status, 404);
  const status = await new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: server.address().port, path: '/api/projects', headers: { Host: 'evil.example' } }, (res) => { res.resume(); resolve(res.statusCode); });
    req.on('error', reject); req.end();
  });
  assert.equal(status, 403);
});

test('only read-only Kling checks are exposed', async () => {
  for (const verb of ['text_to_video', 'image_to_video', 'element_delete', 'logout', 'file_upload']) {
    assert.equal((await call('/api/integrations/kling/' + verb, { method: 'POST' })).status, 403, verb);
  }
});

test('export writes pack, drafts and renamed assets', async () => {
  const p = await (await call('/api/projects', { method: 'POST', body: JSON.stringify({ title: 'Exp' }) })).json();
  const up = await (await call(`/api/projects/${p.id}/upload`, { method: 'POST', body: PNG })).json();
  p.characters = [{ id: 'c', name: 'Mia', pronouns: 'she', images: { front: up.path, side: up.path, extra: [] }, outfits: [] }];
  p.script = 'INT. ROOM - DAY\n\nMIA: Hello.\n';
  await call(`/api/projects/${p.id}`, { method: 'PUT', body: JSON.stringify(p) });
  const r = await (await call(`/api/projects/${p.id}/export`, { method: 'POST' })).json();
  for (const f of r.files) assert.ok(fs.existsSync(path.join(r.dir, f)), f);
  assert.ok(fs.readdirSync(path.join(r.dir, 'assets')).some((n) => n.startsWith('exp_src_char-mia_front_v01')));
  const spec = JSON.parse(fs.readFileSync(path.join(r.dir, 'kling/request-draft.json')));
  assert.ok(spec.every((j) => j.submissionBlocked));
});
