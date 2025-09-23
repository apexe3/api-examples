import requests

# Supported model ids
# gemini-1.5-flash // gemini-2.0-flash // gpt-4o-turbo // o1-mini // o3-mini // o1
# claude-sonnet-3.5 // mistral-large-latest // grok2 // deepseek // nemotron
# gpt-5-chat-latest 
# grok-4
# private Qwen/Qwen2.5-VL-72B-Instruct
# gemini-2.5-pro
# claude-sonnet-4
# o3


def main():
    url = "<Request url from team APEX:E3>"

    body = {
        "prompt": "<your prompt>",
        "model": "<model id>",  
        "systemPrompt": "Your job is to answer questions precisely.",
        "maxOutputTokens": 1000,
        "userId": "<your-email>"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        # Check if the request was successful
        if response.ok:
            # Check if the status code is exactly 201
            if response.status_code == 201:
                print("Response:", response.text)
            else:
                print("Unexpected success status code:", response.status_code)
        else:
            print("Failed to get a response. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Fetch error:", e)

if __name__ == "__main__":
    main()
