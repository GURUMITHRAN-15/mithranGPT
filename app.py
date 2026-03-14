"""
MithranGPT - AI Chatbot with DuckDuckGo Web Search
====================================================
Requirements:
    pip install groq python-dotenv streamlit ddgs

Usage:
    streamlit run mithrangpt.py
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS

load_dotenv()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MithranGPT",
    page_icon="mithrangpt.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f2f6; }
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 800px !important;
}

/* Header */
.header-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 0 0 24px 24px;
    padding: 2.2rem 2rem 1.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(102,126,234,0.3);
}
.header-banner h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.header-banner p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}

/* Chat messages */
[data-testid="stChatMessage"] { background: transparent !important; padding: 0.3rem 0 !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 0.75rem 1.1rem !important;
    box-shadow: 0 2px 10px rgba(102,126,234,0.25) !important;
    display: inline-block !important;
    max-width: 85% !important;
    float: right !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: #f8f9ff !important;
    color: #1e293b !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 0.75rem 1.1rem !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
    border: 1px solid #e8eaf6 !important;
    display: inline-block !important;
    max-width: 85% !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span { color: inherit !important; }

/* Chat Input */
[data-testid="stChatInput"] {
    background: #1e1e2e !important;
    border: 2px solid #3730a3 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.3) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 2px 20px rgba(102,126,234,0.25) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    color: #ffffff !important;
    caret-color: #a5b4fc !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #6b7280 !important; }

/* Search cards */
.search-card {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    font-size: 0.82rem;
    color: #78350f;
}
.search-card a { color: #b45309; font-weight: 600; text-decoration: none; }
.search-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #fef3c7;
    border: 1px solid #fde68a;
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: #92400e;
    font-weight: 600;
    margin-bottom: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}
.sidebar-brand { text-align: center; padding: 1rem 0 0.5rem; }
.sidebar-brand .bot-icon { font-size: 3rem; display: block; margin-bottom: 0.4rem; }
.sidebar-brand h2 {
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
}
.sidebar-brand p { font-size: 0.78rem !important; color: #94a3b8 !important; margin: 0.2rem 0 0 !important; }

.model-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px 14px;
    margin: 6px 0;
}
.model-card .model-name { font-size: 0.82rem; font-weight: 600; color: #a5b4fc !important; }
.model-card .model-detail { font-size: 0.72rem; color: #64748b !important; margin-top: 2px; }

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    padding: 0.6rem !important;
    box-shadow: 0 4px 12px rgba(102,126,234,0.35) !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}

.stat-bar { display: flex; gap: 8px; margin: 0.8rem 0 0; }
.stat-item {
    flex: 1;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 8px 10px;
    text-align: center;
}
.stat-item .sv { font-size: 1.2rem; font-weight: 700; color: #a5b4fc !important; font-family: 'Poppins', sans-serif; }
.stat-item .sl { font-size: 0.65rem; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.06em; }

.sidebar-footer {
    text-align: center;
    padding: 1rem 0 0.5rem;
    font-size: 0.75rem !important;
    color: #475569 !important;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin-top: 1rem;
}

/* Empty state */
.empty-state { text-align: center; padding: 3.5rem 1rem; color: #94a3b8; }
.empty-state .emoji { font-size: 3rem; margin-bottom: 0.75rem; }
.empty-state h3 { font-family: 'Poppins', sans-serif; font-size: 1.2rem; color: #64748b; margin: 0 0 0.4rem; }
.empty-state p { font-size: 0.88rem; margin: 0; }
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 1.2rem; }
.pill {
    background: #f0f2ff;
    border: 1px solid #c7d2fe;
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.8rem;
    color: #4f46e5;
}
hr { border-color: rgba(255,255,255,0.08) !important; }
/* Force visible message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# ── Models ─────────────────────────────────────────────────────────────────────
MODELS = {
    "⚡ Llama 3.1 8B — Fast":      ("llama-3.1-8b-instant",    "8B params · 8k ctx · Best for quick answers"),
    "🧠 Llama 3.3 70B — Powerful": ("llama-3.3-70b-versatile", "70B params · 8k ctx · Best for complex tasks"),
    "🔮 Gemma 2 9B — Balanced":    ("gemma2-9b-it",            "9B params · 8k ctx · Google DeepMind"),
}

# ── Session State ──────────────────────────────────────────────────────────────
if "messages"  not in st.session_state:
    st.session_state.messages = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# ── Groq Client ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    return Groq(api_key=key) if key else None

client = get_client()

# ── Web Search Helpers ─────────────────────────────────────────────────────────
def needs_web_search(query):
    keywords = [
        "today", "now", "current", "latest", "news", "live", "price",
        "weather", "score", "match", "result", "who won", "update",
        "2024", "2025", "2026", "recently", "this week", "this month",
        "right now", "happening", "trending", "stock", "rate"
    ]
    return any(k in query.lower() for k in keywords)

def web_search(query, max_results=4):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception:
        return []

def format_search_context(results):
    if not results:
        return ""
    context = "Here is recent information from the web:\n\n"
    for i, r in enumerate(results, 1):
        context += f"{i}. {r.get('title', '')}\n{r.get('body', '')}\nSource: {r.get('href', '')}\n\n"
    return context

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="bot-icon">🤖</span>
        <h2>MithranGPT</h2>
        <p>An AI chatbot built by Gurumithran</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**🎛️ Model**")
    model_label = st.selectbox("model", list(MODELS.keys()), label_visibility="collapsed")
    model_id, model_desc = MODELS[model_label]

    st.markdown(f"""
    <div class="model-card">
        <div class="model-name">{model_id}</div>
        <div class="model-detail">{model_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    web_search_enabled = st.toggle("🌐 Web Search", value=True,
                                   help="Auto-searches DuckDuckGo for live queries")

    with st.expander("⚙️ Advanced Settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                                help="Higher = more creative")
        max_tokens = st.slider("Max Tokens", 256, 2048, 1024, 128)

    st.divider()

    st.markdown(f"""
    <div class="stat-bar">
        <div class="stat-item">
            <div class="sv">{len(st.session_state.messages) // 2}</div>
            <div class="sl">Turns</div>
        </div>
        <div class="stat-item">
            <div class="sv">{st.session_state.msg_count}</div>
            <div class="sl">Messages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("🗑️  Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.rerun()

    if not client:
        st.error("⚠️ GROQ_API_KEY missing in .env!")

    st.markdown("""
    <div class="sidebar-footer">
        Built with ❤️ using Python and Streamlit<br>
        <span style="color:#334155">by Gurumithran</span>
    </div>
    """, unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>MithranGPT 🤖</h1>
    <p>Your Intelligent AI Assistant</p>
</div>
""", unsafe_allow_html=True)

# ── Chat History ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="emoji">💬</div>
        <h3>How can I help you today?</h3>
        <p>Ask me anything — I'm fast, smart and always ready.</p>
        <div class="pill-row">
            <span class="pill">💡 Explain machine learning</span>
            <span class="pill">🐍 Write Python code</span>
            <span class="pill">🌍 Latest news today</span>
            <span class="pill">📈 Current stock trends</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] in ("user", "assistant"):
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

# ── Chat Input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input("Message MithranGPT...")

if user_input:
    if not client:
        st.error("GROQ_API_KEY not found. Add it to your .env file.")
        st.stop()

    # Save & show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.msg_count += 1
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        search_results = []
        search_context = ""

        # Step 1 — Web search if needed
        if web_search_enabled and needs_web_search(user_input):
            with st.spinner("🌐 Searching the web..."):
                search_results = web_search(user_input)
                search_context = format_search_context(search_results)

            if search_results:
                st.markdown('<div class="search-badge">🌐 Web Search Results</div>', unsafe_allow_html=True)
                for r in search_results[:3]:
                    title = r.get("title", "")
                    body  = r.get("body", "")[:120] + "..."
                    href  = r.get("href", "#")
                    st.markdown(f"""
                    <div class="search-card">
                        <a href="{href}" target="_blank">{title}</a><br>{body}
                    </div>
                    """, unsafe_allow_html=True)

        # Step 2 — Ask Groq
        with st.spinner("MithranGPT is thinking..."):
            try:
                system_prompt = (
                    "You are MithranGPT, a helpful, friendly, and intelligent AI assistant. "
                    "You were built by Gurumithran, a passionate Python and AI developer. "
                    "Gurumithran created you using Python, Streamlit, and the Groq API. "
                    "If anyone asks who built you or who is Gurumithran, say: "
                    "'I was built by Gurumithran, a passionate Python and AI developer who created me using Python, Streamlit, and Groq API.' "
                    "Answer all questions clearly and concisely. "
                    "Never mention knowledge cutoff dates or add disclaimers. "
                    "Just answer confidently and directly."
                )

                if search_context:
                    system_prompt += f"\n\n{search_context}"
                    system_prompt += "\nUse the above web search results to answer the user's question accurately."

                api_msgs = [{"role": "system", "content": system_prompt}]
                api_msgs += [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ("user", "assistant")
                ]

                response = client.chat.completions.create(
                    model=model_id,
                    messages=api_msgs,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                reply = response.choices[0].message.content.strip()

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.msg_count += 1

            except Exception as e:
                err = f"⚠️ Error: {e}"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})

    st.rerun()