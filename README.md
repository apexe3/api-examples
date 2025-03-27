# 🧠 Multi LLM API Examples

This repository contains example clients to interact with the [Apexe3 Multi-LLM API](https://unioninvest.apexe3.ai/alice/multi-llm-service/prompt) and Vision API for image-based prompting.

## 📂 Files

### 💬 Text Prompt Inference
- `multi-llm-inference.js` – JavaScript example using `fetch` to send a text prompt.
- `multi-llm-inference.py` – Python version using `requests`.

### 🖼️ Vision API (Image to Text)
- `multi-llm-vision.py` – Python script for prompting with image files.
- `multi-llm-vision.js` – Node.js version using `axios` and `form-data`.

### 🔐 Token Management
- `test-token.json` – Sample file to store your API key in the format:
  ```json
  {
    "key": "your-token-here"
  }
  ```

## 🧪 Supported Models

You can choose from a variety of LLMs:
- `gemini-1.5-flash`
- `gemini-2.0-flash`
- `gpt-4o-turbo`
- `claude-sonnet-3.5`
- `mistral-large-latest`
- `grok2`
- `deepseek`
- `nemotron`
- `o1`, `o1-mini`, `o3-mini`

## ▶️ Usage

### Text Prompt (Python)
```bash
python multi-llm-inference.py
```

### Text Prompt (Node.js)
```bash
node multi-llm-inference.js
```

### Vision API (Python)
```bash
python multi-llm-vision.py <image_path> <prompt> <model>
```

### Vision API (Node.js)
```bash
node multi-llm-vision.js <image_path> <prompt> <model>
```

Make sure `test-token.json` is in the same folder.

## 🛠️ Dependencies

- Python: `requests`
- Node.js: `axios`, `form-data`

Install Node dependencies:
```bash
npm install axios form-data
```

## 📜 License

Apache 2.0 License. See [LICENSE](LICENSE) for details.

## 👤 Author

Maintained by [usmane3](https://github.com/usmane3)

---

Feel free to open issues or PRs to extend the client examples!
