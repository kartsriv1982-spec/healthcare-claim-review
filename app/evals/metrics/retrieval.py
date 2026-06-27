
from typing import List

from base import BaseMetrics


class RetrievalMetrics(BaseMetrics):

    """
    Metrics related to retrieval quality.
    """

    # -------------------------------------------------------
    # Context Recall
    # -------------------------------------------------------

    def context_recall(
        self,
        expected_documents: List[str],
        retrieved_documents: List[str]
    ):

        score = self.overlap_score(
            expected_documents,
            retrieved_documents
        )

        return self.create_result(
            metric_name="Context Recall",
            score=score,
            threshold=0.90,
            remarks="Relevant documents retrieved."
        )

    # -------------------------------------------------------
    # Context Precision
    # -------------------------------------------------------

    def context_precision(
        self,
        expected_documents: List[str],
        retrieved_documents: List[str]
    ):

        score = self.precision_overlap(
            expected_documents,
            retrieved_documents
        )

        return self.create_result(
            metric_name="Context Precision",
            score=score,
            threshold=0.85,
            remarks="Irrelevant documents minimized."
        )

    # -------------------------------------------------------
    # Groundedness
    # -------------------------------------------------------

    def groundedness(
        self,
        grounded: bool
    ):

        score = self.boolean_score(grounded)

        return self.create_result(
            metric_name="Groundedness",
            score=score,
            threshold=1.0
        )

    # -------------------------------------------------------
    # Faithfulness
    # -------------------------------------------------------

    def faithfulness(
        self,
        faithful: bool
    ):

        score = self.boolean_score(faithful)

        return self.create_result(
            metric_name="Faithfulness",
            score=score,
            threshold=1.0
        )

    # -------------------------------------------------------
    # Similarity
    # -------------------------------------------------------

    def average_similarity(
        self,
        similarities: List[float]
    ):

        score = self.average(similarities)

        return self.create_result(
            metric_name="Embedding Similarity",
            score=score,
            threshold=0.80
        )

    # -------------------------------------------------------
    # Retrieval Latency
    # -------------------------------------------------------

    def latency(
        self,
        milliseconds: float
    ):

        if milliseconds < 100:
            score = 1.0
        elif milliseconds < 300:
            score = 0.9
        elif milliseconds < 500:
            score = 0.75
        elif milliseconds < 1000:
            score = 0.50
        else:
            score = 0.25

        return self.create_result(
            metric_name="Retrieval Latency",
            score=score,
            threshold=0.75,
            metadata={
                "latency_ms": milliseconds
            }
        )