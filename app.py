
import streamlit as st
import google.generativeai as genai
import dotenv
import os
import time

dotenv.load_dotenv()

api_key=os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize session variables
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

if 'time_limit_minutes' not in st.session_state:
    st.session_state.time_limit_minutes = 10  # Default daily limit in minutes

# Layout using Tabs
st.title("🎓 AI Assistant for Students")

tab1, tab2, tab3 = st.tabs(["📚 Learning Hub", "🤖 AI Assistant", "🔒 Parent Controls"])

# ---------------------------
# Learning Hub
# ---------------------------
with tab1:
    st.header("🌟 Discover the World of AI!")

    st.markdown("Pick a question that sparks your curiosity! 🤔✨")

    curious_question = st.selectbox("What do you want to explore today?",
        [
            "🔍 What exactly is Artificial Intelligence?",
            "🧠 How does AI actually 'think'?",
            "💬 How does ChatGPT work?",
            "🚀 How does Gemini by Google work?",
            "🎮 Can AI play games better than humans?",
            "🎨 Can AI create art or music?",
            "🤖 Will robots take over the world?",
            "🌎 How is AI used in everyday life?"
        ]
    )

    if st.button("Explore!"):
        with st.spinner("Finding the coolest answer... 🚀"):
            prompt = f"Explain to a school student in under 100 words, in a fun and simple way: {curious_question}"
            response = model.generate_content(prompt)
            st.success(response.text)

# ---------------------------
# AI Assistant (Daily)
# ---------------------------
with tab2:
    st.header("🤖 Ask Your AI Assistant!")

    elapsed_minutes = (time.time() - st.session_state.start_time) / 60
    if elapsed_minutes >= st.session_state.time_limit_minutes:
        st.error("⏳ Your allowed usage time is over! Please come back tomorrow!")
    else:
        question = st.text_input("Ask your question (school-friendly!)")

        if st.button("Get Answer"):
            if question:
                with st.spinner("Thinking..."):
                    response = model.generate_content(f"Answer this for a school student in less than 100 words: {question}")
                    st.success(response.text)

                    # Save to query history
                    st.session_state.query_history.append({"question": question, "answer": response.text})
            else:
                st.warning("Please type a question!")

# ---------------------------
# Parent Controls
# ---------------------------
with tab3:
    st.header("🔒 Parent Control Panel")

    password = st.text_input("Enter Parent Password", type="password")

    if password == "parent123":  # Simple placeholder
        st.success("Access Granted ✅")

        if st.button("Show Student Query History"):
            if st.session_state.query_history:
                for i, item in enumerate(st.session_state.query_history):
                    st.write(f"**Q:** {item['question']}")
                    st.write(f"**A:** {item['answer']}")
                    st.write("---")
            else:
                st.info("No queries yet.")

        new_limit = st.number_input("Set daily usage limit (minutes)", min_value=1, max_value=120, value=10)
        if st.button("Update Time Limit"):
            st.session_state.time_limit_minutes = new_limit
            st.success(f"Updated usage limit to {new_limit} minutes!")
    else:
        st.warning("Access Denied. Please enter the correct password.")