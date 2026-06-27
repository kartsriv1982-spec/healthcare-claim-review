
from datetime import datetime
from pathlib import Path
import json

from datasetLoader import DatasetLoader
from evaluator import Evaluator
from reportGenerator import ReportGenerator


class EvaluationRunner:

    def __init__(
        self,
        agent_executor,
        result_folder="results"
    ):
        """
        Parameters
        ----------
        agent_executor

            Function responsible for invoking
            the agent.

            Signature:

                result = agent_executor(claim_package)

        """

        self.agent_executor = agent_executor

        self.loader = DatasetLoader()

        self.evaluator = Evaluator()

        self.result_folder = Path(result_folder)

        self.result_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # -------------------------------------------------------

    def run_claim(
        self,
        claim_package
    ):

        print(
            f"Evaluating {claim_package.claim_id}"
        )

        agent_result = self.agent_executor(
            claim_package
        )

        evaluation = self.evaluator.evaluate(
            claim_package.ground_truth,
            agent_result
        )

        self.save_result(
            claim_package.claim_id,
            evaluation
        )

        return evaluation

    # -------------------------------------------------------

    def run_all(self):

        claims = self.loader.load_all()

        evaluations = []

        for claim in claims:

            evaluation = self.run_claim(
                claim
            )

            evaluations.append(
                evaluation
            )
        # -------------------------------
    # Generate Reports
    # -------------------------------

        report_generator = ReportGenerator()

        report_generator.generate_excel(evaluations)

        report_generator.generate_html(evaluations)
    

        return evaluations

    # -------------------------------------------------------

    def save_result(
        self,
        claim_id,
        evaluation
    ):

        filename = self.result_folder / f"{claim_id}.json"

        payload = {

            "claim_id": claim_id,

            "timestamp": datetime.now().isoformat(),

            "overall_score":

                evaluation["overall"].score,

            "passed":

                evaluation["overall"].passed,

            "metrics":[

                {

                    "metric":

                        metric.metric_name,

                    "score":

                        metric.score,

                    "passed":

                        metric.passed,

                    "remarks":

                        metric.remarks

                }

                for metric in

                evaluation["metrics"]

            ]

        }

        with open(
            filename,
            "w"
        ) as fp:

            json.dump(
                payload,
                fp,
                indent=4
            )