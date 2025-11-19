# Local AI Assistant

A fully offline, local AI assistant powered by Gemma 3 (via Ollama), Streamlit, and ChromaDB.

## Features
- **Local & Private**: No data leaves your device.
- **Chat**: Natural conversation with Gemma 3.
- **RAG**: Upload PDF, CSV, or TXT files to chat with your documents.
- **Tools**: Simple reminders and notes.

## Prerequisites
1.  **Python 3.8+** installed.
2.  **Ollama** installed and running.
    - Download from [ollama.com](https://ollama.com).
    - Pull the model: `ollama pull gemma:2b` (or `gemma:7b` / `gemma3:3b` if available).

## Setup
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the App
```bash
streamlit run app.py
```
