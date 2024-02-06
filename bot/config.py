import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
FILENAME = os.path.dirname(__file__).split(f"\\")[-1]