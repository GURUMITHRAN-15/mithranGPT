# MithranGPT 🤖

**MithranGPT** is an intelligent AI chatbot built using Python, powered by the Groq API and enhanced with real-time DuckDuckGo web search.
It provides fast AI responses, a modern chat interface, and the ability to fetch live information from the web.

---

## 🚀 Features

* 🤖 AI-powered chatbot using Groq LLM models
* 🌐 Automatic web search using DuckDuckGo
* ⚡ Multiple AI model options
* 💬 Modern chat UI built with Streamlit
* 📊 Chat statistics and conversation history
* 🎛️ Adjustable AI settings (temperature, tokens)
* 🧹 Clear chat history option
* 🎨 Clean modern interface with custom CSS

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Groq API
* DuckDuckGo Search (DDGS)
* python-dotenv

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/GURUMITHRAN-15/mithranGPT.git
cd mithranGPT
```

Install dependencies:

```bash
pip install -r requirement.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the project directory and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

Start the Streamlit app:

```bash
streamlit run mithrangpt.py
```

The chatbot will open in your browser.

---

## 🧠 Available Models

MithranGPT supports multiple Groq models:

* **Llama 3.1 8B** – Fast responses
* **Llama 3.3 70B** – Powerful reasoning
* **Gemma 2 9B** – Balanced performance

Users can select the model from the sidebar.

---

## 🌐 Web Search Feature

MithranGPT automatically performs web searches when questions involve:

* Latest news
* Current events
* Weather
* Stock prices
* Sports scores
* Real-time updates

Results are fetched using DuckDuckGo and used to improve AI responses.

---

## 📁 Project Structure

```
mithranGPT/
│
├── mithrangpt.py
├── requirement.txt
├── .env
└── README.md
```

---

## 👨‍💻 Author

**Gurumithran**

Passionate Python and AI developer who created MithranGPT using Python, Streamlit, and the Groq API.

---

## ❤️ Acknowledgements

* Groq for ultra-fast AI inference
* Streamlit for the interactive web interface
* DuckDuckGo for web search capabilities

---

## 📜 License

This project is open-source and available under the MIT License.
