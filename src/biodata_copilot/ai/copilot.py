from dotenv import load_dotenv
from openai import OpenAI

from biodata_copilot.ai.questions import QUESTIONS
from biodata_copilot.database.run_sql import run_query


load_dotenv()


def run_question(choice):
    question = QUESTIONS[choice]["question"]
    sql_file = QUESTIONS[choice]["sql_file"]

    result = run_query(sql_file)

    prompt = f"""
You are BioData Copilot.

Answer the question using only the verified SQL result provided below.

Question:
{question}

Verified SQL result:
{result.to_csv(index=False)}

Rules:
- Do not invent numbers.
- State that the findings describe this dataset.
- Do not claim causation.
- Do not provide diagnosis or treatment recommendations.
- Explain the main patterns clearly and concisely.
"""

    client = OpenAI()

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return result, response.output_text