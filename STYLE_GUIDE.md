# AccessFlow Documentation Style Guide

This repository uses **Vale** as an automated prose-quality gate. The goal is not to enforce personal preference or make every sentence sound identical. The goal is to prevent terminology drift and a small set of avoidable wording problems in developer-facing documentation.

## Enforced terminology

Use these forms consistently:

| Preferred | Avoid |
| --- | --- |
| OpenAPI | `Open API`, `openAPI`, `open api` |
| GitHub | `Github` |
| OAuth 2.0 | `OAuth2` |
| JSON Schema | `Json Schema` |

The terminology rule is maintained in [`.github/styles/AccessFlow/Terminology.yml`](.github/styles/AccessFlow/Terminology.yml).

## Word choice

Prefer direct verbs where a simpler form is available. The current automated rule replaces forms of `utilize` with `use`.

The word-choice rule is maintained in [`.github/styles/AccessFlow/WordChoice.yml`](.github/styles/AccessFlow/WordChoice.yml).

## Running Vale locally

Install the Vale CLI, then run this command from the repository root:

```bash
vale .
```

Vale reads [`.vale.ini`](.vale.ini), applies the AccessFlow style to Markdown files, and reports error-level findings.

## CI behavior

The documentation-validation workflow runs Vale on pushes and pull requests. Error-level Vale findings fail the quality gate and must be corrected before the change is accepted.

This repository also runs structural and example validation separately. Vale checks prose and terminology; it does not replace OpenAPI, schema, link, repository-hygiene, or example validation.

## Governance principle

Automated style checks should encode rules that are stable, explainable, and useful to contributors. Rules should be added because they reduce reader friction, ambiguity, or maintenance cost—not merely because a tool can detect them.
