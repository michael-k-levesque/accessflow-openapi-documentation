# AI-Assisted Documentation Workflow

This portfolio project uses a controlled AI-assisted documentation workflow in which **authoritative technical sources, human review, and automated validation remain the decision-making system**. AI can accelerate drafting and review, but it is not treated as a source of truth.

The workflow is designed for technical and API documentation where accuracy, traceability, security, and maintainability matter as much as writing speed.

## Operating principle

> AI may assist with documentation work; it does not establish product behavior.

For AccessFlow, the OpenAPI contract, approved technical decisions, validated examples, and human-reviewed repository content are authoritative. Any AI-generated or AI-revised material must be checked against those sources before it is accepted.

## Workflow

### 1. Establish authoritative source material

Before AI assistance begins, identify the source material that controls the documentation. Depending on the project, that may include:

- OpenAPI or other machine-readable contracts
- approved requirements and architecture decisions
- implementation behavior confirmed by engineers
- product specifications
- security and authorization requirements
- validated request and response examples
- accepted terminology and style guidance

For this portfolio, `openapi.yaml` is the primary source of truth for API behavior.

### 2. Use AI for bounded assistance

AI can be used for tasks that benefit from rapid iteration while remaining easy to verify, such as:

- proposing alternative information structures
- drafting first-pass explanations from supplied source material
- identifying terminology inconsistencies
- suggesting missing reader questions
- generating candidate examples for later validation
- reviewing content for clarity, duplication, and ambiguous wording
- comparing documentation against a defined checklist
- helping transform authoritative technical material for different audiences

AI output is treated as a **candidate contribution**, not approved documentation.

### 3. Verify every technical claim

Technical statements are checked against authoritative sources before acceptance.

For API documentation, verification includes questions such as:

- Does the documented path exist in the contract?
- Is the HTTP method correct?
- Is the required OAuth scope correct?
- Does the request or response shape match the schema?
- Are required and optional fields represented accurately?
- Do status codes reflect the defined operation behavior?
- Are lifecycle or state-transition statements supported?
- Do examples contain invented behavior that is not present in the contract?

If a statement cannot be verified, it is revised, removed, or escalated to an appropriate subject-matter expert.

### 4. Validate structured examples automatically

Draft examples do not become authoritative simply because they look plausible.

The AccessFlow repository validates supplied JSON examples against the JSON Schema definitions in the OpenAPI document. The validation workflow also checks:

- OpenAPI 3.1 declaration
- internal `$ref` resolution
- unique operation IDs
- required repository artifacts
- local Markdown links
- repository hygiene

This reduces the risk of documentation and examples drifting away from the technical contract.

### 5. Apply human editorial review

Human review remains responsible for:

- factual acceptance
- audience appropriateness
- information architecture
- terminology decisions
- security and privacy judgment
- tone and readability
- deciding whether an AI suggestion should be used at all

The writer or reviewing SME owns the final content.

### 6. Use Git-based review and traceability

Documentation changes are handled through the same lightweight Docs-as-Code workflow used elsewhere in this repository:

1. Create a short-lived branch.
2. Make a focused change.
3. Run local validation.
4. Open a pull request.
5. Allow CI quality gates to execute.
6. Review the change and its technical impact.
7. Merge only after the checks pass.

This creates a visible history of what changed, why it changed, and which quality gates were applied.

### 7. Publish from approved content

Only reviewed and validated repository content should be used as the basis for published documentation or downstream knowledge systems.

In a production environment, this principle extends to documentation portals, search indexes, retrieval systems, internal copilots, and AI agents: the quality of the AI experience depends heavily on the quality, structure, provenance, and freshness of the underlying knowledge.

## What AI should not do

AI assistance should not be allowed to:

- invent undocumented API behavior
- create unsupported security or authorization requirements
- silently change source-of-truth contracts
- introduce secrets, credentials, customer data, or proprietary information
- override SME decisions
- bypass review or validation because generated text appears convincing
- convert uncertain assumptions into definitive documentation

## Supporting AI and agentic use cases

Well-structured technical documentation is useful to both people and machines. Authoritative content becomes easier for AI systems and agents to discover and use when it has:

- stable identifiers and operation IDs
- explicit schemas and field definitions
- predictable content structure
- clear authentication and authorization rules
- standardized error contracts
- explicit lifecycle and state information
- validated examples
- version-controlled provenance
- defined contribution and review workflows

The objective is not to optimize documentation only for AI. It is to create high-quality authoritative knowledge that can be trusted by human readers **and** safely reused by AI-assisted systems.

## AccessFlow evidence

This workflow is demonstrated by the repository itself:

- [`openapi.yaml`](openapi.yaml) - authoritative API contract
- [`examples/`](examples/) - validated request, response, and problem examples
- [`scripts/validate_examples.py`](scripts/validate_examples.py) - contract and example validation
- [`scripts/check_repository.py`](scripts/check_repository.py) - repository and documentation checks
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - authoring and review process
- [`.github/workflows/validate.yml`](.github/workflows/validate.yml) - automated CI quality gates
- [`.github/pull_request_template.md`](.github/pull_request_template.md) - repeatable review checklist

## Portfolio note

This document describes the controlled workflow used for this fictional portfolio project and the principles I would apply when incorporating AI into a professional documentation environment. It does not represent a claim that AccessFlow is a production system or that AI replaces engineering, product, security, or editorial authority.
