import requests
import streamlit as st
import sys
import os
from login import login, logout  # Assuming your login code is in login.py

# Add the root directory of the project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from helper import file_helper, get_env

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/chat")
AGENT_LIST_PATH = get_env.retreive_value("AGENT_LIST_PATH")
AVAILABLE_AGENT = file_helper.read_json(AGENT_LIST_PATH).keys()

headers = {'api-key': '49062504109489e78769514b702a6669f5ff9c6aacbbc96f'}

# --- LOGIN CHECK ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Filters")
    
    # Age Filter
    age_input = st.text_input("Age", "")

    # Gene Filter
    gene_input = st.selectbox("Please select a Gene", ('BRCA1', 'BRCA2', 'PALB2'))

    # Category Filter
    option = st.selectbox(
        'Please select a category for your question',
        (
            'Deciding how to best manage your cancer risk',
            'Accessing cancer risk management services',
            'Worry/fear about developing cancer, Concern/fear about surgery',
            'Impact of genetic risk on relationships',
            'Connect with other women with a gene alteration',
            'Worry about children/family members',
            'Starting a family/ having more children',
            'Menopausal symptom',
            'Quitting smoke',
            'Dealing with the after effects of developing cancer'
        )
    )

    # LLM Agent Filter
    llm_input = st.selectbox("LLM", AVAILABLE_AGENT)

    # Prompt Technique Filter
    prompt_technique = st.selectbox(
        'Select a Prompt Technique',
        ('Technique 1', 'Technique 2', 'Technique 3')  # Replace with actual techniques
    )

    # Top-K Retrieval Filter
    top_k_retrieval = st.slider(
        'Select Top-K for Retrieval',
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    if st.button("Logout"):
        logout()

# --- MAIN APP ---
st.title("GenAssist")
st.info(f"Welcome {st.session_state.username}! Ask me questions if you are a BRCA1/BRCA2/PALB2 gene carrier.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message:
            st.markdown(message["output"])
        if "explanation" in message:
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

# --- USER INPUT FEATURE ---
st.markdown("### 💬 Ask a Question")
# Always show the chat input so the user can type their own question
user_input = st.chat_input("What do you want to know?", key="regular_question_input")

# --- POPULAR QUESTIONS SECTION (below the chat input) ---
quick_questions = [
    "I have had a double mastectomy, should I still be having screening?",
    "I haven’t started screening yet. How do I access my first imaging?",
    "What are the menopause symptoms after I get my ovaries out?",
    "I worry I am not doing mammograms frequently enough, should I be doing them more often?"
]
popular_question = st.selectbox("Popular Questions", [""] + quick_questions, key="quick_question_select")

# If a popular question is selected, use that as the prompt.
# Otherwise, use the value entered into the chat input.
if popular_question:
    prompt = popular_question
else:
    prompt = user_input

# --- Submission: Validate Age & Process the Prompt ---
if prompt:
    # Validate age input only after a submission (when prompt is non-empty)
    try:
        age_input_value = int(age_input) if age_input.strip() != "" else None
    except ValueError:
        st.error("Please enter a valid number for age.")
        st.stop()

    if age_input_value is None:
        st.error("Age cannot be empty. Please provide a valid age to continue.")
        st.stop()

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {
        "age": age_input_value,
        "gene_fault": gene_input,
        "category": option,
        "patient_question": prompt,
        "prompt_technique": prompt_technique,
        "top_k_retrieval": top_k_retrieval,
    }

    with st.spinner("Searching for an answer..."):
        try:
            response = requests.post(CHATBOT_URL, headers=headers, json=data)
            if response.status_code == 200:
                output_text = response.json()["output"]
                explanation = response.json()["intermediate_steps"]
                elapsed_time = response.json().get("elapsed_time", "N/A")
            else:
                raise Exception("Backend error")
        except Exception as e:
            output_text = (
                "Thank you for your question. While our system is currently offline, "
                "here's a sample answer: *If you are a carrier of a BRCA1 or BRCA2 mutation, "
                "it is important to follow recommended screening guidelines. Please consult with "
                "your healthcare provider to ensure your screening schedule is appropriate for your age and risk level.*"
            )
            explanation = "This is a placeholder response provided while the backend is offline."
            elapsed_time = "N/A"

    st.markdown(
        f"""<div style="text-align: right; font-size: 0.9em; color: gray;">{elapsed_time}s.</div>""",
        unsafe_allow_html=True,
    )
    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)
    st.session_state.messages.append({
        "role": "assistant",
        "output": output_text,
        "explanation": explanation,
        "elapsed_time": elapsed_time,
    })
