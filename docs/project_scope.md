# BioData Copilot — Project Scope

## Problem

Biomedical datasets can contain many records, variables, missing values, and domain-specific information, making them difficult to inspect and interpret quickly.

## Goal

Build a small cloud-based biomedical data platform that:

1. Retrieves data from a public biomedical source.
2. Preserves the original source data.
3. Performs basic validation and transformation.
4. Stores structured analytical data in BigQuery.
5. Answers predefined analytical questions using SQL.
6. Uses an LLM to explain verified query results.

## Target User

A student or researcher exploring biomedical data.

## Core Principle

The database calculates facts.

The LLM explains verified facts.

## V1 Scope

- One biomedical dataset
- Python ingestion
- GCS raw storage
- Data validation
- BigQuery analytical tables
- 3–5 supported analytical questions
- OpenAI explanation layer
- Simple interface

## Out of Scope

- Medical diagnosis
- Treatment recommendations
- Machine-learning prediction
- Arbitrary natural-language-to-SQL
- Multiple biomedical datasets
- RAG
- Large-scale distributed processing

## Interpretation Rule

BioData Copilot will distinguish directly measurable facts from interpretations that require additional clinical or scientific evidence.

## Future Extensions

- Scientific literature retrieval
- RAG
- Natural-language-to-SQL
- Data lineage and provenance
- Machine-learning experiments
- Trustworthy biomedical AI evaluation