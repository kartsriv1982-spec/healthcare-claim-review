from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================
# Metric Result
# ============================================================

@dataclass
class MetricResult:
    """
    Represents the outcome of a single evaluation metric.
    """

    metric_name: str
    score: float
    threshold: float = 0.90
    passed: bool = False
    remarks: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):

        # Normalize score between 0 and 1
        self.score = max(0.0, min(1.0, self.score))

        # Automatically compute pass/fail
        self.passed = self.score >= self.threshold


# ============================================================
# Base Metrics
# ============================================================

class BaseMetrics:
    """
    Base class providing common utility methods for all metrics.
    """

    # --------------------------------------------------------
    # Safe Division
    # --------------------------------------------------------

    @staticmethod
    def safe_divide(
        numerator: float,
        denominator: float,
        default: float = 0.0
    ) -> float:
        """
        Prevent divide-by-zero errors.
        """

        if denominator == 0:
            return default

        return numerator / denominator

    # --------------------------------------------------------
    # Exact Match
    # --------------------------------------------------------

    @staticmethod
    def exact_match(
        expected: Any,
        actual: Any
    ) -> float:
        """
        Returns 1.0 if values match else 0.0
        """

        return 1.0 if expected == actual else 0.0

    # --------------------------------------------------------
    # Overlap Score
    # --------------------------------------------------------

    @staticmethod
    def overlap_score(
        expected: List[Any],
        actual: List[Any]
    ) -> float:
        """
        Computes overlap between two lists.

        Example:

        Expected:
            A,B,C

        Actual:
            A,C

        Score = 2 / 3 = 0.667
        """

        if not expected:
            return 1.0

        expected_set = set(expected)
        actual_set = set(actual)

        intersection = expected_set.intersection(actual_set)

        return len(intersection) / len(expected_set)

    # --------------------------------------------------------
    # Precision Style Score
    # --------------------------------------------------------

    @staticmethod
    def precision_overlap(
        expected: List[Any],
        actual: List[Any]
    ) -> float:
        """
        Precision-like overlap.

        Example

        Expected:
            A,B

        Actual:
            A,B,C,D

        Score = 2 / 4
        """

        if not actual:
            return 0.0

        expected_set = set(expected)
        actual_set = set(actual)

        return len(expected_set.intersection(actual_set)) / len(actual_set)

    # --------------------------------------------------------
    # Normalize Score
    # --------------------------------------------------------

    @staticmethod
    def normalize_score(
        score: float,
        min_value: float = 0.0,
        max_value: float = 1.0
    ) -> float:
        """
        Ensures score remains within limits.
        """

        return max(min_value, min(score, max_value))

    # --------------------------------------------------------
    # Percentage
    # --------------------------------------------------------

    @staticmethod
    def percentage(
        numerator: float,
        denominator: float
    ) -> float:

        return round(
            BaseMetrics.safe_divide(
                numerator,
                denominator
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # Boolean Score
    # --------------------------------------------------------

    @staticmethod
    def boolean_score(
        condition: bool
    ) -> float:

        return 1.0 if condition else 0.0

    # --------------------------------------------------------
    # Numeric Similarity
    # --------------------------------------------------------

    @staticmethod
    def numeric_similarity(
        expected: float,
        actual: float
    ) -> float:
        """
        Returns similarity between two numbers.

        Perfect match = 1.0

        Larger deviation reduces score.
        """

        if expected == actual:
            return 1.0

        if expected == 0:
            return 0.0

        difference = abs(expected - actual)

        similarity = 1 - (difference / abs(expected))

        return BaseMetrics.normalize_score(similarity)

    # --------------------------------------------------------
    # Average Score
    # --------------------------------------------------------

    @staticmethod
    def average(
        scores: List[float]
    ) -> float:

        if not scores:
            return 0.0

        return round(sum(scores) / len(scores), 3)

    # --------------------------------------------------------
    # Weighted Average
    # --------------------------------------------------------

    @staticmethod
    def weighted_average(
        scores: Dict[str, float],
        weights: Dict[str, float]
    ) -> float:

        weighted_sum = 0.0
        total_weight = 0.0

        for metric_name, score in scores.items():

            weight = weights.get(metric_name, 1.0)

            weighted_sum += score * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return round(weighted_sum / total_weight, 3)

    # --------------------------------------------------------
    # Create Metric Result
    # --------------------------------------------------------

    @staticmethod
    def create_result(
        metric_name: str,
        score: float,
        threshold: float = 0.90,
        remarks: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> MetricResult:

        return MetricResult(
            metric_name=metric_name,
            score=score,
            threshold=threshold,
            remarks=remarks,
            metadata=metadata or {}
        )