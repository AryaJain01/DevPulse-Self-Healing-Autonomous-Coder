# 🤖 DevPulse: Self-Healing Autonomous AI Coder

![Python](https://img.shields.io/badge/Python-3.11-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Agentic--Framework-red)
![Docker](https://img.shields.io/badge/Docker-Sandbox-blue)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**DevPulse** is an autonomous software engineering agent that doesn't just write code — it tests it, fails, learns from the traceback, and heals itself. By combining **Multi-Agent Orchestration (CrewAI)** with a secure **Docker Sandbox**, DevPulse ensures that the code it generates actually works in a real-world environment.

---

## 🎯 The "Self-Healing" Problem Statement

Large Language Models (LLMs) often generate code that looks correct but contains syntax errors, missing imports, or logical bugs. **DevPulse** eliminates the manual "copy → paste → error → fix" cycle by:

1. **Writing** code based on natural language goals.
2. **Executing** the code inside an isolated Docker container.
3. **Analyzing** the error logs if execution fails.
4. **Re-prompting** the AI with the specific traceback to "heal" the script.

---

## 🧠 System Architecture

```text
          User Goal
              ↓
┌──────────────────────────┐       ┌──────────────────────────┐
│      AI AGENT CREW       │       │      DOCKER SANDBOX      │
│  (Architect + Debugger)  │       │   (Isolated Environment) │
│                          │       │                          │
│  1. Analyze Request      │       │  1. Mount Workspace      │
│  2. Generate main.py     │──────▶│  2. Run python main.py   │
│  3. Review Logic         │       │  3. Capture Stdout/Stderr│
└──────────▲───────────────┘       └──────────────┬───────────┘
           │                                      │
           │            ERROR DETECTED?           │
           └──────────────────────────────────────┘
                  (Pass Traceback to Agents)
```

---

## ✨ Features

### 🕵️ Multi-Agent Collaboration
- **Senior Architect** — Focuses on high-level logic and writing clean, PEP-8 compliant Python code.
- **Senior Debugger** — Monitors execution logs and provides targeted fix strategies back to the Architect.

### 🛡️ Secure Execution (Sandbox)
- Every script runs inside a **Docker Container**, protecting your host machine from accidental infinite loops or harmful commands.
- **Volume Mapping** automatically syncs the `workspace/` folder so you can inspect the generated code in real-time.

### 🔄 Autonomous Self-Healing Loop
- Supports up to **3 retry attempts** per goal.
- Captures `RuntimeError`, `ImportError`, and `SyntaxError` to provide closed-loop feedback to the LLM.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | CrewAI |
| LLM Inference | Groq (Llama-3.3-70B) |
| Sandbox Engine | Docker SDK for Python |
| Frontend UI | Streamlit |
| Logic Layer | LangChain (LCEL) |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running.
- A free Groq API Key from [console.groq.com](https://console.groq.com).

### 2. Clone & Install

```bash
git clone https://github.com/AryaJain01/DevPulse.git
cd DevPulse
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 📊 Why This Project Matters

DevPulse demonstrates end-to-end mastery over three engineering disciplines:

- **DevOps** — Containerization, volume mapping, and automated sandboxed testing.
- **AI Engineering** — Building agentic workflows with memory and closed-loop feedback, going far beyond simple prompting.
- **Software Architecture** — Managing complex state across an LLM, a local filesystem, and a virtualized environment.

---

## 👨‍💻 Author

**Arya Jain**
- 📍 Dehradun, Uttarakhand, India
- 🐙 GitHub: [@AryaJain01](https://github.com/AryaJain01)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.