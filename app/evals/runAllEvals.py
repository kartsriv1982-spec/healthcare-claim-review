from runner import EvaluationRunner
from agent.agent_executor import execute_claim_agent


def main():

    runner = EvaluationRunner(
        agent_executor=execute_claim_agent
    )

    runner.run_all()


if __name__ == "__main__":
    main()