
import streamlit as st
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="EchoVerse - An AudioBook",
    page_icon="🎧",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f0ff, #e8f4ff);
}
h1 {
    color: #493477;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #625778;
    font-size: 17px;
}
.stButton > button {
    background-color: #6547a5;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎧 EchoVerse")
st.markdown(
    '<p class="subtitle">Your words, your world, your audiobook.</p>',
    unsafe_allow_html=True
)

st.write("Transform written text into audio you can listen to anywhere.")

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "Japanese": "ja",
    "German": "de",
    "Telugu": "te",
    "Tamil": "ta"
}

language = st.selectbox(
    "🌍 Choose your language",
    list(languages.keys())
)

tone = st.selectbox(
    "🎭 Choose your reading mood",
    ["Neutral", "Calm", "Excited", "Suspenseful"]
)

st.caption(
    "Calm mode uses slower speech. Other moods are preferences; "
    "gTTS does not provide true emotional voice control."
)

uploaded_file = st.file_uploader(
    "📄 Upload a text file (.txt)",
    type=["txt"]
)

if uploaded_file is not None:
    try:
        uploaded_text = uploaded_file.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        uploaded_text = ""
        st.error("Please upload a UTF-8 encoded text file.")
else:
    uploaded_text = ""

text_input = st.text_area(
    "✍️ Enter your text",
    value=uploaded_text,
    placeholder="Once upon a time...",
    height=220
)

if st.button("✨ Generate Audiobook", use_container_width=True):
    if not text_input.strip():
        st.warning("Please enter text or upload a .txt file.")
    else:
        try:
            with st.spinner("Creating your audiobook..."):
                audio_buffer = BytesIO()

                speech = gTTS(
                    text=text_input.strip(),
                    lang=languages[language],
                    slow=(tone == "Calm")
                )

                speech.write_to_fp(audio_buffer)
                audio_data = audio_buffer.getvalue()

            st.success("Your audiobook is ready!")
            st.audio(audio_data, format="audio/mp3")

            st.download_button(
                "⬇️ Download Audiobook",
                data=audio_data,
                file_name="EchoVerse_Audiobook.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

        except Exception as error:
            st.error("Audio generation failed. Check your internet connection.")
            st.code(str(error))

st.divider()
st.caption("EchoVerse | Turning text into listening experiences 🎶")

            
