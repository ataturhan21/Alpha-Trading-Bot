"""Combine strategy signals without executing user-supplied Python."""

import ast
import re

import numpy as np
import pandas as pd


def combine_strategy_signals(strategies, expression):
    """Evaluate S1/S2 references with and, or, not, and parentheses.

    All strategies must have identical indexes. Sell wins when both buy and
    sell expressions are true, preserving the existing mixing behavior.
    """
    if not strategies:
        raise ValueError("Choose at least 1 strategy.")
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a strategy expression.")
    if len(expression) > 1000:
        raise ValueError("Strategy expression is too long.")
    index = strategies[0].index
    for strategy in strategies:
        if not strategy.index.equals(index):
            raise ValueError("Strategy indexes must match.")
        if (
            "Signals" not in strategy
            or not strategy["Signals"].isin([0, 1, 2]).all()
        ):
            raise ValueError(
                "Strategies must contain only 0, 1, or 2 signals."
            )

    tree = ast.parse(expression.strip().lower(), mode="eval")

    def evaluate(node, signal):
        if isinstance(node, ast.Name) and re.fullmatch(
            r"s[1-9][0-9]*", node.id
        ):
            position = int(node.id[1:]) - 1
            if position >= len(strategies):
                raise ValueError("Strategy reference is out of range.")
            return strategies[position]["Signals"].to_numpy() == signal
        if isinstance(node, ast.BoolOp) and isinstance(
            node.op, (ast.And, ast.Or)
        ):
            values = [evaluate(value, signal) for value in node.values]
            operation = (
                np.logical_and
                if isinstance(node.op, ast.And)
                else np.logical_or
            )
            return operation.reduce(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return np.logical_not(evaluate(node.operand, signal))
        raise ValueError("Use S1, S2, and/or/not, and parentheses only.")

    buy = evaluate(tree.body, 1)
    sell = evaluate(tree.body, 2)
    signals = np.where(sell, 2, np.where(buy, 1, 0))
    return pd.DataFrame({"Signals": signals}, index=index)
