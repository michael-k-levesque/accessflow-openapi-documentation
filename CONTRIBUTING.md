# Contributing to the AccessFlow API Documentation Sample

This repository is a portfolio demonstration, but changes follow a lightweight docs-as-code review model so the project can be evaluated like a maintained documentation set.

## Branch and review workflow

1. Create a short-lived branch from `main`.
2. Make the smallest coherent documentation or contract change.
3. Update examples and the changelog when behavior or schema changes.
4. Run the local quality gates.
5. Open a pull request and describe the reader impact, technical impact, and validation performed.
6. Merge only after the automated checks pass and the rendered content has been reviewed when applicable.

## Local quality gates

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/validate_examples.py
python scripts/check_repository.py
vale .
```

The first script validates the OpenAPI structure, local references, unique operation IDs, and supplied JSON examples. The second checks repository hygiene and lightweight documentation-quality rules. Vale applies the repository's prose, terminology, and word-choice rules to Markdown documentation.

## Authoring rules

- Treat `openapi.yaml` as the source of truth for API behavior.
- Keep operation IDs stable after publication unless a breaking change is intentional.
- Reuse component schemas, parameters, headers, and responses instead of duplicating contracts.
- Document authentication and authorization separately; every protected operation must identify its required OAuth scope.
- Use `application/problem+json` for errors and keep the shared problem shape consistent.
- Add or update request/response examples when schemas change.
- Describe lifecycle or state-transition effects when an operation changes resource state.
- Keep examples fictional and free of customer, employer, credential, or proprietary data.
- Record externally visible changes in `CHANGELOG.md`.

## Pull-request acceptance criteria

A change is ready to merge when:

- the OpenAPI file parses and declares OpenAPI 3.1;
- internal `$ref` targets resolve;
- operation IDs remain unique;
- included JSON examples validate against their schemas;
- required repository files are present;
- Markdown and YAML files pass the lightweight repository checks;
- Markdown documentation passes Vale with no error-level findings;
- no temporary render output or editable Office source has been committed; and
- the pull-request description explains what changed and why.
