"""
File Processor - Handles various file types for the AI Prompt Agent
Supports: PDF, Documents, Images, Code files, Audio
"""
import io
import os
import tempfile
from typing import Optional, Tuple
from pathlib import Path
import google.generativeai as genai
from core.config import Config


class FileProcessor:
    """
    Process various file types and extract content for the AI Agent
    """

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        'documents': ['.pdf', '.txt', '.md', '.doc', '.docx'],
        'code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.sql', '.html', '.css', '.json', '.yaml', '.yml'],
        'images': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
        'audio': ['.wav', '.mp3', '.m4a', '.ogg']
    }

    def __init__(self):
        """Initialize with Gemini for image analysis"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')

    def get_file_type(self, filename: str) -> str:
        """Determine file type category from filename"""
        ext = Path(filename).suffix.lower()

        for file_type, extensions in self.SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return file_type

        return "unknown"

    def is_supported(self, filename: str) -> bool:
        """Check if file type is supported"""
        return self.get_file_type(filename) != "unknown"

    def process_file(self, uploaded_file) -> Tuple[str, str]:
        """
        Process uploaded file and extract content

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            Tuple of (extracted_content, file_type)
        """
        filename = uploaded_file.name
        file_type = self.get_file_type(filename)

        try:
            if file_type == "documents":
                content = self._process_document(uploaded_file, filename)
            elif file_type == "code":
                content = self._process_code(uploaded_file)
            elif file_type == "images":
                content = self._process_image(uploaded_file)
            elif file_type == "audio":
                content = self._process_audio(uploaded_file)
            else:
                content = f"Unsupported file type: {filename}"
                file_type = "unknown"

            return content, file_type

        except Exception as e:
            return f"Error processing file: {str(e)}", "error"

    def _process_document(self, uploaded_file, filename: str) -> str:
        """Process document files (PDF, TXT, MD, DOC)"""
        ext = Path(filename).suffix.lower()

        if ext == '.txt' or ext == '.md':
            # Plain text files
            return uploaded_file.read().decode('utf-8')

        elif ext == '.pdf':
            # PDF processing
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                text_content = []
                for page in pdf_reader.pages[:20]:  # Limit to first 20 pages
                    text_content.append(page.extract_text())
                return "\n\n".join(text_content)
            except ImportError:
                # Fallback if PyPDF2 not available
                return self._analyze_with_gemini(uploaded_file, "Extract and summarize the text content from this PDF document.")
            except Exception as e:
                return f"Could not extract PDF text: {str(e)}"

        elif ext in ['.doc', '.docx']:
            # Word documents
            try:
                import docx
                doc = docx.Document(io.BytesIO(uploaded_file.read()))
                text_content = [para.text for para in doc.paragraphs]
                return "\n\n".join(text_content)
            except ImportError:
                return "Word document processing requires python-docx package"
            except Exception as e:
                return f"Could not extract Word document: {str(e)}"

        return "Unsupported document format"

    def _process_code(self, uploaded_file) -> str:
        """Process code files"""
        try:
            content = uploaded_file.read().decode('utf-8')
            # Limit size
            if len(content) > 50000:
                content = content[:50000] + "\n\n... [truncated due to size]"
            return content
        except Exception as e:
            return f"Error reading code file: {str(e)}"

    def _process_image(self, uploaded_file) -> str:
        """Process images using Gemini Vision"""
        try:
            from PIL import Image

            # Read image
            image_data = uploaded_file.read()
            image = Image.open(io.BytesIO(image_data))

            # Analyze with Gemini Vision
            prompt = """Analyze this image in detail. If it contains:
1. Code/Screenshot of code: Extract and transcribe the code
2. Diagram/Architecture: Describe the structure and components
3. Chart/Graph: Describe the data and insights
4. Text/Document: Extract the text content
5. UI/Interface: Describe the interface elements

Provide a comprehensive description that captures all relevant information."""

            response = self.vision_model.generate_content([prompt, image])
            return response.text

        except ImportError:
            return "Image processing requires Pillow package"
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def _process_audio(self, uploaded_file) -> str:
        """Process audio files - transcribe to text"""
        try:
            import speech_recognition as sr

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Transcribe
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data)

            # Cleanup
            os.unlink(tmp_path)

            return f"[Audio Transcription]:\n{text}"

        except ImportError:
            return "Audio processing requires SpeechRecognition package"
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

    def _analyze_with_gemini(self, uploaded_file, prompt: str) -> str:
        """Generic analysis using Gemini"""
        try:
            # For PDFs and documents, use Gemini's file handling
            content = uploaded_file.read()
            response = self.vision_model.generate_content([prompt, {"mime_type": "application/pdf", "data": content}])
            return response.text
        except Exception as e:
            return f"Analysis failed: {str(e)}"


class VoiceProcessor:
    """Process voice input"""

    @staticmethod
    def transcribe_audio_bytes(audio_bytes: bytes) -> Optional[str]:
        """Transcribe audio bytes to text"""
        try:
            import speech_recognition as sr
            import tempfile
            import os

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name

            # Transcribe
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data)

            # Cleanup
            os.unlink(tmp_path)

            return text

        except Exception as e:
            return None
