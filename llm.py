from groq import Groq
client = Groq()

def get_answer(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful python QA engineer, expert in testing problems independently of its nature."
            },
            {
                "role": "user",
                f"content": prompt,
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    return chat_completion.choices[0].message.content
