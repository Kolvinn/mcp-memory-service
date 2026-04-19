
import os
import requests
import json

url = os.getenv("MCP_EXTERNAL_EMBEDDING_URL")
model = os.getenv("MCP_EXTERNAL_EMBEDDING_MODEL")
payload = {
    "model": model,
    "input": "Sample text for testing."
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    print(f"Embedding vector received. Dimensions: {len(data['embeddings'][0])}")
else:
    print(f"Failed with status: {response.status_code}")
    
    

# print(f"Attempting to connect to Ollama at {url}...")

# try:
#     response = requests.get(url, timeout=5)
#     if response.status_code == 200:
#         print("Successfully connected to Ollama!")
#         print(f"Response: {response.json()}")
#     else:
#         print(f"Connected, but received status code: {response.status_code}")
#         #sys.exit(1)
# except requests.exceptions.ConnectionError:
#     print("Error: Could not connect to Ollama. Is the service running and on the same network?")
#     #sys.exit(1)
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     #sys.exit(1)

