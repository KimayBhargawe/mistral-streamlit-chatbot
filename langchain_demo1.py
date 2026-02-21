import streamlit as st
import ollama

st.title("Local Ollama ChatBot")

user_input = st.text_input("Ask Something")

if st.button("Generate"):
    if user_input:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        st.write(response["message"]["content"])