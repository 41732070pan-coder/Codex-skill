# Learning Contract

Formal interface for `tutorial-learning`. `SKILL.md` owns orchestration; medium implementations satisfy `TutorialLearningBase`.

## Core Types

```ts
type TutorialMedium = "pdf-chaptered" | "video-chaptered" | "web-docs" | string;
type StructureProfile = "micro" | "chaptered" | "course-long";
type ContentRole = "core" | "supporting" | "reference_only" | "filler" | "deferred_ops";
type StudyDepth = "skip" | "skim" | "standard" | "deep";
type MasteryLevel = "exposure" | "recall" | "application";

interface TutorialRequest {
  medium?: TutorialMedium;
  source: { url?: string; path?: string; title?: string; license?: string };
  scope: { chapter?: string; section?: string; pageRange?: [number, number] };
  structureProfile?: StructureProfile;
  overlays?: {
    time_budget_minutes?: number;
    familiarity?: "novice" | "rusty" | "comfortable";
    goal?: "exam" | "practice" | "survey";
    personal_relevance_hints?: string[];
  };
}

interface DepthScore {
  importance: number;       // 0-5
  complexity: number;         // 0-5
  personal_relevance: number; // 0-5
  composite: number;          // rounded mean or weighted
  study_depth: StudyDepth;
  est_minutes: number;
  rationale: string;
}

interface TriageBlock {
  id: string;
  title: string;
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
}

interface TutorialArtifacts {
  lecture_md: string;
  triage_json: { blocks: TriageBlock[]; skipped_summary: string[] };
  review_plan_json: { cards: ReviewCard[]; schedule: ReviewScheduleEntry[] };
  h5_stub_json?: H5LessonStub;
}

interface ReviewCard {
  id: string;
  prompt: string;
  answer_hint: string;
  mastery: MasteryLevel;
}

interface ReviewScheduleEntry {
  card_id: string;
  due_offsets_days: number[]; // default [1, 3, 7]
}

interface H5LessonStub {
  h5_lesson_id: string;
  learning_objective_ids: string[];
  schema_version: "0.1-stub";
}
```

## TutorialLearningBase (Template Method)

Every medium implementation MUST implement these stages in order:

| Stage | Responsibility | Output |
| --- | --- | --- |
| `normalizeRequest` | Validate source, scope, overlays | `TutorialRequest` |
| `ingestSource` | Fetch/read source; build TOC map | `SourceOutline` |
| `triageContent` | Label blocks with role + depth | `TriageBlock[]` |
| `planStudyRoute` | Apply skip/skim/deep/deep_dive | routed blocks |
| `generateLecture` | Chinese markdown per `lecture_template.md` | `lecture_md` |
| `generateAssessment` | Micro-test + review cards | assessment + cards |
| `emitArtifacts` | Bundle files | `TutorialArtifacts` |
| `selfCheck` | Quality gate | pass/fail + issues |

## Assessment minimum (per section)

Micro-assessment (`## 微测`) must include at least:

1. One **预测** item (prediction before reveal).
2. One **用自己的话** item (recall / teach-back).
3. One **应用** or transfer item when any objective is `application`.

## Invariants

- Only `core` and selected `supporting` blocks appear in the lecture body.
- `filler` never appears in the body; summarize in `skipped_summary` only.
- `reference_only` goes to appendix, not learning objectives.
- `skip` route requires `deep_dive` when `importance >= 3` and `personal_relevance < 3`.
- Total `est_minutes` for in-lecture blocks should not exceed `time_budget_minutes` when set (trim skim first).
- Learning objectives: 2–4 per section, each with verifiable criterion.

## Overlap

- PDF bytes/rendering: `pdf` skill.
- OS/kernel lesson narrative: `c-os-learning-tutor`.
