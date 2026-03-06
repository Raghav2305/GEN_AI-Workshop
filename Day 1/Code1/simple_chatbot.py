from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY_HERE")


def create_chatbot(personality):
    """Create a chatbot with specific personality"""
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction=f"You are a {personality} assistant. Keep responses concise and friendly. If you don't know the answer, say 'I don't know'. If the question is not related to {personality}, politely decline to answer.",
            temperature=0.9
        )
    )
    return chat

# Use it
support_bot = create_chatbot("customer support for computer science")

print("Customer Support Bot started strictly computer science. Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    
    response = support_bot.send_message(user_input)
    print(f"Bot: {response.text}\n")