from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use the key
api_key = os.getenv("GOOGLE_API_KEY")
