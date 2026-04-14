
import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME

from services.stt import transcribe_audio

from services.llm import (
    clean_transcript,
    parse_user_request,
    generate_code,
    summarize_text,
    chat_response
)

from services.tools import execute_tool
from services.memory import load_memory


app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup Check

@app.get("/")
def root():
    return {
        "success": True,
        "message": f"{APP_NAME} Backend Running"
    }



# HISTORY

@app.get("/history")
def history():
    return {
        "success": True,
        "history": load_memory(limit=25)
    }



#  AUDIO PIPELINE

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):

    temp_path = None

    try:

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:

            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        # STEP 1: SPEECH TO TEXT

        transcript = transcribe_audio(temp_path)

        if transcript.startswith("STT Error"):
            return {
                "success": False,
                "error": transcript
            }

        # STEP 2: VOICE CORRECTION

        transcript = clean_transcript(transcript)

        # STEP 3: COMMAND PARSING

        parsed = parse_user_request(transcript)

        commands = parsed.get("commands", [])

        outputs = []

        # STEP 4: EXECUTE COMMANDS

        for command in commands:

            intent = command.get("intent", "chat")
            filename = command.get("filename", "")
            content = command.get("content", "")

            if intent == "write_code":

                generated_code = generate_code(content)

                result = execute_tool(
                    intent="write_code",
                    filename=filename or "generated.py",
                    content=generated_code
                )

            elif intent == "summarize":

                summary = summarize_text(content)

                result = execute_tool(
                    intent="summarize",
                    filename=filename,
                    content=summary
                )

            elif intent == "chat":

                reply = chat_response(content)

                result = execute_tool(
                    intent="chat",
                    content=reply
                )

            else:

                result = execute_tool(
                    intent=intent,
                    filename=filename,
                    content=content
                )

            outputs.append({
                "intent": intent,
                "filename": filename,
                "result": result
            })

        return {
            "success": True,
            "transcript": transcript,
            "commands": commands,
            "outputs": outputs
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
