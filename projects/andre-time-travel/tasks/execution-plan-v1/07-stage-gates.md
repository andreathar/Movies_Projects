# Stage and edition gates: avoid accidental overblocking

The package catalogue contains **96 responsibility groups**. Some groups contain preparation and approval, both language editions, or distinct chapters. Their expanded [execution graph](execution-graph.json) contains **111 planning instances** and is the authority within this plan for proposed prerequisites. It does not replace the actual board or approve execution. A future dispatcher must use instance prerequisites and scoped evidence, never require every sibling stage/edition to finish before useful work starts.

| Package | Instance | Prerequisites | What it proves |
|---|---|---|---|
| O01 | inventory | Local read-only inspection | Installed solution/contract known; no live lane needed |
| O01 | restore | Inventory; actual user-terminal restoration | Intended native session and current identity ready for handshake |
| O07 | Adapter implementation | O01.inventory + O06 | Fake-adapter development/testing is independent of lane restoration |
| W26 | EN / H | Approved English text / reviewed translations respectively | Scoped dry voice artifacts for that edition |
| W27 | EN / H | Selected voice and that edition's actual dry tracks | Measured timing and conform for that edition |
| W30 | EN | W27.EN + W31 | English speech route proof |
| W30 | H | W27.H + W29 + W31 | Representative difficult localized speech proof based on reviewed actual audio |
| W33 | forecast | W03 + W31 | Offline feasibility estimate with historical values labeled |
| W33 | release | Forecast + W43 | Chapter evidence reconciled for exact release planning; W37 still refreshes live scope/balance/schema |
| W34 | scratch | W21 + W24 | Free local animatic from labeled candidate images and measured guide; no personal likeness or paid-release gate |
| W34 | approval | Scratch + W20 + W23 + W33.forecast | Reviewed production coverage/pacing, distinct from final voice and actual paid release |
| W35 | Reference packet | W34.approval + W22 + W07 | Stable approved-use inputs for later exact shot preflight |
| W45 | G | Accepted compatible takes + Galileo repair disposition | First complete Galileo recipe, with guide/final scope explicit |
| W46 | prepare | Current bibles, selected coverage and guide | Local preparation of the other four chapters independently of Galileo acceptance |
| W46 | C / K / N / O | Preparation + W45.G | Each remaining chapter's own scoped shot loop and complete acceptance evidence |
| W47 | prepare / produce | English text / preparation plus W45.G respectively | Bookend planning remains independent; production follows the proven recipe |
| W48 | English assembly | W46.C/K/N/O + W47.produce | All four remaining chapters and bookends available, not just the first chapter |
| W54 | Final English conform | Corrections + W27.EN + W30.EN + contact-sound conform | Final English speech-route proof cannot be skipped on the path to export |
| W55 | EN / H | English picture/audio lock / historical conform | Actual mix and measurements specific to that edition |
| W57 | EN / H | English lock / historical conform | Captions reviewed against the corresponding actual audio |
| W58 | EN | English mix + English captions | English export independent of H readiness |
| W58 | H | Historical mix + historical conform + H captions | Historical export with all its own language/mix prerequisites |
| W59 | EN / H | Respective exact export | Independent exact-file QC for that edition |
| W60 | Joint final acceptance | W59.EN + W59.H | Both editions ready for final package acceptance |

English review/finishing can proceed while historical-language work remains pending. The joint final-film completion condition still requires both edition outputs, qualified language evidence where applicable, exact-file playback and Andre's required judgments. Individual English acceptance can be recorded earlier, but cannot clear the whole-film final flag.

Package-level output paths ending in `next` are placeholders for scoped new revisions. Per-edition/per-stage assignments must choose distinct actual output paths and name the exact artifact use. Their input fingerprints and evidence cannot be silently shared across editions. Reused media can share original bytes while each edition retains its own audio/timing/caption review. Every split instance has its own acceptance evidence contract; do not copy a whole-package requirement for both editions or finished chapters onto an English-only or preparation instance.

Already completed or unnecessary generation/correction work does not have to be repeated. An instance can use exact prior proof, or a producer-reviewed not-needed/reuse disposition, if that satisfies its intended outcome. This does not waive a mandatory gate: for example, “no new clip needed” can satisfy a new-generation branch when accepted media already covers it, but “no language review needed” cannot erase a required unreviewed translation.

The graph was checked for cycles and six specific independence properties: scratch does not inherit W20 personal likeness or W37 paid preflight; English export does not inherit W56 historical assembly; H speech proof includes reviewed translation and actual H tracks; O07 does not require live lane restoration; joint final acceptance includes both QC instances. Those structural checks do not prove future runtime evaluation; they become regression scenarios for the implementation.

W35–W42 form a reusable per-shot subgraph. Instantiate it with episode, chapter, selected slot/use, request revision and input hash for each necessary new take. The explicit first Galileo instances feed W45.G; the four W46 chapter instances each invoke their own separately scoped copies and end with their own chapter review. This is a finite expansion of selected work, not a loop that automatically requests another generation. W46.prepare and W47.prepare have no Galileo-acceptance ancestor; W48 requires all C/K/N/O instances, not only Caesar.
