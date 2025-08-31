import logging
from ai_services.openai_service import OpenAIService
from ai_services.gemini_service import GeminiService
from ai_services.groq_service import GroqService

class SummarizationTool:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def summarize_text(self, text, api_keys, summary_type="standard"):
        """Summarize text using available AI services"""
        # Try different AI services based on available API keys
        services = []
        
        if 'openai' in api_keys:
            services.append(OpenAIService(api_keys['openai']))
        if 'gemini' in api_keys:
            services.append(GeminiService(api_keys['gemini']))
        if 'groq' in api_keys:
            services.append(GroqService(api_keys['groq']))
        
        if not services:
            raise Exception("No AI service available. Please configure API keys.")
        
        # Use the first available service
        service = services[0]
        
        # Adjust prompt based on summary type
        if summary_type == "bullet":
            prompt_addon = " Provide the summary in bullet points."
        elif summary_type == "brief":
            prompt_addon = " Provide a very brief summary in 2-3 sentences."
        elif summary_type == "detailed":
            prompt_addon = " Provide a detailed summary with key insights and analysis."
        else:
            prompt_addon = ""
        
        # Truncate text if too long
        max_text_length = 10000
        if len(text) > max_text_length:
            text = text[:max_text_length] + "...\n[Text truncated]"
        
        prompt = f"Please summarize the following text concisely while maintaining key points{prompt_addon}:\n\n{text}"
        
        try:
            if isinstance(service, OpenAIService):
                return service.summarize_text(text)
            elif isinstance(service, GeminiService):
                return service.summarize_text(text)
            elif isinstance(service, GroqService):
                return service.summarize_text(text)
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            raise Exception(f"Failed to generate summary: {e}")
    
    def analyze_sentiment(self, text, api_keys):
        """Analyze sentiment of the text"""
        if 'openai' in api_keys:
            service = OpenAIService(api_keys['openai'])
            try:
                return service.analyze_sentiment(text)
            except Exception as e:
                self.logger.error(f"Error analyzing sentiment: {e}")
                raise Exception(f"Failed to analyze sentiment: {e}")
        else:
            raise Exception("Sentiment analysis requires OpenAI API key.")
