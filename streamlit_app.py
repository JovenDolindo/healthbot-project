import streamlit as st
import json
import random
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="HealthBot Dashboard",
    page_icon="🩺",
    layout="wide"
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
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return random.choice(intent["responses"])
    return "I'm sorry, I didn't quite catch that. Can you describe your symptoms? (e.g., 'Headache', 'Flu', 'Stomach pain')"

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am HealthBot. How can I help you today?"}
    ]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=50) # Health Icon
    st.title("🩺 HealthBot")
    st.caption("By: **Joven Dolindo & Fuerzas**")
    st.markdown("---")
    
    # Menu Selection
    selected = st.radio(
        "Navigation", 
        ["📊 Overview", "💬 AI Assistant", "⚙️ Settings"],
        index=1  # Default to AI Assistant
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Drink 8 glasses of water daily!")

# --- PAGE 1: OVERVIEW DASHBOARD ---
if selected == "📊 Overview":
    st.title("Dashboard Overview")
    st.subheader("Welcome back! Here is your session summary.")
    
    # Dashboard Cards (Metrics)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="📩 Messages Sent", value=len(st.session_state.messages)-1) # Minus 1 for greeting
        
    with col2:
        st.metric(label="⚡ System Status", value="Online")
        
    with col3:
        st.metric(label="🚀 Version", value="v1.0")
    
    st.markdown("---")
    
    # Quick Health Tip Section
    st.warning("🍎 **Quick Health Tip:**\n\nEating an apple a day can boost your immune system and provide essential fiber. Don't forget to wash it first!")

# --- PAGE 2: AI ASSISTANT (Chatbot) ---
elif selected == "💬 AI Assistant":
    st.title("💬 HealthBot Assistant")
    st.caption("Ask me about Flu, Diet, First Aid, and more.")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # User Input
    if prompt := st.chat_input("Type your health question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_response(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)

# --- PAGE 3: SETTINGS ---
elif selected == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.write("Manage your application preferences here.")
    
    st.toggle("Enable Dark Mode", value=True)
    st.toggle("Show Notifications", value=True)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am HealthBot. How can I help you today?"}]
        st.success("Chat history cleared!")