# Lifecycle Policy

Lifecycle states are `candidate`, `adapted`, `reviewed`, `approved`,
`deprecated`, and `retired`. Only `approved` Skills enter the release manifest.

Every upstream update is a new immutable intake: diff the pinned revision,
rerun security, portability, overlap, relationship, scenario, and installation
checks, then explicitly approve, replace, deprecate, or reject each impact.
Generated topology and catalogs are rebuilt after every inventory change.

Lifecycle metabolism is event-driven. Any one of the following governed
signals may reopen review without automatically changing the last known-good
release:

- consumer usage, failure, collision, context-cost, or validation evidence;
- community overlap, quality, portability, or maintenance reports;
- security findings or dependency and executable-surface changes;
- license, provenance, ownership, or redistribution changes;
- an upstream revision, archival, maintainer, or availability change; or
- repository validation, routing, scenario, or integrity failure.

Each signal is recorded with a source, date, affected stable identifiers,
evidence limits, and a recheck trigger. The review must choose an explicit
outcome: retain; revise and re-review; compose or route; replace or supersede;
deprecate with a migration window; retire; or reject the proposed change.
Inventory growth is not a default outcome.

Release mutation remains separately governed. Replacing, superseding,
deprecating, or retiring approved content requires impact evidence, compatible
consumer and relationship analysis, migration and rollback instructions, a
versioned decision, repository verification, and the applicable release and
consumer authority. A feedback record may reopen review or suppress an exact
reproposal, but it cannot by itself approve a candidate, overwrite a consumer,
or mutate a runtime.
