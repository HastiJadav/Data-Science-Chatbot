import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import base64
import pandas as pd  # Import pandas
from PIL import Image  # Import Image from PIL (Python Imaging Library)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ API Key is missing. Please add it to the .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Data Science Chatbot 💬", layout="centered")
st.title("🧠 Let's Decode Data Together 📚")

# Sidebar
with st.sidebar:
    st.title("📚 Data Science Chatbot")
    st.markdown("""
        Ask me anything related to:
        - Python 🐍
        - SQL 🧮
        - Machine Learning 🤖
        - Deep Learning 🧠🕸️
        - Statistics 📊
        - Power BI / Tableau 📈
        - EDA / Data Cleaning 🧹

        Made by **Hasti Jadav**
    """)
    st.info("💡 Try asking: *'Explain Random Forest simply'*")

st.markdown("---")  # horizontal line



# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable and friendly Data Science tutor. You help students understand topics like Python, SQL, Machine Learning, Statistics, and Data Visualization with clear and simple explanations."
        }
    ]

# Displays a welcome message from the chatbot (assistant) to the user.
with st.chat_message("assistant"):
    st.markdown("👋 Hey there! Ready to dive into the world of data science? I’m here to help you decode the data, one insight at a time. 🧠💬")


# Display Previous Messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")
# st.chat_input: Displays a text box for the user to type their message.


if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
# If the user enters a message, it is displayed as a "user" message, and the message is stored in the session state for further conversation.

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
# Retrieves the response from the Groq API and displays it as an "assistant" message. Adds the assistant's response to the conversation history

    except Exception as e:
        st.error(f"Something went wrong: {e}")
# If there's an error (e.g., network issue or API error), an error message is shown to the user.


# Download Conversation
if st.session_state.get("messages") and len(st.session_state.messages) > 1:
    st.markdown("---")
    st.markdown("### 📥 Download Your Chat Conversation")

    formatted_conversation = "\n\n".join(
        f"{'👤 You' if msg['role'] == 'user' else '🤖 Assistant'}:\n{msg['content']}"
        for msg in st.session_state.messages[1:]
    )

    st.download_button(
        label="⬇️ Download Conversation",
        data=formatted_conversation.encode("utf-8"),
        file_name="data_science_chat.txt",
        mime="text/plain"
    )


if len(st.session_state.messages) == 1:
    st.markdown("## Hello Hasti 👋")
#     # st.write("This is your Streamlit chatbot interface test!")

# File Upload section
uploaded_file = st.file_uploader("📁 Upload a file or image", type=["csv", "xlsx", "png", "jpg", "jpeg"])

# Handle file upload
if uploaded_file is not None:
    file_type = uploaded_file.type

    # If it's an image
    if file_type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_column_width=True)
        st.chat_message("assistant").markdown(
            "🖼️ I've received an image. Since I'm text-based, I can't analyze it directly, but you can describe it, and I'll assist you based on that description!"
        )

    # If it's a CSV file
    elif file_type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write("📊 Preview of your CSV data:")
        st.dataframe(df.head())
        st.chat_message("assistant").markdown(
            "✅ I've received your CSV file. Let me know what you'd like to explore or analyze!"
        )

    # If it's an Excel file
    elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        st.write("📊 Preview of your Excel data:")
        st.dataframe(df.head())
        st.chat_message("assistant").markdown(
            "✅ I've received your Excel file. How would you like me to assist with it?"
        )

    # If file type is not recognized
    else:
        st.warning("⚠️ Uploaded file type is not supported for preview.")




# cmd type streamlit run app.py
