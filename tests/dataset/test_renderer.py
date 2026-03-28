from __future__ import annotations

import unittest

from unit_test_slm.dataset.renderer import render_jest_test_spec
from unit_test_slm.dataset.test_spec import example_test_spec


class TestSpecRendererTests(unittest.TestCase):
    def test_renderer_produces_normalized_jest_code(self) -> None:
        rendered = render_jest_test_spec(example_test_spec())
        self.assertEqual(
            rendered,
            "import { sum } from './sum';\n"
            "\n"
            "describe('sum', () => {\n"
            "  it('adds two positive integers', async () => {\n"
            "    expect(sum(1, 2)).toBe(3)\n"
            "  })\n"
            "})\n",
        )

    def test_renderer_is_deterministic(self) -> None:
        spec = example_test_spec()
        self.assertEqual(render_jest_test_spec(spec), render_jest_test_spec(spec))


if __name__ == "__main__":
    unittest.main()
