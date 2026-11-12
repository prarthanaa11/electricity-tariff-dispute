# Electricity Tariff Dispute Triage

An AI-powered system designed to assist in analysing and prioritising electricity tariff-related consumer disputes using Retrieval-Augmented Generation (RAG), multi-agent workflows, and observability tools.

## Overview

Electricity tariff disputes can involve complex regulatory documents, tariff orders, electricity supply codes, and consumer-specific circumstances. Manually analysing these disputes can be time-consuming and requires identifying the relevant regulatory provisions.

The Electricity Tariff Dispute Triage system aims to simplify this process by combining document retrieval, AI-assisted analysis, and evidence-based recommendations.

The system retrieves relevant information from regulatory documents, analyses the consumer's complaint, verifies the supporting evidence, and generates a structured response or recommends escalation when sufficient evidence is unavailable.

## Objectives

- Automate the initial analysis of electricity tariff-related complaints.
- Retrieve relevant regulatory provisions from official documents.
- Use multiple AI agents for investigation and verification.
- Generate explainable, evidence-backed recommendations.
- Identify cases that require human intervention.
- Monitor application performance, reliability, and system behaviour.

## Key Features

### 1. Retrieval-Augmented Generation (RAG)
- Processes regulatory documents.
- Splits documents into searchable chunks.
- Generates embeddings for semantic retrieval.
- Retrieves relevant regulatory passages.
- Provides source-based context for AI analysis.

### 2. Multi-Agent Workflow
- **Investigator Agent:** Analyses the complaint and retrieves relevant evidence.
- **Verifier Agent:** Checks whether the recommendation is supported by retrieved evidence.
- **Decision/Router Logic:** Determines whether the case can be answered or requires escalation.

### 3. API and User Interface
- FastAPI backend for handling requests.
- Streamlit interface for submitting and viewing complaints.
- API documentation through Swagger UI.

### 4. Database and Background Processing
- PostgreSQL for structured data persistence.
- Redis for caching and background task coordination.
- Celery for asynchronous task processing.

### 5. Security and Reliability
- Input validation.
- Handling of unsupported or insufficient evidence.
- Retry mechanisms and failure handling.
- Safe handling of untrusted user input.
- Human escalation for uncertain cases.

### 6. Monitoring and Observability
- Prometheus for metrics collection.
- Grafana for dashboards.
- Jaeger for distributed tracing.
- Structured application logs for debugging.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| RAG | Retrieval-Augmented Generation |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Database | PostgreSQL |
| Caching | Redis |
| Task Queue | Celery |
| Containerization | Docker |
| Monitoring | Prometheus |
| Dashboards | Grafana |
| Distributed Tracing | Jaeger |
| Testing | Pytest, Locust |

*The technologies listed above describe the intended project stack. Update this section to match the components actually implemented in your repository.*

## Project Structure

```text
electricity-tariff-dispute/
│
├── app/
│   ├── main.py
│   ├── web.py
│   ├── api/
│   ├── agents/
│   ├── core/
│   ├── models/
│   └── tools/
│
├── corpus/
│   ├── raw/
│   ├── processed/
│   ├── manifest.json
│   └── README.md
│
├── data/
│
├── prompts/
│   ├── investigator_v1.txt
│   ├── investigator_v2.txt
│   ├── verifier_v1.txt
│   └── router_v1.txt
│
├── evaluation/
│   ├── scenarios.jsonl
│   ├── run_evaluation.py
│   └── results/
│
├── monitoring/
│   └── prometheus/
│
├── scripts/
│   ├── build_corpus.py
│   └── init_db.sql
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── runbook.md
│   └── incident-log.md
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*The structure is a reference layout; retain only files and directories that exist in the actual repository.*

## Prerequisites

Install the following before running the project:

- Python 3.11 or compatible version.
- Docker Desktop.
- Git.
- A code editor such as Visual Studio Code.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/electricity-tariff-dispute.git
cd electricity-tariff-dispute
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a template.

Add the required configuration values and API credentials locally.

**Never commit your `.env` file or expose API keys.**

### 5. Start the application

If Docker Compose is configured with all required services:

```bash
docker compose up --build
```

To run in the background:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

## Accessing the Application

When the corresponding services are configured and running:

| Service | URL |
|---|---|
| FastAPI | http://localhost:8000 |
| Swagger API Docs | http://localhost:8000/docs |
| Streamlit Interface | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Jaeger | http://localhost:16686 |

## Example Workflow

1. A consumer complaint is submitted through the application.
2. The API validates the submitted information.
3. The complaint is processed by the triage workflow.
4. Relevant regulatory information is retrieved from the document corpus.
5. The Investigator Agent analyses the complaint using the retrieved evidence.
6. The Verifier Agent checks the supporting evidence.
7. The system generates a structured recommendation or escalates the case.
8. The request and processing information can be monitored through the configured observability stack.

## Testing

Run the test suite:

```bash
python -m pytest -v
```

Run the evaluation pipeline, if configured:

```bash
python -m evaluation.run_evaluation
```

Run load testing, if Locust is configured:

```bash
locust -f locustfile.py --host http://localhost:8000
```

Record actual test results and performance measurements in the project documentation.

## Evaluation Metrics

The system can be evaluated using:

- Retrieval Precision
- Retrieval Recall
- Groundedness
- Recommendation Accuracy
- Response Latency
- API Availability
- Error Rate
- Throughput
- p50 and p95 Response Times

## Regulatory Data Sources

The project is intended to use regulatory documents such as:

- Karnataka Electricity Regulatory Commission (KERC) Retail Tariff Orders.
- Karnataka Electricity Supply Code.

Use the applicable official document versions and maintain source metadata, including document title, issuing authority, version, and page or clause references.

## Limitations

- AI-generated recommendations are dependent on the quality and availability of retrieved regulatory evidence.
- The system does not replace official regulatory authorities or human grievance officers.
- Cases with insufficient or conflicting evidence should be escalated.
- Results should be validated against the applicable regulatory documents.

## Future Enhancements

- Integration with additional electricity regulatory databases.
- Real-time updates to regulatory document collections.
- Improved multilingual complaint support.
- Enhanced evaluation datasets.
- More advanced agent coordination.
- Integration with consumer grievance management platforms.

## Disclaimer

This project is intended as an AI-assisted decision-support and complaint-triage system. It does not provide legally binding decisions or replace official regulatory processes. Final decisions should be made by authorised personnel based on applicable regulations.

## Contributors

Add the names and GitHub profiles of all project team members here.

---

**Project:** Electricity Tariff Dispute Triage  
**Domain:** Artificial Intelligence | RAG | Multi-Agent Systems | Observability
