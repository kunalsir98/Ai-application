import os
import json
from openai import OpenAI

class OpenAIService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self):
        return self.client is not None
    
    def chat_completion(self, messages, model="gpt-5", **kwargs):
        """
        Generate chat completion using OpenAI
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        """
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        if not self.client:
            raise Exception("OpenAI client not initialized")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def summarize_text(self, text):
        """Summarize text using OpenAI"""
        prompt = f"Please summarize the following text concisely while maintaining key points:\n\n{text}"
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages)
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using OpenAI"""
        messages = [
            {
                "role": "system",
                "content": "You are a sentiment analysis expert. "
                + "Analyze the sentiment of the text and provide a rating "
                + "from 1 to 5 stars and a confidence score between 0 and 1. "
                + "Respond with JSON in this format: "
                + "{'rating': number, 'confidence': number}",
            },
            {"role": "user", "content": text},
        ]
        
        if not self.client:
            raise Exception("OpenAI client not initialized")
        
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise Exception("No content in response")
        result = json.loads(content)
        return {
            "rating": max(1, min(5, round(result["rating"]))),
            "confidence": max(0, min(1, result["confidence"])),
        }
    
    def generate_image(self, prompt):
        """Generate image using DALL-E"""
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        if not self.client:
            raise Exception("OpenAI client not initialized")
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        if response.data and len(response.data) > 0:
            return {"url": response.data[0].url}
        else:
            raise Exception("No image data received from OpenAI")
    
    def explain_code(self, code):
        """Explain code using OpenAI"""
        prompt = f"Please explain the following code in detail, including what it does, how it works, and any potential improvements:\n\n```\n{code}\n```"
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages)
    
    def review_code(self, code):
        """Review code for issues and improvements"""
        prompt = f"Please review the following code for potential issues, bugs, security vulnerabilities, and suggest improvements:\n\n```\n{code}\n```"
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages)
    
    def generate_code(self, description):
        """Generate code based on description"""
        prompt = f"Please generate clean, well-commented code based on this description: {description}"
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages)
