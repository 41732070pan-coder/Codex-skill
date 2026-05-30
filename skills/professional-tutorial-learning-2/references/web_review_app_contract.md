# Web Review App Contract

Each section-level lecture must include a lightweight Web app spec. The skill does not build the frontend unless the user asks; it defines the interaction contract so a later frontend agent can implement it.

## WebReviewSpec

```ts
interface WebReviewSpec {
  unitId: string;
  learnerActionLoop: string[];
  screens: WebReviewScreen[];
  state: WebReviewState;
  reviewSchedule: ReviewSchedule;
}

interface WebReviewScreen {
  id: string;
  purpose: "overview" | "concept-drill" | "practice" | "quiz" | "review";
  requiredControls: string[];
  feedbackRule: string;
}

interface WebReviewState {
  cards: ReviewCard[];
  quizAttempts: Array<{ itemId: string; correct: boolean; timestamp?: string }>;
  practiceStatus: "not_started" | "in_progress" | "passed" | "needs_review";
}

interface ReviewSchedule {
  day0: string[];
  day1: string[];
  day3: string[];
  day7: string[];
}
```

## Required Section Spec

- Overview screen: show learning goals and a small knowledge map.
- Concept drill screen: reveal cards by concept and ask the learner to explain in their own words.
- Practice screen: give one executable or written task with expected checks.
- Quiz screen: include immediate feedback and one remediation hint per missed item.
- Review screen: schedule cards for day 0, day 1, day 3, and day 7.

## Technology Guidance

If implementation is requested later, default to a small local React/Vite or static HTML app unless the repo already has a frontend stack. Store knowledge points, quiz items, practice tasks, and review cards as structured JSON so the UI is replaceable.
