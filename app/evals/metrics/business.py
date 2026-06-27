

from base import BaseMetrics

class BusinessMetrics(BaseMetrics):

    def coverage_accuracy(
        self,
        expected_amount,
        actual_amount
    ):

        score = self.numeric_similarity(
            expected_amount,
            actual_amount
        )

        return self.create_result(
            "Coverage Accuracy",
            score,
            0.95
        )

    def copay_accuracy(
        self,
        expected,
        actual
    ):

        score = self.numeric_similarity(
            expected,
            actual
        )

        return self.create_result(
            "Copay Accuracy",
            score,
            0.95
        )

    def deductible_accuracy(
        self,
        expected,
        actual
    ):

        score = self.numeric_similarity(
            expected,
            actual
        )

        return self.create_result(
            "Deductible Accuracy",
            score,
            0.95
        )

    def policy_clause_accuracy(
        self,
        expected,
        actual
    ):

        score = self.exact_match(
            expected,
            actual
        )

        return self.create_result(
            "Policy Clause Accuracy",
            score,
            1.0
        )

    def medical_consistency(
        self,
        prescription,
        report,
        discharge,
        invoice
    ):

        score = self.average([
            self.boolean_score(prescription),
            self.boolean_score(report),
            self.boolean_score(discharge),
            self.boolean_score(invoice)
        ])

        return self.create_result(
            "Medical Consistency",
            score,
            1.0
        )