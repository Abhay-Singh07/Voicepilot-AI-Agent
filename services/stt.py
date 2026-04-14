import whisper
import torch

DEVICE = "cpu"

model = whisper.load_model("tiny", device=DEVICE)


def transcribe_audio(file_path: str) -> str:
    try:
        result = model.transcribe(
            file_path,
            fp16=False
        )

        return result["text"].strip()

    except Exception as e:
        print(e)
        return f"STT Error: {str(e)}"