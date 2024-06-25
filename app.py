import streamlit as st
from groq import Groq
import json

# Set up the page
st.set_page_config(page_title="HS Code Lookup System", layout="wide")

# Initialize the Groq client using the API key from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=groq_api_key)

# Placeholder for the initial system message for the AI
system_message = """
[INSERT YOUR SYSTEM MESSAGE HERE]
"""

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_message}]
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# Placeholder for the product list
products = [
    {"hs_code": "[HS_CODE_1]", "name": "[PRODUCT_NAME_1]", "definisi": "[DEFINISI_1]", "bahan": "[BAHAN_1]"},
    {"hs_code": "[HS_CODE_2]", "name": "[PRODUCT_NAME_2]", "definisi": "[DEFINISI_2]", "bahan": "[BAHAN_2]"},
    # Add all products similarly
]

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
    if st.session_state.input_buffer:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": st.session_state.input_buffer})

        # Call Groq API with the chat history
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.chat_history,
            temperature=0.3,
            max_tokens=2000
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Append chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

        # Clear the input buffer
        st.session_state.input_buffer = ""

# Input for chat messages
user_input = st.text_input("Type your message here:", key="input_buffer")
if st.button("Send"):
    send_message()

# Display product details
st.write("## Product Catalog")
st.write("### Select a product from below and refer to it in the chat:")

for product in products:
    st.markdown(f"""
    <div style='border: 2px solid gray; padding: 10px; margin: 10px 0; border-radius: 8px;'>
        <strong>HS Code:</strong> {product['hs_code']}<br>
        <strong>Name:</strong> {product['name']}<br>
        <strong>Definisi:</strong> {product.get('definisi', 'No definition available')}<br>
        <strong>Bahan:</strong> {product.get('bahan', 'No material info available')}
    </div>
    """, unsafe_allow_html=True)
