import openai
from ..core.config import settings
import logging
import requests
from io import BytesIO

logger = logging.getLogger(__name__)

openai.api_key = settings.GPT_API_KEY

def generate_content(prompt: str = None) -> str:
    try:
        if not prompt:
            prompt = "Generate an engaging post about cryptocurrency or blockchain technology. Include relevant hashtags."
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cryptocurrency content creator. Create engaging and informative posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return ""

def generate_image(prompt: str) -> bytes:
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        
        # Download the image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        return image_response.content
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return b"" 