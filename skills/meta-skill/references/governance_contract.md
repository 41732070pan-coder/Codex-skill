# Governance Contract

Use this contract when designing or reviewing a skill. It defines the minimum information a maintainable skill should expose.

## Core Types

```ts
type SkillStatus = "draft" | "experimental" | "stable" | "deprecated";
type SkillRisk = "low" | "medium" | "high";
type SkillArtifactKind = "instruction" | "reference" | "contract" | "registry" | "template" | "asset" | "example" | "validator";

interface GovernedSkill {
  metadata: SkillMetadata;
  triggerPolicy: TriggerPolicy;
  inputContract: InputContract;
  outputContract: OutputContract;
  workflow: WorkflowStep[];
  references: SkillArtifact[];
  resources: ResourcePolicy;
  extensionPoints: ExtensionPoint[];
  qualityGates: QualityGate[];
}

interface SkillMetadata {
  name: string;
  status: SkillStatus;
  purpose: string;
  risk: SkillRisk;
  owner?: string;
}

interface TriggerPolicy {
  triggers: string[];
  nonTriggers: string[];
  overlapRisks: string[];
  askIfAmbiguous: boolean;
}

interface InputContract {
  requiredInputs: string[];
  optionalInputs: string[];
  normalizedShape: string;
}

interface OutputContract {
  artifactTypes: string[];
  successCriteria: string[];
  failureModes: string[];
}

interface SkillArtifact {
  path: string;
  kind: SkillArtifactKind;
  loadWhen: string;
  ownsDecisions: string[];
}

interface ResourcePolicy {
  assets: SkillAsset[];
  externalDependencies: string[];
  sharedProviders: string[];
  forbiddenResources: string[];
}

interface SkillAsset {
  path: string;
  role: string;
  provenance: string;
  allowedUse: string[];
  forbiddenUse: string[];
}

interface ExtensionPoint {
  name: string;
  pattern: "strategy" | "registry" | "adapter" | "template" | "provider" | "state-machine";
  contractPath?: string;
  registryPath?: string;
  templatePath?: string;
}

interface QualityGate {
  name: string;
  check: string;
  command?: string;
  required: boolean;
}
```

## Required Sections In `SKILL.md`

| Section | Required content |
| --- | --- |
| Front matter | `name` and `description`. |
| Purpose | What capability the skill adds and when to use it. |
| Triggers / Non-triggers | Activation cues and overlap boundaries. |
| Workflow | Ordered steps for using or changing the skill. |
| Inputs / Outputs | Normalized request shape and expected artifacts. |
| References | What to load on demand and when. |
| Resources | Assets, external dependencies, shared providers, and forbidden resources. |
| Extension | How to add strategies, providers, templates, examples, or validators. |
| Quality Gate | Self-checks and runnable validation commands where possible. |

## Review Rules

- If a skill has multiple implementations, it needs a registry.
- If future implementations are expected, it needs a template.
- If a reference owns formal interfaces, name it `*_contract.md`.
- If an asset is bundled, it needs role and provenance documentation.
- If a README update duplicates internal skill details, replace it with a short inventory row and link/path.
