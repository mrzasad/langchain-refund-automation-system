import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check API key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ API Key found!")
    print(f"Key starts with: {api_key[:20]}...")
else:
    print("❌ API Key not found. Please set OPENAI_API_KEY environment variable.")
    print("\nOptions:")
    print("1. Create .env file with: OPENAI_API_KEY=sk-your-key")
    print("2. Set system environment variable")
    print("3. Set in .streamlit/secrets.toml for Streamlit Cloud")