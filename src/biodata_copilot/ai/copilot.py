from pathlib import Path

import duckdb
from dotenv import load_dotenv
from openai import OpenAI

from biodata_copilot.ai.questions import QUESTIONS


load_dotenv()


def run_question(choice):

    question = QUESTIONS[choice]["question"]
    sql_file = QUESTIONS[choice]["sql_file"]

    # Run verified SQL
    connection = duckdb.connect("data/biodata.duckdb")

    sql = Path(sql_file).read_text()

    result = connection.execute(sql).fetchdf()

    connection.close()

    # Explain verified result
    client = OpenAI()

    prompt = f"""
You are BioData Copilot.

Answer the user's question using ONLY the verified SQL result below.

Question:
{question}

Verified SQL result:
{result.to_csv(index=False)}

Rules:
- Do not invent numbers.
- Clearly state that the results describe this dataset.
- Do not claim causation.
- Do not provide diagnosis or treatment recommendations.
- Explain the main patterns clearly and concisely.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return question, result, response.output_text