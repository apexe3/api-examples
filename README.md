# 🧠 Apexe3 API Examples

This repository provides working examples to interact with the **Apexe3 APIs**, including:

- ✅ Multi-LLM API for text-based prompting
- 🖼️ Vision API for image understanding
- 📦 Vector Database API for document and index management

---

## 📁 Folders & Contents

### `multi-llm-*`
💬 **Multi LLM Inference Clients**
- `multi-llm-inference.js` – JavaScript client (text prompt)
- `multi-llm-inference.py` – Python client (text prompt)

🖼️ **Vision API Clients**
- `multi-llm-vision.js` – Node.js client for image-to-text
- `multi-llm-vision.py` – Python client for image-to-text

🔐 **Token File**
- `test-token.json` – Stores API key:
  ```json
  {
    "key": "your-api-key"
  }
  ```

---

### `apexe3-vector-database-examples`
📦 **Vector Database Clients**
- `uploadDoc.py` – Upload a document for vectorization
- `fetchVectorResources.py` – Retrieve resources from the vector DB
- `deleteResource.py` – Delete a document/resource
- `deleteIndex.py` – Delete a full vector index

---

## 🧪 Supported LLMs

Apexe3 supports multiple models through the unified LLM API:
- `Teuken-7B-instruct-research-v0.4`
- `EuroLLM-9B-Instruct`, `EuroLLM-1.7B-Instruct`
- `gpt-4o-turbo`, `gemini-1.5-flash`, `gemini-2.0-flash`
- `claude-sonnet-3.5`, `mistral-large-latest`, `grok2`
- `deepseek`, `nemotron`, `o1`, `o1-mini`, `o3-mini`

---

## ▶️ How to Run

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

### Vector API Examples
```bash
python uploadDoc.py
python fetchVectorResources.py
python deleteResource.py
python deleteIndex.py
```

> ⚠️ Ensure `test-token.json` is in the same directory or adjust the scripts accordingly.

---

## 🛠️ Requirements

### Python
- `requests`

### Node.js
```bash
npm install axios form-data
```

---

## 📜 License

Apache 2.0 License. See [LICENSE](LICENSE).

---

## 👤 Author

Maintained by [usmane3](https://github.com/usmane3)

---
