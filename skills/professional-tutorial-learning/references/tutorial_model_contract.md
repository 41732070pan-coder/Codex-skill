# Tutorial Model Contract

Use this contract when normalizing tutorial sources or when an output must stay compatible with future web-app rendering.

## Core Types

```ts
type MediumType = "pdf" | "web" | "video" | "transcript" | "mixed" | "unknown";
type StructureConfidence = "explicit" | "inferred-high" | "inferred-medium" | "inferred-low";
type ContentClass = "core_knowledge_point" | "supporting_example" | "reading_only_material" | "skip_candidate" | "advanced_optional";
type LearningDepth = "deep" | "normal" | "skim" | "skip_with_link";

interface TutorialSource {
  title: string;
  medium: MediumType;
  locator: string;
  authorOrPublisher?: string;
  accessDate?: string;
  licenseOrUseNote?: string;
  extractionConfidence: StructureConfidence;
}

interface TutorialLearningRequest {
  source: TutorialSource;
  requestedScope: string;
  learnerProfile: {
    level: "novice" | "intermediate" | "advanced" | "unknown";
    background?: string;
    constraints?: string[];
  };
  learnerGoal: string;
  timeBudget?: string;
  depthPolicy: "auto" | "exam" | "project" | "skim" | "deep";
  outputTarget: "markdown_lesson" | "chapter_plan" | "review_pack" | "web_app_data";
  reviewPolicy: "light" | "standard" | "intensive";
  sourceAccessMode: "attached_file" | "url" | "pasted_excerpt" | "extracted_text" | "transcript" | "description_only";
  uncertaintyNotes: string[];
}

interface TutorialUnit {
  unitId: string;
  chapterId?: string;
  sectionId?: string;
  title: string;
  position: string;
  sourceRange?: string;
  boundaryConfidence: StructureConfidence;
}

interface KnowledgePoint {
  id: string;
  label: string;
  contentClass: ContentClass;
  importance: 1 | 2 | 3 | 4 | 5;
  practicalFrequency: 1 | 2 | 3 | 4 | 5;
  complexity: 1 | 2 | 3 | 4 | 5;
  prerequisiteValue: 1 | 2 | 3 | 4 | 5;
  goalRelevance: 1 | 2 | 3 | 4 | 5;
  selectedDepth: LearningDepth;
  rationale: string;
}

interface LessonArtifact {
  lessonId: string;
  source: TutorialSource;
  unit: TutorialUnit;
  objectives: string[];
  knowledgePoints: KnowledgePoint[];
  readingOnlyMaterial: string[];
  skippedMaterial: string[];
  contentBlocks: Array<{ kind: string; title: string; body: string }>;
  practice: Array<{ prompt: string; expectedResult: string; difficulty: string }>;
  checkpoints: Array<{ question: string; answerGuide: string }>;
  reviewSchedule: Array<{ interval: string; prompt: string }>;
  furtherReading: Array<{ label: string; url: string; reason: string }>;
}
```

## Professional Tutorial Scope

This skill can handle software, data, design, engineering, academic, operational, and other professional tutorials. For high-stakes domains such as medical, legal, financial, safety, or compliance training, generate study aids only; do not replace professional judgment, current standards, or qualified instruction.

## Source Fidelity Rules

- Label source material as explicit, paraphrased, inferred, missing, or user-supplied.
- Preserve page ranges, section headings, timestamps, or URLs when available.
- Do not invent chapter content from a title alone; if only a title or table of contents is available, generate an orientation lesson and mark evidence limits.
- Separate source-derived claims from learner-specific recommendations.

## Content Classification Rules

| Class | Use when | Output handling |
| --- | --- | --- |
| `core_knowledge_point` | The idea is needed to understand later material or perform the target skill. | Explain, practice, checkpoint, and review. |
| `supporting_example` | The material demonstrates a core point but is not itself the main concept. | Summarize briefly and tie to the concept. |
| `reading_only_material` | Context, motivation, history, or narrative helps orientation but does not require mastery. | Keep short; no heavy practice unless user asks. |
| `skip_candidate` | The material is repetitive, verbose, low relevance, or too specialized for the stated goal. | Name what was skipped and why. |
| `advanced_optional` | The material is deep, complex, or useful only in special cases. | Give a concise orientation and verified or to-verify deep-dive link. |

## Normalization Checklist

- Capture source metadata before lesson generation.
- Prefer explicit chapter and heading boundaries; mark inferred boundaries.
- Split large chapters into units that can be studied in 15-45 minutes.
- Preserve enough stable ids for future web-app rendering.
- Never hide uncertainty about source structure, importance, or skipped material.
