import openai
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Retrieve the API key securely
api_key = os.getenv("OPENAI_API_KEY")

#Create an OpenAI client
client = openai.OpenAI(api_key=api_key)


#Example API call using GPT-4
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)


#Print response
print(response.choices[0].message.content)

