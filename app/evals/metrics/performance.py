"""
Performance Metrics
"""

from .base import BaseMetrics


class PerformanceMetrics(BaseMetrics):

    def latency(
        self,
        seconds
    ):

        if seconds < 2:
            score = 1

        elif seconds < 5:
            score = 0.9

        elif seconds < 10:
            score = 0.7

        else:
            score = 0.4

        return self.create_result(
            "Execution Latency",
            score,
            0.80
        )

    def confidence(
        self,
        confidence
    ):

        return self.create_result(
            "Confidence",
            confidence,
            0.90
        )

    def token_efficiency(
        self,
        tokens,
        threshold=5000
    ):

        score = min(
            1,
            threshold / tokens
        )

        return self.create_result(
            "Token Efficiency",
            score,
            0.80
        )