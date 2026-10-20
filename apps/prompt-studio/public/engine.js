/* Prompt Studio engine — pure functions, no DOM, no network.
 * Runs in the browser (window.PromptEngine) and in Node (require / import).
 *
 * Platform naming rules encoded here come from:
 *  - Kling CLI contract (docs/kling-manual/05-elements.md, 18-guia-de-prompts.md):
 *      Element marker  <<<ELEMENT_ID>>> + --elements '[{"id":"..","bindName":".."}]'
 *      Image slot      图片1, 图片2 ... (= image_1, image_2) in the order of --image
 *      Tags            Characters | Animals | Items | Costumes | Scenes | Effects | Others
 *      Element image   1 cover + 1–3 secondary
 *  - Kling app/web: @Image1 / @ElementName
 *  - Higgsfield: generate_image / generate_video model ids and media roles
 *      (start_image, end_image, image_references, video_references, audio_references),
 *      character-sheet slot architecture, reference element names (char_<slug>_vN).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.PromptEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------------------------------------------------------------- helpers */
  const slugify = (s) =>
    String(s || '')
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'untitled';
  const pascal = (s) =>
    slugify(s).split('-').filter(Boolean).map((w) => w[0].toUpperCase() + w.slice(1)).join('') || 'Untitled';
  const words = (s) => (String(s || '').trim().match(/\S+/g) || []).length;
  const pad = (n, w = 2) => String(n).padStart(w, '0');
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim();
  const sentence = (s) => { s = clean(s); return !s ? '' : /[.!?]$/.test(s) ? s : s + '.'; };
  const join = (parts, sep = ', ') => parts.map(clean).filter(Boolean).join(sep);

  const PRONOUNS = {
    he: { sub: 'he', obj: 'him', pos: 'his', refl: 'himself', s: 's' },
    she: { sub: 'she', obj: 'her', pos: 'her', refl: 'herself', s: 's' },
    they: { sub: 'they', obj: 'them', pos: 'their', refl: 'themself', s: '' },
  };
  const pron = (c) => PRONOUNS[(c && c.pronouns) || 'they'] || PRONOUNS.they;

  /* --------------------------------------------------------- platform facts */
  const KLING_TAGS = ['Characters', 'Animals', 'Items', 'Costumes', 'Scenes', 'Effects', 'Others'];
  const KLING_IMAGE_MODELS = ['kling-image-o1', 'kling-image-v3_0', 'kling-image-v3_0_omni'];
  const KLING_VIDEO_MODELS = ['kling-video-v3_0', 'kling-video-v3_0_omni', 'kling-video-v3_0_turbo', 'kling-video-o1', 'kling-video-v4_0'];
  const HIGGS_IMAGE_MODELS = ['nano_banana_pro', 'nano_banana_2', 'soul_cinematic', 'gpt_image_2', 'seedream_v5_pro', 'kling_omni_image', 'cinematic_studio_2_5'];
  const HIGGS_VIDEO_MODELS = {
    seedance_2_5: { label: 'Seedance 2.5', duration: [4, 30], roles: ['start_image', 'end_image', 'image_references', 'video_references', 'audio_references'], audio: 'generate_audio' },
    kling3_0: { label: 'Kling v3.0 (via Higgsfield)', duration: [3, 15], roles: ['start_image', 'end_image'], audio: 'sound' },
    grok_video_v15: { label: 'Grok Video 1.5', duration: [2, 15], roles: ['start_image', 'image_references', 'audio_references'], audio: null },
    minimax_h3: { label: 'MiniMax H3', duration: [4, 15], roles: ['start_image', 'end_image', 'image_references', 'video_references', 'audio_references'], audio: null },
    gemini_omni_flash_1_1: { label: 'Gemini Omni Flash 1.1', duration: [3, 10], roles: ['start_image', 'end_image', 'image_references', 'video_references'], audio: null },
  };
  const CAMERA = {
    locked: 'Locked camera, no camera movement, one continuous shot, no cuts.',
    push: 'Camera: slow push in, one continuous shot, no cuts.',
    pull: 'Camera: slow pull back, one continuous shot, no cuts.',
    pan: 'Camera: slow pan left to right, one continuous shot, no cuts.',
    track: 'Camera: smooth tracking shot following the subject, one continuous shot, no cuts.',
    handheld: 'Camera: subtle handheld drift, one continuous shot, no cuts.',
  };

  /* ------------------------------------------------------------ style presets */
  // Modules follow Higgsfield's character-sheet workflow (Realism / Lighting / Quality tail).
  const STYLE_PRESETS = {
    'photoreal-unretouched': {
      label: 'Photoreal, unretouched',
      realism: 'visible fine skin texture with natural pores, fine lines, subtle asymmetries and texture irregularities, faint natural blush, slight natural sheen rather than glossy or dewy retouched finish, no digital smoothing, no beauty filter, no AI-airbrushed look, skin free of artificial glare, shine or highlight blooms, matte-to-natural complexion',
      eyes: 'naturally muted catchlights, no oversized specular glare in the iris, eye color muted rather than glowing',
      lighting: 'soft diffused studio lighting without harsh reflections',
      tail: 'natural anatomy, high-end but unretouched commercial photography style, cinematic realism, clean white background, 4K quality, sharp focus on skin texture detail',
      negative: 'no beauty filter, no digital smoothing, no airbrushing, no plastic skin, no glossy skin',
      photo: true,
    },
    'editorial-polished': {
      label: 'Editorial, polished',
      realism: 'fine skin texture retained, soft dewy highlight on cheekbones, refined natural makeup',
      eyes: 'naturally muted catchlights, no oversized specular glare in the iris',
      lighting: 'editorial beauty lighting with a soft key and gentle fill',
      tail: 'high-end fashion editorial photography, magazine cover quality, cinematic realism, 4K',
      negative: 'no plastic skin, no heavy retouching',
      photo: true,
    },
    'anime-2d': {
      label: 'Anime / 2D',
      realism: 'clean anime illustration, crisp lineart, cel-shaded flat color with soft gradient shadows, consistent character model-sheet style',
      eyes: 'expressive large eyes with detailed iris highlights',
      lighting: 'even flat lighting, soft ambient shading',
      tail: 'high-quality anime key visual, clean vector-like linework, sharp, 4K',
      negative: 'no photorealism, no 3D render look',
      photo: false,
    },
    '3d-stylized': {
      label: '3D stylized',
      realism: 'stylized 3D character render, appealing exaggerated proportions, smooth subsurface-scattering skin, detailed hair strands and cloth simulation',
      eyes: 'large readable eyes with soft catchlights',
      lighting: 'soft global illumination, three-point studio lighting, gentle rim light',
      tail: 'high-end 3D animation studio quality, clean neutral background, 4K',
      negative: 'no photorealism, no flat 2D look',
      photo: false,
    },
    'game-concept': {
      label: 'Game concept art',
      realism: 'painterly game concept art, semi-realistic rendering, orthographic model sheet, clear silhouette',
      eyes: 'clearly readable eyes',
      lighting: 'neutral even concept-art lighting',
      tail: 'professional character concept art, sharp, 4K',
      negative: 'no photographic look',
      photo: false,
    },
  };

  const COMPOSITIONS = {
    'split-screen': {
      label: 'Split-screen (full body + close-up)',
      aspect: '16:9',
      clause: 'Split-screen character sheet composition, left side a full-body shot of the character standing upright in a neutral straight standing pose facing the camera with both feet flat on the ground and arms relaxed at the sides, full head-to-toe framing with the whole body and both feet visible, right side a tight close-up chest-up portrait of the same character',
      extra: 'single subject only, exactly one person, only the character in frame, no other people, no duplicate figures, no mannequin, no reflections, no props, no furniture, no background objects, empty seamless studio, left panel standing full-body head-to-toe not cropped not sitting, right panel tight close-up not full body',
    },
    turnaround: {
      label: 'Turnaround (front / 3/4 / side / back)',
      aspect: '16:9',
      clause: 'Character turnaround model sheet, four consistent full-body views in a row, front view, 3/4 view, side profile and back view, evenly spaced, neutral standing pose, arms relaxed',
      extra: 'same scale and height on all four views, full body and both feet visible in every view, no other people, no props, empty seamless studio',
    },
    expression: {
      label: 'Expression sheet',
      aspect: '16:9',
      clause: 'Character expression sheet, one full-body reference on the left and a grid of head-and-shoulders portraits on the right showing varied expressions (neutral, smiling, serious, surprised, concerned, laughing)',
      extra: 'same face and identity in every portrait, no other people, no props, empty seamless studio',
    },
    'face-angles': {
      label: 'Face angles (front / 3/4 / profile)',
      aspect: '16:9',
      clause: 'Face reference sheet, three head-and-shoulders portraits in a row of the same character, front view, 3/4 view and side profile, evenly spaced, neutral expression, same lighting on all three',
      extra: 'identical face, hair and skin on all three portraits, no other people, no props, empty seamless studio',
    },
    'single-portrait': {
      label: 'Single portrait (cover image for Element)',
      aspect: '3:4',
      clause: 'Single front-facing head-and-shoulders portrait of the character, neutral expression, looking straight into the camera',
      extra: 'exactly one person, no other people, no props, empty seamless studio',
    },
  };

  /* ---------------------------------------------------------------- naming */
  const NAME_KINDS = {
    char: 'Character reference / sheet',
    outfit: 'Outfit / costume',
    loc: 'Location plate',
    shot: 'Shot keyframe',
    vid: 'Video take',
    src: 'Source upload',
  };

  /** File name: <project>_<kind>_<subject>_<variant>_v<NN>.<ext>  (lowercase, ASCII, no spaces). */
  function assetName({ project, kind, subject, variant, version = 1, ext = 'png' }) {
    return [slugify(project), kind, slugify(subject), variant ? slugify(variant) : '', 'v' + pad(version)]
      .filter(Boolean).join('_') + '.' + String(ext).replace(/^\./, '').toLowerCase();
  }
  /** Higgsfield reference element name (matches existing convention char_andre-athar_v2). */
  function higgsElementName(kind, subject, version = 1) {
    return `${kind}_${slugify(subject)}_v${version}`;
  }
  /** Kling Element name: short, no spaces. Tag is chosen separately. */
  function klingElementName(subject, suffix = '') {
    return pascal(subject) + (suffix ? '_' + pascal(suffix) : '');
  }

  /* ------------------------------------------------------------ script parser */
  const HEADING_RE = /^\s*(?:(?:INT|EXT|INT\.?\/EXT|EXT\.?\/INT|I\/E)[.\s]|SCENE\s+\d+\b|CENA\s+\d+\b)/i;
  function parseHeading(line) {
    const m = line.trim().replace(/^\.+/, '').match(/^(?:(INT|EXT|INT\.?\/EXT|EXT\.?\/INT|I\/E)\.?\s+)?(.*?)(?:\s+[-–—]\s+([^-–—]+))?$/i);
    return { intExt: (m && m[1] || '').toUpperCase(), place: clean(m && m[2]) || clean(line), time: clean(m && m[3]) };
  }

  function parseScript(text, knownNames = []) {
    const known = new Map(knownNames.map((n) => [clean(n).toUpperCase(), clean(n)]));
    const lines = String(text || '').replace(/\r/g, '').split('\n');
    const scenes = [];
    let cur = null;
    let pendingSpeaker = null;
    const ensure = () => {
      if (!cur) { cur = { index: scenes.length + 1, heading: 'Scene 1', intExt: '', place: '', time: '', beats: [] }; scenes.push(cur); }
      return cur;
    };
    const flushSpeaker = () => { pendingSpeaker = null; };
    for (const raw of lines) {
      const line = raw.trim();
      if (!line) { flushSpeaker(); continue; }
      if (HEADING_RE.test(line)) {
        flushSpeaker();
        const h = parseHeading(line);
        cur = { index: scenes.length + 1, heading: line.replace(/^\.+/, ''), ...h, beats: [] };
        scenes.push(cur);
        continue;
      }
      // "NAME: text" or "NAME (paren): text"
      const inline = line.match(/^([A-ZÀ-Ü][A-Za-zÀ-ÿ0-9 .'_-]{0,30}?)\s*(\(([^)]*)\))?\s*:\s*(.+)$/);
      if (inline && (known.has(inline[1].trim().toUpperCase()) || inline[1] === inline[1].toUpperCase())) {
        const name = known.get(inline[1].trim().toUpperCase()) || clean(inline[1]);
        ensure().beats.push({ type: 'dialogue', character: name, parenthetical: clean(inline[3]), text: stripQuotes(inline[4]) });
        flushSpeaker();
        continue;
      }
      // Fountain style: NAME on its own line, dialogue underneath.
      const bare = line.match(/^([A-ZÀ-Ü][A-ZÀ-Ü0-9 .'_-]{0,30})\s*(\(([^)]*)\))?$/);
      if (bare && (known.has(bare[1].trim()) || /^[A-ZÀ-Ü0-9 .'_-]+$/.test(bare[1])) && !pendingSpeaker && !/^[A-Z]{1,3}\.?$/.test(bare[1].trim())) {
        pendingSpeaker = { name: known.get(bare[1].trim()) || clean(bare[1]), paren: clean(bare[3]) };
        continue;
      }
      if (pendingSpeaker) {
        const par = line.match(/^\((.*)\)$/);
        if (par) { pendingSpeaker.paren = clean(par[1]); continue; }
        ensure().beats.push({ type: 'dialogue', character: pendingSpeaker.name, parenthetical: pendingSpeaker.paren, text: stripQuotes(line) });
        continue;
      }
      ensure().beats.push({ type: 'action', text: line });
    }
    return scenes;
  }
  function stripQuotes(s) { return clean(s).replace(/^["“”]+|["“”]+$/g, ''); }

  /** Characters mentioned in a scene (dialogue speaker or named in action text). */
  function sceneCast(scene, characters) {
    const found = [];
    for (const c of characters) {
      const n = c.name.toLowerCase();
      const hit = scene.beats.some((b) =>
        (b.type === 'dialogue' && b.character.toLowerCase() === n) ||
        (b.type === 'action' && new RegExp('\\b' + n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(b.text)));
      if (hit) found.push(c);
    }
    return found;
  }

  /* -------------------------------------------------------------- shots */
  function estimateDuration(beat) {
    const w = words(beat.text);
    if (beat.type === 'dialogue') return Math.max(4, Math.min(15, Math.ceil(w / 2.6 + 2)));
    return Math.max(3, Math.min(8, Math.ceil(w / 2.5)));
  }

  function findLocation(scene, locations, override) {
    if (override) return locations.find((l) => l.id === override) || null;
    const p = scene.place.toLowerCase();
    if (!p) return null;
    return locations.find((l) => p.includes(l.name.toLowerCase()) || l.name.toLowerCase().includes(p)) || null;
  }

  function resolveScene(project, scene) {
    const settings = (project.sceneSettings || {})['S' + pad(scene.index)] || {};
    const location = findLocation(scene, project.locations || [], settings.locationId);
    const cast = sceneCast(scene, project.characters || []);
    const outfits = {};
    for (const c of cast) {
      const id = (settings.outfits || {})[c.id];
      outfits[c.id] = (c.outfits || []).find((o) => o.id === id) || (c.outfits || [])[0] || null;
    }
    return { scene, key: 'S' + pad(scene.index), settings, location, cast, outfits };
  }

  function buildShots(project) {
    const scenes = parseScript(project.script, (project.characters || []).map((c) => c.name));
    const shots = [];
    for (const sc of scenes) {
      const r = resolveScene(project, sc);
      let n = 0;
      let lastAction = '';
      for (const b of sc.beats) {
        if (b.type === 'action') { lastAction = b.text; }
        n += 1;
        const speaker = b.type === 'dialogue' ? (project.characters || []).find((c) => c.name.toLowerCase() === b.character.toLowerCase()) : null;
        const subjects = speaker ? [speaker, ...r.cast.filter((c) => c !== speaker)] : r.cast;
        shots.push({
          id: `${r.key}_SH${pad(n)}`,
          sceneKey: r.key,
          sceneIndex: sc.index,
          heading: sc.heading,
          type: b.type,
          text: b.text,
          character: b.character || '',
          parenthetical: b.parenthetical || '',
          context: b.type === 'dialogue' ? lastAction : '',
          duration: (project.shotOverrides || {})[`${r.key}_SH${pad(n)}`]?.duration || estimateDuration(b),
          subjects: subjects.map((c) => c.id),
          locationId: r.location ? r.location.id : '',
        });
      }
    }
    return { scenes, shots };
  }

  /* --------------------------------------------------- character description */
  function identityPhrase(c) {
    return join([c.age, c.skin]);
  }
  function describeAppearance(c) {
    return join([
      c.face, c.build ? c.build : '', c.hair ? 'hair: ' + c.hair : '', c.eyes ? 'eyes: ' + c.eyes : '',
      c.distinct ? 'distinguishing features: ' + c.distinct : '',
    ]);
  }
  function outfitPhrase(o) { return o ? clean(o.description) : ''; }

  /* =============================================== HIGGSFIELD CHARACTER SHEET */
  function higgsfieldCharacterSheet(project, c, outfit, compKey = 'split-screen') {
    const style = STYLE_PRESETS[project.style] || STYLE_PRESETS['photoreal-unretouched'];
    const comp = COMPOSITIONS[compKey] || COMPOSITIONS['split-screen'];
    const hasRefs = !!(c.images && (c.images.front || c.images.side));
    const refs = [];
    if (c.images && c.images.front) refs.push({ role: 'image_references', file: c.images.front, label: 'Front headshot' });
    if (c.images && c.images.side) refs.push({ role: 'image_references', file: c.images.side, label: 'Side headshot' });
    for (const x of (outfit && outfit.refs) || []) refs.push({ role: 'image_references', file: x, label: 'Outfit reference' });

    const idLead = hasRefs
      ? `Use the attached reference photos (front and side headshots) as the exact facial identity: keep the same face shape, features, skin tone, hair and age, do not beautify or alter the person`
      : '';
    const parts = [
      comp.clause,
      hasRefs ? 'the identical person on all views' : 'identical original character on all views',
      idLead,
      'pure white seamless studio background, professional character sheet presentation',
      identityPhrase(c),
      c.face,
      join([c.eyes, style.eyes]),
      c.brows, c.hair ? c.hair : '',
      style.realism,
      c.build ? c.build + ' with balanced proportions' : '',
      outfit ? 'wearing ' + outfitPhrase(outfit) : '',
      style.lighting,
      style.tail,
      comp.extra,
      'no text, no watermark, no logos, no frame borders',
      style.negative,
      c.adult !== false ? 'no babyface, no overly youthful rounded proportions' : '',
    ];
    const prompt = join(parts);
    const model = (project.higgsfield && project.higgsfield.imageModel) || 'nano_banana_pro';
    return {
      platform: 'higgsfield',
      tool: 'generate_image',
      model,
      aspect_ratio: comp.aspect,
      prompt,
      references: refs,
      elementName: higgsElementName('char', c.name, 1),
      fileName: assetName({ project: project.title, kind: 'char', subject: c.name, variant: `${compKey}${outfit ? '-' + outfit.name : ''}`, version: 1 }),
      notes: [
        'Generate only on your explicit go-ahead; check credits first (balance).',
        'Upload headshots with media_upload and pass them as image_references.',
        'After you accept the sheet, save it as a reference element: ' + higgsElementName('char', c.name, 1),
      ],
    };
  }

  /* ===================================================== KLING CHARACTER SHEET */
  function klingCharacterSheet(project, c, outfit, compKey = 'split-screen') {
    const style = STYLE_PRESETS[project.style] || STYLE_PRESETS['photoreal-unretouched'];
    const comp = COMPOSITIONS[compKey] || COMPOSITIONS['split-screen'];
    const images = [];
    if (c.images && c.images.front) images.push({ label: 'Front headshot', file: c.images.front });
    if (c.images && c.images.side) images.push({ label: 'Side headshot', file: c.images.side });
    for (const x of (outfit && outfit.refs) || []) if (images.length < 6) images.push({ label: 'Outfit reference', file: x });
    const tok = (i, target) => (target === 'cli' ? `图片${i}` : `@Image${i}`);
    const build = (target) => {
      const idx = {};
      images.forEach((im, i) => { idx[im.label + i] = i + 1; });
      const front = images.findIndex((i) => i.label === 'Front headshot') + 1;
      const side = images.findIndex((i) => i.label === 'Side headshot') + 1;
      const outfitIdx = images.map((im, i) => (im.label === 'Outfit reference' ? i + 1 : 0)).filter(Boolean);
      const idLines = [];
      if (front) idLines.push(`the person with EXACTLY the face of ${tok(front, target)}`);
      if (side) idLines.push(`${tok(side, target)} is the same person in side profile`);
      const outfitRef = outfitIdx.length ? `, wearing the outfit shown in ${outfitIdx.map((i) => tok(i, target)).join(' and ')}` : '';
      const text = join([
        comp.clause,
        idLines.join('; ') || 'original character',
        'identical on all views',
        'pure white seamless studio background',
        c.hair ? 'hair: ' + c.hair : '',
        c.build,
        outfit ? 'wearing ' + outfitPhrase(outfit) + (outfitRef ? '' : '') : '',
        outfitRef ? outfitRef.slice(2) : '',
        style.lighting,
        style.photo ? 'natural skin texture, no retouching, no beauty filter' : style.realism,
        comp.extra,
      ]);
      // Exclusions belong in the prompt body (no negative_prompt on current Kling image/video models).
      return sentence(text) + ' No text, no watermark, no logos, no frame borders. Do not alter the identity, age or proportions of the person.';
    };
    const model = (project.kling && project.kling.imageModel) || 'kling-image-o1';
    const imageFlags = images.map((im) => `--image ./${shellSafe(im.file)}`).join(' ');
    const cliPrompt = build('cli');
    const elementId = c.klingElementId ? c.klingElementId : '';
    return {
      platform: 'kling',
      tool: 'image_to_image',
      model,
      aspect_ratio: comp.aspect,
      promptCli: cliPrompt,
      promptApp: build('app'),
      images,
      tokenMap: images.map((im, i) => ({ cli: `图片${i + 1}`, app: `@Image${i + 1}`, label: im.label, file: im.file })),
      fileName: assetName({ project: project.title, kind: 'char', subject: c.name, variant: `${compKey}${outfit ? '-' + outfit.name : ''}`, version: 1 }),
      cli: `kling image_to_image --model ${model} ${imageFlags} --aspect_ratio ${comp.aspect} --imageCount 1 ${shellQuote(cliPrompt)}`,
      elementNote: elementId ? `Element ${elementId} is linked; add --elements '[{"id":"${elementId}","bindName":"${klingElementName(c.name)}"}]' and put <<<${elementId}>>> in the prompt.` : 'Create the Element first (see Element spec) to bind identity with <<<id>>>.',
      notes: [
        'Image slots are positional: 图片1 = first --image, 图片2 = second …',
        'Use kling-image-o1 for Element-bound identity; kling-image-v3_0_omni drifted in project tests.',
        'Confirm model/arguments with `kling who_am_i` before running; paid generation needs your go-ahead.',
      ],
    };
  }

  function shellSafe(p) { return String(p || '').replace(/^\/+/, ''); }
  function shellQuote(s) { return "'" + String(s).replace(/'/g, "'\\''") + "'"; }

  /* ====================================================== KLING ELEMENT SPECS */
  function klingElementSpecCharacter(project, c) {
    const front = c.images && c.images.front;
    const secondary = [c.images && c.images.side, ...(((c.images && c.images.extra) || []))].filter(Boolean).slice(0, 3);
    const name = klingElementName(c.name);
    const description = clean(join([c.name, c.role, c.age, c.build, c.hair, c.distinct], ', ')).slice(0, 200);
    const problems = [];
    if (!front) problems.push('Cover image missing (front headshot).');
    if (!secondary.length) problems.push('Needs 1–3 secondary images (side headshot, extra angles).');
    return {
      kind: 'Characters', tag: 'Characters', name, description, cover: front || '', secondary,
      problems,
      cli: front ? `kling element_create --name ${shellQuote(name)} --description ${shellQuote(description)} --tag Characters --cover ./${shellSafe(front)} ${secondary.map((s) => `--secondary ./${shellSafe(s)}`).join(' ')}`.trim() : '',
      note: 'Cover cannot be changed after creation. Secondary list is replaced as a whole on update. Costs and uploads need your go-ahead.',
    };
  }
  function klingElementSpecCostume(project, c, o) {
    const name = klingElementName(c.name, o.name);
    const secondary = (o.refs || []).slice(1, 4);
    const cover = (o.refs || [])[0] || '';
    const problems = [];
    if (!cover) problems.push('Add at least one outfit reference image.');
    if (cover && !secondary.length) problems.push('Kling needs 1–3 secondary images; add another angle of the outfit.');
    return {
      kind: 'Costumes', tag: 'Costumes', name, description: clean(o.description).slice(0, 200), cover, secondary, problems,
      cli: cover ? `kling element_create --name ${shellQuote(name)} --description ${shellQuote(clean(o.description).slice(0, 200))} --tag Costumes --cover ./${shellSafe(cover)} ${secondary.map((s) => `--secondary ./${shellSafe(s)}`).join(' ')}`.trim() : '',
      note: 'Costume Elements should not show a recognisable face on the cover.',
    };
  }
  function klingElementSpecScene(project, l) {
    const cover = (l.images || [])[0] || '';
    const secondary = (l.images || []).slice(1, 4);
    const name = klingElementName(l.name);
    const problems = [];
    if (!cover) problems.push('Add at least one location image.');
    if (cover && !secondary.length) problems.push('Kling needs 1–3 secondary images; add another angle.');
    return {
      kind: 'Scenes', tag: 'Scenes', name, description: clean(l.description).slice(0, 200), cover, secondary, problems,
      cli: cover ? `kling element_create --name ${shellQuote(name)} --description ${shellQuote(clean(l.description).slice(0, 200))} --tag Scenes --cover ./${shellSafe(cover)} ${secondary.map((s) => `--secondary ./${shellSafe(s)}`).join(' ')}`.trim() : '',
      note: 'Element ids come back from element_create; paste them into the character/location card to unlock <<<id>>> prompts.',
    };
  }

  /* ============================================================ LOCATION PLATES */
  const PLATES = [
    { key: 'wide', label: 'Wide establishing', lens: 'wide establishing shot, 24 mm, eye level', ratio: '16:9' },
    { key: 'medium', label: 'Medium (action area)', lens: 'medium shot of the main action area, 35 mm, eye level', ratio: '16:9' },
    { key: 'reverse', label: 'Reverse angle', lens: 'reverse angle of the same room, 35 mm, eye level', ratio: '16:9' },
    { key: 'detail', label: 'Detail / props', lens: 'close detail of the most characteristic surface or prop, 85 mm, shallow depth of field', ratio: '16:9' },
    { key: 'empty-vertical', label: 'Vertical plate (9:16)', lens: 'vertical framing of the same location, 28 mm, eye level', ratio: '9:16' },
  ];
  function locationPlates(project, l) {
    const style = STYLE_PRESETS[project.style] || STYLE_PRESETS['photoreal-unretouched'];
    const base = join([l.description, l.time ? 'time of day: ' + l.time : '', l.mood ? 'mood: ' + l.mood : '', l.palette ? 'palette: ' + l.palette : '']);
    const hasImg = (l.images || []).length > 0;
    return PLATES.map((p) => {
      const nlight = style.photo ? 'natural cinematic lighting, realistic materials, no CGI look' : style.lighting;
      const higgsPrompt = join([
        `Environment reference plate, ${p.lens}`,
        hasImg ? 'faithful to the attached location reference images (same architecture, materials, layout and colours)' : '',
        base, nlight,
      ]) + '. Empty location, no people, no characters, no reflections of people, no readable text, no watermark.';
      const tokCli = (i) => `图片${i}`;
      const kPromptCli = join([
        `Environment reference plate, ${p.lens}`,
        hasImg ? `same location as ${(l.images || []).slice(0, 3).map((_, i) => tokCli(i + 1)).join(', ')}, keep architecture, materials, layout and colours` : '',
        base, nlight,
      ]) + '. Empty location, no people, no silhouettes, no shadows of people, no reflections of people, no readable text, no watermark.';
      const kPromptApp = kPromptCli.replace(/图片(\d)/g, '@Image$1');
      const tool = hasImg ? 'image_to_image' : 'text_to_image';
      const model = (project.kling && project.kling.imageModel) || 'kling-image-o1';
      const imgFlags = hasImg ? (l.images || []).slice(0, 3).map((f) => `--image ./${shellSafe(f)}`).join(' ') + ' ' : '';
      return {
        key: p.key, label: p.label, aspect_ratio: p.ratio,
        fileName: assetName({ project: project.title, kind: 'loc', subject: l.name, variant: p.key, version: 1 }),
        higgsfield: { tool: 'generate_image', model: (project.higgsfield && project.higgsfield.imageModel) || 'nano_banana_pro', aspect_ratio: p.ratio, prompt: higgsPrompt, references: (l.images || []).map((f) => ({ role: 'image_references', file: f })) , elementName: higgsElementName('loc', l.name, 1)},
        kling: { tool, model, aspect_ratio: p.ratio, promptCli: kPromptCli, promptApp: kPromptApp, images: (l.images || []).slice(0, 3), cli: `kling ${tool} --model ${model} ${imgFlags}--aspect_ratio ${p.ratio} --imageCount 1 ${shellQuote(kPromptCli)}` },
      };
    });
  }

  /* ================================================================ OUTFIT SHEET */
  function outfitSheet(project, c, o) {
    const style = STYLE_PRESETS[project.style] || STYLE_PRESETS['photoreal-unretouched'];
    const hasRefs = (o.refs || []).length > 0;
    const text = join([
      `Costume reference sheet, outfit laid out as a clean front and back flat-lay on a neutral seamless background, plus one detail close-up of the fabric, closures and accessories`,
      hasRefs ? 'faithful to the attached outfit reference images (same garments, cut, colours, patterns and materials)' : '',
      outfitPhrase(o),
      style.photo ? 'soft diffused lighting, true colours, visible fabric texture' : style.lighting,
    ]) + '. No person, no mannequin, no face, no text, no watermark, no logos unless part of the garment.';
    return {
      fileName: assetName({ project: project.title, kind: 'outfit', subject: c.name, variant: o.name, version: 1 }),
      higgsfield: { tool: 'generate_image', model: (project.higgsfield && project.higgsfield.imageModel) || 'nano_banana_pro', aspect_ratio: '16:9', prompt: text, references: (o.refs || []).map((f) => ({ role: 'image_references', file: f })), elementName: higgsElementName('outfit', `${c.name}-${o.name}`, 1) },
      kling: {
        tool: hasRefs ? 'image_to_image' : 'text_to_image', model: (project.kling && project.kling.imageModel) || 'kling-image-o1', aspect_ratio: '16:9',
        promptCli: hasRefs ? text.replace('attached outfit reference images', (o.refs || []).slice(0, 3).map((_, i) => `图片${i + 1}`).join(', ')) : text,
        promptApp: hasRefs ? text.replace('attached outfit reference images', (o.refs || []).slice(0, 3).map((_, i) => `@Image${i + 1}`).join(', ')) : text,
      },
    };
  }

  /* ================================================================ SHOT PROMPTS */
  function castTokens(project, shot, target, ctx) {
    // Returns {ref: 'string used in prompt for each subject', binds, images}
    const out = [];
    for (const id of shot.subjects) {
      const c = (project.characters || []).find((x) => x.id === id);
      if (!c) continue;
      const el = c.klingElementId;
      if (target === 'cli') out.push({ c, ref: el ? `<<<${el}>>>` : `<<<ELEMENT_ID:${klingElementName(c.name)}>>>`, el });
      else out.push({ c, ref: `@${klingElementName(c.name)}`, el });
    }
    return out;
  }

  function actionLine(shot) {
    return sentence(shot.text);
  }

  function shotPrompts(project, shot, opts = {}) {
    const camera = CAMERA[(opts.camera || (project.shotOverrides || {})[shot.id]?.camera || project.defaultCamera || 'locked')] || CAMERA.locked;
    const style = STYLE_PRESETS[project.style] || STYLE_PRESETS['photoreal-unretouched'];
    const loc = (project.locations || []).find((l) => l.id === shot.locationId);
    const scene = (project.sceneSettings || {})['S' + pad(shot.sceneIndex)] || {};
    const speaker = shot.type === 'dialogue' ? (project.characters || []).find((c) => c.name.toLowerCase() === shot.character.toLowerCase()) : null;
    const cli = castTokens(project, shot, 'cli');
    const app = castTokens(project, shot, 'app');
    const subjectCli = cli[0] ? cli[0].ref : 'The subject';
    const subjectApp = app[0] ? app[0].ref : 'The subject';
    const preserve = (c) => `Preserve ${pron(c).pos} face, hair, wardrobe, the set and the lighting exactly as in the image.`;
    const first = (cli[0] && cli[0].c) || null;
    const exclusions = 'Nobody else enters the frame; no extra people, no text, no watermark.';
    const dur = shot.duration;
    const audioOn = shot.type === 'dialogue';

    // ----- action text depends on shot type
    let motionCli; let motionApp;
    if (shot.type === 'dialogue') {
      const who = speaker || first;
      const p = who ? pron(who) : PRONOUNS.they;
      const verb = (v) => v + p.s; // speaks / speak
      const delivery = shot.parenthetical ? `${shot.parenthetical}` : 'calmly';
      const quoted = `"${shot.text}"` + (/[.!?…]$/.test(shot.text) ? '' : '.');
      const speakCli = `${subjectCli} ${p.sub === 'they' ? 'speak' : 'speaks'} ${delivery} to the person off-screen, in a plain, unhurried voice. ${who ? who.name : 'The character'} says: ${quoted} ${cap(p.sub)} pause${p.s} briefly mid-line, then fall${p.s === 's' ? 's' : ''} silent after the last word. Quiet room tone only, no music.`;
      motionCli = speakCli.replace(/ {2,}/g, ' ');
      // Kling official native-audio syntax: Name (delivery, language): "line"
      motionApp = `${subjectApp} (${(shot.parenthetical || 'calm, unhurried').trim()}, in ${project.dialogueLanguage || 'English'}): ${quoted} ${cap(p.sub)} stay${p.s === 's' ? 's' : ''} still apart from natural speech movement and fall${p.s === 's' ? 's' : ''} silent after the last word. Quiet room tone only, no music.`;
    } else {
      motionCli = `${subjectCli} ${lowerFirst(actionLine(shot))}`;
      motionApp = `${subjectApp} ${lowerFirst(actionLine(shot))}`;
      if (!/(then|settles|stops|holds|returns|falls silent)\b/i.test(shot.text)) {
        motionCli = motionCli.replace(/\.$/, '') + ', then settles still.';
        motionApp = motionApp.replace(/\.$/, '') + ', then settles still.';
      }
    }

    const i2vCli = [motionCli, camera, first ? preserve(first) : 'Preserve the set and the lighting exactly as in the image.', exclusions].join(' ');
    const i2vApp = [motionApp, camera, first ? preserve(first) : 'Preserve the set and the lighting exactly as in the image.', exclusions].join(' ');

    // ----- keyframe (still image that starts the shot)
    const placeText = loc ? `${loc.name}${loc.time ? ', ' + loc.time : ''}${loc.mood ? ', ' + loc.mood : ''}` : (scene.place || 'the location');
    const keyBits = (target) => {
      const ctx = [];
      let n = 0;
      const ids = [];
      const refs = [];
      for (const t of (target === 'cli' ? cli : app)) {
        const outfit = (resolveScene(project, { index: shot.sceneIndex, place: '', beats: [] }).outfits[t.c.id]) || null;
        void outfit;
        const o = ((project.sceneSettings || {})['S' + pad(shot.sceneIndex)] || {}).outfits;
        const oid = o && o[t.c.id];
        const ofit = (t.c.outfits || []).find((x) => x.id === oid) || (t.c.outfits || [])[0];
        ids.push(`${t.ref}${target === 'cli' && t.el ? '' : ''}`);
        if (t.c.images && t.c.images.front) { n += 1; refs.push({ idx: n, file: t.c.images.front, label: t.c.name + ' face' }); }
        ctx.push(`${t.c.name}${ofit ? ' wearing ' + outfitPhrase(ofit) : ''}`);
      }
      let locIdx = 0;
      if (loc && (loc.images || [])[0]) { n += 1; locIdx = n; refs.push({ idx: n, file: loc.images[0], label: loc.name + ' plate' }); }
      return { ctx, ids, refs, locIdx };
    };
    const kc = keyBits('cli');
    const tokC = (i) => `图片${i}`;
    const keyframeCli = join([
      'Single cinematic still, first frame of the shot',
      kc.ids.length ? kc.ids.join(' and ') + (kc.refs.filter((r) => r.label.endsWith('face')).map((r) => ` with EXACTLY the face of ${tokC(r.idx)}`).join('')) : '',
      shot.type === 'dialogue' && speaker ? `${speaker.name} is about to speak` : actionStill(shot),
      kc.ctx.length ? kc.ctx.join('; ') : '',
      kc.locIdx ? `set in the location of ${tokC(kc.locIdx)} (keep architecture, materials, layout)` : `set in ${placeText}`,
      'natural skin texture, no retouching',
    ]) + '. Nobody else in the frame, no text, no watermark.';
    const keyframeApp = keyframeCli.replace(/图片(\d)/g, '@Image$1').replace(/<<<[^>]+>>>/g, (m) => {
      const name = (cli.find((t) => t.ref === m) || {}).c;
      return name ? '@' + klingElementName(name.name) : m;
    });
    const higgsKeyframe = join([
      'Single cinematic still, first frame of the shot',
      kc.ctx.length ? kc.ctx.join('; ') : '',
      'identity strictly from the attached character reference images',
      loc ? `location faithful to the attached location reference: ${loc.description}` : `set in ${placeText}`,
      shot.type === 'dialogue' && speaker ? `${speaker.name} is about to speak` : actionStill(shot),
      style.photo ? 'natural cinematic lighting, natural skin texture, no retouching' : style.lighting,
    ]) + '. Nobody else in the frame, no text, no watermark.';

    // ----- Higgsfield video prompts
    const hv = HIGGS_VIDEO_MODELS[(project.higgsfield && project.higgsfield.videoModel) || 'seedance_2_5'] || HIGGS_VIDEO_MODELS.seedance_2_5;
    const hvId = (project.higgsfield && project.higgsfield.videoModel) || 'seedance_2_5';
    const hDur = Math.max(hv.duration[0], Math.min(hv.duration[1], dur));
    const higgsRefs = [{ role: 'start_image', file: '<keyframe from step above>' }];
    if (hv.roles.includes('image_references')) {
      for (const t of cli) if (t.c.images && t.c.images.front) higgsRefs.push({ role: 'image_references', file: t.c.images.front, label: t.c.name + ' identity' });
    }
    const higgsVideoPrompt = [
      shot.type === 'dialogue'
        ? `${speaker ? speaker.name : 'The character'} speaks to the person off-screen${shot.parenthetical ? ' (' + shot.parenthetical + ')' : ''}: "${shot.text}"${/[.!?…]$/.test(shot.text) ? '' : '.'} Natural lip sync, ${hv.audio ? 'dialogue audio on' : 'natural mouth movement'}, falls silent after the last word. Quiet room tone, no music.`
        : sentence(shot.text) + ' Then everything settles still.',
      CAMERA[(opts.camera || (project.shotOverrides || {})[shot.id]?.camera || project.defaultCamera || 'locked')],
      'Keep the character identity, wardrobe, set and lighting exactly as in the start image. Nobody else enters the frame, no text, no watermark.',
    ].join(' ');

    // ----- Kling CLI args
    const vModel = (project.kling && project.kling.videoModel) || 'kling-video-v3_0';
    const klingArgs = {
      model: vModel,
      duration: String(Math.max(3, Math.min(15, dur))),
      resolution: '1080p',
      enable_audio: audioOn,
      prefer_multi_shots: false,
      aspect_ratio: project.aspect || '16:9',
    };
    const elArg = cli.filter((t) => t.el).map((t) => ({ id: t.el, bindName: klingElementName(t.c.name) }));
    const firstFile = `${assetName({ project: project.title, kind: 'shot', subject: shot.id, variant: 'keyframe', version: 1 })}`;
    const cliCmd = `kling image_to_video --model ${vModel} --input first_image=./${firstFile} --duration ${klingArgs.duration} --resolution ${klingArgs.resolution} --enable_audio ${klingArgs.enable_audio} --prefer_multi_shots false` +
      (elArg.length ? ` --elements '${JSON.stringify(elArg)}'` : '') + ' ' + shellQuote(i2vCli);

    return {
      id: shot.id,
      duration: dur,
      fileNames: {
        keyframe: firstFile,
        video: assetName({ project: project.title, kind: 'vid', subject: shot.id, variant: 'take', version: 1, ext: 'mp4' }),
      },
      kling: {
        keyframe: { tool: 'image_to_image', model: (project.kling && project.kling.imageModel) || 'kling-image-o1', promptCli: keyframeCli, promptApp: keyframeApp, images: kc.refs, elements: elArg },
        video: { tool: 'image_to_video', args: klingArgs, promptCli: i2vCli, promptApp: i2vApp, elements: elArg, cli: cliCmd },
      },
      higgsfield: {
        keyframe: { tool: 'generate_image', model: (project.higgsfield && project.higgsfield.imageModel) || 'nano_banana_pro', aspect_ratio: project.aspect || '16:9', prompt: higgsKeyframe, references: kc.refs.map((r) => ({ role: 'image_references', file: r.file, label: r.label })) },
        video: { tool: 'generate_video', model: hvId, duration: hDur, aspect_ratio: project.aspect || '16:9', prompt: higgsVideoPrompt, references: higgsRefs, audio: hv.audio ? { param: hv.audio, value: hv.audio === 'sound' ? (audioOn ? 'on' : 'off') : audioOn } : null },
      },
    };
  }
  function cap(s) { return s ? s[0].toUpperCase() + s.slice(1) : s; }
  function lowerFirst(s) { return s ? s[0].toLowerCase() + s.slice(1) : s; }
  function actionStill(shot) { return 'the opening pose of: ' + clean(shot.text).replace(/\.$/, ''); }

  /* ===================================================================== LINTER */
  /** Returns [{level:'error'|'warn'|'info', msg}] for a prompt in a given target. */
  function lintPrompt(prompt, ctx = {}) {
    const out = [];
    const target = ctx.target || 'kling-cli'; // kling-cli | kling-app | higgsfield
    const n = words(prompt);
    const add = (level, msg) => out.push({ level, msg });
    if (!prompt || !prompt.trim()) { add('error', 'Prompt is empty.'); return out; }
    const unresolved = prompt.match(/<<<ELEMENT_ID:[^>]+>>>/g);
    if (unresolved) add('error', `Unresolved Element marker ${unresolved[0]} — create the Element and paste its id on the character card.`);
    if (target === 'kling-cli') {
      if (/@(Image|image|video|[A-Z])/.test(prompt)) add('warn', 'CLI prompts use 图片N / <<<id>>> tokens, not @ handles (@ is the app syntax).');
      const idx = [...prompt.matchAll(/图片(\d+)/g)].map((m) => +m[1]);
      const max = ctx.imageCount;
      if (max != null && idx.some((i) => i > max)) add('error', `Prompt references 图片${Math.max(...idx)} but only ${max} image(s) are attached.`);
      const marks = [...prompt.matchAll(/<<<(\d+)>>>/g)].map((m) => m[1]);
      if (marks.length && ctx.elementIds && marks.some((m) => !ctx.elementIds.includes(m))) add('error', 'Element marker without matching --elements binding.');
      if (!marks.length && ctx.elementIds && ctx.elementIds.length) add('warn', '--elements given but no <<<id>>> marker in the prompt.');
    }
    if (target === 'kling-app' && /<<<|图片\d/.test(prompt)) add('warn', 'App prompts use @Image1 / @ElementName, not <<<id>>> or 图片N.');
    if (ctx.kind === 'i2v') {
      if (n > 130) add('warn', `Image-to-video prompt is ${n} words; keep it to motion only (60–120). Do not redescribe the scene.`);
      if (n < 15) add('warn', 'Very short prompt; add camera and preservation instructions.');
    } else if (ctx.kind === 'sheet') {
      if (n > 360) add('warn', `Sheet prompt is ${n} words; long prompts dilute identity.`);
    } else if (n > 220) add('warn', `Prompt is ${n} words; tighter prompts follow better.`);
    if (ctx.kind === 'i2v' || ctx.kind === 't2v') {
      if (!/camera/i.test(prompt)) add('warn', 'No camera instruction — the model will improvise. Add e.g. "Locked camera, no camera movement".');
      if (!/\b(no|nobody|never|without)\b/i.test(prompt)) add('info', 'No exclusions found; add what must not appear ("No text, no extra people").');
      if (!/(then|settles|stops|holds|returns|falls silent|ends)\b/i.test(prompt)) add('warn', 'Action has no end point ("then settles still") — open-ended motion can hang or drift.');
    }
    if (ctx.dialogue) {
      const sentences = ctx.dialogue.split(/[.!?]+/).filter((s) => s.trim()).length;
      if (sentences > 2) add('warn', `Dialogue has ${sentences} sentences; 1–2 per shot keeps lip sync stable.`);
      if (!prompt.includes(ctx.dialogue)) add('error', 'Dialogue line was altered — it must match the script exactly.');
      if (!/music/i.test(prompt)) add('info', 'Say "no music" if you want only room tone.');
    }
    if (target === 'higgsfield' && ctx.kind === 'sheet') {
      for (const need of ['no text', 'no watermark']) if (!prompt.toLowerCase().includes(need)) add('warn', `Missing "${need}" in negative tail.`);
    }
    if (/[“”]/.test(prompt) && target !== 'higgsfield') add('info', 'Curly quotes found; straight quotes are safer in CLI prompts.');
    return out;
  }

  /* ================================================================== FULL PACK */
  function buildPack(project) {
    const { scenes, shots } = buildShots(project);
    const characters = (project.characters || []).map((c) => ({
      character: c,
      element: klingElementSpecCharacter(project, c),
      sheets: Object.keys(COMPOSITIONS).map((k) => ({
        composition: k,
        higgsfield: higgsfieldCharacterSheet(project, c, (c.outfits || [])[0] || null, k),
        kling: klingCharacterSheet(project, c, (c.outfits || [])[0] || null, k),
      })),
      outfits: (c.outfits || []).map((o) => ({
        outfit: o,
        element: klingElementSpecCostume(project, c, o),
        sheet: outfitSheet(project, c, o),
        characterSheets: ['split-screen', 'turnaround'].map((k) => ({
          composition: k,
          higgsfield: higgsfieldCharacterSheet(project, c, o, k),
          kling: klingCharacterSheet(project, c, o, k),
        })),
      })),
    }));
    const locations = (project.locations || []).map((l) => ({ location: l, element: klingElementSpecScene(project, l), plates: locationPlates(project, l) }));
    const shotPack = shots.map((s) => ({ shot: s, prompts: shotPrompts(project, s) }));
    return { project: { id: project.id, title: project.title, style: project.style, aspect: project.aspect }, scenes, characters, locations, shots: shotPack };
  }

  /** Kling runner-compatible spec (blocked drafts; the producer removes submissionBlocked after review). */
  function klingSpec(project) {
    const pack = buildPack(project);
    const jobs = [];
    for (const { shot, prompts } of pack.shots) {
      const v = prompts.kling.video;
      jobs.push({
        job: `${slugify(project.title).toUpperCase()}-${shot.id}`,
        tool: 'image_to_video',
        model: v.args.model,
        auth: 'REPLACE-WITH-AUTHORIZED-APR-ID',
        submissionBlocked: 'Draft from Prompt Studio — review prompt, media, schema and budget before removing this field.',
        prompt: v.promptCli,
        args: { duration: v.args.duration, resolution: v.args.resolution, imageCount: '1', enable_audio: v.args.enable_audio, prefer_multi_shots: v.args.prefer_multi_shots },
        inputs: { first_image: prompts.fileNames.keyframe },
        ...(v.elements.length ? { elements: v.elements } : {}),
      });
    }
    return jobs;
  }

  /* ------------------------------------------------------------ markdown export */
  function toMarkdown(project) {
    const pack = buildPack(project);
    const L = [];
    L.push(`# ${project.title} — Prompt pack`, '', `Style: ${(STYLE_PRESETS[project.style] || {}).label || project.style} · Aspect: ${project.aspect} · Generated ${new Date().toISOString().slice(0, 10)}`, '');
    L.push('> Prompts only. Nothing here has been submitted or paid for. Confirm models with `kling who_am_i` / Higgsfield `models_explore` and your credit balance before generating.', '');
    for (const ch of pack.characters) {
      L.push(`## Character — ${ch.character.name}`, '');
      L.push(`**Kling Element** \`${ch.element.name}\` (tag ${ch.element.tag})`, '');
      if (ch.element.problems.length) L.push(...ch.element.problems.map((p) => `- ⚠ ${p}`), '');
      if (ch.element.cli) L.push('```bash', ch.element.cli, '```', '');
      for (const s of ch.sheets) {
        L.push(`### ${COMPOSITIONS[s.composition].label}`, '', `**Higgsfield** \`${s.higgsfield.model}\` · ${s.higgsfield.aspect_ratio} · file \`${s.higgsfield.fileName}\``, '', '```text', s.higgsfield.prompt, '```', '');
        L.push(`**Kling (CLI)** \`${s.kling.model}\``, '', '```text', s.kling.promptCli, '```', '', '**Kling (app)**', '', '```text', s.kling.promptApp, '```', '');
      }
      for (const o of ch.outfits) {
        L.push(`### Outfit — ${o.outfit.name}`, '', '```text', o.sheet.higgsfield.prompt, '```', '');
      }
    }
    for (const lo of pack.locations) {
      L.push(`## Location — ${lo.location.name}`, '');
      for (const p of lo.plates) {
        L.push(`### ${p.label} (${p.aspect_ratio}) — \`${p.fileName}\``, '', '**Higgsfield**', '', '```text', p.higgsfield.prompt, '```', '', '**Kling (CLI)**', '', '```text', p.kling.promptCli, '```', '');
      }
    }
    for (const sc of pack.scenes) {
      L.push(`## Scene ${sc.index} — ${sc.heading}`, '');
      for (const { shot, prompts } of pack.shots.filter((x) => x.shot.sceneIndex === sc.index)) {
        L.push(`### ${shot.id} · ${shot.type} · ${shot.duration}s`, '', `> ${shot.character ? shot.character + ': ' : ''}${shot.text}`, '');
        L.push('**Keyframe — Kling (CLI)**', '', '```text', prompts.kling.keyframe.promptCli, '```', '', '**Keyframe — Higgsfield**', '', '```text', prompts.higgsfield.keyframe.prompt, '```', '');
        L.push('**Video — Kling (CLI)**', '', '```text', prompts.kling.video.promptCli, '```', '', '**Video — Kling (app)**', '', '```text', prompts.kling.video.promptApp, '```', '', `**Video — Higgsfield** \`${prompts.higgsfield.video.model}\` ${prompts.higgsfield.video.duration}s`, '', '```text', prompts.higgsfield.video.prompt, '```', '');
      }
    }
    return L.join('\n');
  }

  return {
    slugify, pascal, words, pad, PRONOUNS, KLING_TAGS, KLING_IMAGE_MODELS, KLING_VIDEO_MODELS, HIGGS_IMAGE_MODELS, HIGGS_VIDEO_MODELS,
    CAMERA, STYLE_PRESETS, COMPOSITIONS, PLATES, NAME_KINDS,
    assetName, higgsElementName, klingElementName,
    parseScript, sceneCast, buildShots, resolveScene, estimateDuration,
    higgsfieldCharacterSheet, klingCharacterSheet, klingElementSpecCharacter, klingElementSpecCostume, klingElementSpecScene,
    locationPlates, outfitSheet, shotPrompts, lintPrompt, buildPack, klingSpec, toMarkdown,
  };
});
