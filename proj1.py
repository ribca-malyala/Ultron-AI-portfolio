import io
import json
from datetime import datetime

import streamlit as st
import ollama

# Optional cloud provider
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ULTRON • AI Command Center",
    page_icon="🐷",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS — PINK / LAVENDER / GLASSMORPHISM
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --pink: #ff4fa3;
    --hot-pink: #ff2f92;
    --lavender: #9b7cff;
    --purple: #6f4cff;
    --rose: #ff9fcf;
    --cream: #fff8fc;
    --ink: #2b2030;
    --muted: #756878;
    --card: rgba(255,255,255,.78);
    --border: rgba(255,79,163,.20);
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(255,120,190,.25), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(155,124,255,.24), transparent 28%),
        linear-gradient(135deg, #fff7fc 0%, #f8f3ff 52%, #fffafd 100%);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--ink) !important;
}

h1 {
    font-size: 3.4rem !important;
    letter-spacing: -2px;
    margin-bottom: 0 !important;
}

h2 {
    color: #6f4cff !important;
}

p, li, label, .stMarkdown, .stCaption {
    color: var(--ink) !important;
}

.stCaption {
    color: var(--muted) !important;
}

.hero {
    padding: 2.2rem 2rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,.88), rgba(255,240,249,.82));
    border: 1px solid var(--border);
    box-shadow: 0 20px 60px rgba(143,75,126,.13);
    margin-bottom: 1.3rem;
}

.hero-badge {
    display: inline-block;
    padding: .4rem .8rem;
    border-radius: 999px;
    background: #ffe1f0;
    color: #c92878;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .08em;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.8rem;
    font-weight: 700;
    color: #2b2030;
    letter-spacing: -.05em;
    margin-top: .7rem;
}

.hero-title span {
    color: #ff3f98;
}

.hero-subtitle {
    color: #756878;
    font-size: 1.05rem;
    max-width: 760px;
}

.metric-card {
    padding: 1rem;
    border-radius: 18px;
    background: rgba(255,255,255,.72);
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(143,75,126,.08);
    min-height: 105px;
}

.metric-label {
    color: #817180;
    font-size: .8rem;
    text-transform: uppercase;
    letter-spacing: .08em;
}

.metric-value {
    color: #302237;
    font-size: 1.45rem;
    font-weight: 700;
    margin-top: .25rem;
}

.status-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #39d98a;
    box-shadow: 0 0 12px rgba(57,217,138,.8);
    margin-right: 6px;
}

.chat-user, .chat-ai {
    padding: 1rem 1.15rem;
    border-radius: 18px;
    margin: .7rem 0;
    border: 1px solid var(--border);
}

.chat-user {
    background: linear-gradient(135deg, #ffe3f1, #f5e9ff);
    margin-left: 10%;
}

.chat-ai {
    background: rgba(255,255,255,.8);
    margin-right: 10%;
}

.chat-label {
    font-size: .76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #9a4b7b;
    margin-bottom: .35rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff3fa 0%, #f6f0ff 100%);
    border-right: 1px solid rgba(255,79,163,.14);
}

[data-testid="stSidebar"] h2 {
    color: #ff3f98 !important;
}

.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,.82) !important;
    color: #2b2030 !important;
    border: 1px solid rgba(155,124,255,.28) !important;
    border-radius: 14px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #ff4fa3 !important;
    box-shadow: 0 0 0 3px rgba(255,79,163,.12) !important;
}

.stButton > button {
    border: 0 !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #ff4fa3, #8d6bff) !important;
    color: white !important;
    font-weight: 700 !important;
    min-height: 44px;
    box-shadow: 0 8px 22px rgba(166,79,151,.20);
    transition: transform .2s ease, box-shadow .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(166,79,151,.28);
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,.60);
    border: 1px dashed rgba(255,79,163,.35);
    border-radius: 16px;
    padding: 8px;
}

[data-baseweb="select"] {
    border-radius: 12px;
}

hr {
    border-color: rgba(155,124,255,.16) !important;
}

.small-note {
    text-align: center;
    color: #8d7b8b;
    font-size: .8rem;
    padding: 1rem;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 14px !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_context" not in st.session_state:
    st.session_state.uploaded_context = ""

if "provider" not in st.session_state:
    st.session_state.provider = "Ollama (Local)"

if "model" not in st.session_state:
    st.session_state.model = "llama3.2"


# =========================================================
# HELPERS
# =========================================================

SYSTEM_PROMPT = """
You are ULTRON, a fictional futuristic AI assistant.

Personality:
- Intelligent, precise, confident and analytical.
- Modern and slightly dramatic, but never rude.
- Address the user as Operator when it fits naturally.
- Give useful, structured answers.
- Do not claim to have performed actions you cannot perform.
- If a file is supplied, use its contents as context and clearly distinguish
  document-derived information from general knowledge.
"""

def extract_file_text(uploaded_file):
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        if PdfReader is None:
            return "PDF support is unavailable because pypdf is not installed."
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        if Document is None:
            return "DOCX support is unavailable because python-docx is not installed."
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    return "Unsupported file type."


def build_prompt(user_text):
    prompt = SYSTEM_PROMPT

    if st.session_state.uploaded_context:
        prompt += (
            "\n\nREFERENCE FILE CONTENT:\n"
            + st.session_state.uploaded_context[:20000]
        )

    return prompt, user_text


def ask_ai(user_text, provider, model):
    system_prompt, clean_question = build_prompt(user_text)

    conversation = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    if provider == "Ollama (Local)":
        response = ollama.chat(
            model=model,
            messages=conversation,
        )
        return response["message"]["content"]

    if provider == "OpenAI (Cloud)":
        if OpenAI is None:
            raise RuntimeError(
                "The openai package is not installed."
            )

        api_key = st.secrets.get("OPENAI_API_KEY", None)

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. Add it through "
                "Streamlit Secrets before using OpenAI Cloud."
            )

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=conversation,
        )

        return response.choices[0].message.content

    raise RuntimeError("Unknown AI provider selected.")


def export_chat():
    export_data = {
        "application": "ULTRON AI Command Center",
        "exported_at": datetime.now().isoformat(),
        "messages": st.session_state.messages,
    }

    return json.dumps(
        export_data,
        indent=2,
        ensure_ascii=False,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("##  ULTRON")

    st.caption("AI Command Center")

    st.divider()

    st.markdown("### ⚙️ AI Configuration")

    provider = st.selectbox(
        "AI Provider",
        ["Ollama (Local)", "OpenAI (Cloud)"],
        index=0 if st.session_state.provider == "Ollama (Local)" else 1,
    )
    st.session_state.provider = provider

    if provider == "Ollama (Local)":
        model = st.text_input(
            "Ollama model",
            value=st.session_state.model,
            help="Example: llama3.2, llama3.1, mistral",
        )
    else:
        model = st.selectbox(
            "OpenAI model",
            ["gpt-4o-mini", "gpt-4.1-mini"],
        )

    st.session_state.model = model

    st.divider()

    st.markdown("### ✨ Quick Prompts")

    quick_prompts = [
        "Explain Python to me like a beginner.",
        "Give me 5 project ideas for my GitHub portfolio.",
        "Review this code and find bugs.",
        "Create a professional README for my project.",
    ]

    for prompt in quick_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.quick_prompt = prompt
            st.rerun()

    st.divider()

    st.markdown("###  🐾Knowledge File")

    uploaded_file = st.file_uploader(
        "Upload TXT, PDF or DOCX",
        type=["txt", "pdf", "docx"],
    )

    if uploaded_file:
        with st.spinner("Reading your file..."):
            st.session_state.uploaded_context = extract_file_text(
                uploaded_file
            )

        st.success(
            f"Loaded: {uploaded_file.name}"
        )

    st.divider()

    st.markdown("### 🧹 Session")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.download_button(
        "Download chat JSON",
        data=export_chat(),
        file_name="ultron_chat_history.json",
        mime="application/json",
        use_container_width=True,
    )

    st.divider()

    st.caption(
        "👻 Built with Streamlit + Python + AI"
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-badge">✦ PERSONAL AI COMMAND CENTER</div>
    <div class="hero-title">ULTR<span>O</span>N</div>
    <div class="hero-subtitle">
        A feminine, futuristic AI workspace for conversations,
        document context, coding help and intelligent productivity.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# STATUS CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">System</div>
            <div class="metric-value">
                <span class="status-dot"></span>Online
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Provider</div>
            <div class="metric-value">{provider}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Messages</div>
            <div class="metric-value">{len(st.session_state.messages)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    file_status = "Attached" if st.session_state.uploaded_context else "None"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Knowledge File</div>
            <div class="metric-value">{file_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# =========================================================
# QUICK START
# =========================================================

st.markdown("## ✨ What can ULTRON do?")

q1, q2, q3 = st.columns(3)

with q1:
    st.info("💻 **Code Assistant**\n\nDebug, explain and improve code.")

with q2:
    st.info("📚 **Study Companion**\n\nAsk questions and work from uploaded notes.")

with q3:
    st.info("💡 **Idea Generator**\n\nCreate project, portfolio and productivity ideas.")


# =========================================================
# CHAT
# =========================================================

st.markdown("## 💬 Command Terminal")

if "quick_prompt" in st.session_state:
    default_question = st.session_state.pop("quick_prompt")
else:
    default_question = ""

question = st.text_area(
    "Your command",
    value=default_question,
    placeholder="Ask ULTRON anything... ✨",
    height=110,
    label_visibility="collapsed",
)

send_col, exit_col = st.columns([4, 1])

with send_col:
    execute = st.button(
        "🐔 Execute Command",
        use_container_width=True,
    )

with exit_col:
    exit_chat = st.button(
        "Reset",
        use_container_width=True,
    )


if exit_chat:
    st.session_state.messages = []
    st.rerun()


if execute:
    if not question.strip():
        st.warning("Please enter a command first.")
    else:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question.strip(),
            }
        )

        with st.spinner("ULTRON is thinking..."):
            try:
                answer = ask_ai(
                    question.strip(),
                    provider,
                    model,
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:
                st.error(
                    "ULTRON could not complete the request."
                )
                st.caption(str(error))


# =========================================================
# CHAT DISPLAY
# =========================================================

if st.session_state.messages:
    st.markdown("## 👽 Conversation")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-user">
                    <div class="chat-label">🐔 Operator</div>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-ai">
                    <div class="chat-label">✦ ULTRON</div>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        """
        <div class="small-note">
            ✨ No conversation yet. Your command terminal is ready.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PROJECT / GITHUB VALUE SECTION
# =========================================================

st.divider()

with st.expander("🌷 About this project"):
    st.markdown(
        """
        **ULTRON AI Command Center** is a portfolio-oriented
        Streamlit application demonstrating:

        - Python application development
        - Streamlit UI engineering
        - LLM integration
        - Local AI with Ollama
        - Optional cloud AI integration
        - Session-state conversation memory
        - Document context ingestion
        - JSON conversation export
        - Responsive dashboard-style UI
        - Deployment-ready dependency management

        The application is designed so the local Ollama workflow can
        be used during development while a cloud provider can be
        configured for public deployment.
        """
    )

st.markdown(
    """
    <div class="small-note">
        🐔 ULTRON AI • Built for learning, experimentation & portfolio development
    </div>
    """,
    unsafe_allow_html=True,
)
