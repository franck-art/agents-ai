#!/usr/bin/env python
import warnings
from exam_ai.crew import ExamAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    question = "Est il moralement acceptable de mentir si cela permet d'eviter une injustice ?"

    try:
        crew = ExamAi().crew()

        result = crew.kickoff(
            inputs={
                "question": question,
            }
        )

        print("\n===== RÉSULTAT FINAL =====\n")
        print(result)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
