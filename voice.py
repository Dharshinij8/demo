import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
from PIL import Image
import cv2
import numpy as np
import qrcode
import io

st.set_page_config(page_title="Chatbot + QR Scanner", layout="centered")
st.markdown(
    """
    <style>
    .glow-icon {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: url('https://cdn-icons-png.flaticon.com/512/4712/4712039.png') no-repeat center/cover;
        box-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc, 0 0 40px #00ffcc;
        animation: pulse 2s infinite;
        margin: auto;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 20px #00ffcc; }
        50% { box-shadow: 0 0 40px #00ffcc; }
        100% { box-shadow: 0 0 20px #00ffcc; }
    }
    </style>
    <div class="glow-icon"></div>
    """,
    unsafe_allow_html=True
)
st.title("🤖 Chatbot + 📷 QR Code Scanner")

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Wikipedia Chatbot", "📷 QR Code Scanner", "ℹ️ About Us"])

# --- TAB 1: Wikipedia Chatbot ---
with tab1:
    st.subheader("Ask anything. Type or speak!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def get_wikipedia_summary(query):
        try:
            results = wikipedia.search(query)
            if not results:
                return "❌ Sorry, no results found."
            summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)
            return summary
        except wikipedia.DisambiguationError as e:
            return f"⚠️ Too broad. Did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.PageError:
            return "❌ Page not found."
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    user_input_text = st.text_input("Type your question here:")

    audio_file = st.file_uploader("🎤 Or upload your voice question (WAV format)", type=["wav"])

    if audio_file is not None:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_filename = tmp_file.name

        with sr.AudioFile(tmp_filename) as source:
            audio_data = recognizer.record(source)
            try:
                recognized_text = recognizer.recognize_google(audio_data)
                st.success(f"You said: {recognized_text}")
                user_input_text = recognized_text
            except sr.UnknownValueError:
                st.error("Sorry, could not understand your voice.")
            except sr.RequestError:
                st.error("Could not connect to speech recognition service.")

        os.remove(tmp_filename)

    user_input = user_input_text.strip() if user_input_text else ""

    if user_input:
        if user_input.lower() == "hi":
            response = "Hello!"
        elif user_input.lower() == "what is your name":
            response = "I'm a chatbot."
        else:
            response = get_wikipedia_summary(user_input)

        st.session_state.chat_history.append((user_input, response))

    if st.session_state.chat_history:
        st.markdown("### 💬 Chat History")
        for idx, (user, bot) in enumerate(reversed(st.session_state.chat_history), 1):
            st.markdown(f"**🧑 You {idx}:** {user}")
            st.markdown(f"**🤖 Bot {idx}:** {bot}")
            st.markdown("---")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history.clear()
            st.success("Chat history cleared!")


# URL of image or video
url = "https://example.com/myimage.jpg"  # Replace with your actual URL

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')

# Convert to bytes for display in Streamlit
buf = io.BytesIO()
img.save(buf)
buf.seek(0)

# Show QR code in Streamlit
st.image(buf, caption="Scan to view image/video")

# Optionally, show the image/video itself embedded below
st.markdown(f"[Click here to view image/video]({url})")


# --- TAB 3: About Us ---
with tab3:
    st.subheader("About Us")
    st.markdown("""
    ### Welcome to Chatbot + QR Scanner!

    This app combines two handy tools into one interface:

    - 🤖 **Wikipedia Chatbot**: Ask questions by typing or uploading your voice! Powered by Wikipedia API and speech recognition.
    - 📷 **QR Code Scanner**: Upload images containing QR codes and get the decoded information instantly.

    ---
    **Developed by:**  
    AKSHAYA V, DHARSHINI J, HARSHITHA B.M, SRIMATHI K

    **Contact:**  
    - Email: dharshudharshu148@gmail.com, acquireness@gmail.com  

    ---
    Thank you for using our app! Feel free to contribute or suggest features.
    """)

    # Removed website and project link section

    st.subheader("🖼️ Snapshots of the Project")

    SNAPSHOT_DIR = "snapshots"
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    uploaded_files = st.file_uploader("Upload snapshots (multiple allowed)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(SNAPSHOT_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success("✅ Files uploaded successfully!")

    saved_files = os.listdir(SNAPSHOT_DIR)
    if saved_files:
        st.markdown("### Saved Snapshots:")
        for fname in saved_files:
            fpath = os.path.join(SNAPSHOT_DIR, fname)
            st.image(fpath, use_column_width=True)
    else:
        st.info("No snapshots uploaded yet.")

