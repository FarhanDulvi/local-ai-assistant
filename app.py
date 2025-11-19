import streamlit as st
import os
import json
from utils.llm import LLMClient
from utils.db import DBManager
from utils.parsers import parse_file

# Page Config
st.set_page_config(page_title="Local AI Assistant", layout="wide")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemma3:1b"

# Sidebar
with st.sidebar:
    st.title("Settings")
    model_name = st.text_input("Ollama Model Name", value=st.session_state.model_name)
    if model_name != st.session_state.model_name:
        st.session_state.model_name = model_name
        st.rerun()

    st.divider()
    st.title("Knowledge Base")
    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, type=["txt", "pdf", "csv"])
    
    if st.button("Process Documents"):
        if uploaded_files:
            db = DBManager()
            with st.spinner("Processing..."):
                for file in uploaded_files:
                    text = parse_file(file)
                    if text:
                        db.add_document(text, metadata={"source": file.name})
            st.success("Documents processed!")

    st.divider()
    st.title("Tools")
    tool_choice = st.radio("Select Tool", ["Chat", "Reminders", "Notes"])

# Main Content
llm = LLMClient(model_name=st.session_state.model_name)
db = DBManager()

if tool_choice == "Chat":
    st.header("Chat with Gemma")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # RAG
                context_docs = db.query_documents(prompt)
                context = "\n".join(context_docs) if context_docs else None
                
                response = llm.generate_response(prompt, context=context)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

elif tool_choice == "Reminders":
    st.header("Reminders")
    if "reminders" not in st.session_state:
        st.session_state.reminders = []
    
    new_reminder = st.text_input("Add Reminder")
    if st.button("Add"):
        if new_reminder:
            st.session_state.reminders.append(new_reminder)
            st.success("Added!")
            st.rerun()
    
    for i, rem in enumerate(st.session_state.reminders):
        col1, col2 = st.columns([0.9, 0.1])
        col1.write(f"- {rem}")
        if col2.button("X", key=f"rem_{i}"):
            st.session_state.reminders.pop(i)
            st.rerun()

elif tool_choice == "Notes":
    st.header("Personal Notes")
    note_file = "notes.json"
    
    if os.path.exists(note_file):
        with open(note_file, "r") as f:
            notes = json.load(f)
    else:
        notes = []

    new_note_title = st.text_input("Note Title")
    new_note_content = st.text_area("Content")
    
    if st.button("Save Note"):
        if new_note_title and new_note_content:
            notes.append({"title": new_note_title, "content": new_note_content})
            with open(note_file, "w") as f:
                json.dump(notes, f)
            st.success("Saved!")
            st.rerun()
            
    st.divider()
    for note in notes:
        with st.expander(note["title"]):
            st.write(note["content"])
