#!/usr/bin/env node
// Prompt Studio — local server. Node >= 18, no dependencies.
// Binds to 127.0.0.1 only. Stores projects + uploads under ./data (git-ignored).
// It never submits paid Kling/Higgsfield jobs; CLI calls are limited to read-only checks.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFile } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const E = createRequire(import.meta.url)('./public/engine.js');
const PORT = Number(process.env.PORT || 4317);
const HOST = '127.0.0.1';
const DATA = path.resolve(process.env.PROMPT_STUDIO_DATA || path.join(here, 'data'));
const PUBLIC = path.join(here, 'public');
const MAX_UPLOAD = 25 * 1024 * 1024;
const MAX_JSON = 4 * 1024 * 1024;

fs.mkdirSync(path.join(DATA, 'projects'), { recursive: true });

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json', '.md': 'text/markdown; charset=utf-8' };
const ID_RE = /^[a-z0-9][a-z0-9-]{0,47}$/;

function sniff(buf) {
  if (buf.length > 8 && buf.slice(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return 'png';
  if (buf.length > 3 && buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff) return 'jpg';
  if (buf.length > 12 && buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') return 'webp';
  return null;
}
const projDir = (id) => path.join(DATA, 'projects', id);
const projFile = (id) => path.join(projDir(id), 'project.json');

function send(res, code, body, type = 'application/json') {
  const data = typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body);
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
  res.end(data);
}
const readBody = (req, limit) => new Promise((resolve, reject) => {
  const chunks = []; let n = 0;
  req.on('data', (c) => { n += c.length; if (n > limit) { reject(Object.assign(new Error('Payload too large'), { code: 413 })); req.destroy(); } else chunks.push(c); });
  req.on('end', () => resolve(Buffer.concat(chunks)));
  req.on('error', reject);
});

function loadProject(id) {
  if (!ID_RE.test(id)) return null;
  try { return JSON.parse(fs.readFileSync(projFile(id), 'utf8')); } catch { return null; }
}
function saveProject(p) {
  fs.mkdirSync(path.join(projDir(p.id), 'uploads'), { recursive: true });
  p.updatedAt = new Date().toISOString();
  const tmp = projFile(p.id) + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(p, null, 2));
  fs.renameSync(tmp, projFile(p.id));
  return p;
}
function blankProject(title) {
  const base = E.slugify(title).slice(0, 36);
  let id = base; let i = 1;
  while (fs.existsSync(projDir(id))) { i += 1; id = `${base}-${i}`; }
  return {
    id, title, createdAt: new Date().toISOString(), style: 'photoreal-unretouched', aspect: '16:9', defaultCamera: 'locked', dialogueLanguage: 'English',
    consent: false, kling: { imageModel: 'kling-image-o1', videoModel: 'kling-video-v4_0' }, higgsfield: { imageModel: 'nano_banana_pro', videoModel: 'seedance_2_5' },
    characters: [], locations: [], script: '', sceneSettings: {}, shotOverrides: {},
  };
}

function run(cmd, args, timeout = 30000) {
  return new Promise((resolve) => {
    execFile(cmd, args, { timeout, maxBuffer: 2 * 1024 * 1024 }, (err, stdout, stderr) => {
      resolve({ ok: !err, code: err ? err.code : 0, stdout: String(stdout || '').slice(0, 20000), stderr: String(stderr || '').slice(0, 4000) });
    });
  });
}
function which(bin) {
  return new Promise((resolve) => execFile(process.platform === 'win32' ? 'where' : 'which', [bin], (e, out) => resolve(e ? null : String(out).split('\n')[0].trim())));
}

// Read-only CLI calls only. Anything that generates, uploads, deletes or logs in is not on this list.
const SAFE_KLING = { who_am_i: ['who_am_i', '-q'], account: ['account'], tool_list: ['tool_list', '-q'], element_list: ['element_list'] };

function localOnly(req) {
  const host = (req.headers.host || '').split(':')[0];
  if (host !== '127.0.0.1' && host !== 'localhost') return false;
  const origin = req.headers.origin;
  if (origin) { try { const h = new URL(origin).hostname; if (h !== '127.0.0.1' && h !== 'localhost') return false; } catch { return false; } }
  return true;
}

async function exportProject(p) {
  const out = path.join(DATA, 'exports', p.id, new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19));
  fs.mkdirSync(path.join(out, 'kling'), { recursive: true });
  fs.mkdirSync(path.join(out, 'higgsfield'), { recursive: true });
  fs.mkdirSync(path.join(out, 'assets'), { recursive: true });
  const pack = E.buildPack(p);
  fs.writeFileSync(path.join(out, 'prompt-pack.md'), E.toMarkdown(p));
  fs.writeFileSync(path.join(out, 'pack.json'), JSON.stringify(pack, null, 2));
  fs.writeFileSync(path.join(out, 'kling', 'request-draft.json'), JSON.stringify(E.klingSpec(p), null, 2));
  const higgs = [];
  for (const ch of pack.characters) for (const s of ch.sheets) higgs.push({ kind: 'character-sheet', subject: ch.character.name, ...s.higgsfield });
  for (const lo of pack.locations) for (const pl of lo.plates) higgs.push({ kind: 'location-plate', subject: lo.location.name, file: pl.fileName, ...pl.higgsfield });
  for (const { shot, prompts } of pack.shots) { higgs.push({ kind: 'keyframe', subject: shot.id, ...prompts.higgsfield.keyframe }); higgs.push({ kind: 'video', subject: shot.id, ...prompts.higgsfield.video }); }
  fs.writeFileSync(path.join(out, 'higgsfield', 'requests-draft.json'), JSON.stringify(higgs, null, 2));
  // Copy uploads under their platform-correct names.
  const manifest = [];
  const copy = (rel, kind, subject, variant) => {
    if (!rel) return;
    const src = path.join(projDir(p.id), rel);
    if (!src.startsWith(projDir(p.id)) || !fs.existsSync(src)) return;
    const ext = path.extname(rel).slice(1) || 'jpg';
    const name = E.assetName({ project: p.title, kind: 'src', subject: `${kind}-${subject}`, variant, version: 1, ext });
    fs.copyFileSync(src, path.join(out, 'assets', name));
    manifest.push({ original: rel, exported: `assets/${name}` });
  };
  for (const c of p.characters) {
    copy(c.images?.front, 'char', c.name, 'front'); copy(c.images?.side, 'char', c.name, 'side');
    (c.images?.extra || []).forEach((x, i) => copy(x, 'char', c.name, 'extra' + (i + 1)));
    for (const o of c.outfits || []) (o.refs || []).forEach((x, i) => copy(x, 'outfit', `${c.name}-${o.name}`, 'ref' + (i + 1)));
  }
  for (const l of p.locations) (l.images || []).forEach((x, i) => copy(x, 'loc', l.name, 'ref' + (i + 1)));
  fs.writeFileSync(path.join(out, 'assets', 'manifest.json'), JSON.stringify(manifest, null, 2));
  return { dir: out, files: ['prompt-pack.md', 'pack.json', 'kling/request-draft.json', 'higgsfield/requests-draft.json', 'assets/manifest.json'], copied: manifest.length };
}

async function api(req, res, url) {
  const parts = url.pathname.split('/').filter(Boolean).slice(1); // after /api
  const m = req.method;
  if (parts[0] === 'projects' && parts.length === 1) {
    if (m === 'GET') {
      const list = fs.readdirSync(path.join(DATA, 'projects')).map(loadProject).filter(Boolean)
        .map((p) => ({ id: p.id, title: p.title, updatedAt: p.updatedAt || p.createdAt, characters: p.characters.length, locations: p.locations.length }));
      return send(res, 200, list.sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt))));
    }
    if (m === 'POST') {
      const body = JSON.parse((await readBody(req, MAX_JSON)).toString() || '{}');
      const title = String(body.title || '').trim().slice(0, 80);
      if (!title) return send(res, 400, { error: 'Title required' });
      return send(res, 201, saveProject(blankProject(title)));
    }
  }
  if (parts[0] === 'projects' && parts[1]) {
    const id = parts[1];
    const p = loadProject(id);
    if (!p) return send(res, 404, { error: 'Project not found' });
    if (parts.length === 2) {
      if (m === 'GET') return send(res, 200, p);
      if (m === 'PUT') {
        const body = JSON.parse((await readBody(req, MAX_JSON)).toString());
        body.id = id; body.createdAt = p.createdAt;
        return send(res, 200, saveProject(body));
      }
      if (m === 'DELETE') { fs.rmSync(projDir(id), { recursive: true, force: true }); return send(res, 200, { ok: true }); }
    }
    if (parts[2] === 'upload' && m === 'POST') {
      const buf = await readBody(req, MAX_UPLOAD);
      const ext = sniff(buf);
      if (!ext) return send(res, 415, { error: 'Only PNG, JPEG or WEBP images are accepted.' });
      const hash = crypto.createHash('sha256').update(buf).digest('hex').slice(0, 16);
      const rel = `uploads/${hash}.${ext}`;
      fs.mkdirSync(path.join(projDir(id), 'uploads'), { recursive: true });
      fs.writeFileSync(path.join(projDir(id), rel), buf);
      return send(res, 201, { path: rel, bytes: buf.length });
    }
    if (parts[2] === 'file' && m === 'GET') {
      const rel = url.searchParams.get('p') || '';
      const full = path.resolve(projDir(id), rel);
      if (!full.startsWith(path.join(projDir(id), 'uploads') + path.sep) || !fs.existsSync(full)) return send(res, 404, { error: 'Not found' });
      return send(res, 200, fs.readFileSync(full), MIME[path.extname(full)] || 'application/octet-stream');
    }
    if (parts[2] === 'export' && m === 'POST') return send(res, 200, await exportProject(p));
    if (parts[2] === 'markdown' && m === 'GET') {
      res.setHeader?.('Content-Disposition', `attachment; filename="${p.id}-prompt-pack.md"`);
      return send(res, 200, E.toMarkdown(p), 'text/markdown; charset=utf-8');
    }
  }
  if (parts[0] === 'integrations') {
    if (parts[1] === 'status' && m === 'GET') {
      const kling = await which('kling');
      let version = null;
      if (kling) { const v = await run('kling', ['--version'], 10000); version = v.ok ? v.stdout.trim() : null; }
      return send(res, 200, {
        kling: { installed: !!kling, path: kling, version, readOnlyChecks: Object.keys(SAFE_KLING) },
        higgsfield: { cli: !!(await which('higgsfield')), note: 'Higgsfield runs through its MCP connector / web app. Use the exported requests-draft.json or paste prompts directly.' },
      });
    }
    if (parts[1] === 'kling' && parts[2] && m === 'POST') {
      const args = SAFE_KLING[parts[2]];
      if (!args) return send(res, 403, { error: 'Only read-only Kling checks are allowed from this app.' });
      return send(res, 200, await run('kling', args));
    }
  }
  if (parts[0] === 'reference' && m === 'GET') {
    return send(res, 200, {
      styles: E.STYLE_PRESETS, compositions: E.COMPOSITIONS, plates: E.PLATES, camera: E.CAMERA,
      kling: { tags: E.KLING_TAGS, imageModels: E.KLING_IMAGE_MODELS, videoModels: E.KLING_VIDEO_MODELS },
      higgsfield: { imageModels: E.HIGGS_IMAGE_MODELS, videoModels: E.HIGGS_VIDEO_MODELS },
    });
  }
  return send(res, 404, { error: 'Unknown endpoint' });
}

const server = http.createServer(async (req, res) => {
  try {
    if (!localOnly(req)) return send(res, 403, { error: 'Local access only' });
    const url = new URL(req.url, `http://${HOST}:${PORT}`);
    if (url.pathname.startsWith('/api/')) return await api(req, res, url);
    if (req.method !== 'GET') return send(res, 405, { error: 'Method not allowed' });
    let rel = decodeURIComponent(url.pathname);
    if (rel === '/') rel = '/index.html';
    const full = path.resolve(PUBLIC, '.' + rel);
    if (!full.startsWith(PUBLIC + path.sep) || !fs.existsSync(full) || fs.statSync(full).isDirectory()) return send(res, 404, 'Not found', 'text/plain');
    return send(res, 200, fs.readFileSync(full), MIME[path.extname(full)] || 'application/octet-stream');
  } catch (e) {
    return send(res, e.code === 413 ? 413 : 500, { error: e.message });
  }
});

export { server, DATA };
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  server.listen(PORT, HOST, () => console.log(`Prompt Studio running at http://${HOST}:${PORT}  (data: ${DATA})`));
}
