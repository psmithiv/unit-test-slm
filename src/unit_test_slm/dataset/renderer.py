"""Deterministic renderer from TEST_SPEC to normalized Jest code."""

from __future__ import annotations

from typing import Any

from unit_test_slm.dataset.normalize import normalize_jest_test
from unit_test_slm.dataset.test_spec import validate_test_spec


def _render_case(case: dict[str, Any], export_name: str) -> list[str]:
    name = case["name"]
    invocation = f"{export_name}({', '.join(case.get('input', []))})"
    assertion = case["assertion"]
    case_type = case["type"]

    if case_type == "returns":
        body = [f"expect({invocation}).{assertion}"]
    elif case_type == "throws":
        body = [f"expect(() => {invocation}).{assertion}"]
    elif case_type in {"resolves", "rejects"}:
        body = [f"await expect({invocation}).{assertion}"]
    elif case_type == "side_effect":
        body = [invocation, assertion]
    else:
        raise ValueError(f"unsupported case type: {case_type}")

    lines = [f"it('{name}', async () => {{"]
    lines.extend(f"  {line}" for line in body)
    lines.append("})")
    return lines


def render_jest_test_spec(spec: dict[str, Any]) -> str:
    errors = validate_test_spec(spec)
    if errors:
        raise ValueError(f"invalid TEST_SPEC: {', '.join(errors)}")

    target = spec["target"]
    setup = spec["setup"]
    imports = sorted(set(setup.get("imports", []))) or [target["export_name"]]
    import_list = ", ".join(imports)

    lines = [f"import {{ {import_list} }} from '{target['module_path']}';", ""]

    for mock in spec["mocks"]:
        lines.append(f"jest.mock('{mock['module_path']}');")
    if spec["mocks"]:
        lines.append("")

    lines.append(f"describe('{spec['suite']['describe']}', () => {{")
    for statement in setup.get("before_each", []):
        lines.append("  beforeEach(() => {")
        lines.append(f"    {statement}")
        lines.append("  })")
        lines.append("")

    for index, case in enumerate(spec["cases"]):
        rendered_case = _render_case(case, target["export_name"])
        lines.extend(f"  {line}" for line in rendered_case)
        if index != len(spec["cases"]) - 1:
            lines.append("")

    lines.append("})")
    return normalize_jest_test("\n".join(lines))
