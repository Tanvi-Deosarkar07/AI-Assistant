

import streamlit as st
import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()

api_key=os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def response(messages):
    try:
      response = model.generate_content(messages)
      return response
    except Exception as e:
      return f"Error {str(e)}"

def fetch_conversation_history():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "user", "parts": "System Prompt: You are UXGemini - You are an expert UX research and product strategy assistant built to support product teams during the discovery phase. Your role is to assist in generating ideas, guiding user research, validating product concepts, planning A/B tests, and supporting early-stage design thinking. Based on the user’s input, help them clarify the product goal or feature idea, suggest relevant user research questions, and offer creative, data-driven A/B test plans that include a hypothesis, test variants, and success metrics. Provide a low-fidelity wireframe structure suggestion using a simple textual layout and recommend suitable prototyping tools such as Figma, Framer, or Streamlit depending on the context. Your responses should be clear and actionable, and presented in a structured format that includes: a brief product summary, suggested research questions, A/B test plan with hypothesis and variants, wireframe layout suggestion, recommended prototyping tool, and next suggested steps for the product team."}
        ]
    return st.session_state['messages']


st.title("You are UXGemini - My Virtual UX Research Assistant")

user_input = st.chat_input("You: ")


if user_input:
    messages = fetch_conversation_history()
    messages.append({"role": "user", "parts": user_input})
    response = response(messages)
    messages.append({"role": "model", "parts": response.candidates[0].content.parts[0].text})

    for message in messages:
        if message["role"] == "model":
            st.write(f"UXGemini: {message['parts']}")
        elif message["role"] == "user" and ("System Prompt" not in message["parts"]) :
            st.write(f"You: {message['parts']}")
