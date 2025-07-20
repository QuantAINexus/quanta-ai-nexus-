import os
from dotenv import load_dotenv

load_dotenv()

print("\n--- Environment Variables ---")
for k, v in os.environ.items():
    if "OPENAI" in k:
        print(f"{k} = {v}")
