"""
Quick test script to verify Gemini API integration
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] GEMINI_API_KEY not found in .env file!")
    exit(1)

if api_key == "your_gemini_api_key_here":
    print("[ERROR] Please replace 'your_gemini_api_key_here' with your actual Gemini API key in .env file!")
    exit(1)

print("[SUCCESS] Found Gemini API key in .env file")
print(f"   Key starts with: {api_key[:10]}...")

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("[SUCCESS] Gemini API configured successfully")
except Exception as e:
    print(f"[ERROR] Error configuring Gemini API: {e}")
    exit(1)

# Test the API with the configured model
try:
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    print(f"\n[TEST] Testing with model: {model_name}...")
    model = genai.GenerativeModel(model_name)

    response = model.generate_content("Say 'Hello, AI Prompt Optimizer!' in a friendly way")

    print(f"[SUCCESS] Gemini API test successful with model: {model_name}!")
    print(f"\n[RESPONSE] Response from Gemini:")
    # Encode special characters for Windows console
    try:
        print(f"   {response.text}")
    except UnicodeEncodeError:
        # If console can't display Unicode, show encoded version
        print(f"   {response.text.encode('ascii', 'replace').decode('ascii')}")

except Exception as e:
    print(f"[ERROR] Model test failed: {str(e)}")
    print("\n[INFO] Try running: python list_models.py to see available models")
    exit(1)

print("\n" + "="*60)
print("SUCCESS! Your Gemini integration is working perfectly!")
print("="*60)
print("\n[NEXT STEPS]")
print("   1. Your API key is configured correctly")
print("   2. Gemini API is responding")
print("   3. You can now run: streamlit run home.py")
print("   4. Go to Prompt Lab and try optimizing a prompt!")
print("\n")
