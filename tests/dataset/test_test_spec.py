from __future__ import annotations

import unittest

from unit_test_slm.dataset.test_spec import (
    CASE_TYPES,
    TEST_SPEC_VERSION,
    example_test_spec,
    validate_test_spec,
)


class TestSpecSchemaTests(unittest.TestCase):
    def test_example_test_spec_is_valid(self) -> None:
        spec = example_test_spec()
        self.assertEqual(validate_test_spec(spec), [])
        self.assertEqual(spec["schema_version"], TEST_SPEC_VERSION)
        self.assertIn(spec["cases"][0]["type"], CASE_TYPES)

    def test_validate_test_spec_rejects_invalid_case_type(self) -> None:
        spec = example_test_spec()
        spec["cases"][0]["type"] = "snapshot_only"
        errors = validate_test_spec(spec)
        self.assertIn("case_0_invalid_type", errors)


if __name__ == "__main__":
    unittest.main()
