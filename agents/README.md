# Agent Roles

`registry.json` is the index of the local role briefs: producer, director, continuity, historian, dialogue-sound, storyboard, editor, qc and lighting at the time of writing. Read the registry for the current list; do not hard-code a count here. These documents do not start autonomous agents. The producer passes the relevant brief, exact film/task paths, current state and allowed scope when it delegates explicitly, to whichever tool or session is assigned. A platform name is not a role; who holds each role in an episode is recorded only in the responsibilities table of [PARLEY_PROTOCOL.md](../docs/PARLEY_PROTOCOL.md). Reviewers return findings; the producer verifies artifacts and applies task transitions.

Spending, paid submission and credential rules are in [AGENTS.md](../AGENTS.md) and are not restated in the briefs' index. No daemon, cron, agent credential store or third-party agent process is created.

Local source editing is authorized within assigned responsibilities. Follow [LOCAL_AGENT_HANDOFF.md](../docs/LOCAL_AGENT_HANDOFF.md); preserve other agents' work and record input/output hashes using [agent-handoff.json](../shared/templates/agent-handoff.json). Read-only defaults in individual reviewer briefs yield to an explicit local editing assignment, while producer-only state changes and the paid-submission restriction remain in force.
