# NeuralForecast NHITS Stock Forecasting Specification

This repository defines a **reproducible, production-safe specification** for building a stock price forecasting system using **Nixtla's NeuralForecast library**, specifically the **NHITS** architecture.

The specification is explicitly aligned with the internal design, constraints, and dependency requirements of the official NeuralForecast repository:
https://github.com/Nixtla/neuralforecast

The system is guaranteed to run correctly on:
- **CPU**
- **NVIDIA CUDA**
- **macOS Apple Silicon (MPS)**

---

## 🎯 Objectives

- Forecast **S&P 500 (^GSPC)** closing prices
- **5 business-day horizon**
- Deterministic and reproducible training
- No undocumented assumptions about NeuralForecast internals
- DO NOT DOWNLOAD or CLONE https://github.com/apexe3/api-examples github repository
- Install python 3.9 in the virtual environment and use it

---

## 🧠 NeuralForecast Architectural Constraints

NeuralForecast:
- Is built on **PyTorch**
- Manages devices internally
- Requires **long-format time series**
- Uses a **wrapper-based training API**

### Forbidden Patterns
- ❌ Calling `model.fit()` directly
- ❌ Custom PyTorch DataLoaders
- ❌ Shuffling time series data

### Required Pattern
```python
from neuralforecast import NeuralForecast

nf = NeuralForecast(models=[model], freq="B")
nf.fit(df=train_df, val_size=60)
```

---

## 🐍 Python Version Support (STRICT)

| Version | Support |
|-------|--------|
| **3.9** | ✅ Fully supported |
| 3.10 | ⚠️ Partial |
| 3.11+ | ❌ Unsupported (Numba incompatibility) |

**Python 3.9 is mandatory for reliability.**

---

## 🖥️ Hardware Backends

| Platform | Backend |
|--------|--------|
| NVIDIA GPU | CUDA |
| Apple Silicon (macOS) | MPS |
| Any system | CPU |

Device selection is handled automatically by PyTorch.

---

## 📦 Deterministic Dependency Matrix

These versions are validated against NeuralForecast internals.

| Package | Version |
|------|--------|
| torch | 2.1.2 |
| neuralforecast | 1.6.4 |
| numpy | 1.24.4 |
| numba | 0.58.1 |
| llvmlite | 0.41.1 |
| pandas | >=1.5.3 |
| scikit-learn | >=1.2.0 |

---

## ⚙️ Installation (MANDATORY ORDER)

### 1. Create Environment
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

### 2. Install PyTorch (Choose One)

CPU:
```bash
pip install torch==2.1.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

CUDA (example CUDA 11.8):
```bash
pip install torch==2.1.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

macOS Apple Silicon:
```bash
pip install torch==2.1.2 torchvision torchaudio
```

Verify:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

### 3. Install Scientific Stack
```bash
pip install numpy==1.24.4
pip install numba==0.58.1 llvmlite==0.41.1
```

---

### 4. Install NeuralForecast
```bash
pip install neuralforecast==1.6.4
```

---

## 🧠 Runtime Device Detection

```python
import torch, platform

def detect_device():
    if torch.cuda.is_available():
        return "cuda"
    if platform.system().lower() == "darwin" and torch.backends.mps.is_available():
        return "mps"
    return "cpu"
```

No manual `.to(device)` calls are required.

---

## 📊 Data Requirements

NeuralForecast **requires long-format data**.

```python
df = pd.DataFrame({
    "unique_id": "^GSPC",
    "ds": pd.to_datetime(dates),
    "y": close_prices
})
```

- Chronological order required
- Business-day frequency (`freq="B"`)
- No missing timestamps

---

## 🏗️ NHITS Model Specification

```python
NHITS(
    input_size=60,
    h=5,
    n_blocks=[2, 2, 2],
    mlp_units=[[256, 128], [256, 128], [256, 128]],
    dropout_prob_theta=0.2,
    learning_rate=1e-3,
    batch_size=32,
    max_steps=1000
)
```

Minimum required samples:
```
len(series) ≥ 5 × input_size
```

---

## 🍎 macOS (MPS) Safeguard

```python
if device == "mps":
    batch_size = min(batch_size, 16)
```

Some operations may fall back to CPU.

---

## 📈 Evaluation Metrics

- MAE
- MSE
- RMSE
- MAPE
- R²
- Directional Accuracy

Benchmarks:
- **MAPE < 5%**
- **Directional Accuracy > 55%**

---

## 💾 Model Persistence

Persist:
- Model weights
- Configuration
- Device metadata
- Training statistics

---

## 🚨 Known Failure Modes

| Issue | Cause | Fix |
|-----|------|----|
| LLVM crash | llvmlite mismatch | Pin versions |
| NaNs in loss | Missing dates | Reindex |
| Silent freeze | CUDA mismatch | Use CPU |
| Slow training | Large batch | Reduce batch size |

---

## ✅ Summary

This specification:
- Matches **Nixtla/neuralforecast internals**
- Works on **CPU / CUDA / macOS MPS**
- Avoids undocumented behavior
- Pins fragile dependencies
- Is reproducible and production-safe

---

Treat NeuralForecast as **infrastructure**, not a typical Python library.