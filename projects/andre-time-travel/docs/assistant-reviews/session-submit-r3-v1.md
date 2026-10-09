# Session submit R3 v1

Written 2026-10-09. Six prepared image jobs were submitted once through the installed Kling CLI. No Element, no video, and no extra image. R3-session-01 and R3-session-07 were not submitted. No retry. Inbox originals were not moved. Approvals, bibles, and STATE.md were not edited.

Live account read before any create: **6716** credits. The CLI schema for `gemini-3-pro-image` does not publish a price. The last observed charge at 2k / `image_count` 1 was 20, which is under the 30-credit stop. The live balance was above 120, so the batch proceeded.

Each create response returned `creditsConsumed: 20`. Query status after that was COMPLETED with one work each. A later account read was **6596** (6716 minus 120). That matches the six reported charges. Cost was returned; it was not guessed.

| Job | Generation id | Submit status | Query status | creditsConsumed |
|---|---|---|---|---|
| R3-session-02 | `AVh3-PtlINQfPQU4zJ5K2ufTQQ6DH9Oy6n6B14nLq8qquXxUuvJMqEtvCOVzZp4ox-2U2iJb` | QUEUING | COMPLETED | 20 |
| R3-session-03 | `AbWqjlXSbsPqSmacIpTsswjAj7JWBeF5aqZEDDsBo3I6EWk8WmI5GB68IB36rQ0D2fxniHjg` | QUEUING | COMPLETED | 20 |
| R3-session-04 | `AQ3lJeiYD_O0xmYlaWllQVRzyMas1e3uPZqBWFbABlUO7Lxbr7O4syjy58RR4QU1zOYbJB_3` | QUEUING | COMPLETED | 20 |
| R3-session-05 | `AY72ooKEeU3l_RVmtEgSGL-DUTzHqmkHAkkssThmNO6m4KQhCU5x40GVL4hiZglmcLX4VVlk` | QUEUING | COMPLETED | 20 |
| R3-session-06 | `ATOX4rpOMNTtNUQXUfXxOHdf4qK9JEJsdCfftXPosZWvajGYTsE5ur6jqEmGRZChJnLPG8u2` | QUEUING | COMPLETED | 20 |
| R3-session-08 | `Ac1sk-wsnA3F5tpsp3MHQXnlqqy1zwFBvm4VJ1AbhJij8DbjuvFhzk2I7AfFqGgeYB4HIn_M` | QUEUING | COMPLETED | 20 |

**Total reported by the CLI: 120 credits.** No job failed to submit.

Create responses: `07_generations/responses/R3-session-02.response.json` through `08`, skipping 01 and 07. Ledger rows `LR3-session-02` through `LR3-session-08` use those ids and the returned `creditsConsumed`. `balance_after` on those rows is 6716 minus the running sum of the reported charges in submit order. The live post-batch read was 6596.

Downloaded works, labelled synthetic and unapproved: `07_generations/originals/R3-session-02_1.jpg`, `03_1.jpg`, `04_1.jpg`, `05_1.jpg`, `06_1.jpg`, `08_1.jpg`. Likeness is not approved by this file.
