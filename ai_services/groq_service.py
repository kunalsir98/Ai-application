import os
import json
import requests

class GroqService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
    
    def is_available(self):
        return self.api_key is not None
    
    def chat_completion(self, messages, model="llama-3.3-70b-versatile", **kwargs):
        """Generate chat completion using Groq"""
        if not self.is_available():
            raise Exception("Groq API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def summarize_text(self, text):
        """Summarize text using Groq"""
        prompt = f"Please summarize the following text concisely while maintaining key points:\n\n{text}"
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages)
    
    def explain_code(self, code):
        """Explain code using Groq"""
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
