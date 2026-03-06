from google import genai
import os

def make_gemini_api_call(api_key, prompt_content):
    
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_content
        )
        
        return response.text
    except Exception as e:
        return f"An API error occurred: {e}"

if __name__ == "__main__":
    
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE") 
    
    if not api_key:
        print("Error: The GEMINI_API_KEY environment variable is not set.")
        print("Please set the environment variable with your API key.")
    else:
        user_prompt = "Tell me a fun fact about large language models."
        print(f"Sending prompt: '{user_prompt}'")
        gemini_response = make_gemini_api_call(api_key, user_prompt)
        print("\nGemini's response:")
        print(gemini_response)
