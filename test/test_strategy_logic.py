"""Offline regression checks for strategy expressions."""

import unittest

import pandas as pd
from app.strategy_logic import combine_strategy_signals


class StrategyLogicTests(unittest.TestCase):
    def setUp(self):
        index = pd.date_range("2024-01-01", periods=4)
        self.strategies = [
            pd.DataFrame({"Signals": [1, 2, 0, 1]}, index=index),
            pd.DataFrame({"Signals": [1, 0, 2, 2]}, index=index),
        ]

    def test_documented_uppercase_references(self):
        result = combine_strategy_signals(self.strategies, "S1 and S2")
        self.assertEqual(result.Signals.tolist(), [1, 0, 0, 0])

    def test_parentheses_and_sell_precedence(self):
        result = combine_strategy_signals(self.strategies, "(s1 or S2)")
        self.assertEqual(result.Signals.tolist(), [1, 2, 2, 2])

    def test_inputs_are_not_modified(self):
        before = [frame.copy(deep=True) for frame in self.strategies]
        combine_strategy_signals(self.strategies, "s1 and not s2")
        for expected, actual in zip(before, self.strategies):
            pd.testing.assert_frame_equal(actual, expected)

    def test_rejects_python_execution_and_unsupported_syntax(self):
        for expression in [
            "__import__('os')",
            "s1.__class__",
            "[s1]",
            "True",
            "s0",
            "s3",
            "s1 + s2",
        ]:
            with self.subTest(expression=expression), self.assertRaises(
                ValueError
            ):
                combine_strategy_signals(self.strategies, expression)

    def test_rejects_misaligned_indexes(self):
        self.strategies[1].index = self.strategies[1].index[::-1]
        with self.assertRaises(ValueError):
            combine_strategy_signals(self.strategies, "s1 and s2")

    def test_rejects_invalid_signals(self):
        self.strategies[0].iloc[0, 0] = 3
        with self.assertRaises(ValueError):
            combine_strategy_signals(self.strategies, "s1")

    def test_rejects_empty_inputs(self):
        with self.assertRaises(ValueError):
            combine_strategy_signals([], "s1")
        with self.assertRaises(ValueError):
            combine_strategy_signals(self.strategies, " ")

    def test_handles_aligned_empty_frames(self):
        result = combine_strategy_signals([self.strategies[0].iloc[:0]], "s1")
        self.assertTrue(result.empty)
        self.assertEqual(list(result.columns), ["Signals"])


if __name__ == "__main__":
    unittest.main()
