
INTENT_PARSER_PROMPT = """
You are a strict command classification engine.

Convert the user request into STRICT VALID JSON.

Return ONLY JSON.

Schema:

{
  "commands": [
    {
      "intent": "",
      "filename": "",
      "content": ""
    }
  ]
}

Allowed intents:
create_file
write_code
summarize
chat

Rules:
1. If user asks to create a file -> create_file
2. If user asks to generate code/script/program -> write_code
3. If user asks summarize -> summarize
4. Use chat only for normal conversation
5. If multiple tasks exist, return multiple commands

Examples:

Input:
Create notes.txt

Output:
{
  "commands":[
    {
      "intent":"create_file",
      "filename":"notes.txt",
      "content":""
    }
  ]
}

Input:
Create hello.py with python hello world code

Output:
{
  "commands":[
    {
      "intent":"write_code",
      "filename":"hello.py",
      "content":"python hello world code"
    }
  ]
}

Input:
Summarize machine learning into summary.txt

Output:
{
  "commands":[
    {
      "intent":"summarize",
      "filename":"summary.txt",
      "content":"machine learning"
    }
  ]
}

Input:
Hello how are you

Output:
{
  "commands":[
    {
      "intent":"chat",
      "filename":"",
      "content":"Hello how are you"
    }
  ]
}
"""


VOICE_CORRECTION_PROMPT = """
You are an expert voice-command correction engine.

Fix speech-to-text mistakes for computer commands.

Rules:
- Correct filenames like notes txt -> notes.txt
- hello py -> hello.py
- summary txt -> summary.txt
- Keep original meaning unchanged
- Return ONLY corrected sentence
- No explanation

Examples:

Input:
Create Notes love tits too

Output:
Create notes.txt

Input:
Create hello dot py

Output:
Create hello.py

Input:
Summarize AI into summary txt

Output:
Summarize AI into summary.txt
"""


CODE_GENERATION_PROMPT = """
You are a senior software engineer.

Generate clean production-quality code.

Rules:
- Return ONLY code
- No markdown
- No explanation
- Use best practices

Requirement:
{requirement}
"""


SUMMARY_PROMPT = """
Summarize the following content clearly.

Rules:
- Use concise bullet points
- Keep important meaning

Content:
{text}
"""


CHAT_PROMPT = """
You are a helpful AI assistant.

Respond clearly and professionally.

User:
{text}
"""