import os
import logging
from flask import render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from extensions import db

# Initialize tools (import inside function to avoid circular imports)
def get_tools():
    from tools.pdf_chat import PDFChatTool
    from tools.summarization import SummarizationTool
    from tools.image_generation import ImageGenerationTool
    from tools.code_assistant import CodeAssistantTool
    
    return {
        'pdf_chat': PDFChatTool(),
        'summarization': SummarizationTool(),
        'image_generation': ImageGenerationTool(),
        'code_assistant': CodeAssistantTool()
    }

def register_routes(app):
    # Import models inside functions to avoid circular imports
    def get_models():
        from models import User, APIKey, ChatSession, ChatMessage, UploadedFile
        return User, APIKey, ChatSession, ChatMessage, UploadedFile

    @app.route('/')
    def index():
        """Landing page"""
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        """Main dashboard"""
        # For demo purposes, we'll use a session-based user system
        user_id = session.get('user_id', 1)
        
        # Import models inside function
        _, APIKey, ChatSession, _, _ = get_models()
        
        # Get user's API keys
        api_keys = APIKey.query.filter_by(user_id=user_id, is_active=True).all()
        
        # Get recent chat sessions
        recent_sessions = ChatSession.query.filter_by(user_id=user_id).order_by(ChatSession.created_at.desc()).limit(5).all()
        
        return render_template('dashboard.html', api_keys=api_keys, recent_sessions=recent_sessions)

    @app.route('/api-keys', methods=['GET', 'POST'])
    def api_keys():
        """API key management"""
        user_id = session.get('user_id', 1)
        
        # Import models inside function
        _, APIKey, _, _, _ = get_models()
        
        if request.method == 'POST':
            provider = request.form.get('provider')
            key_value = request.form.get('key_value')
            
            if provider and key_value:
                # Deactivate existing key for this provider
                existing_key = APIKey.query.filter_by(user_id=user_id, provider=provider, is_active=True).first()
                if existing_key:
                    existing_key.is_active = False
                
                # Add new key
                new_key = APIKey()
                new_key.user_id = user_id
                new_key.provider = provider
                new_key.key_value = key_value
                new_key.is_active = True
                db.session.add(new_key)
                db.session.commit()
                
                flash(f'{provider.title()} API key updated successfully!', 'success')
            else:
                flash('Please provide both provider and API key.', 'error')
            
            return redirect(url_for('api_keys'))
        
        # Get current API keys
        api_keys = APIKey.query.filter_by(user_id=user_id, is_active=True).all()
        return render_template('api_keys.html', api_keys=api_keys)

    @app.route('/pdf-chat', methods=['GET', 'POST'])
    def pdf_chat():
        """Chat with PDF functionality"""
        user_id = session.get('user_id', 1)
        
        # Import models inside function
        _, _, _, _, UploadedFile = get_models()
        tools = get_tools()
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'upload':
                if 'file' not in request.files:
                    return jsonify({'error': 'No file provided'}), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400
                
                if file and file.filename and file.filename.lower().endswith('.pdf'):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Save file info to database
                    uploaded_file = UploadedFile()
                    uploaded_file.user_id = user_id
                    uploaded_file.filename = filename
                    uploaded_file.file_path = file_path
                    uploaded_file.file_type = 'pdf'
                    uploaded_file.file_size = os.path.getsize(file_path)
                    db.session.add(uploaded_file)
                    db.session.commit()
                    
                    # Extract text from PDF
                    try:
                        text_content = tools['pdf_chat'].extract_pdf_text(file_path)
                        session['pdf_content'] = text_content
                        session['pdf_filename'] = filename
                        return jsonify({'success': True, 'filename': filename})
                    except Exception as e:
                        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 400
                else:
                    return jsonify({'error': 'Please upload a PDF file'}), 400
            
            elif action == 'chat':
                question = request.form.get('question')
                if not question:
                    return jsonify({'error': 'No question provided'}), 400
                
                pdf_content = session.get('pdf_content')
                if not pdf_content:
                    return jsonify({'error': 'Please upload a PDF first'}), 400
                
                try:
                    # Get user's API keys
                    api_keys = get_user_api_keys(user_id)
                    answer = tools['pdf_chat'].ask_question(question, pdf_content, api_keys)
                    return jsonify({'answer': answer})
                except Exception as e:
                    return jsonify({'error': f'Error generating answer: {str(e)}'}), 400
        
        return render_template('pdf_chat.html')

    @app.route('/summarization', methods=['GET', 'POST'])
    def summarization():
        """Text summarization tool"""
        user_id = session.get('user_id', 1)
        tools = get_tools()
        
        if request.method == 'POST':
            text = request.form.get('text')
            if not text:
                return jsonify({'error': 'No text provided'}), 400
            
            try:
                api_keys = get_user_api_keys(user_id)
                summary = tools['summarization'].summarize_text(text, api_keys)
                return jsonify({'summary': summary})
            except Exception as e:
                return jsonify({'error': f'Error generating summary: {str(e)}'}), 400
        
        return render_template('summarization.html')

    @app.route('/image-generation', methods=['GET', 'POST'])
    def image_generation():
        """Image generation tool"""
        user_id = session.get('user_id', 1)
        tools = get_tools()
        
        if request.method == 'POST':
            prompt = request.form.get('prompt')
            if not prompt:
                return jsonify({'error': 'No prompt provided'}), 400
            
            try:
                api_keys = get_user_api_keys(user_id)
                result = tools['image_generation'].generate_image(prompt, api_keys)
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': f'Error generating image: {str(e)}'}), 400
        
        return render_template('image_generation.html')

    @app.route('/code-assistant', methods=['GET', 'POST'])
    def code_assistant():
        """Code assistant tool"""
        user_id = session.get('user_id', 1)
        tools = get_tools()
        
        if request.method == 'POST':
            action = request.form.get('action')
            code = request.form.get('code', '')
            question = request.form.get('question', '')
            
            try:
                api_keys = get_user_api_keys(user_id)
                
                if action == 'explain':
                    result = tools['code_assistant'].explain_code(code, api_keys)
                elif action == 'review':
                    result = tools['code_assistant'].review_code(code, api_keys)
                elif action == 'generate':
                    result = tools['code_assistant'].generate_code(question, api_keys)
                else:
                    return jsonify({'error': 'Invalid action'}), 400
                
                return jsonify({'result': result})
            except Exception as e:
                return jsonify({'error': f'Error processing request: {str(e)}'}), 400
        
        return render_template('code_assistant.html')

    def get_user_api_keys(user_id):
        """Helper function to get user's API keys"""
        # Import models inside function
        _, APIKey, _, _, _ = get_models()
        
        api_keys = {}
        keys = APIKey.query.filter_by(user_id=user_id, is_active=True).all()
        for key in keys:
            api_keys[key.provider] = key.key_value
        return api_keys

    @app.before_request
    def ensure_user_session():
        if 'user_id' not in session:
            session['user_id'] = 1  # Default to first user for demo