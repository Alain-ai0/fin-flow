# COGNIS
**Neural Financial Intelligence & Private Ledger Engine**

[![System Status](https://img.shields.io/badge/System-Operational-00ffb3?style=flat-square&logo=render&logoColor=white)](https://github.com/yourusername/cognis)
[![Privacy](https://img.shields.io/badge/Data_Privacy-Local_Only-blue?style=flat-square&logo=shield-lock&logoColor=white)](https://github.com/yourusername/cognis)
[![AI Engine](https://img.shields.io/badge/AI_Core-Ollama_Llama3-orange?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com)

Cognis is a professional-grade financial intelligence engine designed to replace cloud-dependent budgeting apps with a locally hosted, AI-driven architecture. By processing raw financial data through local Large Language Models (LLMs), Cognis provides deep insights into spending patterns without compromising sensitive personal data.

---

## ◈ Project Description
In an era of data harvesting, Cognis was built to prove that sophisticated financial analysis doesn't require cloud exposure. The application handles the end-to-end lifecycle of financial data: from raw CSV ingestion and AI-augmented semantic labeling to persistent storage and real-time visualization. 

The core philosophy is **Local-First Intelligence**. By utilizing a local Ollama instance, Cognis performs complex natural language processing to categorize messy bank descriptions into clean, actionable data points, ensuring that your financial "footprint" never leaves your physical hardware.

---

## ◈ System Architecture
Cognis utilizes a decoupled client-server architecture designed for low latency and high data integrity.

### 1. Intelligence Layer (Ollama & Llama 3)
*   **Semantic Analysis:** Raw transaction strings are fed into a localized Llama 3 model.
*   **Contextual Inference:** The AI interprets ambiguous vendor names (e.g., "SQ *PLUMBING") and maps them to logical categories (e.g., "Home Maintenance").

### 2. Backend Engine (FastAPI & Pandas)
*   **Stateless Processing:** API endpoints handle file uploads and data retrieval via asynchronous I/O.
*   **Data Normalization:** Uses Pandas to perform de-duplication, ensuring that redundant uploads do not corrupt the financial ledger.
*   **Immutable Persistence:** Implements absolute pathing logic on the host filesystem to maintain a consistent data state across server restarts and environment shifts.

### 3. Interface Layer (React & Tailwind)
*   **State Synchronization:** Utilizes React hooks (`useCallback`, `useEffect`) to ensure the UI stays in sync with the backend CSV state.
*   **Reactive Visualization:** Implements Recharts for dynamic data modeling and CSS-based "Dark Mode" optimized for professional workstations.

---

## ◈ Engineering Stack
| Layer | Technology |
| :--- | :--- |
| **Intelligence** | Ollama Core (Llama 3 / Phi-3) |
| **Data Engine** | Python 3.10+, Pandas, Absolute FS |
| **Interface** | React 18, Tailwind CSS, Recharts |
| **API Layer** | FastAPI (Asynchronous I/O) |

---

## ◈ Deployment Instructions

### Prerequisites
*   **Hardware:** Optimized for local LLM execution (8GB+ RAM recommended).
*   **Environment:** Python 3.10+, Node.js 18+.
*   **LLM Host:** [Ollama](https://ollama.com/) must be installed and running `llama3`.

### 1. Backend Deployment
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate 
# Linux/Mac
source venv/bin/activate  

pip install -r requirements.txt
uvicorn main:app --port 8000 --reload