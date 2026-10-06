import ollama


response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Give me one simple photography tip."
        }
    ]
)


print("\nAI RESPONSE:")
print(response["message"]["content"])