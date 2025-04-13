import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    @staticmethod
    async def generate_text(prompt, max_tokens=1000):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"Error generating text: {str(e)}"
    
    @staticmethod
    async def generate_image(prompt, size="512x512"):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=size
            )
            image_url = response['data'][0]['url']
            return image_url
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return None
    
    @staticmethod
    async def generate_code(prompt, language="python"):
        system_message = f"You are an expert {language} programmer. Provide only code without explanation."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"Error generating code: {str(e)}"
