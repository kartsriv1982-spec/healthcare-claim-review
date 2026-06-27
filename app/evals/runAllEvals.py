
import time
from datetime import datetime

from runner import EvaluationRunner

# ---------------------------------------------------------
# Import your Agent Executor
#
# Replace this import with your actual implementation
# ---------------------------------------------------------

from agent.agent_executor import execute_claim_agent


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("\n")
    print("=" * 70)
    print("Healthcare Claims Agent Evaluation Framework")
    print("=" * 70)

    start = time.perf_counter()

    try:

        runner = EvaluationRunner(
            agent_executor=execute_claim_agent
        )

        evaluations = runner.run_all()

        end = time.perf_counter()

        duration = round(end - start, 2)

        total_claims = len(evaluations)

        passed = sum(
            1
            for evaluation in evaluations
            if evaluation["overall"].passed
        )

        failed = total_claims - passed

        average_score = round(
            sum(
                evaluation["overall"].score
                for evaluation in evaluations
            ) / total_claims,
            3
        )

        print("\n")
        print("=" * 70)
        print("Evaluation Completed")
        print("=" * 70)

        print(f"Execution Time : {duration} sec")
        print(f"Claims Evaluated : {total_claims}")
        print(f"Passed : {passed}")
        print(f"Failed : {failed}")
        print(f"Average Score : {average_score}")

        print("=" * 70)

        #
        # Future:
        # ReportGenerator()
        # DriftMonitor()
        #

    except Exception as ex:

        print("\nEvaluation Failed")
        print(str(ex))

        raise


# ---------------------------------------------------------

if __name__ == "__main__":

    main()