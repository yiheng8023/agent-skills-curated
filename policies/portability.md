# Portability Policy

Portable cores describe goals, inputs, outputs, invariants, decisions, side
effects, authorization boundaries, and verification. Agent-specific tool names,
Hook events, command syntax, filesystem paths, and subagent semantics belong in
explicit adapters.

Cross-agent portability never means pretending every environment has the same
capability. Missing behavior must be declared and safely degraded.
