
import streamlit as st
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="EchoVerse — A Little Space for Stories",
    page_icon="🎧",
    layout="centered"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #51415e;
    --muted: #897b94;
    --purple: #80638f;
    --purple-dark: #684d79;
    --lavender: #f0e9f7;
    --border: #e7ddec;
}

/* Soft, barely-there lavender with hazy corners */
.stApp {
    background:
        radial-gradient(ellipse at 0% 0%,
            rgba(202, 174, 226, 0.30), transparent 32%),
        radial-gradient(ellipse at 100% 100%,
            rgba(211, 190, 235, 0.32), transparent 34%),
        radial-gradient(ellipse at 100% 0%,
            rgba(226, 211, 241, 0.20), transparent 25%),
        #faf8fc;
    color: var(--ink);
    font-family: 'Nunito', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.block-container {
    max-width: 820px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Brand */
.brand {
    font-size: 56px;
    font-weight: 900;
    color: #59417f;
    line-height: 1.1;
    letter-spacing: -2px;
    text-align: center;
}

.brand-note {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* Welcome section */
.welcome {
    padding: 3.2rem 0 2.2rem 0;
}

.eyebrow {
    color: #967da5;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    color: #51405e;
    font-size: clamp(2.1rem, 5vw, 3.3rem);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin: 0 0 1rem 0;
}

.hero-description {
    color: #82738d;
    font-size: 1.05rem;
    line-height: 1.8;
    max-width: 560px;
}

/* Section headings */
.section-heading {
    color: #5b4768;
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}

.section-note {
    color: #95879d;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Input area */
.stTextArea textarea {
    background: rgba(244, 238, 249, 0.90) !important;
    color: #51415e !important;
    border: 1px solid #e5d9ed !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.8 !important;
    box-shadow: none !important;
}

.stTextArea textarea:focus {
    border-color: #b9a0cc !important;
    box-shadow: 0 0 0 2px rgba(185, 160, 204, 0.14) !important;
}

.stTextArea textarea::placeholder {
    color: #a99bb2 !important;
}

/* Labels and dropdowns */
label, .stSelectbox label, .stFileUploader label {
    color: #655270 !important;
    font-weight: 700 !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background: #fff !important;
    border-color: #e5d9ed !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: #80638f !important;
    color: white !important;
    border: 1px solid #80638f !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.2rem !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    transition: background 0.2s ease, transform 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #684d79 !important;
    border-color: #684d79 !important;
    transform: translateY(-1px);
}

/* File upload */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.55);
    border: 1px dashed #d5c4e1;
    border-radius: 14px;
    padding: 12px;
}

/* Audio player */
audio {
    width: 100%;
    border-radius: 12px;
}

/* Quiet footer */
.footer {
    color: #a092aa;
    text-align: center;
    font-size: 0.82rem;
    padding-top: 2rem;
}

hr {
    border-color: #e9e0ef !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------

st.markdown("""
<div class="brand">echoverse<span style="color:#b69ac8">.</span></div>
<div class="brand-note">a little space for stories</div>

<div class="welcome">
    <div class="eyebrow">Your own little reading nook</div>
    <div class="hero-title">Some stories deserve<br>to be heard.</div>
    <div class="hero-description">
        Bring your favourite words, settle in, and let EchoVerse
        read them to you. A quiet little space to turn reading
        into listening.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- TEXT INPUT --------------------

st.markdown(
    '<div class="section-heading">What shall we listen to today?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-note">A passage, a favourite quote, or a story you love.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Bring your own text",
    type=["txt"],
    help="Upload a plain text (.txt) file."
)

uploaded_text = ""

if uploaded_file is not None:
    try:
        uploaded_text = uploaded_file.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        st.error("Please upload a UTF-8 encoded text file.")

text_input = st.text_area(
    "Your story",
    value=uploaded_text,
    placeholder="Once upon a time... paste your words here.",
    height=220,
    label_visibility="collapsed"
)

# -------------------- VOICE SETTINGS --------------------

with st.expander("Voice and language settings", expanded=True):
    languages = {
        "English": "en",
        "Hindi": "hi",
        
    }

    language = st.selectbox(
        "Choose a language",
        list(languages.keys())
    )

    tone = st.selectbox(
        "Choose a reading pace",
        ["Neutral", "Calm", "Excited", "Suspenseful"]
    )

    
# -------------------- GENERATE AUDIO --------------------


# -------------------- GENERATE AUDIO --------------------

st.write("")


# -------------------- GENERATE AUDIO --------------------

if st.button("✨ Generate Audiobook", use_container_width=True):
    if not text_input.strip():
        st.warning("Please enter text or upload a .txt file.")

    else:
        target_language = languages[language]
        original_text = text_input.strip()

        # Step 1: Translate only when Hindi is selected
        try:
            with st.spinner("Preparing your story..."):
                if target_language == "hi":
                    translated_text = GoogleTranslator(
                        source="auto",
                        target="hi"
                    ).translate(original_text)
                else:
                    translated_text = original_text

            if not translated_text:
                st.error("Translation returned no text. Please try again.")
                st.stop()

        except Exception as error:
            st.error("We couldn't translate your story.")
            st.caption(f"Translation error: {error}")
            st.stop()

        # Step 2: Generate audio in the selected language
        try:
            with st.spinner("Creating your audiobook..."):
                audio_buffer = BytesIO()

                speech = gTTS(
                    text=translated_text,
                    lang=target_language,
                    slow=(tone == "Calm")
                )

                speech.write_to_fp(audio_buffer)
                audio_data = audio_buffer.getvalue()

            st.success("Your audiobook is ready!")
            st.audio(audio_data, format="audio/mp3")

            st.download_button(
                "⬇️ Download Audiobook",
                data=audio_data,
                file_name=f"EchoVerse_{language}_Audiobook.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

        except Exception as error:
            st.error("We couldn't generate the audio.")
            st.caption(f"Audio error: {error}")


# -------------------- FOOTER --------------------

st.markdown("""
<div class="footer">
    made for the love of stories · echoverse ♡
</div>
""", unsafe_allow_html=True)
