# AI Test Case Generator

This project is an AI-powered test case generator that leverages LLMs (LangChain, Groq) and a graph-based workflow for prompt-driven test generation, validation, and export.

## Features
- **Prompt-driven test generation** using LLMs
- **Graph-based workflow** with retry logic for invalid outputs
- **Export test cases** in various formats
- **Interactive prototyping** in Jupyter notebooks

## Project Structure
- `src/`
  - `graph.py`: Defines the workflow graph and state transitions
  - `exporter.py`: Handles exporting test cases (format and destination logic)
  - `__init__.py`: Module marker
- `notebooks/`
  - `demo.ipynb`: Main notebook for prototyping and running the workflow
- `data/`, `outputs/`: For input requirements and generated test cases
- `.github/copilot-instructions.md`: AI agent instructions and project conventions

## How It Works
- The workflow uses a `TestGenState` dict to track requirements, test cases, and retry attempts
- Built with `langgraph.StateGraph`, with nodes for parsing requirements, generating test cases (via LLM), and retry logic for invalid JSON
- LLM integration via `langchain_groq.ChatGroq` (model: llama-3.1-8b-instant)
- API key is loaded from `.env` (see below)

## Getting Started
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up your Groq API key**
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
3. **Run the workflow**
   - Open `notebooks/demo.ipynb` and follow the cells to run the workflow interactively

## Developer Notes
- All workflow state is passed as a single dict (`TestGenState`)
- LLM prompts are defined inline in node functions - this is temporarly
- Retry logic is explicit: if JSON is invalid, the workflow can re-invoke the LLM up to `MAX_RETRIES` - STILL TO DO
- Use pandas for tabular display in notebooks
- For new export formats, extend `src/exporter.py` and update the notebook - TO DO 

## Example Usage
See `notebooks/demo.ipynb` for a full example, including:
- Setting up the workflow
- Invoking with a sample requirement
- Displaying results as a DataFrame

## License
MIT License
