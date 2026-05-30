# Learning Contract

Shared interface for learning from PDF, HTML, Markdown, and heading-structured tutorial sources.

## Core Types

```ts
type HypertextSourceFormat = "pdf" | "html" | "markdown" | "plain_text_with_headings" | "unknown";
type SourceAccessMode = "attached_file" | "url" | "pasted_excerpt" | "extracted_text" | "description_only";
type BoundaryConfidence = "explicit" | "inferred-high" | "inferred-medium" | "inferred-low";
type EvidenceType = "source-derived" | "paraphrased" | "inferred" | "user-supplied" | "supplementary" | "missing";
type HypertextBlockType = "heading" | "paragraph" | "code" | "table" | "figure" | "callout" | "exercise" | "navigation" | "sidebar" | "appendix" | "reference";
type ContentRole = "core" | "supporting" | "reference_only" | "filler" | "deferred_ops";
type StudyDepth = "skip" | "skim" | "standard" | "deep";
type MasteryLevel = "exposure" | "recall" | "application";
type LessonState = "completed" | "current" | "ready-to-generate" | "locked";
type ExplanationPreference = "balanced" | "intuition-first" | "math-focused" | "practice-focused";

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
  source: {
    format?: HypertextSourceFormat;
    accessMode: SourceAccessMode;
    locator?: string;
    url?: string;
    path?: string;
    title?: string;
    authorOrPublisher?: string;
    licenseOrUseNote?: string;
  };
  scope: {
    chapter?: string;
    section?: string;
    headingPath?: string[];
    pageRange?: [number, number];
    anchor?: string;
  };
  learner_preferences?: {
    time_budget_minutes?: number;
    familiarity?: "novice" | "rusty" | "comfortable";
    goal?: "exam" | "practice" | "project" | "survey";
    personal_relevance_hints?: string[];
    explanation_preference?: ExplanationPreference;
  };
  design_style?: TutorialDesignStyleRequest;
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
  composite: number;
  study_depth: StudyDepth;
  est_minutes: number;
  rationale: string;
  guardrails_applied?: string[];
  risk_flags?: ("safety" | "compliance" | "irreversible_operation")[];
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

interface TutorialDesignStyleRequest {
  designSkill?: string; // default "my-design-style"
  theme?: string; // default "chinese-traditional-color-style"
  themeVariant?: string; // default "academy-calm"
  customOverrides?: Record<string, unknown>;
}

interface LearningSignal {
  topic_id: string;
  kind: "first_attempt_error" | "repeated_attempt" | "uncertain" | "unfinished_optional_practice" | "due_review";
  detail?: string;
}

interface LearnerState {
  version: number;
  course_id: string;
  updated_at: string; // ISO 8601
  preferences: { explanation_preference: ExplanationPreference };
  lesson_records: Record<string, unknown>[];
  review_records: Record<string, unknown>[];
  notes: Record<string, unknown>[];
}

interface NextLessonContext {
  version: number;
  course_id: string;
  generated_at: string; // ISO 8601
  trigger: "initial" | "next_lesson_generation" | "manual_resume";
  next_lesson_id: string;
  source_state_file: "state/learner_state.json";
  explanation_preference: ExplanationPreference;
  completed_lesson_ids: string[];
  learning_signals: LearningSignal[];
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

interface LearningRoute {
  blocks: TriageBlock[];
  est_minutes_total: number;
}

interface ReviewPlan {
  section_id: string;
  cards: ReviewCard[];
  schedule: ReviewScheduleEntry[];
}

interface EvaluatorReport {
  scores: {
    source_fidelity: number;
    triage_depth_routing: number;
    chinese_lecture_quality: number;
    assessment_review: number;
    interactive_web_learning: number;
  };
  blocking_failures: string[];
  patches: { priority: "P0" | "P1" | "P2" | "P3"; issue: string; fix: string }[];
  delivery_allowed: boolean;
}

type WebpageDeliveryMode = "complete_course" | "progressive_chapter";

interface LearningPlan {
  delivery_mode: WebpageDeliveryMode;
  estimated_total_minutes: number;
  estimated_lesson_pages: number;
  generated_scope: string;
  planned_pages: { id: string; title: string; path: string; status: LessonState; unlock_condition?: string; preview?: string }[];
  explanation_preference?: ExplanationPreference;
  design_style?: TutorialDesignStyleRequest;
}

interface TutorialArtifacts {
  learning_plan_md: string; // emit first
  interactive_tutorial_html: string; // runnable learner-facing web page
  lecture_md: string; // source-traced content sidecar
  triage_json: { blocks: TriageBlock[]; skipped_summary: string[]; learning_objectives: LearningObjective[] };
  review_plan_json: ReviewPlan;
  source_outline_json?: SourceOutline; // recommended audit sidecar
  evaluator_report_json?: EvaluatorReport; // internal self-check or optional output
  learner_state_json: LearnerState; // state/learner_state.json; durable local learner submissions and confirmations
  next_lesson_context_json: NextLessonContext; // state/next_lesson_context.json; compact model-facing extraction
}
```

## Architecture Roles

Treat the workflow as a template-method pipeline contract, not as a requirement to implement an object-oriented runtime.

| Role | Responsibility | Output |
| --- | --- | --- |
| `TutorialLearningPipeline` | Own the shared stage order and invariants. | `TutorialArtifacts` |
| `SourceAdapter` | Convert one source medium into the shared intermediate representation. | `SourceOutline` |
| `TriagePolicy` | Classify blocks and calculate depth with guardrails. | `TriageBlock[]` |
| `LearningRoutePlanner` | Route blocks to lecture, appendix, or deep dive under the time budget. | `LearningRoute` |
| `LectureRenderer` | Render the Chinese learner-facing artifact. | `lecture_md` |
| `AssessmentBuilder` | Create prediction, teach-back, application, and practice items. | assessment sections |
| `ReviewScheduler` | Create review cards and spaced schedule. | `ReviewPlan` |
| `LearnerStateStore` | Persist learner submissions and confirmations locally, then rebuild compact next-lesson context before model use. | `state/learner_state.json` + `state/next_lesson_context.json` |
| `ProgressiveGenerationController` | For long tutorials, preserve route visibility, learning signals, explicit next-lesson generation, and lock explanations. | progressive lesson state |
| `DesignStyleResolver` | Resolve a pluggable visual theme without changing pedagogy or interaction invariants. | theme tokens and component rules |
| `LearningPlanRenderer` | Arrange the full study route before interactive rendering and estimate content size. | `learning_plan_md` |
| `InteractiveTutorialRenderer` | Render routed teaching content, homepage navigation, micro-tests, practice, completion, and review interactions into a runnable page. | `interactive_tutorial_html` |
| `Evaluator` | Check fidelity, routing, lecture quality, assessment, and blocking failures. | `EvaluatorReport` |

Only `SourceAdapter` varies by input medium. The later stages remain shared.

## Workflow Contract

| Stage | Responsibility | Output |
| --- | --- | --- |
| Normalize request | Validate source, scope, rights note, learner preferences, and requested artifact types. | `TutorialRequest` |
| Ingest source | Read supplied source and build a traceable outline. | `SourceOutline` |
| Triage content | Label blocks with content role, evidence, and depth scores. | `TriageBlock[]` |
| Plan study route | Apply skip/skim/standard/deep and route blocks to body, appendix, or deep dive. | routed blocks |
| Generate lecture | Produce Chinese markdown per `lecture_template.md`. | `lecture_md` |
| Generate assessment | Produce micro-test, practice task when applicable, and review cards. | assessment + cards |
| Plan learning delivery | Arrange the complete study route, estimate lesson-page count and minutes, and choose `complete_course` or `progressive_chapter`. | `learning_plan_md` |
| Persist learner state | Initialize local state files; update durable state on meaningful learner actions; rebuild compact context before next-lesson generation or resume. | `state/learner_state.json` + `state/next_lesson_context.json` |
| Render interactive tutorial | Render homepage navigation, learning plan, current lesson content, micro-tests, practice, completion, review interactions, and planned future routes. | `interactive_tutorial_html` |
| Emit artifacts | Bundle the learner-facing plan and runnable HTML with structured audit/review sidecars. | `TutorialArtifacts` |
| Self-check | Verify quality criteria and stop on blocking issues. | pass/fail + issues |

## Assessment Minimum

Per section, `## 微测` must include at least:

1. One **预测** item before explanation or reveal.
2. One **用自己的话** item for recall / teach-back.
3. One **应用** or transfer item when any objective has `mastery: application`.

## Invariants

- PDF, HTML, Markdown, and heading-structured text use the same source-outline model.
- Only `core` and selected `supporting` blocks appear in the lecture body.
- `filler` never appears in the body; summarize it in `skipped_summary` only when useful for trust.
- `reference_only` goes to an appendix, not learning objectives.
- `skip` route requires `deep_dive` when `importance >= 3` and current learner relevance is low.
- Total `est_minutes` for in-lecture blocks should not exceed `time_budget_minutes` when set; trim skim blocks first.
- Learning objectives: 2–4 per section, each with verifiable criteria and source trace ids.
- Do not teach from headings alone. If only a title, TOC, or navigation tree is available, ask for text or generate only a clearly labeled orientation.

## Interactive Tutorial Web Delivery Invariants

- Emit the complete learning arrangement before the interactive tutorial page.
- Use `complete_course` by default only for a small route (guideline: at most 3 lesson pages and at most 90 minutes); otherwise use `progressive_chapter`.
- In `progressive_chapter`, fully render the first learnable chapter or section now and keep future pages visible as inspectable `ready-to-generate` or `locked` homepage-navigation entries.
- Every interactive page has homepage navigation containing the learning plan, all lesson pages, and the review center.
- The runnable HTML teaches the routed source content and wires usable micro-test, practice, completion, and review interactions.
- Persist meaningful learner submissions and confirmations using `learner_state_contract.md`; rebuild compact local context immediately before next-lesson generation.
- Read `interactive_webpage_contract.md` for the content-first HTML contract and quality gate.
