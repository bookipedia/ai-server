import requests

url = "http://localhost:8000/stream_response_and_sources"

# Parameters
params = {
    "user_prompt": "what is their mathematical basis?",
    "chat_summary": "user discussed positional encodings in transformers",
    "chat": """
    User: Hi! I've been reading about transformers and positional encodings. Can you explain how they work?
    Assistant: Sure! Positional encodings help transformers understand the sequence order of tokens by encoding positional information. They're added directly to the input embeddings using mathematical functions like sine and cosine.
    User: Got it. How does the model learn to interpret these positional encodings?
    Assistant: Through training, the model learns to associate positional encoding patterns with token positions. This helps it understand sequential relationships between tokens better.
    """,
    "book_ids": ['1'],
    "enable_web_retrieval": False
}
params1 = {
    "user_prompt": "what are Tesla's major contributions?",
    "chat_summary": "Nikola Tesla was a Serbian-American inventor, electrical engineer, and futurist. He is known for his contributions.",
    "chat": """
    User: Who is Nikola Tesla?
    Answer: Nikola Tesla was a famous inventor.
    User: What is his nationality?
    Answer: He was a Serbian-American.
    """,
    "enable_web_retrieval": True
}

# Print response content
response = requests.get(url, params=params, stream=True)
for line in response.iter_lines():
    print(line.decode('utf-8'))