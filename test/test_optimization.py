"""Offline regression checks for the optimizer's selection weights."""

import sys
import types
import unittest
from pathlib import Path

import numpy as np

# optimization.py imports Streamlit and the backtest module at import time;
# stub them so the pure selection helpers can be tested offline.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
sys.modules.setdefault("streamlit", types.ModuleType("streamlit"))
backtest_stub = types.ModuleType("create_backtest")
backtest_stub.financial_evaluation = None
backtest_stub.qs_metrics = None
sys.modules.setdefault("create_backtest", backtest_stub)

import optimization  # noqa: E402


class SelectionProbabilityTests(unittest.TestCase):
    def test_zero_mean_scores_fall_back_to_uniform_weights(self):
        probs = optimization.selection_probabilities(np.array([0.0, 0.0]))
        self.assertEqual(probs.tolist(), [1.0, 1.0])
        self.assertIn(optimization.roulette_wheel_selection(probs), (0, 1))

    def test_symmetric_scores_with_zero_mean(self):
        probs = optimization.selection_probabilities([-1.0, 1.0])
        self.assertTrue(np.all(probs == 1.0))

    def test_higher_scores_get_higher_weights(self):
        probs = optimization.selection_probabilities([1.0, 2.0, 3.0])
        self.assertTrue(np.all(np.diff(probs) > 0))


if __name__ == "__main__":
    unittest.main()
