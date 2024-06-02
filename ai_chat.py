import requests
import json

API_KEY = 'hk-6m4it81000033157bf0809ee76d3858cf3d61469a400734d'
API_URL = "https://api.openai-hk.com/v1/chat/completions"

def chat_with_openai(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "max_tokens": 1200,
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "top_p": 1,
        "presence_penalty": 1,
        "messages": [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data).encode('utf-8'))
    result = response.json()

    if response.status_code == 200:
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
