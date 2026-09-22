#!/usr/bin/env python3
"""Lightweight validation for the AccessFlow OpenAPI portfolio sample.

This is intentionally dependency-light: PyYAML and jsonschema are sufficient.
It does not replace a full OpenAPI linter, but it catches common portfolio-level
contract errors and validates the supplied JSON examples against JSON Schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "openapi.yaml"


def load_spec() -> dict[str, Any]:
    with SPEC_PATH.open("r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    if not isinstance(spec, dict):
        raise AssertionError("OpenAPI document must parse to an object")
    return spec


def resolve_pointer(doc: Any, ref: str) -> Any:
    if not ref.startswith("#/"):
        raise AssertionError(f"Only local refs are expected in this sample: {ref}")
    node = doc
    for raw in ref[2:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        node = node[token]
    return node


def walk_refs(node: Any):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from walk_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk_refs(item)


def dereference_schema(spec: dict[str, Any], schema: Any) -> Any:
    if isinstance(schema, dict) and set(schema) == {"$ref"}:
        return dereference_schema(spec, resolve_pointer(spec, schema["$ref"]))
    if isinstance(schema, dict):
        return {k: dereference_schema(spec, v) for k, v in schema.items()}
    if isinstance(schema, list):
        return [dereference_schema(spec, item) for item in schema]
    return schema


def validate_document_structure(spec: dict[str, Any]) -> None:
    assert str(spec.get("openapi", "")).startswith("3.1."), "Expected OpenAPI 3.1.x"
    assert "paths" in spec and spec["paths"], "At least one path is required"

    operation_ids: list[str] = []
    methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
    for path, path_item in spec["paths"].items():
        for method, operation in path_item.items():
            if method not in methods:
                continue
            op_id = operation.get("operationId")
            assert op_id, f"Missing operationId: {method.upper()} {path}"
            assert operation.get("summary"), f"Missing summary: {op_id}"
            assert operation.get("responses"), f"Missing responses: {op_id}"
            operation_ids.append(op_id)

    assert len(operation_ids) == len(set(operation_ids)), "operationId values must be unique"

    for ref in walk_refs(spec):
        resolve_pointer(spec, ref)


def validate_json_file(spec: dict[str, Any], file_name: str, schema_ref: str) -> None:
    with (ROOT / "examples" / file_name).open("r", encoding="utf-8") as fh:
        instance = json.load(fh)
    schema = dereference_schema(spec, {"$ref": schema_ref})
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(instance)


def main() -> None:
    spec = load_spec()
    validate_document_structure(spec)
    validate_json_file(spec, "create-access-request.json", "#/components/schemas/AccessRequestCreate")
    validate_json_file(spec, "access-request-approved.json", "#/components/schemas/AccessRequest")
    validate_json_file(spec, "problem-validation.json", "#/components/schemas/Problem")
    print("PASS: OpenAPI structure, internal refs, operation IDs, and example payloads validated.")


if __name__ == "__main__":
    main()
