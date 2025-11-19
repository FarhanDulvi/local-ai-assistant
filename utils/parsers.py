import pandas as pd
from pypdf import PdfReader
import io

def read_txt(file):
    return file.getvalue().decode("utf-8")

def read_csv(file):
    df = pd.read_csv(file)
    return df.to_string()

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_file(uploaded_file):
    """
    Dispatches to the correct parser based on file extension.
    """
    if uploaded_file.name.endswith(".txt"):
        return read_txt(uploaded_file)
    elif uploaded_file.name.endswith(".csv"):
        return read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        return read_pdf(uploaded_file)
    else:
        return "Unsupported file format."
