---
name: deprecation-and-migration
description: Use when replacing, retiring, or consolidating systems, APIs, features, dependencies, or data contracts and a measured compatibility, migration, or removal plan is required.
metadata:
  source: https://github.com/addyosmani/agent-skills/tree/17214a29c429a19f7a9607f2c06f9d650ea87eb0/skills/deprecation-and-migration
  license: MIT
  adapted-for: cross-agent
---

# Deprecation and Migration

> This Skill plans and verifies lifecycle change. Removing code, data,
> infrastructure, or user access remains an explicitly authorized operation.

## Coordination and Authority

This Skill owns lifecycle analysis, migration evidence, and removal readiness.
The canonical debugging workflow owns unknown failures; observability owns
durable usage telemetry; the active testing workflow owns regression evidence;
and shipping owns GO/NO-GO, rollout, deployment, and rollback decisions.

Do not install dependencies, change CI or production configuration, remove
consumer-facing behavior, commit, push, or deploy unless the current user
instruction and active permission process authorize that exact scope.

## Overview

Code provides value and also carries ongoing cost: bugs, dependencies, security
patches, compatibility obligations, records, and operational knowledge.
Deprecation evaluates whether a system still earns that cost; migration moves
affected subjects safely when replacement or retirement is justified.

This Skill addresses the recurring gap between building new capability and
governing its eventual replacement, preservation, or retirement.

## When to Use

- Replacing an old system, API, or library with a new one
- Sunsetting a feature that's no longer needed
- Consolidating duplicate implementations
- Removing dead code that nobody owns but everybody depends on
- Planning the lifecycle of a new system (deprecation planning starts at design time)
- Deciding whether to maintain a legacy system or invest in migration

## Core Principles

### Code Has Carrying Cost

Maintained production code generally has ongoing cost: tests, documentation, security patches,
dependency updates, and cognitive overhead. Removal is justified only when the
replacement or retirement path preserves required value, safety, compliance,
history, recoverability, and compatibility better than continued maintenance.

### Hyrum's Law Makes Removal Hard

With enough users, every observable behavior becomes depended on — including bugs, timing quirks, and undocumented side effects. This is why deprecation requires active migration, not just announcement. Users can't "just switch" when they depend on behaviors the replacement doesn't replicate.

### Deprecation Planning Starts at Design Time

When building something new, ask: "How would we remove this in 3 years?" Systems designed with clean interfaces, feature flags, and minimal surface area are easier to deprecate than systems that leak implementation details everywhere.

## The Deprecation Decision

Before deprecating anything, answer these questions:

```
1. Does this system still provide unique value?
   → If yes, maintain it. If no, proceed.

2. How many users/consumers depend on it?
   → Quantify the migration scope.

3. Does a replacement or safe withdrawal path exist?
   → If no, keep the system unless an urgent safety, legal, or security duty
     requires controlled shutdown without a like-for-like replacement.

4. What's the migration cost for each consumer?
   → If trivially automated, do it. If manual and high-effort, weigh against maintenance cost.

5. What's the ongoing maintenance cost of NOT deprecating?
   → Security risk, engineer time, opportunity cost of complexity.
```

## Compulsory vs Advisory Deprecation

| Type | When to Use | Mechanism |
|------|-------------|-----------|
| **Advisory** | Migration is optional, old system is stable | Warnings, documentation, nudges. Users migrate on their own timeline. |
| **Compulsory** | Old system has security issues, blocks progress, or maintenance cost is unsustainable | Set an authorized deadline and provide migration tooling or controlled-withdrawal protections, as applicable. |

**Default to advisory.** Use compulsory only when the maintenance cost or risk
justifies forcing migration. Where migration is possible, provide proportionate
tooling, documentation, and support. An urgent controlled shutdown may instead
require notice, export, preservation, recovery, and exception handling.

## The Migration Process

### Step 1: Build the Replacement

For a replacement migration, establish a working alternative before compulsory
removal. A controlled shutdown may instead require export, archival, notice,
retention, and recovery measures. A replacement should:

- Cover all critical use cases of the old system
- Have documentation and migration guides
- Be proven through evidence proportionate to risk, such as dual-run, canary,
  shadow traffic, staged rollout, or production telemetry

### Step 2: Announce and Document

```markdown
## Deprecation Notice: OldService

**Status:** Deprecated as of 2025-03-01
**Replacement:** NewService (see migration guide below)
**Removal date:** Advisory — no hard deadline yet
**Reason:** OldService requires manual scaling and lacks observability.
            NewService handles both automatically.

### Migration Guide
1. Replace `import { client } from 'old-service'` with `import { client } from 'new-service'`
2. Update configuration (see examples below)
3. Run the migration verification script: `npx migrate-check`
```

### Step 3: Migrate Incrementally

Prefer risk-bounded incremental migration when consumers can move independently.
Use a coordinated atomic or batched cutover when consistency, coupling, or the
small number of consumers requires it. For each migration unit:

```
1. Identify all touchpoints with the deprecated system
2. Update to use the replacement
3. Verify behavior matches (tests, integration checks)
4. Remove references to the old system
5. Confirm no regressions
```

**The Churn Rule:** The owner of the deprecated surface remains accountable for
a workable migration path, while consumer owners share responsibility for
adopting it. Define ownership, support, compatibility, and escalation instead
of announcing deprecation and abandoning affected users.

### Step 4: Remove the Old System

For planned ordinary removal, proceed only after all consumers have migrated.
An urgent safety, legal, or security withdrawal follows its separately
authorized containment, notice, preservation, export, and recovery plan.

For planned ordinary removal, zero observed usage is necessary but not
sufficient authorization. Confirm evidence quality, retention and compliance
obligations, rollback needs, ownership, and explicit approval for the removal
scope. An urgent withdrawal instead follows its approved protection and
containment plan, including explicit treatment of residual consumers.

For planned ordinary removal, subject to the approved retention plan:

1. Verify zero active usage through metrics, logs, and dependency analysis.
2. Remove the implementation from active runtime and consumer paths.
3. Remove active tests, documentation, and configuration, or retain and label
   archival, compatibility, audit, and rollback material under the approved plan.
4. Remove active deprecation notices or replace them with accurate archival,
   compatibility, or withdrawal guidance.
5. Record the verified outcome and retained artifacts.

## Migration Patterns

### Strangler Pattern

Run old and new systems in parallel. Route traffic incrementally from old to
new. When the old system handles 0% of traffic, enter removal-readiness review;
zero traffic does not itself authorize deletion.

```
Phase 1: New system handles 0%, old handles 100%
Phase 2: New system handles 10% (canary)
Phase 3: New system handles 50%
Phase 4: New system handles 100%, old system idle
Phase 5: Verify obligations and request authorized removal
```

### Adapter Pattern

Create an adapter that translates calls from the old interface to the new implementation. Consumers keep using the old interface while you migrate the backend.

```typescript
// Adapter: old interface, new implementation
class LegacyTaskService implements OldTaskAPI {
  constructor(private newService: NewTaskService) {}

  // Old method signature, delegates to new implementation
  getTask(id: number): OldTask {
    const task = this.newService.findById(String(id));
    return this.toOldFormat(task);
  }
}
```

### Feature Flag Migration

Use feature flags to switch consumers from old to new system one at a time:

```typescript
function getTaskService(userId: string): TaskService {
  if (featureFlags.isEnabled('new-task-service', { userId })) {
    return new NewTaskService();
  }
  return new LegacyTaskService();
}
```

## Zombie Code

Zombie code is code that nobody owns but everybody depends on. It's not actively maintained, has no clear owner, and accumulates security vulnerabilities and compatibility issues. Signs:

- No commits in 6+ months but active consumers exist
- No assigned maintainer or team
- Failing tests that nobody fixes
- Dependencies with known vulnerabilities that nobody updates
- Documentation that references systems that no longer exist

**Response:** Classify value, consumers, evidence, ownership, security,
compliance, and preservation needs. Then assign maintenance, migration,
archival, containment, or authorized removal rather than leaving risk invisible.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It still works, why remove it?" | Working code that nobody maintains accumulates security debt and complexity. Maintenance cost grows silently. |
| "Someone might need it later" | Compare preservation value, rebuild feasibility, compliance duties, and ongoing maintenance cost. Archive or retain only when evidence justifies it. |
| "The migration is too expensive" | Compare migration cost and risk with the long-term maintenance, security, compatibility, and opportunity costs; neither side is automatically cheaper. |
| "We'll deprecate it after we finish the new system" | Deprecation planning starts at design time. By the time the new system is done, you'll have new priorities. Plan now. |
| "Users will migrate on their own" | Do not assume they will. Measure adoption and provide proportionate tooling, documentation, incentives, or owner-led migration. |
| "We can maintain both systems indefinitely" | Parallel systems may be justified for resilience, regulation, compatibility, or migration, but their duplicated cost and exit conditions must be explicit. |

## Red Flags

- Deprecated systems with neither a replacement nor a safe withdrawal path
- Deprecation announcements with no proportionate migration or withdrawal support
- "Soft" deprecation that's been advisory for years with no progress
- Zombie code with no owner and active consumers
- Unjustified feature expansion on a deprecated system; safety, security, legal, and compatibility fixes may still be required
- Deprecation without measuring current usage
- Ordinary removal without verifying zero active consumers, or urgent withdrawal without an approved protection plan

## Verification

After completing a replacement migration:

- [ ] Replacement is production-proven and covers all critical use cases
- [ ] Migration guide exists with concrete steps and examples
- [ ] All active consumers have been migrated (verified by metrics/logs)
- [ ] Removal scope, retention duties, rollback needs, and authorization are confirmed
- [ ] Old implementation is removed from active runtime and consumer paths; any archive, compatibility tombstone, audit record, or rollback artifact is retained only under an approved retention plan
- [ ] No misleading active references to the deprecated system remain; historical and archival references are clearly labeled
- [ ] Active deprecation notices are removed or replaced by accurate archival, compatibility, or withdrawal guidance

After a controlled withdrawal without a replacement:

- [ ] The safety, legal, security, or other authority for withdrawal is recorded
- [ ] Affected subjects received proportionate notice and support
- [ ] Required export, retention, archival, preservation, and recovery measures are verified
- [ ] Residual consumers and compatibility impacts are explicitly accepted or contained
- [ ] The authorized removal or containment scope is verified
