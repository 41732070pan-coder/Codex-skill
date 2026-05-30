---
name: professional-tutorial-learning
description: Build focused tutorial-learning artifacts from professional tutorials. Use for chaptered PDF tutorials today; use for media-agnostic planning, extension, or unresolved routing when the source is video, web course, repository, or mixed media. Produces Chinese lecture notes, depth triage, quiz, practice, Web review specs, spaced review cards, and evaluation loops.
---

# Professional Tutorial Learning

## Purpose

Use this skill to turn a professional tutorial into a focused learning path. The skill first normalizes the tutorial medium and structure, then selects one implementation family member, currently `pdf-chaptered`, to generate section-level lecture notes, assessment, review cards, and Web app learning specs.

The default output language for learning artifacts is Chinese. Keep source claims traceable and do not copy long copyrighted passages; summarize and cite public metadata or user-provided material instead.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Professional tutorial study, chaptered PDF learning, course-note generation, tutorial triage, skip filler, depth decision, spaced review, Web review app spec, lecture notes from a tutorial, evaluate learning output. |
| Non-trigger | One-off PDF extraction, generic file conversion, generic web app building without tutorial-learning content, OS-kernel-only tutoring, raw document layout work. |
| Ask if ambiguous | The source is not a tutorial, the user wants verbatim excerpts, the medium cannot be accessed, or the learner goal is missing and changes depth decisions. |

## Workflow

1. Normalize the request into the contracts in `references/tutorial_learning_contract.md`.
2. Determine the tutorial medium, structure, learner goal, available time, and desired artifact types.
3. Resolve an implementation through `registry/tutorial-implementations.json` or `scripts/resolve_implementation.py`; do not read all implementations.
4. Load only the resolved implementation with `scripts/get_implementation.py`.
5. Classify source material as core knowledge, reading material, exercise/example, reference, or low-value filler.
6. Assign each major knowledge point a depth decision: skip/link-only, skim, understand, practice, or master.
7. Generate the requested artifact: lecture notes, knowledge map, quiz, practice task, Web review app spec, spaced review cards, or evaluation report.
8. Evaluate the output with `references/evaluation_rubric.md`, revise, and record decisions when running an iteration loop.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source locator or file, learner goal, section/chapter target, desired output format. |
| Optional inputs | Time budget, prior knowledge, preferred depth, output language, Web app technology preference, assessment style, review cadence. |
| Normalized shape | `{ source, learner, structureHint, implementationId, targetUnit, depthPolicy, artifactTypes, constraints, iterationState }`. |
| Outputs | Chinese markdown lecture notes, triage table, quiz, practice task, review cards, Web review app spec, evaluation report, iteration log. |
| Failure modes | Stop or ask when the source is inaccessible, content rights forbid the requested use, the tutorial structure cannot be inferred, or depth choices depend on missing learner goals. |

## References

Load references progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/tutorial_learning_contract.md` | Normalizing source, learner, unit, knowledge-point, and artifact contracts. |
| `references/depth_policy.md` | Deciding what to skip, skim, understand, practice, or master. |
| `references/web_review_app_contract.md` | Producing the per-section Web learning/review app spec. |
| `references/evaluation_rubric.md` | Reviewing lecture quality, skill quality, and iteration-loop quality. |
| `references/iteration_loop_contract.md` | Running or auditing repeated source-to-lecture improvement loops. |

## Resources

- Assets: none.
- External dependencies: source access, optional PDF text extraction tools, optional web search for public source metadata and deeper links.
- Shared providers: none.
- Discovery resources: `registry/tutorial-implementations.json`, `scripts/list_implementations.py`, `scripts/resolve_implementation.py`.
- Implementation resources: load only the selected implementation, currently `implementations/pdf-chaptered.md`, through `scripts/get_implementation.py` or a scoped direct read during maintenance.
- Generated resources: `examples/` and `logs/` hold sample lectures and experiment records; do not treat them as source truth.

## Implementation Families

| Family | Registry | List | Resolve | Get / Materialize | Validate |
| --- | --- | --- | --- | --- | --- |
| `tutorial-implementations` | `registry/tutorial-implementations.json` | `python scripts/list_implementations.py` | `python scripts/resolve_implementation.py --query "<request>"` | `python scripts/get_implementation.py pdf-chaptered` | `python scripts/validate_family.py` |

Normal-use rule: resolve from the registry and load one implementation. If resolution is ambiguous, show candidates and recommend a registered implementation; do not blend unregistered strategies.

## Overlay / Decorator Support

Temporary overlays are allowed through the normalized `constraints` and `artifactTypes` fields. Examples include a stricter time budget, exam-prep emphasis, implementation-heavy practice, or a preferred Web stack. Overlays must preserve source traceability, content classification, depth decisions, assessment, and review cards. Promote repeated overlays into registry-backed implementations only when they require distinct contracts, assets, or validators.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New tutorial medium or structure | Implementation family | `registry/tutorial-implementations.json`, `implementations/<id>.md` |
| Learning artifact contract | Contract | `references/tutorial_learning_contract.md` |
| Depth and skip rules | Strategy reference | `references/depth_policy.md` |
| Web study/review experience | Contract | `references/web_review_app_contract.md` |
| Evaluation loop | Quality gate | `references/evaluation_rubric.md`, `logs/iteration-log.md` |

## Quality Gate

Before finishing any output, verify:

- The implementation was registry-resolved and only one implementation body was loaded.
- Source metadata, access date, and section trace are recorded.
- Major knowledge points include importance, difficulty, usefulness, and a depth decision.
- Reading material, core knowledge, examples/exercises, references, and low-value filler are explicitly separated.
- Complex but low-frequency content is skipped or link-only with a reason and deeper link.
- Every section-level lecture includes quiz, practice, Web review app spec, and spaced review cards.
- Evaluation findings map to concrete skill or output revisions during iteration.
- `python scripts/validate_family.py` passes when changing registry, implementations, examples, or logs.
