
from metrics.classification import ClassificationMetrics
from metrics.retrieval import RetrievalMetrics
from metrics.tool import ToolMetrics
from metrics.business import BusinessMetrics
from metrics.performance import PerformanceMetrics
from metrics.aggregate import AggregateMetrics


class Evaluator:

    def __init__(self):

        self.classification = ClassificationMetrics()
        self.retrieval = RetrievalMetrics()
        self.tool = ToolMetrics()
        self.business = BusinessMetrics()
        self.performance = PerformanceMetrics()
        self.aggregate = AggregateMetrics()

    def evaluate(self, ground_truth, agent_result):

        results = []

        # ---------------------------------------------------
        # Decision Accuracy
        # ---------------------------------------------------

        results.append(

            self.classification.decision_accuracy(

                ground_truth.expected_decision,

                agent_result.decision

            )

        )

        # ---------------------------------------------------
        # Reason Accuracy
        # ---------------------------------------------------

        results.append(

            self.classification.reason_accuracy(

                ground_truth.expected_reasons,

                agent_result.reasons

            )

        )

        # ---------------------------------------------------
        # Tool Accuracy
        # ---------------------------------------------------

        results.append(

            self.tool.tool_accuracy(

                ground_truth.expected_tools,

                agent_result.tools_used

            )

        )

        # ---------------------------------------------------
        # RAG Recall
        # ---------------------------------------------------

        results.append(

            self.retrieval.context_recall(

                ground_truth.expected_rag_documents,

                agent_result.retrieved_documents

            )

        )

        # ---------------------------------------------------
        # RAG Precision
        # ---------------------------------------------------

        results.append(

            self.retrieval.context_precision(

                ground_truth.expected_rag_documents,

                agent_result.retrieved_documents

            )

        )

        # ---------------------------------------------------
        # Coverage Accuracy
        # ---------------------------------------------------

        if hasattr(ground_truth, "eligible_amount"):

            results.append(

                self.business.coverage_accuracy(

                    ground_truth.eligible_amount,

                    agent_result.eligible_amount

                )

            )

        # ---------------------------------------------------
        # Human Review Routing
        # ---------------------------------------------------

        results.append(

            self.business.human_review_accuracy(

                ground_truth.expected_human_review,

                agent_result.human_review

            )

        )

        # ---------------------------------------------------
        # Confidence
        # ---------------------------------------------------

        results.append(

            self.performance.confidence(

                agent_result.confidence

            )

        )

        # ---------------------------------------------------
        # Latency
        # ---------------------------------------------------

        results.append(

            self.performance.latency(

                agent_result.execution_time

            )

        )

        # ---------------------------------------------------
        # Token Efficiency
        # ---------------------------------------------------

        results.append(

            self.performance.token_efficiency(

                agent_result.token_usage["total_tokens"]

            )

        )

        overall = self.aggregate.overall_score(results)

        return {

            "overall": overall,

            "metrics": results

        }