import requests
import json

url = "<URL FROM APEXE3>"

context = "August 13, 2024: In a significant development today, TLX Corp (TLXC), a leading player in the technology sector, witnessed a sharp decline in its stock price following news of a major cybersecurity breach. The breach, which reportedly exposed sensitive customer data, has led to widespread concerns among investors, causing the stock to plummet by nearly 15% in early trading.The cybersecurity incident was discovered late last night, with TLX Corp releasing a statement this morning confirming the breach. The company assured its customers that they are taking immediate steps to secure their systems and mitigate any potential damage. However, the news has already shaken investor confidence, leading to a sell-off that has significantly impacted TLXC's market value.This incident comes at a time when the technology sector is facing increased scrutiny over data security practices, with regulatory bodies around the world calling for stricter measures. TLX Corp has been a prominent name in the sector, known for its innovative products and services. However, today's events have raised questions about the company's ability to protect its vast network from such attacks.Market analysts are closely monitoring the situation, with many predicting that TLX Corp may face further challenges in the coming days as the full extent of the breach becomes clearer. The company has scheduled a press conference for later today to address the issue and outline their response plan.Investors are advised to stay cautious as the situation develops, with many opting to diversify their portfolios to minimize exposure to potential risks in the technology sector."

# supported model ids: claude-sonnet-3.5 | gemini-1.5-flash | gpt-4o-turbo

body = { "systemPrompt": "Your job is to extract content from the provided context and convert it into a JSON object. Do not provide any explaination.",
         "prompt": "Extract a JSON object from the following context into the following example format { date: '2021-01-01', symbol: 'AAPL', name: 'Apple', sector: 'technology', sentiment: 'positive' }. Do not provide any explaination. " + context,
         "model": "gpt-4o-turbo",
         "maxOutputTokens" : 1024,
        "temperature" : 0,
        "topP" : 0.5 }

# Sending POST request
response = requests.post(url, json=body)

# Checking if the request was successful
if response.status_code == 201:
    print("Response:", response.text)
    jsonObject = response.text.replace('```json', '').replace('```', '')
    jsonObject = json.loads(jsonObject)
    print(jsonObject)
    print(jsonObject['date'], jsonObject['symbol'],  jsonObject['sentiment'])
else:
    print("Failed to get a response. Status code:", response.status_code)
