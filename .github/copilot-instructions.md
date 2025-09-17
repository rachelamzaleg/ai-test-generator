# Copilot Instructions for AI Agents

## Project Overview
This project is an AI-powered test case generator using LLMs (LangChain, Groq) and a graph-based workflow. It is organized for experimentation with prompt-driven test generation, validation, and export.

## Key Components
- `src/`
  - `exporter.py`: Handles exporting test cases (format and destination logic).
  - `graph.py`: Defines the workflow graph and state transitions for test generation.
  - `__init__.py`: Module marker.
- `notebooks/`
  - `demo.ipynb`: Main notebook for prototyping and running the test generation workflow. Shows how to set up, invoke, and display results.
- `data/`, `outputs/`: For input requirements and generated test cases.

## Core Workflow
- Uses a `TestGenState` dict to track requirements, test cases, and retry attempts.
- The workflow is built with `langgraph.StateGraph`, with nodes for parsing requirements, generating test cases (via LLM), and retry logic for invalid JSON.
- LLM integration is via `langchain_groq.ChatGroq` (model: llama-3.1-8b-instant). API key is loaded from `.env`.

## Developer Workflows
- **Run/Prototype:** Use `notebooks/demo.ipynb` to run the full workflow interactively.
- **Add/Change Logic:** Update or add nodes in `src/graph.py` and reflect changes in the notebook.
- **Export:** Use `src/exporter.py` for output logic (CSV, JSON, etc.).
- **Dependencies:** Install from `requirements.txt` (root and `data/` for data-specific deps).

## Conventions & Patterns
- All workflow state is passed as a single dict (`TestGenState`), not as separate arguments.
- LLM prompts are defined inline in node functions.
- Retry logic is explicit: if JSON is invalid, the workflow can re-invoke the LLM up to `MAX_RETRIES`.
- Use pandas for tabular display in notebooks.
- API keys/secrets are loaded via `dotenv` and must be present in `.env`.

## Examples
- See `notebooks/demo.ipynb` for end-to-end usage, including:
  - Setting up the workflow
  - Invoking with a sample requirement
  - Displaying results as a DataFrame

## Integration Points
- LLM: `langchain_groq.ChatGroq` (Groq API)
- Workflow: `langgraph`
- Data display: `pandas`

## Tips for AI Agents
- When adding new workflow nodes, follow the pattern in `src/graph.py` and `demo.ipynb`.
- Keep all state in the `TestGenState` dict for compatibility.
- Document new node purposes and expected state changes in docstrings.
- For new export formats, extend `src/exporter.py` and update the notebook to use it.

---
For questions or unclear patterns, review `notebooks/demo.ipynb` and `src/graph.py` for canonical examples.