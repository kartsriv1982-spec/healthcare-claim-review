"""
Aggregate Metrics
"""

from typing import List

from .base import MetricResult
from .base import BaseMetrics


class AggregateMetrics(BaseMetrics):

    def overall_score(
        self,
        metrics: List[MetricResult]
    ):

        scores = [
            metric.score
            for metric in metrics
        ]

        score = self.average(scores)

        return self.create_result(
            "Overall Evaluation Score",
            score,
            0.90
        )

    def pass_rate(
        self,
        metrics: List[MetricResult]
    ):

        passed = len([
            metric
            for metric in metrics
            if metric.passed
        ])

        score = self.safe_divide(
            passed,
            len(metrics)
        )

        return self.create_result(
            "Pass Rate",
            score,
            0.90
        )