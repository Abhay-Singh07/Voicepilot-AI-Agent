# Voicepilot-AI-Agent

This project is a voice-controlled local AI agent built for the Mem0 AI/ML & Generative AI Developer Internship Assignment.

The goal was to create a system that can take voice input, understand the user’s intent, run local tools, and show the full pipeline in a clean UI.

Instead of making only a basic prototype, I tried to make it feel like a real usable product.

---

## 🚀 What It Can Do

The agent accepts input through:

* 🎤 Direct microphone recording
* 📁 Audio file upload (`.wav`, `.mp3`, `.m4a`)

It then performs:

* 📝 Speech-to-text transcription
* 🧠 Intent detection using LLM
* ⚙️ Local tool execution
* 📊 Result display in UI

Supported intents:

* Create a file
* Write code into a file
* Summarize text
* General chat

---

## 💡 Example Commands

* “Create notes.txt”
* “Create hello.py with retry function”
* “Summarize artificial intelligence into summary.txt”
* “What is machine learning?”

---

## 🛠 Tech Stack

Frontend:

* Streamlit

Backend:

* FastAPI

Models:

* Whisper (local STT)
* Groq LLM API for intent parsing + code generation

Language:

* Python

---

## 🧱 Project Structure

```text
backend/
frontend/
services/
output/
history/
config.py
requirements.txt
```

---

## 🔄 System Flow

1. User records/upload audio
2. Audio converted to text using Whisper
3. Transcript cleaned for filename / command errors
4. LLM classifies intent
5. Tool executes inside safe `output/` folder
6. UI shows transcript, commands, actions, results

---

## ✨ Bonus Features Implemented

* ✅ Compound command support
* ✅ Human-in-the-loop confirmation before execution
* ✅ Persistent action history
* ✅ Error handling / graceful degradation
* ✅ File viewer / delete / download options
* ✅ Improved polished UI

---

## ⚠️ Challenges Faced

### 1. Speech recognition on filenames

Commands like `notes.txt` often transcribed incorrectly.

Solution:
Added a transcript correction layer before intent parsing.

### 2. GPU instability with Whisper

On local GPU, inference caused NaN errors.

Solution:
Used CPU inference for stable execution.

### 3. Session state issues in Streamlit

Old mic recordings persisted across reruns.

Solution:
Managed session state carefully.


---

## 🔮 Future Improvements

* Fully local LLM with Ollama
* Better multi-step memory
* Smarter tool routing
* Voice reply output (TTS)
* Better desktop packaging

---
