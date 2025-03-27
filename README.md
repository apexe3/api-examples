# 🧠 Multi LLM API Examples

This repository provides simple examples for interacting with the [Apexe3 Multi-LLM API](https://unioninvest.apexe3.ai/alice/multi-llm-service/prompt). You can use these clients to prompt different large language models (LLMs) via a unified endpoint.

## 📂 Files

- `multi-llm-inference.js` – JavaScript example using `fetch` for sending a prompt to the API.
- `multi-llm-inference.py` – Python example using the `requests` library for the same API interaction.

## 🚀 Supported Models

Here are some of the available models you can use with the API (configure via the `model` parameter):

- `gemini-1.5-flash`
- `gemini-2.0-flash`
- `gpt-4o-turbo`
- `o1-mini`, `o3-mini`, `o1`
- `claude-sonnet-3.5`
- `mistral-large-latest`
- `grok2`
- `deepseek`
- `nemotron`

## 🔧 Example Request Payload

```json
{
  "prompt": "Describe the ETF create and redeem process.",
  "model": "gemini-2.0-flash",
  "systemPrompt": "Your job is to summarise earnings transcripts",
  "maxOutputTokens": 1000,
  "userId": "your-email@example.com"
}
```

## ✅ Requirements

- Python: `requests` library (`pip install requests`)
- JavaScript: Any modern environment with `fetch` support (e.g. Node.js 18+, browser)

## 📜 License

This project is licensed under the [Apache 2.0 License](LICENSE).

## ✍️ Author

Maintained by [usmane3](https://github.com/usmane3)

---

Feel free to open issues or pull requests for improvements.
