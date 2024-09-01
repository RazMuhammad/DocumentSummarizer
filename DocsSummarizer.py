import requests
import os
import fitz  # PyMuPDF
import nltk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import streamlit as st
from groq import Groq


# Download NLTK resources
nltk.download('punkt')
GROQ_API_KEY = st.secrets['GROQ_API_KEY']
# Initialize Groq Client
client = Groq(
    api_key= GROQ_API_KEY
)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to segment text into topics
def segment_text_into_topics(text):
    topics = text.split('\n\n')  # Simple split by double newline; can be customized
    return topics

# Function to summarize text using LLM
def summarize_text(topic):
    prompt = f"Summarize the following text and define any technical terms used. Provide clear and contextually relevant definitions for the terms, especially those related to AI and machine learning:\n\n{topic}"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert summarizer and technical writer who provides concise and clear summaries of topics, and defines any technical terms with relevance to the context."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to define technical terms using LLM
def define_technical_terms(terms):
    definitions = {}
    for term in terms:
        prompt = f"Define the technical term '{term}' in the context of AI and machine learning."
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in AI and machine learning. Provide clear and contextually relevant definitions for technical terms."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-70b-versatile",
            )
            definitions[term] = chat_completion.choices[0].message.content.strip()
        except Exception as e:
            definitions[term] = f"Definition not found due to an error: {str(e)}"
    return definitions

# Function to process the entire PDF and generate summaries
def process_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    topics = segment_text_into_topics(text)
    summary_output = ""

    for topic in topics:
        summary = summarize_text(topic)
        summary_output += f"Summary:\n{summary}\n\n"

        # Extract and define technical terms
        words = set(topic.split())
        technical_terms = [word for word in words if word.isalpha() and word.isupper()]
        if technical_terms:
            definitions = define_technical_terms(technical_terms)
            summary_output += "Technical Terms and Definitions:\n"
            for term, definition in definitions.items():
                summary_output += f"{term}: {definition}\n"
            summary_output += "\n"

    return summary_output

# Function to create a PDF from the summary with improved formatting
def create_summary_pdf(output_text, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    story = []

    # Define styles
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    para_style = styles['BodyText']
    tech_term_style = ParagraphStyle(
        'TechTerm',
        parent=styles['BodyText'],
        textColor=colors.blue,
        spaceBefore=10,
        leftIndent=20
    )

    # Process the text for PDF
    lines = output_text.split('\n\n')
    for line in lines:
        if line.startswith("Summary:"):
            title = line.split(":", 1)[1].strip()
            story.append(Paragraph("Summary", subheading_style))
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(title, para_style))
            story.append(Spacer(1, 0.2 * inch))
        elif "Technical Terms and Definitions:" in line:
            story.append(Paragraph("Technical Terms and Definitions", subheading_style))
            story.append(Spacer(1, 0.1 * inch))
            terms = line.split("\n")[1:]
            for term in terms:
                story.append(Paragraph(term, tech_term_style))
                story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Paragraph(line, para_style))
            story.append(Spacer(1, 0.2 * inch))

    doc.build(story)

# Streamlit Interface
st.title("PDF Summarizer with Technical Definitions")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Processing...")
    summary = process_pdf(uploaded_file)

    output_pdf_path = "summary_output.pdf"
    create_summary_pdf(summary, output_pdf_path)

    with open(output_pdf_path, "rb") as file:
        btn = st.download_button(
            label="Download Summary PDF",
            data=file,
            file_name="summary_output.pdf",
            mime="application/pdf"
        )
