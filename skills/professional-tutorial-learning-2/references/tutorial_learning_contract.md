# Tutorial Learning Contract

This contract is the high-level abstraction layer. Concrete implementations must fill these shapes rather than inventing ad hoc lecture formats.

## Core Types

```ts
type TutorialMedium = "pdf" | "video" | "web-course" | "repository" | "mixed" | "unknown";
type ContentClass = "core_knowledge" | "reading_material" | "exercise_example" | "reference" | "low_value_filler";
type DepthDecision = "skip_link_only" | "skim" | "understand" | "practice" | "master";
type ArtifactKind = "lecture_md" | "knowledge_map" | "quiz" | "practice_task" | "web_review_spec" | "review_cards" | "evaluation";

interface TutorialSource {
  medium: TutorialMedium;
  locator: string;
  title?: string;
  author?: string;
  license?: string;
  accessDate: string;
  sourceTrust: "public" | "user-provided" | "uncertain";
}

interface LearnerProfile {
  goal: string;
  priorKnowledge?: string;
  timeBudget?: string;
  outputLanguage: string;
  skipPreference?: "aggressive" | "balanced" | "conservative";
}

interface TutorialStructure {
  units: LearningUnit[];
  evidence: string[];
  confidence: "high" | "medium" | "low";
}

interface LearningUnit {
  id: string;
  title: string;
  sourceLocation: string;
  parentId?: string;
  unitType: "chapter" | "section" | "subsection" | "exercise" | "appendix";
  contentClasses: ContentClass[];
  knowledgePoints: KnowledgePoint[];
}

interface KnowledgePoint {
  id: string;
  label: string;
  sourceTrace: string;
  importance: 1 | 2 | 3 | 4 | 5;
  difficulty: 1 | 2 | 3 | 4 | 5;
  usefulness: 1 | 2 | 3 | 4 | 5;
  depthDecision: DepthDecision;
  reason: string;
  deeperLinks?: string[];
}

interface LectureArtifact {
  source: TutorialSource;
  unit: LearningUnit;
  learningGoals: string[];
  sourceStructureRecognition: string[];
  coreKnowledgeMap: KnowledgePoint[];
  requiredContent: string[];
  skimOrSkipContent: string[];
  deeperLinks: string[];
  pitfalls: string[];
  quiz: AssessmentItem[];
  practiceTask: PracticeTask;
  webReviewSpec: WebReviewSpec;
  reviewCards: ReviewCard[];
}
```

## Output Invariants

- Record source metadata and access date before teaching.
- Prefer paraphrase and synthesis over quotation.
- Make depth decisions explicit for every major knowledge point.
- Separate reading material and filler from core knowledge.
- Include assessment, practice, Web review spec, and spaced review cards for each section-level lecture.
- When source evidence is weak, label uncertainty instead of filling gaps from memory.
