"""
Streamlit frontend for Bhrahma chat interface
"""
import streamlit as st
import requests
import time
from datetime import datetime
from typing import List, Dict
import uuid
import os

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Bhrahma - AI Agent System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000;
        font-weight: 500;
    }
    .status-processing {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        color: #856404;
    }
    .status-ready {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        color: #0c5460;
    }
    .message-user {
        background-color: #cfe2ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        color: #052c65;
        border-left: 4px solid #0d6efd;
    }
    .message-assistant {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        color: #084298;
        border-left: 4px solid #6c757d;
    }
    strong {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'waiting_for_response' not in st.session_state:
        st.session_state.waiting_for_response = False


def get_queue_status() -> Dict:
    """Get current queue status from API"""
    try:
        response = requests.get(f"{API_URL}/queue/status")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching queue status: {str(e)}")
    return {"queue_size": 0, "is_processing": False, "current_task": None}


def get_messages(session_id: str) -> List[Dict]:
    """Fetch messages for current session"""
    try:
        response = requests.get(f"{API_URL}/chat/{session_id}/messages")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching messages: {str(e)}")
    return []


def send_message(message: str, session_id: str) -> Dict:
    """Send message to Bhrahma"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"content": message, "session_id": session_id}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error sending message: {response.text}")
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
    return None


def get_skills() -> List[Dict]:
    """Fetch available skills"""
    try:
        response = requests.get(f"{API_URL}/skills")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching skills: {str(e)}")
    return []


def learn_new_skill(topic: str, description: str) -> Dict:
    """Request Bhrahma to learn a new skill"""
    try:
        response = requests.post(
            f"{API_URL}/skills/learn",
            json={
                "topic": topic,
                "description": description,
                "search_web": True,
                "auto_test": True
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error learning skill: {response.text}")
    except Exception as e:
        st.error(f"Error learning skill: {str(e)}")
    return None


def main():
    """Main application"""
    init_session_state()

    # Header
    st.markdown('<div class="main-header">🧠 Bhrahma AI Agent</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Session info
        st.subheader("Session")
        st.text(f"ID: {st.session_state.session_id[:8]}...")

        if st.button("New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

        st.divider()

        # Queue Status
        st.subheader("Queue Status")
        queue_status = get_queue_status()

        if queue_status['is_processing']:
            st.markdown(f"""
            <div class="status-box status-processing">
                <strong>🔄 Processing</strong><br>
                Queue: {queue_status['queue_size']} messages
            </div>
            """, unsafe_allow_html=True)

            if queue_status['current_task']:
                st.caption(f"Current: {queue_status['current_task'][:50]}...")
        else:
            st.markdown(f"""
            <div class="status-box status-ready">
                <strong>✅ Ready</strong><br>
                Queue: {queue_status['queue_size']} messages
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Skills
        st.subheader("Available Skills")
        skills = get_skills()
        st.metric("Total Skills", len(skills))

        if st.button("Refresh Skills"):
            st.rerun()

        with st.expander("View Skills"):
            for skill in skills:
                st.write(f"**{skill['name']}**")
                st.caption(f"{skill['category']} - {skill['description'][:100]}...")
                st.divider()

    # Main chat area
    st.header("💬 Chat with Bhrahma")

    # Auto-refresh messages
    if st.session_state.waiting_for_response:
        # Fetch latest messages
        messages = get_messages(st.session_state.session_id)
        if messages:
            st.session_state.messages = messages
            # Check if we got a new assistant response
            if messages[-1]['role'] == 'assistant':
                st.session_state.waiting_for_response = False
                st.rerun()

    # Display messages
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.info("👋 Hello! I'm Bhrahma, your AI agent. I can learn new skills and help you with complex tasks. How can I assist you today?")
        else:
            for msg in st.session_state.messages:
                role = msg['role']
                content = msg['content']
                timestamp = msg.get('timestamp', '')

                if role == 'user':
                    st.markdown(f"""
                    <div class="message-user">
                        <strong>You</strong> <small>{timestamp}</small><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
                elif role == 'assistant':
                    meta_data = msg.get('meta_data', {})
                    skills_used = meta_data.get('skills_used', [])

                    st.markdown(f"""
                    <div class="message-assistant">
                        <strong>Bhrahma</strong> <small>{timestamp}</small><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)

                    if skills_used:
                        st.caption(f"🔧 Skills used: {', '.join(skills_used)}")

    # Show processing indicator
    if st.session_state.waiting_for_response:
        st.info("⏳ Bhrahma is processing your request...")
        time.sleep(2)  # Wait before checking again
        st.rerun()

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Send message
        result = send_message(user_input, st.session_state.session_id)

        if result:
            # Add user message to display
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.session_state.waiting_for_response = True
            st.rerun()

    # Auto-refresh when waiting
    if st.session_state.waiting_for_response:
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()
