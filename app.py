import streamlit as st
from groq import Groq
import json

# Set up the page
st.set_page_config(page_title="HS Code Lookup System", layout="wide")

# Initialize the Groq client
groq_api_key = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=groq_api_key)

# Placeholder for the initial system message for the AI
system_message = """
[INSERT YOUR SYSTEM MESSAGE HERE]
"""

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_message}]

# Title and description
st.title("HS Code Lookup System")
st.write("Automated and accurate HS Code information at your fingertips.")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div style='border: 2px solid blue; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: right; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: left; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)

# Function to handle message sending and processing
def send_message():
    user_input = st.session_state.input_buffer  # Get the user input
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call Groq API or process internally here
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.chat_history,
            temperature=0.3,
            max_tokens=2000
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Append chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

        # Clear the input buffer and trigger rerun
        st.session_state.input_buffer = ""
        st.experimental_rerun()

# Input for chat messages
user_input = st.text_input("Type your message here:", key="input_buffer", on_change=send_message)
st.button("Send", on_click=send_message)

# Dummy element to force rerun without showing error
st.write(f"Run count: {st.session_state.get('run_count', 0)}")
