import os
import json
import logging
from google import genai
from google.genai import types

class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self):
        return self.client is not None
    
    def generate_content(self, prompt, model="gemini-2.5-flash"):
        """Generate content using Gemini"""
        if not self.is_available():
            raise Exception("Gemini API key not configured")
        
        if not self.client:
            raise Exception("Gemini client not initialized")
        
        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text or "No response generated"
    
    def summarize_text(self, text):
        """Summarize text using Gemini"""
        prompt = f"Please summarize the following text concisely while maintaining key points:\n\n{text}"
        return self.generate_content(prompt)
    
    def generate_image(self, prompt):
        """Generate image using Gemini"""
        if not self.is_available():
            raise Exception("Gemini API key not configured")
        
        # Create unique filename for generated image
        import uuid
        image_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        image_path = os.path.join("static", "generated_images", image_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        if not self.client:
            raise Exception("Gemini client not initialized")
        
        response = self.client.models.generate_content(
            # IMPORTANT: only this gemini model supports image generation
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        if not response.candidates:
            raise Exception("No image generated")
        
        try:
            content = response.candidates[0].content
            if not content or not content.parts:
                raise Exception("No content in response")
            
            for part in content.parts:
                if part.inline_data and part.inline_data.data:
                    with open(image_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    return {"url": f"/static/generated_images/{image_filename}"}
            
            raise Exception("No image data found in response")
        except Exception as e:
            raise Exception(f"Failed to generate image: {e}")
    
    def explain_code(self, code):
        """Explain code using Gemini"""
        prompt = f"Please explain the following code in detail, including what it does, how it works, and any potential improvements:\n\n```\n{code}\n```"
        return self.generate_content(prompt, model="gemini-2.5-pro")
    
    def review_code(self, code):
        """Review code for issues and improvements"""
        prompt = f"Please review the following code for potential issues, bugs, security vulnerabilities, and suggest improvements:\n\n```\n{code}\n```"
        return self.generate_content(prompt, model="gemini-2.5-pro")
    
    def generate_code(self, description):
        """Generate code based on description"""
        prompt = f"Please generate clean, well-commented code based on this description: {description}"
        return self.generate_content(prompt, model="gemini-2.5-pro")
