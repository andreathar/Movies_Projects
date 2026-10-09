# Historian Review — English Script v2 (T05)

Reviewed: `01_script/script-en.md` (v2, 2026-10-09) against `00_brief/research/snapshots/source-01..17.md` plus the three snapshots created during this review (18, 19, 20). Method: every factual anchor was searched verbatim in the cached snapshot text; "supported" means the wording is covered by the cited snapshot, not by general knowledge. All dialogue is fictional and is assessed only for (a) factual anchors it relies on and (b) whether it could be mistaken for a documented statement.

Files touched by this review: this report; `snapshots/source-18.md`, `snapshots/source-19.md`, `snapshots/source-20.md` (new). Nothing else was modified. Registry/citations edits are proposed below, not applied.

## 1. Summary verdict

**APPROVE WITH EDITS.**

The dialogue (v2) contains no unsupported dates, numbers, casualty figures, legendary quotations, or single-cause claims. Two edits are required in the script's notes/sources, none in the spoken lines:

1. O-chapter factual note: replace `[NEEDS SOURCE — historian to add to registry]` with `[20]` (OSTI "Japan Surrenders, August 10-15, 1945", snapshot saved). Add [20] to the Sources block.
2. Registry: sources 18 and 19 now have snapshots; titles and hashes below should be entered in `source-registry.json` (currently `snapshotStatus: not_found_in_current_cache`).

Scene bibles (not the script) carry several unsourced precision claims (Trinity 05:29:21, Longwood/Northumberland dates, Chasseurs uniform, Galileo's eyesight in 1634, Discorsi attributed to [3], "millions who died"); see §4. They also still quote v1 dialogue.

## 2. Claim table

Status key: **S** supported by cited snapshot · **I** dramatic interpretation (no factual claim; no source needed) · **U** unsupported by cited source · **W** needs wording change.

| Line ID | Claim | Source ID(s) | Status | Proposed wording / note |
|---|---|---|---|---|
| IN-L01 | none (framing) | — | I | — |
| C-setting | Rome, early 44 BCE, before assassination on Ides of March 44 BCE | [1] | S | [1]: "assassinated … on the Ides of March in 44 bce". |
| C-L01 | fictional question | — | I | — |
| C-L02 | "victories and the reforms" studied | [1] | S | [1]: "conquest of Gaul (58–50 bce), his victory in the civil war of 49–45 bce … a series of political and social reforms". |
| C-L02 | "what one man's power did to a republic" | [1] | S | [1]: "accumulation of power, including his appointment as dictator, threatened the Roman Republic"; "central role in the transformation of the Roman Republic into the Roman Empire". Wording avoids single-cause claim; keep. |
| C-L03 | "tyrant?" (figure's fictional question) | — | I | Not an attributed quotation. |
| C-L04 | "Could the republic survive you?" / "still asking it — about other men" | [1] | I | Interpretation; no named person. Nothing beyond [1] asserted. |
| C-note | "avoid making him the single cause" | [1] | S | Consistent with [1] ("contributing to the end of the republic"). |
| K-setting | campaign tent, 1227 | [2][15] | S | [2]: "destructive campaign … against Xi Xia in 1226–27 … death of Genghis Khan during that campaign (1227)". [15]: "invaded Xixia in 1227 and besieged the capital of Zhongxing". Confirms the Western Xia context used in `genghis.md`. |
| K-L01 | "my sons" | [2] | S | [2] names Tolui, Ögödei, Chagatai, Jöchi and their ulus. |
| K-L02 | successors made the empire larger | [2][15] | S | [2]: Hülegü "completed the conquest of Iran, Iraq, and Syria"; [15]: Möngke-era campaigns, Qubilai. Attributed to successors, not Genghis — correct. |
| K-L02 | "Merchants, ideas, and knowledge will cross it" | [2][15] | S | [15]: "merchants and others could now travel from one end of the empire to another … Pax Mongolica"; "mechanical printing, gunpowder, and the blast furnace made their way west". [2]: "The Mongols favored trade". |
| K-L02 | "cities that are no longer there" | [2] | S | [2]: "destruction of the prosperous towns" (Khwārezm); Xi Xia culture "virtually annihilated". No city named, no figure — compliant. |
| K-L04 | "Founder. Conqueror." | [15][16] | S | [15]: Temüjin unified tribes into the Yeke Mongol Ulus; [16] snapshot: "one of the most famous conquerors of history". |
| K-L04 | "Neither one can make the dead speak" | — | I | — |
| G-setting | Arcetri, 1634, house arrest after 1633 trial | [3][12] | S | [3]: "The trial ended on June 22, 1633. Galileo was sentenced to life imprisonment and forced to abjure". [12]: "permitted to return to the villa on December 1, 1633, but was barred from receiving visitors". 1634 falls inside this confinement. |
| G-L02 | "Believed, taught — and turned into a simple story" | — | I | Reputation synthesis, labelled as such in the script preamble. |
| G-L02 | "The truth was harder" | — | I | — |
| G-L04 | "Your observations" survive | [3] | S | [3] lists objective lens (1609–10) and *Sidereus Nuncius* (1610). |
| G-L04 | "one lesson from your trial … silencing a man does not settle a question" | [3] | I | Interpretation of a documented trial; not a quotation. "And yet it moves" absent — correct. |
| N-setting | Saint Helena, 1816 | [4] | S (by inference) | [4]: defeated at Waterloo 18 June 1815, "forced to abdicate for a second time", "exiled to … St. Helena", "died on 5 May 1821". 1816 lies within; exact arrival date is not in [4] (see §4). |
| N-L02 | "Your code outlives your throne" | [17][4] | S | [17]: "enacted on March 21, 1804, and is still extant, with revisions"; [4]: abdication 1815. |
| N-L02 | "Other nations borrow from it" | [17] | S | [17]: "main influence on the 19th-century civil codes of most countries of continental Europe and Latin America". |
| N-L02 | "promises equality — and still finds people to leave out" | [17] | S | [17]: "civil equality, equality before the law" … "reverted to patriarchal standards … wives owe their husbands obedience"; "rolled back some gains women had made". |
| N-L03 | Napoleon asks about Andre's world | — | I | Fully fictional; contains no factual assertion. Confirmed. |
| N-L04 | "We are still not sure who pays it" | — | I | — |
| O-setting | fictional room near Trinity base camp, 15 July 1945 | [5] | S | [5]: observers "at base camp"; "pouring rain"; test fired 16 July 1945. |
| O-L02 | "It works" | [5] | S | [5]: "At precisely 5:30 a.m. on Monday, July 16, 1945 … the device exploded". |
| O-L02 | "Three weeks later, Hiroshima" | [5][18] | S | [18]: "(Hiroshima, Japan, August 6, 1945)". 16 Jul → 6 Aug = 21 days. |
| O-L02 | "Three days after that, Nagasaki" | [18][19] | S | [19]: "just three days after the attack on Hiroshima"; "(Nagasaki, Japan, August 9, 1945)". |
| O-L02 | "The war ends that summer" | **[20]** (new) | S — was unsourced | [20]: "On August 15, 1945, the emperor's broadcast announcing Japan's surrender was heard via radio all over Japan … on September 2, 1945, the formal surrender ceremony took place on the deck of the U.S.S. Missouri." Line asserts timing only, not cause — acceptable. **Required edit:** replace `[NEEDS SOURCE …]` in the O factual note with `[20]`; add [20] to Sources. |
| O-L02 | "What it cost — and whether it had to — people are still asking" | [9] | S | [9] documents the Franck Report / Scientific Panel / Interim Committee disagreement. [20] additionally records Soviet entry (8 Aug) and the emperor's tie-break — supports keeping the line multi-causal. No casualty figure in dialogue — compliant ([18][19] give only estimates with "No one will ever know for certain"). |
| O-L03 | fictional question | — | I | — |
| O-L04 | "I can tell you what came next. I can't tell you that." | — | I | — |
| O-note | "famous later Oppenheimer quotation" not used | — | S | Confirmed absent. |
| OUT-L01 | none | — | I | — |

## 3. New sources found

| Proposed ID | URL | Title (as fetched) | Supports | Snapshot path | SHA-256 |
|---|---|---|---|---|---|
| 18 (existing ID, snapshot was missing) | https://www.osti.gov/opennet/manhattan-project-history/Events/1945/hiroshima.htm | Manhattan Project: The Atomic Bombing of Hiroshima, August 6, 1945 | Hiroshima date; "Little Boy" uranium gun-type bomb; Truman statement; Soviet declaration 8 Aug | `00_brief/research/snapshots/source-18.md` | `9168c68ba49932e80cbd72b57349bdb4421e12f769b0934a88f96282a4770f99` |
| 19 (existing ID, snapshot was missing) | https://www.osti.gov/opennet/manhattan-project-history/Events/1945/nagasaki.htm | Manhattan Project: The Atomic Bombing of Nagasaki, August 9, 1945 | Nagasaki date; "three days after"; "Fat Man" plutonium implosion bomb; emperor's intervention next day | `00_brief/research/snapshots/source-19.md` | `960255fda52d7d48335651a11d3e4425c5779787b3d58d83c97ccb3ab5ecec13` |
| **20 (new)** | https://www.osti.gov/opennet/manhattan-project-history/Events/1945/surrender.htm | Manhattan Project: Japan Surrenders, August 10-15, 1945 | Surrender offer 10 Aug; US reply 12 Aug; emperor's broadcast 15 Aug; formal ceremony 2 Sep 1945 aboard USS Missouri; multi-factor account (Soviet entry, Nagasaki, Imperial Council 3–3 tie) | `00_brief/research/snapshots/source-20.md` | `5bb6911eb04e041d595cfc0fd8c770176728fa4e451ba711167496ab5fb97a37` |

All three fetched 2026-10-09 via web extraction, saved in the same raw-markdown format as source-01..17 (page body, no header). Suggested registry entries: `accessed: 2026-10-09`, `snapshotStatus: "fetched_extraction"`, `evidenceValidated: false`.

Candidate for a later registry add (fetched for cross-check, **not** snapshotted — outside this task's file remit): https://www.britannica.com/biography/Galileo-Galilei/Galileos-Copernicanism — supports: six months at the archbishop's palace in Siena before Arcetri; Maria Celeste's death in 1634; "Galileo was then 70 years old"; *Discorsi* published Leiden 1638; blindness "by then" (1638). Needed to back several `galileo.md` claims (see §4).

## 4. Scene-bible flags (`03_bibles/scene-bibles/`)

General (all five files): §3 dialogue tables still contain **v1 lines** (e.g. "Your name survives. So do the reforms…", "They will enlarge it…", "And do they call me great?", "That is not the same as answering the question"). Eye-cue triggers in §1 also reference v1 phrases ("families who never return", "When they say greatness…"). Not a historical error, but the bibles must be re-synced to v2 line text before translation/atlas work.

**caesar.md**
- "dictator perpetuo" (×2): [1]/[13] say "dictator (46–44 bce)"; the title *perpetuo* is not in the cached sources. Unverified; either source it or write "dictator".
- "provincial reorganization, and debt relief": not found in [1]/[13] snapshots ([13] mentions calendar reform 46 BCE and the *municipia* law 45 BCE). Unverified; reword to "calendar reform and local-government law" or add a source.
- Props/wardrobe (wax tablet, toga praetexta, signet ring): fictional design, no claim; fine.

**genghis.md**
- "Western Xia / Yinchuan campaign, summer 1227": campaign and year supported [2][15]; "Yinchuan" (modern name of the Xi Xia capital Zhongxing) is not in the sources — [15] says "modern Ningxia and Gansu". Prefer "Zhongxing (Xi Xia capital)".
- "he died in August 1227": the source-16 snapshot carries "died August 18, 1227 … during a campaign against the Tangut kingdom of Xixia", but that text belongs to Britannica's Genghis Khan biography, whereas registry [16] is titled/URL'd as the Golden Horde page. Flag the registry mismatch; cite [16] only after the registry entry is corrected, or add the biography URL as its own ID.
- "Jochi, Chagatai, Ögedei, Tolui", "Yeke Monggol Ulus", "Pax Mongolica", Kublai: supported [2][15][16].
- "massive civilian casualties and demographic disruption": qualitatively supported by [2] ("destruction of the prosperous towns … disintegration of the irrigation system"); contains no number — acceptable.

**galileo.md**
- "failing eyesight", "milky-strained eyes", "slight cataract haze" (1634): **not supported** by [3] or [12]. Britannica (candidate source above) dates blindness to "by then" 1638. For late 1634 the eyes should read as weariness, not visual impairment — this also matches the script's own Eye cue A ("exhausted attention, not blindness"). Recommend removing cataract/milky language or sourcing a 1634-specific account.
- "Aged 70": supported ([12] gives 1564–1642; Britannica candidate: "Galileo was then 70 years old").
- "house arrest first in Siena and then at Villa Il Gioiello": Siena is not in [3]/[12]; supported only by the Britannica candidate. Add that source or drop "Siena".
- "Published *Discorsi* … in Leiden in 1638 … [3]": [3] does not mention the *Discorsi*; it mentions the 1632 *Dialogue* and the ban. Mis-citation. Re-cite to the Britannica candidate once registered.
- Props: "manuscript sheets of astronomical diagrams" — fictional, unreadable per review rule; fine. If a copy of the *Dialogo* is placed on the table, note that [3] records the book was banned in 1633; owning a copy is plausible but unsourced for this villa. Notes toward the motion/strength-of-materials work are consistent with the Britannica candidate ("In Siena he had begun a new book on the sciences of motion and strength of materials"), not with [3].
- "lifelong papal house arrest": supported by [3] ("life imprisonment") + [12] (confinement at villa until death 1642).

**napoleon.md**
- "Longwood House", "aboard HMS Northumberland in October 1815", "Longwood House from December 1815", "autumn 1816": none of these names/dates are in [4] ([4] gives only Waterloo 18 June 1815, exile to St. Helena, "very damp and dark house", death 5 May 1821). Unverified precision — source or soften to "Saint Helena, 1816".
- "dictating his memoirs to Las Cases": [4] says he "dictated the memoirs of his reign"; Las Cases not named. Partial.
- "Dark forest-green wool tailcoat of the Chasseurs-à-Cheval with red piping; brass eagle buttons; Légion d'Honneur star": uniform is **unsourced** ([4] only notes he created the Légion d'honneur). Needs a costume reference or a note that it is a design choice.
- "establishing legal equality and religious freedom": [17] says "freedom of conscience … secular nature of the state" — reword to "freedom of conscience" to stay inside the source.
- Eye cue B: "acknowledging the millions who died under his eagles" — unsupported casualty claim; violates the no-casualty-numbers rule. Delete "millions".
- Linguistic note (Corsican/Italian, French by age nine at Autun, retained accent): supported [8]. "Brienne" and "Italo-Romance dialect closely related to Tuscan" are paraphrase; [8] says "idioms with Tuscan roots".
- "*Code Civil des Français*, 1804": supported [17].

**oppenheimer.md**
- "05:29:21 MWT" / "5:29:21 AM MWT": [5] says "At precisely 5:30 a.m." and that the shot was "pushed … back to 5:30". The second-level timestamp is not in the cited source. Change to "about 5:30 a.m." or add a source that gives the exact second.
- "Alamogordo Bombing and Gunnery Range, 35 miles southeast of Socorro": [5] gives "Alamagordo Bombing Range … 'Jornada del Muerto' … 210 miles south of Los Alamos". The Socorro distance is unsourced.
- "chainsmoking, pacing": unsourced characterization (fictional motivation is allowed, but it reads as biography). Mark as dramatic.
- "stormy desert night", rain on roof: supported [5] ("pouring rain"; "At 4:00, the rain stopped").
- "Little Boy" uranium / "Fat Man" plutonium: supported [18][19].
- "Franck Committee, Interim Committee … demonstration, international control": supported [9].
- Props (field notebook, cigarettes, pocket watch): fictional; no claim; fine.

## 5. Proposed edits (for the producer; not applied)

Script `script-en.md`:
1. O factual note: `… surrender announced 15 August / signed 2 September 1945: **[NEEDS SOURCE — historian to add to registry]**` → `… surrender announced 15 August / formal ceremony 2 September 1945.[20]`
2. Sources block: append `[20] https://www.osti.gov/opennet/manhattan-project-history/Events/1945/surrender.htm`.
3. Optional, O factual note: add "[20] also records Soviet entry on 8 August and the emperor's intervention; the line states a date, not a cause."

`source-registry.json` / `citations.json`:
4. ID 18: title "Manhattan Project: The Atomic Bombing of Hiroshima, August 6, 1945", snapshotPath `00_brief/research/snapshots/source-18.md`, sha256 above.
5. ID 19: title "Manhattan Project: The Atomic Bombing of Nagasaki, August 9, 1945", snapshotPath `00_brief/research/snapshots/source-19.md`, sha256 above.
6. Add ID 20 as in §3.
7. Check ID 16: snapshot content includes the Genghis Khan biography, registry URL is the Golden Horde page.

Scene bibles: items in §4.

## 6. Items I could not verify

- Trinity detonation time to the second (05:29:21 MWT) — not in [5].
- Napoleon's arrival at Saint Helena (October 1815), HMS *Northumberland*, Longwood from December 1815 — not in [4]; no fetch attempted beyond the registry.
- Chasseurs-à-Cheval uniform and Légion d'honneur insignia at Longwood — no source in registry.
- Caesar "dictator perpetuo", "provincial reorganization", "debt relief" — not in [1]/[13] snapshots.
- Galileo's eyesight in 1634 — no source found that dates visual impairment to 1634; Britannica places blindness by 1638.
- Galileo at Siena and *Discorsi* Leiden 1638 — supported only by a page fetched during review that is not yet in the registry.
- "Yinchuan" as the 1227 campaign site — modern toponym not in sources.
- Web searches for a Museo Galileo page on blindness returned no results; no other fetch failed.
