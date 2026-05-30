# Learning Contract

Formal interface for `tutorial-learning`. `SKILL.md` owns orchestration; the single active implementation, `hypertext-tutorial`, satisfies `TutorialLearningBase`.

## Core Types

```ts
type TutorialImplementation = "hypertext-tutorial";
type HypertextSourceFormat = "pdf" | "html" | "markdown" | "plain_text_with_headings" | "unknown";
type SourceAccessMode = "attached_file" | "url" | "pasted_excerpt" | "extracted_text" | "description_only";
type SourceTrust = "public" | "user_provided" | "uncertain";
type BoundaryConfidence = "explicit" | "inferred-high" | "inferred-medium" | "inferred-low";
type EvidenceType = "source-derived" | "paraphrased" | "inferred" | "user-supplied" | "supplementary" | "missing";
type HypertextBlockType = "heading" | "paragraph" | "code" | "table" | "figure" | "callout" | "exercise" | "navigation" | "sidebar" | "appendix" | "reference";
type ContentRole = "core" | "supporting" | "reference_only" | "filler" | "deferred_ops";
type StudyDepth = "skip" | "skim" | "standard" | "deep";
type MasteryLevel = "exposure" | "recall" | "application";

interface SourceTrace {
  id: string;
  source_format: HypertextSourceFormat;
  locator?: string;
  pageRange?: [number, number];
  headingPath?: string[];
  anchor?: string;
  url?: string;
  blockId?: string;
  extractionSlice?: string;
  boundaryConfidence: BoundaryConfidence;
  evidenceType: EvidenceType;
}

interface TutorialRequest {
  implementation?: TutorialImplementation;
  source: {
    format?: HypertextSourceFormat;
    accessMode: SourceAccessMode;
    trust: SourceTrust;
    locator?: string;
    url?: string;
    path?: string;
    title?: string;
    authorOrPublisher?: string;
    licenseOrUseNote?: string;
    accessDate?: string;
  };
  scope: {
    chapter?: string;
    section?: string;
    headingPath?: string[];
    pageRange?: [number, number];
    anchor?: string;
  };
  overlays?: {
    time_budget_minutes?: number;
    familiarity?: "novice" | "rusty" | "comfortable";
    goal?: "exam" | "practice" | "project" | "survey";
    personal_relevance_hints?: string[];
  };
  uncertaintyNotes?: string[];
}

interface HypertextBlock {
  id: string;
  type: HypertextBlockType;
  title?: string;
  textSummary?: string;
  sourceTrace: SourceTrace;
}

interface SourceOutline {
  sourceTitle?: string;
  format: HypertextSourceFormat;
  structureKind: "outline" | "heading_tree" | "page_range" | "anchor_graph" | "linear_document";
  navigationOrder: string[];
  blocks: HypertextBlock[];
  sourceTraces: SourceTrace[];
  uncertaintyNotes: string[];
}

interface DepthScore {
  importance: number;            // 0-5
  complexity: number;            // 0-5
  practical_frequency: number;   // 0-5
  prerequisite_value: number;    // 0-5
  goal_relevance: number;        // 0-5
  personal_relevance: number;    // 0-5
  composite: number;             // rounded weighted result
  study_depth: StudyDepth;
  est_minutes: number;
  rationale: string;
}

interface TriageBlock {
  id: string;
  title: string;
  sourceTrace: SourceTrace;
  blockType: HypertextBlockType;
  content_role: ContentRole;
  depth: DepthScore;
  route: "in_lecture" | "appendix" | "skip_with_deep_dive";
  deep_dive?: { label: string; url?: string; note?: string };
}

interface LearningObjective {
  id: string;
  text: string;
  mastery: MasteryLevel;
  verifiable: string;
  sourceTraceIds: string[];
}

interface TutorialArtifacts {
  lecture_md: string;
  triage_json: { blocks: TriageBlock[]; skipped_summary: string[] };
  review_plan_json: { cards: ReviewCard[]; schedule: ReviewScheduleEntry[] };
  h5_stub_json?: HypertextLessonProjection;
}

interface ReviewCard {
  id: string;
  prompt: string;
  answer_hint: string;
  mastery: MasteryLevel;
  objective_ids: string[];
  source_trace_ids: string[];
}

interface ReviewScheduleEntry {
  card_id: string;
  due_offsets_days: number[]; // default [1, 3, 7]
}

interface HypertextLessonProjection {
  schema_version: "0.2-hypertext-stub";
  h5_lesson_id: string;
  source_trace_ids: string[];
  concept_ids: string[];
  learning_objective_ids: string[];
  review_card_ids: string[];
  interaction_ids: string[];
  progress_key: string;
}
```

## TutorialLearningBase

The active implementation MUST implement these stages in order:

| Stage | Responsibility | Output |
| --- | --- | --- |
| `normalizeRequest` | Validate source, scope, rights note, overlays, and requested artifact types. | `TutorialRequest` |
| `ingestSource` | Read/fetch supplied source and build a hypertext outline with source traces. | `SourceOutline` |
| `triageContent` | Label blocks with content role, evidence, and depth scores. | `TriageBlock[]` |
| `planStudyRoute` | Apply skip/skim/standard/deep and route blocks to body, appendix, or deep dive. | routed blocks |
| `generateLecture` | Produce Chinese markdown per `lecture_template.md`. | `lecture_md` |
| `generateAssessment` | Produce micro-test, practice task, and review cards. | assessment + cards |
| `emitArtifacts` | Bundle markdown and structured sidecars/projection stubs. | `TutorialArtifacts` |
| `selfCheck` | Verify quality gate and stop on blocking issues. | pass/fail + issues |

## Assessment Minimum

Per section, `## 微测` must include at least:

1. One **预测** item before explanation or reveal.
2. One **用自己的话** item for recall / teach-back.
3. One **应用** or transfer item when any objective has `mastery: application`.

## Invariants

- PDF, HTML, Markdown, and heading-structured text are source formats under `hypertext-tutorial`.
- Non-hypertext carrier sources are out of scope.
- Only `core` and selected `supporting` blocks appear in the lecture body.
- `filler` never appears in the body; summarize it in `skipped_summary` only when useful for trust.
- `reference_only` goes to an appendix, not learning objectives.
- `skip` route requires `deep_dive` when `importance >= 3` and current learner relevance is low.
- Total `est_minutes` for in-lecture blocks should not exceed `time_budget_minutes` when set; trim skim blocks first.
- Learning objectives: 2–4 per section, each with verifiable criteria and source trace ids.
- Do not teach from headings alone. If only a title, TOC, or navigation tree is available, ask for text or generate only a clearly labeled orientation.

## Overlap

- Low-level PDF extraction, OCR, rendering, and layout QA belong to document/PDF tooling.
- Repository-level skill governance belongs to `meta-skill`.
- Frontend implementation of an H5 app is outside this skill unless explicitly requested; this skill only emits a projection contract.
