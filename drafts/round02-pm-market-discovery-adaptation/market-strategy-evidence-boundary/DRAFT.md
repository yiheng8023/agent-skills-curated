# Market Strategy Evidence Boundary Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a product, service, or business idea needs a
bounded strategy workflow for:

- competitive landscape and battlecard evidence;
- market sizing and opportunity framing;
- positioning alternatives;
- product strategy coherence;
- assumptions and validation paths.

This is a market and strategy evidence-boundary candidate. It should help an
agent distinguish current facts, sourced evidence, estimates, assumptions,
strategic options, and owner decisions.

## Intake Boundary

Before producing strategy output, bind:

- product, market, geography, segment, and time horizon;
- whether current public research is required and authorized;
- available first-party evidence such as sales notes, win/loss data, customer
  feedback, pricing, roadmap, or analytics;
- whether the output is a brief, battlecard, market-sizing model, positioning
  options, strategy canvas, or decision memo;
- who owns the business decision and what confidence level is acceptable.

When market facts may be stale, require dated sources or explicitly label the
output as memory-free, source-limited, or assumption-based.

## Workflow

1. Define the strategic question and evidence surface.
2. Separate first-party materials, public research, estimates, and assumptions.
3. For competitor work, record source dates and avoid unverifiable claims.
4. For market sizing, present ranges, assumptions, and sensitivity drivers.
5. For positioning, generate options and identify the proof needed for each
   claim.
6. For product strategy, map trade-offs and dependencies instead of producing
   a one-way recommendation.
7. End with decision options, validation paths, and residual uncertainty.

## Must Not

- Do not present estimates, competitor claims, pricing, funding, or market share as current facts without dated sources.
- Do not provide investment, legal, financial, or guaranteed business advice.
- Do not scrape, quote, or redistribute restricted market reports.
- Do not claim competitor weaknesses from hearsay without labeling the source
  and confidence.
- Do not fabricate customer proof, win/loss patterns, or market numbers.
- Do not turn a generated battlecard into approved sales collateral without
  owner review.
- Do not treat a strategy canvas as authority over company strategy.

## Likely Release Direction

This draft is most likely a reference or recipe candidate. Before release, a
separate gate must decide whether the behavior becomes:

- a market-research external baseline note;
- a merge into a questioning, planning, or launch-readiness Skill;
- a recipe step for strategy review;
- or reference-only evidence if advice and current-data boundaries are too
  high for portable payload.
