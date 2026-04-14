import sys
from pathlib import Path
import os
import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from config import APP_NAME, BACKEND_URL, OUTPUT_DIR

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎙️",
    layout="wide"
)

# CUSTOM UI

st.markdown("""
<style>
.block-container{
    max-width:1200px;
    padding-top:1.2rem;
    padding-bottom:2rem;
}
.stButton > button{
    width:100%;
    height:3rem;
    border-radius:14px;
    font-weight:700;
}
.stDownloadButton > button{
    width:100%;
    border-radius:14px;
}
.big-title{
    font-size:44px;
    font-weight:800;
}
.subtle{
    opacity:0.75;
    margin-bottom:10px;
}
.glass{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.12);
    padding:14px;
    border-radius:18px;
    margin-bottom:12px;
}
.result-card{
    border:1px solid rgba(0,255,0,0.18);
    padding:14px;
    border-radius:16px;
    margin-bottom:10px;
}
.metric-card{
    text-align:center;
    padding:10px;
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.12);
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE

if "mic_audio_bytes" not in st.session_state:
    st.session_state.mic_audio_bytes = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "preview_file" not in st.session_state:
    st.session_state.preview_file = None


# HEADER

st.markdown(
    '<div class="big-title">🎙️ VoicePilot AI Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtle">Voice-Controlled Local AI Assistant</div>',
    unsafe_allow_html=True
)

output_path = ROOT_DIR / OUTPUT_DIR
output_path.mkdir(exist_ok=True)

all_files = sorted(output_path.glob("*"))


# TOP STATS

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📁 Files Created", len(all_files))

with c2:
    history_count = 0
    try:
        hr = requests.get(f"{BACKEND_URL}/history").json()
        history_count = len(hr["history"])
    except:
        pass
    st.metric("⚙️ Commands Run", history_count)

with c3:
    st.metric("🚀 Status", "Ready")


# SIDEBAR HISTORY

st.sidebar.header("📜 Action History")

try:
    history_response = requests.get(f"{BACKEND_URL}/history")
    history_data = history_response.json()

    if history_data["history"]:
        for item in reversed(history_data["history"][-10:]):
            st.sidebar.info(item)
    else:
        st.sidebar.caption("No history yet.")

except:
    st.sidebar.warning("Backend not running.")


# SIDEBAR FILE MANAGER

st.sidebar.divider()
st.sidebar.header("📁 Files Manager")

if all_files:

    for file in all_files:

        st.sidebar.write(f"📄 {file.name}")

        b1, b2 = st.sidebar.columns(2)

        with b1:
            if st.button(
                f"View {file.name}",
                key=f"view_{file.name}"
            ):
                st.session_state.preview_file = file.name

        with b2:
            if st.button(
                f"Delete {file.name}",
                key=f"delete_{file.name}"
            ):
                os.remove(file)
                st.rerun()

else:
    st.sidebar.caption("No files generated yet.")


# AUDIO SOURCE SELECT

st.divider()

left, right = st.columns([3, 1])

with left:
    st.subheader("Choose Input Method")

with right:
    st.success("System Ready")

mode = st.radio(
    "Select audio source:",
    ["Upload Audio", "Use Microphone"],
    horizontal=True
)

audio_bytes = None
audio_name = "audio.wav"


# FILE UPLOAD MODE

if mode == "Upload Audio":

    uploaded_file = st.file_uploader(
        "Upload .wav / .mp3 / .m4a",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file:
        st.audio(uploaded_file)
        audio_bytes = uploaded_file.read()
        audio_name = uploaded_file.name
        st.success("Audio file loaded successfully")


# MICROPHONE MODE

else:

    st.markdown(
        '<div class="glass">🎤 Press start recording, speak clearly, then stop.</div>',
        unsafe_allow_html=True
    )

    mic_audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True
    )

    if mic_audio:
        st.session_state.mic_audio_bytes = mic_audio["bytes"]

    if st.session_state.mic_audio_bytes:
        audio_bytes = st.session_state.mic_audio_bytes
        audio_name = "mic_recording.wav"

        st.audio(audio_bytes)
        st.success("Recording captured successfully")


# EXECUTION

if audio_bytes:

    st.divider()
    st.subheader("Human-in-the-Loop Confirmation")

    confirm = st.checkbox(
        f"Do you want to execute commands extracted from {audio_name}?"
    )

    if confirm:

        if st.button("🚀 Run AI Agent"):

            st.info("🎤 Audio Received")
            st.info("🧠 Transcribing...")
            st.info("🤖 Understanding Intent...")
            st.info("⚙️ Executing Commands...")

            with st.spinner("Processing audio..."):

                files = {
                    "file": (
                        audio_name,
                        audio_bytes,
                        "audio/wav"
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/process-audio",
                    files=files
                )

                data = response.json()

                st.session_state.last_result = data
                st.session_state.mic_audio_bytes = None


# RESULTS

if st.session_state.last_result:

    data = st.session_state.last_result

    if data["success"]:

        st.success("✅ Execution Complete")

        st.divider()

        l1, l2 = st.columns(2)

        with l1:
            st.subheader("📝 Transcript")
            st.write(data["transcript"])

        with l2:
            st.subheader("🤖 Commands")

            for cmd in data["commands"]:
                st.success(
                    f"{cmd['intent']} | "
                    f"{cmd['filename'] if cmd['filename'] else 'No file'}"
                )

        st.subheader("⚙️ Results")

        for item in data["outputs"]:

            st.markdown(
                f"""
                <div class="result-card">
                <b>Intent:</b> {item['intent']}<br>
                <b>File:</b> {item['filename'] if item['filename'] else 'N/A'}<br><br>
                {item['result']}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.error(data["error"])


# FILE PREVIEW (ONLY WHEN NEEDED)

if st.session_state.preview_file:

    st.divider()
    st.subheader("📂 File Preview")

    selected_path = output_path / st.session_state.preview_file

    if selected_path.exists():

        try:
            content = selected_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            st.code(content)

            c1, c2 = st.columns(2)

            with c1:
                with open(selected_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download File",
                        data=f,
                        file_name=selected_path.name
                    )

            with c2:
                if st.button("❌ Close Preview"):
                    st.session_state.preview_file = None
                    st.rerun()

        except:
            st.warning("Unable to preview this file.")
