#!/usr/bin/env python
import sys
import warnings
import gradio as gr
import time
from PyPDF2 import PdfReader
import docx2txt
# import crewai.agent

# from crew import Radify
from create_rad import generate


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

job_desc = """
We’re building an AI-powered healthcare chatbot to assist patients with symptom assessment, medical FAQs, and appointment scheduling. The chatbot must integrate with EHR systems, comply with HIPAA/GDPR, and leverage OpenAI models fine-tuned for medical contexts.

𝑺𝒄𝒐𝒑𝒆 𝒐𝒇 𝑾𝒐𝒓𝒌
✔ Chatbot Development:
Implement OpenAI models (GPT-4, GPT-4o) for symptom analysis and patient interaction.
Fine-tune models using healthcare-specific datasets for accuracy and safety.
Integrate a vector database (Pinecone, ChromaDB, or Weaviate) for context-aware conversations and semantic search.
✔ Compliance & Security:
Ensure end-to-end encryption and HIPAA-compliant data handling.
Implement secure user authentication and PII redaction.
✔ Integration:
Connect with EHR systems (FHIR/HL7 standards) and telehealth APIs (Twilio, Zoom).
Enable multi-language support for diverse patient demographics.
✔ Testing & Optimization:
Conduct rigorous testing with healthcare professionals.
Optimize response accuracy and latency using real user feedback.

𝑹𝒆𝒒𝒖𝒊𝒓𝒆𝒅 𝑺𝒌𝒊𝒍𝒍𝒔
✔ AI/ML Expertise: Proven experience with OpenAI API, LangChain, or Hugging Face for NLP tasks.
✔ Vector Databases: Hands-on experience with Pinecone, ChromaDB, or similar tools.
✔ Healthcare Compliance: Knowledge of HIPAA, GDPR, and secure data storage (e.g., PostgreSQL with encryption).
✔ Backend Development: Proficiency in Python (FastAPI/Flask) or Node.js.
✔ API Integration: Experience with EHR systems (Cerner, Epic) and telehealth platforms.

𝑯𝒐𝒘 𝒕𝒐 𝑨𝒑𝒑𝒍𝒚
✔ Submit portfolios showcasing previous healthcare/AI projects.
✔ Provide a brief strategy outlining your approach to:
  - Model fine-tuning for medical accuracy
  - HIPAA-compliant data pipeline design
  - Vector DB integration for context retention
✔ Timeline and total Budget
"""
# rad_doc = generate(job_desc=job_desc)
# print(rad_doc)

# Gradio UI Development
def extract_text_from_file(file):
    if file is None:
        return ""
    file_path = file.name
    if file_path.endswith(".pdf"):
        # doc = fitz.open(file_path)
        # text = "\n".join([page.get_text() for page in doc])
        # doc.close()
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    else:
        text = ""
    return text.strip()

def preprocess_input(text_input, file_input):
    if not text_input and not file_input:
        return gr.update(visible=False), gr.update(value="⚠️ Please enter job requirement text or upload a file.", visible=True), gr.update(visible=False), ""

    final_text = text_input.strip()
    if not final_text and file_input:
        final_text = extract_text_from_file(file_input)

    if not final_text:
        return gr.update(visible=False), gr.update(value="⚠️ The uploaded file appears empty or unsupported.", visible=True), gr.update(visible=False), ""

    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), final_text

def generate_rad(job_desc):
    rad_result = generate(job_desc)
    return gr.update(visible=False), gr.update(visible=True, value=rad_result)

with gr.Blocks(title="RADify") as demo:
    gr.Markdown("## 📄 RADify\n**AI agent to generate a professional Requirement Analysis Document (RAD)**")

    with gr.Row():
        text_input = gr.Textbox(label="📝 Enter Job Requirement", lines=8, placeholder="Paste job requirement here...")
        file_input = gr.File(label="📁 Upload Job Requirement File (PDF/DOCX)", file_types=[".pdf", ".docx"])

    job_text_state = gr.State()

    submit_btn = gr.Button("🚀 Generate RAD", variant="primary")
    # clear_btn = gr.ClearButton("Reset")

    spinner = gr.HTML("""
        <div id="loader" style="display: flex; justify-content: center; margin: 20px;">
            <div style="border: 6px solid #f3f3f3; border-top: 6px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite;"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    """, visible=False)

    error_md = gr.Markdown("", visible=False)
    output_md = gr.Markdown("", visible=False)

    # Step 1: Preprocess and show spinner
    submit_btn.click(preprocess_input,
                     inputs=[text_input, file_input],
                     outputs=[spinner, error_md, output_md, job_text_state])

    # Step 2: Trigger actual RAD generation
    submit_btn.click(generate_rad,
                     inputs=[job_text_state],
                     outputs=[spinner, output_md])

demo.launch(share=True)