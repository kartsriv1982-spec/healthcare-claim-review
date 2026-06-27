
from typing import List

from base import BaseMetrics

class ToolMetrics(BaseMetrics):

    def tool_accuracy(
        self,
        expected_tools: List[str],
        used_tools: List[str]
    ):

        score = self.overlap_score(
            expected_tools,
            used_tools
        )

        return self.create_result(
            "Tool Accuracy",
            score,
            0.95
        )

    def tool_precision(
        self,
        expected_tools,
        used_tools
    ):

        score = self.precision_overlap(
            expected_tools,
            used_tools
        )

        return self.create_result(
            "Tool Precision",
            score,
            0.90
        )

    def success_rate(
        self,
        successful_calls,
        total_calls
    ):

        score = self.safe_divide(
            successful_calls,
            total_calls
        )

        return self.create_result(
            "Tool Success Rate",
            score,
            0.95
        )

    def failure_rate(
        self,
        failures,
        total
    ):

        score = 1 - self.safe_divide(
            failures,
            total
        )

        return self.create_result(
            "Tool Failure Rate",
            score,
            0.95
        )