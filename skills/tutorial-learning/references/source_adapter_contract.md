# Source Adapter Contract

A source adapter is a lightweight ingest profile. It converts one source medium into a shared `SourceOutline`; it does not replace triage, lecture, assessment, review, or evaluation stages.

## Profile Shape

```ts
interface SourceAdapterProfile {
  id: string;
  format: HypertextSourceFormat;
  status: "experimental" | "stable" | "deprecated";
  acceptedAccessModes: SourceAccessMode[];
  outlineSignals: string[];
  requiredTraceFields: string[];
  noiseRules: string[];
  failureModes: string[];
  delegatedTools: string[];
}
```

## Registry Upgrade Path

The adapter family is intentionally small, so `source_profiles.md` is the source of truth. Keep each Markdown profile aligned with `SourceAdapterProfile` so a later registry migration remains mechanical.

Add a YAML registry and list/resolve/get scripts when any trigger makes deterministic dispatch or profile-specific validation necessary:

- source profiles exceed five;
- aliases or cues overlap enough to make selection ambiguous;
- one adapter owns dedicated assets or external tools;
- one adapter needs special validation rules; or
- examples or review reveal incorrect adapter selection.

Each profile must preserve upgrade-compatible metadata: stable `id`, status, cues, summary, ambiguity risks, fallback policy, and delegated tooling.

## Shared Boundary

Adapters may:

- recognize format and access-mode cues;
- identify structural signals;
- remove or label source-specific noise;
- emit source traces and uncertainty notes;
- stop or delegate when low-level extraction is needed.

Adapters must not:

- invent missing lesson content;
- duplicate the shared triage, lecture, assessment, review, or evaluator pipeline;
- perform raw OCR, PDF rendering, or layout QA inside this skill.
