"""
List available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("[INFO] Listing available Gemini models...\n")

try:
    for model in genai.list_models():
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported Generation Methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"[ERROR] Error listing models: {e}")
