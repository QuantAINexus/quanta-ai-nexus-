import streamlit as st
from openai import OpenAI

# Your real API key goes here
api_key = import os
openai.api_key = os.getenv("OPENAI_API_KEY")
 
client = OpenAI(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="QuantAI Nexus", layout="centered")
st.title("🤖 Welcome to QuantAI Nexus")
st.write("Talk to your own AI assistant!")

# Input from user
prompt = st.text_input("You:", "")

# If there's a prompt, generate response
if prompt:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if you're on free plan
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        st.markdown(f"**AI:** {reply}")
