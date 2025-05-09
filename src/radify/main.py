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
def extract_text_from_files(files):
    if not files:
        return ""

    all_text = ""

    for file in files:
        file_path = file.name
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                all_text += page.extract_text() or ""
        elif file_path.endswith(".docx"):
            all_text += docx2txt.process(file_path)
    
    return all_text.strip()

def validate_and_store(text_input, file_input):
    if not text_input and not file_input:
        raise gr.Error("⚠️ Please enter job requirement text or upload a file.")

    final_text = text_input.strip()
    if not final_text and file_input:
        final_text = extract_text_from_files(file_input)

    if not final_text:
        raise gr.Error("⚠️ The uploaded file appears empty or unsupported.")

    return (
        final_text, 
        gr.update(visible=True),                 # spinner
        gr.update(visible=False),                # output_md
        gr.update(interactive=False),            # submit_btn (disable)
        gr.update(interactive=False)             # clear_btn (disable)
    )

def generate_rad(job_desc):
    if not job_desc.strip():
        # No action if input is empty (after clear)
        return (
            gr.update(visible=False),     # output_md
            gr.update(visible=False),     # spinner
            gr.update(interactive=True),  # submit_btn
            gr.update(interactive=True)   # clear_btn
        )

    try:
        result = generate(job_desc)
        return (
            gr.update(value=result, visible=True),  # output_md
            gr.update(visible=False),               # spinner
            gr.update(interactive=True),            # submit_btn
            gr.update(interactive=True)             # clear_btn
        )
    except Exception as e:
        error_msg = f"❌ RAD generation failed: {e}"
        return (
            gr.update(value=error_msg, visible=True),  # show in output_md as error text
            gr.update(visible=False),
            gr.update(interactive=True),
            gr.update(interactive=True)
        )
    

def clear_form():
    return "", None, "", gr.update(visible=False), gr.update(value="", visible=False), gr.update(value="", visible=False)

with gr.Blocks(title="RADify") as demo:
    gr.Markdown("## 📄 RADify\n**AI agent to generate a professional Requirement Analysis Document (RAD)**")

    with gr.Row():
        text_input = gr.Textbox(label="📝 Enter Job Requirement", lines=8, placeholder="Paste job requirement here...")
        file_input = gr.File(label="📁 Upload Job Requirement Files (PDF/DOCX)", file_types=[".pdf", ".docx"], file_count="multiple")

    with gr.Row():
        submit_btn = gr.Button("🚀 Generate RAD", variant="primary")
        clear_btn = gr.Button("🧹 Clear")

    job_text_state = gr.State()

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

    output_md = gr.Markdown("", visible=False)

    # Step 1: Validate input and set state
    submit_btn.click(
        fn=validate_and_store,
        inputs=[text_input, file_input],
        outputs=[job_text_state, spinner, output_md, submit_btn, clear_btn]
    )

    # Step 2: Trigger generate only if state is set
    job_text_state.change(
        fn=generate_rad,
        inputs=[job_text_state],
        outputs=[output_md, spinner, submit_btn, clear_btn]
    )

    # Clear button
    clear_btn.click(
        fn=clear_form,
        inputs=[],
        outputs=[text_input, file_input, job_text_state, spinner, output_md]
    )

demo.launch()

# demo.launch(share=True)