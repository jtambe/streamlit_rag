import streamlit as st
import json
from difflib import SequenceMatcher
import os

# Load predefined Q&A data
QA_DATA = {
    "questions": [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
}

def find_similar_question(user_input, threshold=0.1):
    """Find the most relevant predefined answer using similarity matching."""
    best_match = None
    best_score = 0
    
    for qa in QA_DATA["questions"]:
        score = SequenceMatcher(None, user_input.lower(), qa["question"].lower()).ratio()
        print(f"Comparing '{user_input}' with '{qa['question']}' - Similarity Score: {score}")
        if score > best_score:
            best_score = score
            best_match = qa
    
    return best_match if best_score >= threshold else None

def get_response(user_input):
    """Get response from predefined data or fallback message."""
    if not user_input.strip():
        return "Please enter a question to get started! 😊"
    
    match = find_similar_question(user_input)
    
    if match:
        return match["answer"]
    else:
        return "I'm not sure about that. I'm specifically trained to answer questions about Thoughtful AI's automation agents (EVA, CAM, and PHIL). Feel free to ask me about them!"

# Streamlit UI
st.set_page_config(page_title="Thoughtful AI Support Agent", layout="centered")
st.title("🤖 Thoughtful AI Support Agent")
st.markdown("Ask me anything about Thoughtful AI's automation agents!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get and display agent response
    response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)