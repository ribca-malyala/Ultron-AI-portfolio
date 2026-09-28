# 💗 ULTRON AI Command Center

A feminine, futuristic AI assistant built with **Python + Streamlit + Ollama**, with optional cloud AI support.

## ✨ Features

- 💗 Pink/lavender glassmorphism UI
- 💬 Persistent chat history using Streamlit session state
- 🧠 Local AI support through Ollama
- ☁️ Optional OpenAI cloud provider for deployment
- 📎 TXT/PDF/DOCX document context
- ✨ Quick prompt buttons
- 📊 Live system/provider/message status cards
- 📥 Export conversation as JSON
- 🧹 Clear/reset conversation
- 📱 Responsive Streamlit layout
- 🚀 Deployment-ready GitHub structure

## 📁 Project structure

```text
ULTRON-AI/
├── proj1.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🖥️ Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start Streamlit:

```bash
python -m streamlit run proj1.py
```

### Local Ollama

Install Ollama and pull a model, for example:

```bash
ollama pull llama3.2
```

Then select **Ollama (Local)** in the sidebar.

## ☁️ Public deployment

The project is structured for Streamlit Community Cloud.

1. Push this folder to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Create an app from the GitHub repository.
4. Select `proj1.py` as the entrypoint.
5. Deploy.

For cloud AI, select **OpenAI (Cloud)** and configure `OPENAI_API_KEY` in Streamlit Secrets.

Do **not** commit API keys to GitHub.

## ⚠️ Ollama deployment note

Ollama is intended here for local development. A public Streamlit deployment should use the optional cloud provider unless you separately host an Ollama-compatible backend and configure networking for it.

## 🧰 Tech stack

- Python
- Streamlit
- Ollama
- OpenAI API (optional)
- PyPDF
- python-docx
- HTML/CSS

## 🎯 Portfolio value

This project demonstrates more than a basic chatbot: it combines UI design, state management, LLM integration, document processing, export functionality and deployment preparation in one application.
