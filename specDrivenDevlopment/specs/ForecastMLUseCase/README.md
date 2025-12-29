# Stock Price Forecasting with NHITS (NeuralForecast)

This project implements a **reproducible stock price forecasting pipeline** using **NeuralForecast’s NHITS (Neural Hierarchical Interpolation for Time Series Forecasting)** model to predict **S&P 500 (^GSPC)** prices for the next **5 trading days**, leveraging the **APEXE3 MCP server API** for historical financial data.

The repository is designed to:
- Be deterministic and reproducible
- Avoid common NeuralForecast installation failures
- Automatically detect and use **CUDA**, **Apple Silicon (MPS)**, or **CPU**
- Follow best practices for time-series forecasting

---

## 📁 Project Structure

```
ForecastMLUseCase/
├── data_fetcher.py
├── data_preprocessor.py
├── model_builder.py
├── trainer.py
├── forecaster.py
├── evaluator.py
├── device.py
├── config.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚨 NeuralForecast Installation (Read Carefully)

### Supported Python Versions
- **Python 3.9 – Recommended**
- Python 3.10 – Fragile
- Python 3.11+ – Not supported

---

## 🧪 Environment Setup

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

### Install PyTorch First (Critical)

CPU:
```bash
pip install torch==2.1.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

CUDA (example):
```bash
pip install torch==2.1.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Verify:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

### Install Pinned Dependencies

```bash
pip install numpy==1.24.4
pip install numba==0.58.1 llvmlite==0.41.1
pip install neuralforecast==1.6.4
pip install -r requirements.txt
```

---

## 🧠 Automatic Device Detection

The system detects the best backend automatically:

- CUDA → NVIDIA GPUs
- MPS → Apple Silicon macOS
- CPU → fallback

```python
import torch, platform

def detect_device():
    if torch.cuda.is_available():
        return "cuda"
    if platform.system().lower() == "darwin" and torch.backends.mps.is_available():
        return "mps"
    return "cpu"
```

---

## 📊 Data Source

**APEXE3 API**
```
GET /asset_price_history/{symbol}
```

---

## 🏗 NHITS Configuration

```python
NHITS(
    input_size=60,
    h=5,
    n_blocks=[2,2,2],
    mlp_units=[[256,128],[256,128],[256,128]],
    dropout_prob_theta=0.2,
    learning_rate=1e-3,
    batch_size=32
)
```

---

## ▶️ Run

```bash
python main.py
```

---

## ✅ Success Criteria

✔ Deterministic setup  
✔ Automatic device detection  
✔ Stable NHITS training  
✔ Accurate 5-day forecast  
