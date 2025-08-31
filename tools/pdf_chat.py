import PyPDF2
import logging
from ai_services.openai_service import OpenAIService
from ai_services.gemini_service import GeminiService
from ai_services.groq_service import GroqService

class PDFChatTool:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_pdf_text(self, file_path):
        """Extract text content from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
                
                return text_content.strip()
        except Exception as e:
            self.logger.error(f"Error extracting PDF text: {e}")
            raise Exception(f"Failed to extract text from PDF: {e}")
    
    def ask_question(self, question, pdf_content, api_keys):
        """Ask a question about the PDF content"""
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
        
        # Truncate PDF content if too long (to avoid token limits)
        max_content_length = 8000  # Adjust based on model limits
        if len(pdf_content) > max_content_length:
            pdf_content = pdf_content[:max_content_length] + "...\n[Content truncated]"
        
        prompt = f"""Based on the following PDF content, please answer the question accurately and comprehensively.

PDF Content:
{pdf_content}

Question: {question}

Please provide a detailed answer based only on the information available in the PDF content. If the information is not available in the PDF, please state that clearly."""

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
            self.logger.error(f"Error generating answer: {e}")
            raise Exception(f"Failed to generate answer: {e}")
