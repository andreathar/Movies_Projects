# Agent Roles

`registry.json` indexes the seven local role briefs. These documents do not start autonomous agents. The parent passes the relevant brief, exact film/task paths, current state and allowed scope into an explicit Hermes delegation. Reviewers return findings; the parent verifies artifacts and applies task transitions. Only the producer can run an approved paid shot.

No daemon, cron, agent credential store or third-party agent process is created.

Local source editing is now authorized within assigned responsibilities. Follow [LOCAL_AGENT_HANDOFF.md](../docs/LOCAL_AGENT_HANDOFF.md); preserve other agents' work and record input/output hashes using [agent-handoff.json](../shared/templates/agent-handoff.json). Read-only defaults in individual reviewer briefs yield to an explicit local editing assignment, while producer-only state changes and paid submission restrictions remain in force.
