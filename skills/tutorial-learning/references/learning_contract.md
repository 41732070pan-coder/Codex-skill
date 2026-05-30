# Learning Contract

Shared medium-neutral interface for learning from PDF, HTML, Markdown, and heading-structured tutorial sources.

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
type RouteStageStatus = "designed" | "planned" | "deferred";
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
  scope: { chapter?: string; section?: string; headingPath?: string[]; pageRange?: [number, number]; anchor?: string };
  learner_preferences?: {
    time_budget_minutes?: number;
    familiarity?: "novice" | "rusty" | "comfortable";
    goal?: "exam" | "practice" | "project" | "survey";
    personal_relevance_hints?: string[];
    explanation_preference?: ExplanationPreference;
  };
  uncertaintyNotes?: string[];
}

interface HypertextBlock { id: string; type: HypertextBlockType; title?: string; textSummary?: string; sourceTrace: SourceTrace }
interface SourceOutline { sourceTitle?: string; format: HypertextSourceFormat; structureKind: "outline" | "heading_tree" | "page_range" | "anchor_graph" | "linear_document"; navigationOrder: string[]; blocks: HypertextBlock[]; sourceTraces: SourceTrace[]; uncertaintyNotes: string[] }
interface DepthScore { importance: number; complexity: number; practical_frequency: number; prerequisite_value: number; goal_relevance: number; personal_relevance: number; composite: number; study_depth: StudyDepth; est_minutes: number; rationale: string; guardrails_applied?: string[]; risk_flags?: ("safety" | "compliance" | "irreversible_operation")[] }
interface TriageBlock { id: string; title: string; sourceTrace: SourceTrace; blockType: HypertextBlockType; content_role: ContentRole; depth: DepthScore; route: "in_lecture" | "appendix" | "skip_with_deep_dive"; deep_dive?: { label: string; url?: string; note?: string } }
interface LearningObjective { id: string; text: string; mastery: MasteryLevel; verifiable: string; sourceTraceIds: string[] }
interface ReviewCard { id: string; prompt: string; answer_hint: string; mastery: MasteryLevel; objective_ids: string[]; source_trace_ids: string[] }
interface ReviewScheduleEntry { card_id: string; due_offsets_days: number[] }
interface ReviewPlan { section_id: string; cards: ReviewCard[]; schedule: ReviewScheduleEntry[] }
interface LearningRouteStage { id: string; title: string; objective_ids: string[]; prerequisite_stage_ids: string[]; study_depth: StudyDepth; est_minutes: number; status: RouteStageStatus; preview?: string }
interface LearningRoute { stages: LearningRouteStage[]; est_minutes_total: number; designed_scope: string }
interface EvaluatorReport { scores: { source_fidelity: number; triage_depth_routing: number; chinese_lecture_quality: number; assessment_review: number; tutorial_design_completeness: number }; blocking_failures: string[]; patches: { priority: "P0" | "P1" | "P2" | "P3"; issue: string; fix: string }[]; delivery_allowed: boolean }
```

## Template-Method Pipeline

```text
TutorialRequest
→ SourceAdapter
→ SourceOutline
→ TriagePolicy
→ LearningRoutePlanner
→ TutorialDesignRenderer
→ ReviewPlan
→ EvaluatorReport
→ optional downstream presentation renderer
```

The first eight stages belong to `tutorial-learning`. The final presentation renderer does not.

## Required Markdown Bundle

```text
learning_plan.md
tutorial_structure.md
lecture.md
triage.md
assessment_plan.md
practice_plan.md
review_plan.md
source_fidelity.md
```

Optional JSON sidecars may mirror source outlines, triage decisions, routes, review cards, and evaluator reports for automation or auditing. Do not emit final HTML, PPT, H5, DOCX, CSS, JavaScript, visual-theme selections, or runtime learner-state files from this skill.
