import requests
import json

def stream_kinos(role):
    url = f"https://autonomous.digitalkin.ai/kinos?role={role}"
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if 'output' in data:
                        print(f"Output: {data['output']}")
                    elif 'error' in data:
                        print(f"Error: {data['error']}")
                    elif 'debug' in data:
                        print(f"Debug: {data['debug']}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {line}")

if __name__ == "__main__":
    stream_kinos("vox")