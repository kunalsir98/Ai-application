import logging
from ai_services.openai_service import OpenAIService
from ai_services.gemini_service import GeminiService
from ai_services.groq_service import GroqService

class CodeAssistantTool:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def explain_code(self, code, api_keys):
        """Explain code using available AI services"""
        service = self._get_best_service(api_keys)
        
        try:
            return service.explain_code(code)
        except Exception as e:
            self.logger.error(f"Error explaining code: {e}")
            raise Exception(f"Failed to explain code: {e}")
    
    def review_code(self, code, api_keys):
        """Review code for issues and improvements"""
        service = self._get_best_service(api_keys)
        
        try:
            return service.review_code(code)
        except Exception as e:
            self.logger.error(f"Error reviewing code: {e}")
            raise Exception(f"Failed to review code: {e}")
    
    def generate_code(self, description, api_keys, language=None):
        """Generate code based on description"""
        service = self._get_best_service(api_keys)
        
        # Add language specification to description if provided
        if language:
            description = f"Generate {language} code: {description}"
        
        try:
            return service.generate_code(description)
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            raise Exception(f"Failed to generate code: {e}")
    
    def optimize_code(self, code, api_keys):
        """Optimize code for better performance"""
        service = self._get_best_service(api_keys)
        
        prompt = f"Please optimize the following code for better performance, readability, and maintainability:\n\n```\n{code}\n```"
        
        try:
            if isinstance(service, OpenAIService):
                messages = [{"role": "user", "content": prompt}]
                return service.chat_completion(messages)
            elif isinstance(service, GeminiService):
                return service.generate_content(prompt)
            elif isinstance(service, GroqService):
                messages = [{"role": "user", "content": prompt}]
                return service.chat_completion(messages)
        except Exception as e:
            self.logger.error(f"Error optimizing code: {e}")
            raise Exception(f"Failed to optimize code: {e}")
    
    def _get_best_service(self, api_keys):
        """Get the best available AI service for code tasks"""
        # Prefer services in order of coding capability
        if 'openai' in api_keys:
            return OpenAIService(api_keys['openai'])
        elif 'groq' in api_keys:
            return GroqService(api_keys['groq'])
        elif 'gemini' in api_keys:
            return GeminiService(api_keys['gemini'])
        else:
            raise Exception("No AI service available. Please configure API keys.")
    
    def get_supported_languages(self):
        """Get list of supported programming languages"""
        return [
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'C',
            'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala',
            'HTML', 'CSS', 'SQL', 'Shell/Bash', 'PowerShell'
        ]
