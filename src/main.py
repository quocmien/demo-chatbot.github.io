# call api openai from chatbot messenger


import openai
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")


# Define your prompt for the OpenAI API
prompt = input("Enter your prompt: ")

# Call the OpenAI API to generate a response
response = openai.Completion.create(
  engine='text-davinci-003', 
  prompt=prompt, 
  max_tokens=100
)

# Retrieve the generated response and print it
message = response.choices[0].text.strip()
print(message)