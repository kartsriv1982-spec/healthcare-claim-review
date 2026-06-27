"""
Healthcare Agent Evaluation Framework (HAEF)

classification.py

Classification evaluation metrics for the
Claims Adjudication Agent.
"""

from __future__ import annotations

from typing import List
from typing import Dict

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from base import BaseMetrics


class ClassificationMetrics(BaseMetrics):

    """
    Metrics related to claim decision classification.
    """

    # -------------------------------------------------
    # Overall Accuracy
    # -------------------------------------------------

    def accuracy(
        self,
        expected: List[str],
        predicted: List[str]
    ):

        score = accuracy_score(
            expected,
            predicted
        )

        return self.create_result(
            metric_name="Classification Accuracy",
            score=score,
            threshold=0.95,
            remarks="Overall claim decision accuracy."
        )

    # -------------------------------------------------
    # Decision Accuracy
    # -------------------------------------------------

    def decision_accuracy(
        self,
        expected: str,
        predicted: str
    ):

        score = self.exact_match(
            expected,
            predicted
        )

        return self.create_result(
            metric_name="Decision Accuracy",
            score=score,
            threshold=1.0,
            remarks=f"Expected={expected}, Predicted={predicted}"
        )

    # -------------------------------------------------
    # Precision
    # -------------------------------------------------

    def precision(
        self,
        expected: List[str],
        predicted: List[str],
        label: str
    ):

        score = precision_score(
            expected,
            predicted,
            labels=[label],
            average="macro",
            zero_division=0
        )

        return self.create_result(
            metric_name=f"{label} Precision",
            score=score,
            threshold=0.90
        )

    # -------------------------------------------------
    # Recall
    # -------------------------------------------------

    def recall(
        self,
        expected: List[str],
        predicted: List[str],
        label: str
    ):

        score = recall_score(
            expected,
            predicted,
            labels=[label],
            average="macro",
            zero_division=0
        )

        return self.create_result(
            metric_name=f"{label} Recall",
            score=score,
            threshold=0.90
        )

    # -------------------------------------------------
    # F1
    # -------------------------------------------------

    def f1(
        self,
        expected: List[str],
        predicted: List[str],
        label: str
    ):

        score = f1_score(
            expected,
            predicted,
            labels=[label],
            average="macro",
            zero_division=0
        )

        return self.create_result(
            metric_name=f"{label} F1",
            score=score,
            threshold=0.90
        )

    # -------------------------------------------------
    # Confusion Matrix
    # -------------------------------------------------

    def confusion(
        self,
        expected: List[str],
        predicted: List[str]
    ):

        labels = sorted(
            list(
                set(expected + predicted)
            )
        )

        matrix = confusion_matrix(
            expected,
            predicted,
            labels=labels
        )

        return {
            "labels": labels,
            "matrix": matrix
        }

    # -------------------------------------------------
    # Classification Report
    # -------------------------------------------------

    def report(
        self,
        expected: List[str],
        predicted: List[str]
    ) -> Dict:

        return classification_report(
            expected,
            predicted,
            output_dict=True,
            zero_division=0
        )

    # -------------------------------------------------
    # Full Evaluation
    # -------------------------------------------------

    def evaluate(
        self,
        expected: List[str],
        predicted: List[str]
    ):

        labels = sorted(
            list(
                set(expected + predicted)
            )
        )

        results = {}

        results["overall_accuracy"] = self.accuracy(
            expected,
            predicted
        )

        for label in labels:

            results[label] = {

                "precision": self.precision(
                    expected,
                    predicted,
                    label
                ),

                "recall": self.recall(
                    expected,
                    predicted,
                    label
                ),

                "f1": self.f1(
                    expected,
                    predicted,
                    label
                )

            }

        results["confusion_matrix"] = self.confusion(
            expected,
            predicted
        )

        results["classification_report"] = self.report(
            expected,
            predicted
        )

        return results