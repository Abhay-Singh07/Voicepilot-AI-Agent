import os
from config import OUTPUT_DIR
from services.memory import save_memory



def ensure_output_dir():
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)



def safe_filename(filename: str) -> str:
    
    if not filename:
        filename = "untitled.txt"

    return os.path.basename(filename.strip())


def get_output_path(filename: str) -> str:
    
    ensure_output_dir()

    clean_name = safe_filename(filename)

    return os.path.join(OUTPUT_DIR, clean_name)


# FILE TOOLS

def create_file(filename: str) -> str:
    
    clean_name = safe_filename(filename)
    path = get_output_path(clean_name)

    with open(path, "w", encoding="utf-8") as f:
        pass

    save_memory(f"create_file | {clean_name}")

    return f"Created file: {clean_name}"


def write_file(filename: str, content: str) -> str:
    
    clean_name = safe_filename(filename)
    path = get_output_path(clean_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    save_memory(f"write_file | {clean_name}")

    return f"Written content to: {clean_name}"


def append_file(filename: str, content: str) -> str:
    
    clean_name = safe_filename(filename)
    path = get_output_path(clean_name)

    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

    save_memory(f"append_file | {clean_name}")

    return f"Appended content to: {clean_name}"


def read_file(filename: str) -> str:
    
    clean_name = safe_filename(filename)
    path = get_output_path(clean_name)

    if not os.path.exists(path):
        return "File does not exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    save_memory(f"read_file | {clean_name}")

    return content


def file_exists(filename: str) -> bool:
    
    clean_name = safe_filename(filename)
    path = get_output_path(clean_name)

    return os.path.exists(path)


def list_output_files():
    
    ensure_output_dir()

    return os.listdir(OUTPUT_DIR)



# EXECUTION


def execute_tool(intent: str, filename: str = "", content: str = ""):
    """
    Main action router.
    """

    if intent == "create_file":
        return create_file(filename)

    elif intent == "write_code":
        return write_file(filename, content)

    elif intent == "summarize":
        if filename:
            return write_file(filename, content)
        return content

    elif intent == "chat":
        save_memory("chat_response")
        return content

    else:
        save_memory(f"unknown_intent | {intent}")
        return "Unknown intent."