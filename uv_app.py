import streamlit as st
import requests

# -------------- Page Config ----------------
st.set_page_config(
    page_title="🔮 Multi-Model Chat via OpenRouter",
    page_icon="🤖",
    layout="wide",
)

# -------------- Title ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🔮 Multi-Model Chat</h1>
    <h4 style='text-align: center; color: gray;'>Talk to multiple AI models side-by-side using <a href='https://openrouter.ai' target='_blank'>OpenRouter</a></h4>
    <br>
    """, unsafe_allow_html=True
)

# -------------- Sidebar ----------------
st.sidebar.header("🔧 Settings")
st.sidebar.markdown("Choose the models you want to use:")

# ✅ Final tested working models
model_options = {
    "GPT-3.5 (OpenAI)": "openai/gpt-3.5-turbo",
    "Mistral-7B (MistralAI)": "mistralai/mistral-7b-instruct",
    "LLaMA 3-8B (Meta)": "meta-llama/llama-3-8b-instruct",
    "PPLX-7B Online (Perplexity)": "perplexity/pplx-7b-online",
    "Nous Hermes-2 Mixtral": "nousresearch/nous-hermes-2-mixtral"
}

selected_models = st.sidebar.multiselect("Select AI Models", list(model_options.keys()), default=list(model_options.keys()))

# -------------- Prompt Input ----------------
st.markdown("### ✏️ Enter your prompt below:")
user_input = st.text_area("Prompt", height=120, placeholder="Ask anything...")

# 🔐 Your OpenRouter API key here
# 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
API_KEY = "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"

# -------------- Query Function ----------------
def query_model(model, prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512  # reduce to avoid token errors
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ **Error {response.status_code}**: {response.text}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

# -------------- Main Execution ----------------
if user_input and selected_models:
    st.markdown("## 🧠 AI Model Responses:")
    for model_name in selected_models:
        model_id = model_options[model_name]
        with st.spinner(f"🤖 Getting response from `{model_name}`..."):
            reply = query_model(model_id, user_input)
            with st.expander(f"💬 Response from {model_name}", expanded=True):
                st.markdown(f"<div style='color:#222;padding:5px;'>{reply}</div>", unsafe_allow_html=True)
else:
    st.markdown("> ⬅️ Use the sidebar to select models and enter a prompt above to begin chatting!")

# -------------- Footer ----------------
st.markdown("---")
st.markdown("<small style='color:gray;'>Made with ❤️ using Streamlit and OpenRouter API</small>", unsafe_allow_html=True)
