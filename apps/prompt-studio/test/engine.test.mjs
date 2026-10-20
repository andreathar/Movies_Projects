import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const E = createRequire(import.meta.url)('../public/engine.js');

const project = () => ({
  id: 'demo', title: 'The Table', style: 'photoreal-unretouched', aspect: '16:9',
  dialogueLanguage: 'English',
  characters: [{
    id: 'c1', name: 'Andre', pronouns: 'he', age: 'man in his late thirties', skin: 'olive skin', face: 'angular jaw, defined cheekbones',
    hair: 'short dark hair', eyes: 'dark brown eyes', build: 'lean build', images: { front: 'uploads/f.jpg', side: 'uploads/s.jpg', extra: [] },
    outfits: [{ id: 'o1', name: 'Grey jacket', description: 'grey pinstripe jacket over a white striped shirt, open collar, dark trousers', refs: ['uploads/o1.jpg', 'uploads/o2.jpg'] }],
  }],
  locations: [{ id: 'l1', name: 'Oak Dining Room', description: 'pale oak table, tall window, plaster walls', time: 'dusk', mood: 'quiet', images: ['uploads/l1.jpg', 'uploads/l2.jpg'] }],
  script: `INT. OAK DINING ROOM - DUSK

Andre sits at the table and looks across it.

ANDRE (softly): Do you remember this table?

Andre lowers his eyes to the ring stain.
`,
});

test('naming helpers', () => {
  assert.equal(E.slugify('Áudio & Vídeo!'), 'audio-video');
  assert.equal(E.assetName({ project: 'The Table', kind: 'char', subject: 'Andre', variant: 'split-screen', version: 2, ext: 'PNG' }), 'the-table_char_andre_split-screen_v02.png');
  assert.equal(E.higgsElementName('char', 'Andre Athar', 2), 'char_andre-athar_v2');
  assert.equal(E.klingElementName('Andre Athar', 'grey jacket'), 'AndreAthar_GreyJacket');
});

test('script parsing: headings, inline and bare dialogue', () => {
  const sc = E.parseScript(project().script, ['Andre']);
  assert.equal(sc.length, 1);
  assert.equal(sc[0].place, 'OAK DINING ROOM');
  assert.equal(sc[0].time, 'DUSK');
  assert.deepEqual(sc[0].beats.map((b) => b.type), ['action', 'dialogue', 'action']);
  assert.equal(sc[0].beats[1].character, 'Andre');
  assert.equal(sc[0].beats[1].parenthetical, 'softly');
  const f = E.parseScript('INT. ROOM - DAY\n\nANDRE\n(quietly)\nHello there.\n', ['Andre']);
  assert.equal(f[0].beats[0].text, 'Hello there.');
  assert.equal(f[0].beats[0].parenthetical, 'quietly');
});

test('shots link location and cast', () => {
  const { shots } = E.buildShots(project());
  assert.equal(shots.length, 3);
  assert.equal(shots[0].id, 'S01_SH01');
  assert.equal(shots[1].locationId, 'l1');
  assert.deepEqual(shots[1].subjects, ['c1']);
  assert.ok(shots[1].duration >= 4);
});

test('Higgsfield sheet follows slot architecture and keeps framing rules', () => {
  const p = project();
  const s = E.higgsfieldCharacterSheet(p, p.characters[0], p.characters[0].outfits[0], 'split-screen');
  assert.match(s.prompt, /^Split-screen character sheet composition/);
  assert.match(s.prompt, /exact facial identity/);
  assert.match(s.prompt, /not cropped not sitting/);
  assert.match(s.prompt, /no text, no watermark/);
  assert.equal(s.aspect_ratio, '16:9');
  assert.equal(s.references.length, 4);
  assert.equal(s.elementName, 'char_andre_v1');
  assert.ok(s.prompt.indexOf('Split-screen') < s.prompt.indexOf('wearing'));
});

test('Kling sheet uses 图片N for CLI and @ImageN for app, in slot order', () => {
  const p = project();
  const k = E.klingCharacterSheet(p, p.characters[0], p.characters[0].outfits[0], 'turnaround');
  assert.match(k.promptCli, /图片1/);
  assert.match(k.promptCli, /图片2/);
  assert.doesNotMatch(k.promptCli, /@Image/);
  assert.match(k.promptApp, /@Image1/);
  assert.doesNotMatch(k.promptApp, /图片/);
  assert.match(k.cli, /--image \.\/uploads\/f\.jpg --image \.\/uploads\/s\.jpg/);
  assert.equal(k.tokenMap[0].cli, '图片1');
  assert.equal((k.promptCli.match(/wearing/g) || []).length, 1);
  assert.match(k.promptCli, /exactly as shown in 图片3/);
  const hh = E.higgsfieldCharacterSheet(p, p.characters[0], p.characters[0].outfits[0], 'split-screen');
  assert.doesNotMatch(hh.prompt, /, Use /);
});

test('Kling element spec: cover + 1-3 secondary, valid tag', () => {
  const p = project();
  const e = E.klingElementSpecCharacter(p, p.characters[0]);
  assert.equal(e.tag, 'Characters');
  assert.ok(E.KLING_TAGS.includes(e.tag));
  assert.equal(e.cover, 'uploads/f.jpg');
  assert.deepEqual(e.secondary, ['uploads/s.jpg']);
  assert.match(e.cli, /--cover \.\/uploads\/f\.jpg --secondary \.\/uploads\/s\.jpg/);
  const bare = E.klingElementSpecCharacter(p, { name: 'X', images: {} });
  assert.equal(bare.problems.length, 2);
  assert.equal(bare.cli, '');
});

test('shot prompts: element marker, dialogue exact, camera, endpoint', () => {
  const p = project();
  const { shots } = E.buildShots(p);
  let sp = E.shotPrompts(p, shots[1]);
  assert.match(sp.kling.video.promptCli, /<<<ELEMENT_ID:Andre>>>/);
  assert.ok(sp.kling.video.promptCli.includes('"Do you remember this table?"'));
  assert.equal(sp.kling.video.args.enable_audio, true);
  assert.equal(sp.kling.video.args.prefer_multi_shots, false);
  p.characters[0].klingElementId = '323525046658711';
  sp = E.shotPrompts(p, shots[1]);
  assert.match(sp.kling.video.promptCli, /<<<323525046658711>>>/);
  assert.match(sp.kling.video.promptApp, /@Andre/);
  assert.match(sp.kling.video.cli, /--elements '\[\{"id":"323525046658711","bindName":"Andre"\}\]'/);
  assert.match(sp.kling.video.promptCli, /Locked camera/);
  const a = E.shotPrompts(p, shots[0]);
  assert.equal(a.kling.video.args.enable_audio, false);
  assert.match(a.kling.video.promptCli, /then settles still/);
  assert.equal(a.fileNames.video, 'the-table_vid_s01-sh01_take_v01.mp4');
});

test('pronouns are never guessed; default is they', () => {
  const p = project();
  delete p.characters[0].pronouns;
  const { shots } = E.buildShots(p);
  const sp = E.shotPrompts(p, shots[1]);
  assert.match(sp.kling.video.promptCli, /Preserve their face/);
  assert.doesNotMatch(sp.kling.video.promptCli, /\b(his|her)\b/);
});

test('linter catches syntax mix-ups and unresolved elements', () => {
  const l1 = E.lintPrompt('<<<ELEMENT_ID:Andre>>> waves. @Image1', { target: 'kling-cli', kind: 'i2v', imageCount: 1 });
  assert.ok(l1.some((x) => x.level === 'error' && /Unresolved/.test(x.msg)));
  assert.ok(l1.some((x) => /@ handles/.test(x.msg)));
  const l2 = E.lintPrompt('Same as 图片3', { target: 'kling-cli', imageCount: 2 });
  assert.ok(l2.some((x) => x.level === 'error'));
  const l3 = E.lintPrompt('A man talks.', { target: 'kling-cli', kind: 'i2v' });
  assert.ok(l3.some((x) => /camera/i.test(x.msg)));
  const l4 = E.lintPrompt('x "wrong line" y. Locked camera. No text.', { target: 'kling-cli', kind: 'i2v', dialogue: 'right line' });
  assert.ok(l4.some((x) => /altered/.test(x.msg)));
});

test('generated prompts lint clean (no errors) once elements are linked', () => {
  const p = project();
  p.characters[0].klingElementId = '123';
  const { shots } = E.buildShots(p);
  for (const s of shots) {
    const sp = E.shotPrompts(p, s);
    const res = E.lintPrompt(sp.kling.video.promptCli, { target: 'kling-cli', kind: 'i2v', dialogue: s.type === 'dialogue' ? s.text : '', elementIds: ['123'] });
    assert.deepEqual(res.filter((r) => r.level === 'error'), [], s.id);
  }
});

test('location plates and full pack/spec export', () => {
  const p = project();
  const plates = E.locationPlates(p, p.locations[0]);
  assert.equal(plates.length, 5);
  assert.match(plates[0].higgsfield.prompt, /no people/);
  assert.match(plates[0].kling.promptCli, /图片1/);
  assert.equal(plates[4].aspect_ratio, '9:16');
  const spec = E.klingSpec(p);
  assert.equal(spec.length, 3);
  assert.ok(spec.every((j) => j.submissionBlocked && j.auth.startsWith('REPLACE')));
  assert.ok(E.toMarkdown(p).includes('# The Table — Prompt pack'));
});

test('production sheet matches the 4-view + details + face layout', () => {
  const p = project();
  const o = p.characters[0].outfits[0];
  const h = E.higgsfieldCharacterSheet(p, p.characters[0], o, 'production-sheet');
  const k = E.klingCharacterSheet(p, p.characters[0], o, 'production-sheet');
  for (const phrase of ['four consistent full-body views', 'back view', 'detail insets', 'face close-up']) {
    assert.ok(JSON.stringify(h).includes(phrase), `higgsfield missing "${phrase}"`);
    assert.ok(JSON.stringify(k).includes(phrase), `kling missing "${phrase}"`);
  }
  assert.equal(E.COMPOSITIONS['production-sheet'].aspect, '2:3');
});

test('Kling 4.0 follows the live schema: no v3-only args, 30s cap, omni_ref_video with elements', () => {
  const p = project();
  p.kling = { imageModel: 'kling-image-o1', videoModel: 'kling-video-v4_0' };
  let { shots } = E.buildShots(p);
  let v = E.shotPrompts(p, shots[0]).kling.video;
  assert.equal(v.tool, 'image_to_video');
  assert.equal(v.inputKey, 'first_image');
  assert.equal(v.args.prefer_multi_shots, undefined);
  assert.equal(v.args.enable_audio, undefined);
  assert.ok(!v.cli.includes('--prefer_multi_shots'));
  p.characters[0].klingElementId = '12345';
  ({ shots } = E.buildShots(p));
  v = E.shotPrompts(p, shots[0]).kling.video;
  assert.equal(v.tool, 'omni_ref_video');
  assert.equal(v.inputKey, 'image_1');
  assert.deepEqual(v.elements[0].type, 'image');
  assert.ok(v.cli.startsWith('kling omni_ref_video --model kling-video-v4_0 --input image_1='));
  const spec = E.klingSpec(p)[0];
  assert.equal(spec.tool, 'omni_ref_video');
  assert.ok(spec.inputs.image_1 && !spec.inputs.first_image);
  assert.equal(E.KLING_VIDEO_LIMITS['kling-video-o1'].maxDuration, 10);
});
