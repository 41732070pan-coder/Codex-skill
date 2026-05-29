# Source Workflow Registry

This registry resolves tutorial media into one selected workflow. Keep the table concise; detailed behavior belongs in the referenced workflow file.

## Registry Entries

| Id | Path | Status | Medium | Summary | Exact aliases | Contextual cues | Ambiguity risks | Fallback policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pdf-chaptered` | `references/pdf_chapter_workflow.md` | experimental | PDF or PDF-derived text | Process a chaptered tutorial PDF into lesson-sized markdown study units. | pdf; PDF tutorial; textbook PDF; chaptered document | page ranges, table of contents, chapters, sections, extracted PDF text | PDF may be scanned, missing TOC, or have uncertain section boundaries. | Recommend when a PDF file, PDF URL, or PDF-derived text is present. |
| `web-course` | `references/web_course_workflow.md` | draft | Web tutorial or article series | Convert web tutorial pages into sourced markdown lessons with links preserved. | web tutorial; online course; article series; docs tutorial | URL, navigation tree, next/previous links, headings, course pages | Web pages may mix navigation, marketing, comments, or reference docs. | Recommend for URL-first sources when no PDF/transcript is provided. |
| `video-course` | `references/video_course_workflow.md` | draft | Video or transcript | Convert transcript/timestamped lessons into concepts, practice, and review prompts. | video course; lecture; transcript; recording | timestamps, captions, modules, slides, playlist | Videos may lack transcripts or include long demonstrations with sparse concepts. | Recommend only when transcript or timestamped outline is available. |
| `mixed-media` | `references/tutorial_model_contract.md` | planned | Multiple media | Normalize a tutorial that combines PDF, videos, exercises, and web references. | mixed course; hybrid tutorial | syllabus, readings plus videos, labs plus docs | Risk of overloading a single lesson with too many source types. | Ask for the primary medium and first selected unit before proceeding. |

## Resolution Rules

- Exact `Id` or exact alias wins.
- Strong file/URL evidence may select a workflow when the user did not name one.
- If candidates tie, ask once and show candidate ids with summaries.
- Do not blend workflow bodies during normal use. Select one primary workflow and treat other media as supporting resources.
- If no workflow fits, propose a new registry row before inventing behavior.

## Entry Shape

```ts
interface SourceWorkflowRegistryEntry {
  id: string;
  path: `references/${string}.md`;
  status: "planned" | "draft" | "experimental" | "stable" | "deprecated";
  medium: string;
  summary: string;
  exactAliases: string[];
  contextualCues: string[];
  ambiguityRisks: string[];
  fallbackPolicy: string;
}
```
