import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

# Sidebar UI
st.sidebar.title("Personalization")
prompt = st.sidebar.text_input("System Prompt: ")

model = st.sidebar.selectbox(
    "Choose a model",
    [
        "llama-3.1-8b-instant",
        "llama3-8b-8192",
        "mixtral-8x7b-32768"
    ]
)

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Main UI
st.title("💬 Chat with Groq's LLM")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Enter your query: ", "")

# Button click
if st.button("Submit"):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt if prompt else "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model=model,
    )

    # Extract response
    response = chat_completion.choices[0].message.content

    # Store history
    st.session_state.history.append({
        "query": user_input,
        "response": response
    })

    # Display response
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

# Sidebar history
st.sidebar.title("History")

for i, entry in enumerate(st.session_state.history):
    if st.sidebar.button(f'Query {i+1}: {entry["query"]}'):
        st.markdown(
            f'<div class="response-box">{entry["response"]}</div>',
            unsafe_allow_html=True
        )