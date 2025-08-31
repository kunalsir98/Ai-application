import logging
import os
from ai_services.openai_service import OpenAIService
from ai_services.gemini_service import GeminiService

class ImageGenerationTool:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Ensure generated images directory exists
        os.makedirs("static/generated_images", exist_ok=True)
    
    def generate_image(self, prompt, api_keys, provider_preference=None):
        """Generate image using available AI services"""
        
        # Determine which service to use
        service = None
        service_name = ""
        
        if provider_preference == "openai" and 'openai' in api_keys:
            service = OpenAIService(api_keys['openai'])
            service_name = "OpenAI DALL-E"
        elif provider_preference == "gemini" and 'gemini' in api_keys:
            service = GeminiService(api_keys['gemini'])
            service_name = "Google Gemini"
        else:
            # Auto-select available service
            if 'openai' in api_keys:
                service = OpenAIService(api_keys['openai'])
                service_name = "OpenAI DALL-E"
            elif 'gemini' in api_keys:
                service = GeminiService(api_keys['gemini'])
                service_name = "Google Gemini"
        
        if not service:
            raise Exception("No image generation service available. Please configure OpenAI or Gemini API keys.")
        
        try:
            result = service.generate_image(prompt)
            result['provider'] = service_name
            return result
        except Exception as e:
            self.logger.error(f"Error generating image with {service_name}: {e}")
            raise Exception(f"Failed to generate image: {e}")
    
    def get_supported_providers(self, api_keys):
        """Get list of supported image generation providers"""
        providers = []
        
        if 'openai' in api_keys:
            providers.append({
                'id': 'openai',
                'name': 'OpenAI DALL-E',
                'description': 'High-quality realistic and artistic images'
            })
        
        if 'gemini' in api_keys:
            providers.append({
                'id': 'gemini',
                'name': 'Google Gemini',
                'description': 'AI-powered image generation'
            })
        
        return providers
