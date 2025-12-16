import streamlit as st
import json
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="HealthBot",
    page_icon="🩺",
    layout="centered"
)

# --- LOAD DATABASE ---
@st.cache_data
def load_intents():
    with open('intents.json', 'r') as file:
        return json.load(file)

data = load_intents()

# --- LOGIC FUNCTION ---
def get_response(user_input):
    user_input = user_input.lower()
    
    # 1. Check exact/substring matches from intents
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            # Check if pattern exists in user input (Simple Keyword Matching)
            if pattern in user_input:
                return random.choice(intent["responses"])
    
    # 2. Fallback Response
    return "I'm sorry, I didn't quite catch that. Can you describe your symptoms? (e.g., 'Headache', 'Flu', 'Stomach pain')"

# --- UI LAYOUT ---
st.title("🩺 HealthBot AI")
st.write("Created by: **Joven Dolindo & Fuerzas**")
st.markdown("---")

# --- CHAT HISTORY (Para hindi mawala ang chat) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am HealthBot. How can I help you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Use unsafe_allow_html=True para gumana ang <b> at <br>
        st.markdown(message["content"], unsafe_allow_html=True)

# --- USER INPUT ---
if prompt := st.chat_input("Type your health question here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = get_response(prompt)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)