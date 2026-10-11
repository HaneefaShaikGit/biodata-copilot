# BioData Copilot — Architecture

## V1 Data Flow

Public Biomedical Source
        ↓
      REST API
        ↓
      Python
        ↓
       GCS
   Raw Data Storage
        ↓
Python Validation and Transformation
        ↓
    BigQuery
Structured Analytical Data
        ↓
       SQL
        ↓
 Verified Query Result
        ↓
     OpenAI
Grounded Explanation
        ↓
      User

## Component Responsibilities

### Public Biomedical Source
Provides the original biomedical data.

### Python
Handles ingestion, validation, transformation, and service integration.

### GCS
Stores untouched source files.

### BigQuery
Stores structured analytical data and calculates deterministic results.

### OpenAI
Explains verified results. It is not the source of dataset-specific facts.