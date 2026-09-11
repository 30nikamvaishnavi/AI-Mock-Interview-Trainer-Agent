# AI Mock Interview Trainer Agent

An AI-powered mock interview assistant built with Streamlit, IBM watsonx Granite, resume parsing, RAG, chat practice, voice answers, answer evaluation, and interview history.

## Features

- Upload and analyze PDF or DOCX resumes
- Build a candidate profile from resume content
- Generate technical, project, HR, and coding interview questions
- Practice through text or voice answers
- Evaluate answers with IBM watsonx Granite
- Chat with a resume-aware interview assistant
- Save and review completed interviews
- Retrieve supporting context from the local knowledge base

## Requirements

- Python 3.10 or newer
- An IBM watsonx account and project
- IBM watsonx API credentials

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root. Do not commit this file:

   ```env
   IBM_API_KEY=your_ibm_watsonx_api_key
   IBM_PROJECT_ID=your_ibm_watsonx_project_id
   PROJECT_ID=your_ibm_watsonx_project_id
   ```

   `IBM_API_KEY` and `IBM_PROJECT_ID` are required by the main interview agent. `PROJECT_ID` is used by the answer evaluator and should contain the same project ID.

## Run the application

```powershell
streamlit run app_ui.py
```

Then open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Project layout

- `app_ui.py` - Streamlit user interface
- `agent.py` - interview generation, answer evaluation, and chat integration
- `resume_parser.py` - PDF/DOCX resume extraction and profile analysis
- `rag.py`, `rag_agent.py`, `vector_store.py` - knowledge-base retrieval
- `history.py` - interview history storage
- `voice.py` - speech-to-text support
- `knowledge_base/` - interview preparation content
- `requirements.txt` - Python dependencies

## Notes

- Uploaded resumes, local vector databases, SQLite databases, audio recordings, reports, virtual environments, and `.env` files are excluded from Git.
- Microphone support may require additional system audio dependencies and permissions.
- IBM watsonx model access and credentials are required for live generation and evaluation.

## Tests

Run the available tests individually as needed, for example:

```powershell
python test_agent.py
python test_rag.py
python test_env.py
```
