# Lifecycle Policy

Lifecycle states are `candidate`, `adapted`, `reviewed`, `approved`,
`deprecated`, and `retired`. Only `approved` Skills enter the release manifest.

Every upstream update is a new immutable intake: diff the pinned revision,
rerun security, portability, overlap, relationship, scenario, and installation
checks, then explicitly approve, replace, deprecate, or reject each impact.
Generated topology and catalogs are rebuilt after every inventory change.
