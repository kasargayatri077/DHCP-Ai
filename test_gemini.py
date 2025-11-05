import google.generativeai as genai
import os

def test_gemini_api():
    try:
        # Try to get the API key from the same source as the app
        import streamlit as st
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        # Fallback to environment variable if running outside Streamlit
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: No API key found. Please set GEMINI_API_KEY environment variable.")
        return
    
    print(f"API Key found (first 10 chars): {api_key[:10]}...")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models as a simple test
        print("Attempting to list available models...")
        models = genai.list_models()
        
        print("\nSuccess! Available models:")
        for model in models:
            print(f"- {model.name}")
            
    except Exception as e:
        print(f"\nError occurred while testing the API:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify your API key is correct")
        print("2. Make sure the Gemini API is enabled in Google AI Studio")
        print("3. Check if your Google Cloud account has billing enabled")
        print("4. Ensure your API key has the necessary permissions")

if __name__ == "__main__":
    test_gemini_api()
