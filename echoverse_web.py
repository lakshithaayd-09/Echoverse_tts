import streamlit as st
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
import uuid


# ---------------- CSS Styling ----------------

st.markdown("""
<style>

:root{
  --bg:#0f172a;
  --bg2:#111827;
  --muted:#94a3b8;
  --text:#e5e7eb;
  --brand1:#8b5cf6;
  --brand2:#22d3ee;
  --shadow:0 10px 30px rgba(0,0,0,.35);
}


body, .stApp {

background:
radial-gradient(1200px 600px at 10% -10%,rgba(34,211,238,.15),transparent 60%),
radial-gradient(1000px 500px at 110% -20%,rgba(139,92,246,.18),transparent 55%),
linear-gradient(180deg,var(--bg),var(--bg2));

color:var(--text);
font-family:"Segoe UI",sans-serif;

}


header{
visibility:hidden;
}


.block-container{

padding-top:4rem;
padding-bottom:2rem;
max-width:900px;

}


/* Title */

.site-title{

text-align:center;

font-size:clamp(40px,6vw,64px);

font-weight:900;

font-style:italic;

background:
linear-gradient(90deg,var(--brand2),var(--brand1));

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

text-shadow:
0 0 30px rgba(139,92,246,.25);

margin-top:20px;

margin-bottom:15px;

}


/* Intro */

.intro{

text-align:center;

color:var(--muted);

font-size:18px;

margin-bottom:35px;

}


/* Buttons */

.stButton>button,
.stDownloadButton>button{

background:
linear-gradient(90deg,var(--brand2),var(--brand1));

color:#0b1021;

border:none;

border-radius:999px;

padding:12px 20px;

font-weight:600;

box-shadow:var(--shadow);

}


.stButton>button:hover,
.stDownloadButton>button:hover{

transform:translateY(-2px);

}


audio{

width:100%;

margin-top:15px;

}


.footer{

margin-top:50px;

text-align:center;

color:var(--muted);

}

</style>

""", unsafe_allow_html=True)



# ---------------- Header ----------------

st.markdown(
    "<h1 class='site-title'>Echo Verse</h1>",
    unsafe_allow_html=True
)


st.markdown(
"""
<p class='intro'>
Your personalized audiobook experience.
Convert stories into immersive audio.
</p>
""",
unsafe_allow_html=True
)



# ---------------- Input Section ----------------
# ---------------- Input Section ----------------

mode = st.radio(
    "Choose Input Mode:",
    [
        "Add Some Text",
        "Browse Library"
    ]
)


text = ""


if mode == "Add Some Text":

    text = st.text_area(
        "Enter text to convert into speech:",
        height=200
    )


elif mode == "Browse Library":

    uploaded_file = st.file_uploader(
        "Upload TXT file",
        type=["txt"]
    )


    if uploaded_file:

        text = uploaded_file.read().decode("utf-8")

        st.subheader("📄 Extracted Text Preview")

        st.write(
            text[:1000] + "..."
            if len(text) > 1000
            else text
        )

# ---------------- Language Settings ----------------

language_options = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja"
}


selected_language = st.selectbox(
    "🌐 Choose Language",
    list(language_options.keys())
)


language = language_options[selected_language]





# ---------------- Generate Audio ----------------

if st.button("🎧 GENERATE AUDIO"):


    if not text.strip():

        st.error("Please enter or upload some text.")


    else:

        with st.spinner("Translating and generating audiobook..."):


            translated_text = GoogleTranslator(
                source="auto",
                target=language
            ).translate(text)



            output_file = f"echoverse_{uuid.uuid4().hex}.mp3"


            tts = gTTS(
                text=translated_text,
                lang=language
            )


            tts.save(output_file)

   


        st.success(
            "Audio generated successfully!"
        )


        st.audio(
            output_file,
            format="audio/mp3"
        )


        with open(output_file,"rb") as f:

            st.download_button(
                "⬇ Download Audio",
                f,
                file_name="echoverse_audio.mp3",
                mime="audio/mp3"
            )
