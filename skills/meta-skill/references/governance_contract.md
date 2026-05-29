# Governance Contract

Use this contract when designing or reviewing a skill. It defines the minimum information a maintainable skill should expose.

## Core Types

```ts
type SkillStatus = "draft" | "experimental" | "stable" | "deprecated";
type SkillRisk = "low" | "medium" | "high";
type SkillArtifactKind = "instruction" | "reference" | "contract" | "registry" | "template" | "asset" | "example" | "validator" | "implementation" | "script";
type ImplementationKind = "style" | "provider" | "strategy" | "adapter" | "mode" | "template" | string;

interface GovernedSkill {
  metadata: SkillMetadata;
  triggerPolicy: TriggerPolicy;
  inputContract: InputContract;
  outputContract: OutputContract;
  workflow: WorkflowStep[];
  references: SkillArtifact[];
  resources: ResourcePolicy;
  extensionPoints: ExtensionPoint[];
  implementationFamilies?: ImplementationFamily[];
  loadPolicy: LoadPolicy;
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
  accessClass?: "public-entry" | "governance-reference" | "discovery" | "implementation" | "asset" | "generated" | "maintenance-only";
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
  pattern: "strategy" | "registry" | "adapter" | "template" | "provider" | "state-machine" | "implementation-family";
  contractPath?: string;
  registryPath?: string;
  templatePath?: string;
}

interface ImplementationFamily {
  familyName: string;
  kind: ImplementationKind;
  registryPath: string;
  listCommand: string;
  resolveCommand: string;
  materializeCommand: string;
  validateCommand: string;
  defaultLoadPolicy: "registry-only" | "single-implementation-only";
  directReadPolicy: "forbidden-during-normal-use" | "maintenance-only";
}

interface LoadPolicy {
  publicEntry: string[];
  discoveryResources: string[];
  implementationResources: string[];
  normalUseRule: string;
  maintenanceException: string;
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
| Extension | How to add strategies, providers, templates, examples, validators, or implementation families. |
| Quality Gate | Self-checks and runnable validation commands where possible. |

## Review Rules

- If a skill has multiple implementations, it needs an implementation-family contract and a registry.
- If future implementations are expected, it needs a template and deterministic list/resolve/materialize commands.
- If a reference owns formal interfaces, name it `*_contract.md`.
- If an asset is bundled, it needs role and provenance documentation.
- If a README update duplicates internal skill details, replace it with a short inventory row and link/path.


## Implementation Family Rules

- A growing implementation family must expose list, resolve, materialize/get, and validate commands.
- `SKILL.md` documents the dispatch workflow, not the full implementation catalog.
- Registries contain concise metadata for discovery; implementation files contain detailed behavior.
- Normal use loads only the selected implementation after resolution.
- Direct reads of implementation files are maintenance-only unless a script returns that exact implementation content.
- Asset use is scoped to the selected implementation or a documented shared provider.

## Resource Access Rules

- Public entry resources are safe to read when the skill triggers.
- Discovery resources are safe to query before implementation selection.
- Implementation resources are loaded only after selection or during scoped maintenance.
- Generated and maintenance-only resources must be labeled or documented.
- A boundary validator should flag `SKILL.md` files that fan out into large implementation or asset catalogs.
