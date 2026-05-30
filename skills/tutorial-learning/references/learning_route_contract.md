# Learning Route Contract

Plan lesson sequencing without choosing a webpage, slide deck, H5 screen flow, or other presentation medium.

## Route Requirements

A route records the selected `design_mode`, strongest supported `evidence_granularity`, learner-profile summary, and concrete personalization decisions. It also records:

- ordered lesson or stage identifiers;
- objective coverage for each stage;
- prerequisites and bridge concepts;
- estimated minutes;
- study depth: `skip | skim | standard | deep`;
- which stages are included in the current design bundle;
- which stages are deferred for later instructional design when the source scope is large.

## Long Sources

For a long tutorial, expose the full route and fully design the requested scope. Later stages may remain `planned` with a short preview and prerequisites. Do not prescribe buttons, page states, navigation components, local storage, or generation runtime behavior. Those decisions belong to a downstream renderer or orchestration layer.

## Handoff Guidance

A downstream renderer may map the route into pages, slides, screens, chapters, or progressive generation behavior. That mapping must preserve the instructional order, objective coverage, assessment timing, and review plan.

## Optional JSON Audit Sidecar

When a machine-readable handoff is useful, emit `learning_route.json` and validate it with `schemas/learning_route.schema.json`. Each route stage records its objective ids, prerequisites, depth, estimated minutes, and `designed | planned | deferred` status. The Markdown route remains part of the required tutorial-design bundle.
