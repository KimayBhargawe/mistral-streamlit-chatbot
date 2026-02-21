import streamlit as st
from mistralai import Mistral

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(page_title="Mistral Chatbot", page_icon="🤖")
st.title("🤖 Free Mistral API Chatbot")

# -----------------------------------
# Load API Key Safely
# -----------------------------------
MISTRAL_API_KEY = st.secrets.get("MISTRAL", {}).get("api_key")

if not MISTRAL_API_KEY:
    st.error("❗ Add your Mistral API key inside .streamlit/secrets.toml")
    st.stop()

# -----------------------------------
# Initialize Mistral Client
# -----------------------------------
client = Mistral(api_key=MISTRAL_API_KEY)

# -----------------------------------
# Session State (Chat History)
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# -----------------------------------
# Display Previous Messages
# -----------------------------------
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# -----------------------------------
# Chat Input
# -----------------------------------
if prompt := st.chat_input("Type your message here..."):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Mistral API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.complete(
                model="mistral-small-latest",
                messages=st.session_state.messages
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )