import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv

# Initialize OpenAI API Key
load_dotenv()
openai_api_key = os.getenv("NVIDIA_API_KEY")

# App Configuration
st.set_page_config(page_title="Language Translator", page_icon="🌍", layout="centered")

# Persistent Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# Login System
def login_page():
    st.title("Login to Language Translator 🌍")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        # Placeholder for actual authentication logic
        if username == "user" and password == "password123":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

def main_app():
    st.title("English to Local Language Translator 🌐")
    st.write("Translate English text into various local languages in real-time.")

    #API Call Setup
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = openai_api_key
        )

    # Input Section
    english_text = st.text_area("Enter English Text", placeholder="Type your text here...")
    target_language = st.selectbox("Select Target Language", options=["Hausa", "Yoruba", "Igbo", "Others"])

    # Translate Button
    if st.button("Translate"):
        if english_text.strip():
            with st.spinner("Translating..."):
                try:
                    # OpenAI API Call
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct",
                        messages=[{"role": "user", "content": f"Translate the following English text to {target_language} NO PREAMBLE: {english_text}"}],
                        max_tokens=30,
                        temperature=0.7,
                        stream=False,
                    )

                    translation = response.choices[0].message.content.strip()
                    st.success("Translation Complete!")
                    st.text_area("Translated Text", translation, height=150)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter English text to translate.")

    # Real-Time Update Example (Refresh Button)
    #if st.button("Refresh"):
    #    st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown("**Note:** You are using the trial version. [Login](#) for unlimited access.")

# Trial Limitation
if not st.session_state.logged_in:
    if "trial_expired" not in st.session_state:
        st.session_state.trial_expired = False

    if not st.session_state.trial_expired:
        main_app()
        st.session_state.trial_expired = True
        st.warning("Trial session ended. Please login to continue.")
    else:
        login_page()
else:
    main_app()
