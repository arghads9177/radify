#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

import crewai.agent

from crew import Radify

import crewai
print(dir(crewai))


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

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

def run():
    """
    Run the crew.
    """
    inputs = {
        "job_description": job_desc
    }
    
    try:
        response = Radify().crew().kickoff(inputs=inputs)
        print(response)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Radify().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Radify().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Radify().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

run()