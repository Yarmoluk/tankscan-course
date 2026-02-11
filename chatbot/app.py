#!/usr/bin/env python3
"""
TankScan Intelligent Textbook Chatbot

A Streamlit-based chatbot that answers questions about TankScan
wireless tank monitoring using the textbook content as its knowledge base.

Usage:
    1. Set your Anthropic API key: export ANTHROPIC_API_KEY=your-key-here
    2. Build the knowledge base: python build_knowledge_base.py
    3. Run the app: streamlit run app.py
"""

import os
from pathlib import Path

import anthropic
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="TankScan Expert Bot",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Constants ---
KNOWLEDGE_BASE_PATH = Path(__file__).parent / "knowledge_base.txt"
MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 2048


# --- Load Knowledge Base ---
@st.cache_data
def load_knowledge_base():
    """Load the compiled knowledge base from file."""
    if not KNOWLEDGE_BASE_PATH.exists():
        st.error(
            "Knowledge base not found. Run `python build_knowledge_base.py` first."
        )
        return ""
    return KNOWLEDGE_BASE_PATH.read_text()


# --- Initialize Client ---
def get_client():
    """Get the Anthropic client with API key."""
    api_key = os.environ.get("ANTHROPIC_API_KEY") or st.session_state.get("api_key")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


# --- System Prompt ---
def get_system_prompt(knowledge_base: str) -> str:
    return f"""You are the TankScan Expert Bot, an AI assistant trained on the comprehensive
TankScan Intelligent Textbook about wireless tank monitoring systems.

Your role is to answer questions about:
- TankScan products (TSR, TSU, TSP, TSC, TSD, TSG monitors)
- Wireless tank monitoring technology (radar, ultrasonic, pressure sensing)
- The Asset Intelligence Platform (AIP) cloud dashboard
- IoT architecture, cellular, Wi-Fi, and satellite connectivity
- Installation, deployment, and troubleshooting
- Industry solutions (fuel, chemicals, lubricants, waste oil, c-stores)
- Safety and compliance (C1D1, C1D2, ATEX, EPA regulations)
- Data analytics, route optimization, and fleet management
- Predictive maintenance and AI applications
- Cloud integration and APIs
- ROI and business case development

Guidelines:
- Answer based on the textbook knowledge provided below
- Be accurate and technical but accessible
- Reference specific TankScan products and features when relevant
- If asked about something not covered in the textbook, say so honestly
- Use clear formatting with bullet points and headers when helpful
- For technical calculations, show the formulas and steps

TEXTBOOK KNOWLEDGE BASE:
{knowledge_base}"""


# --- Sidebar ---
with st.sidebar:
    st.image(
        "https://img.shields.io/badge/TankScan-Expert_Bot-blue?style=for-the-badge",
        use_container_width=True,
    )
    st.title("TankScan Expert Bot")
    st.markdown("---")
    st.markdown(
        """
    **Ask me anything about:**
    - Wireless tank monitoring
    - TankScan products & platform
    - Sensor technology (radar, ultrasonic)
    - IoT architecture & connectivity
    - Installation & deployment
    - Industry solutions
    - Safety & compliance
    - Data analytics & AI
    - Cloud integration & APIs
    - ROI & business cases
    """
    )
    st.markdown("---")

    # API Key input if not set via environment
    if not os.environ.get("ANTHROPIC_API_KEY"):
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Enter your Anthropic API key to enable the chatbot",
        )
        if api_key:
            st.session_state["api_key"] = api_key

    st.markdown("---")
    st.markdown(
        "*Built from the [TankScan Intelligent Textbook]"
        "(https://github.com/Yarmoluk/tankscan-course)*"
    )
    st.markdown("*Dedicated to Craig Truempi*")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


# --- Main Chat Interface ---
st.title("🛢️ TankScan Expert Bot")
st.markdown(
    "Ask any question about wireless tank monitoring, TankScan technology, "
    "or the intelligent textbook content."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about TankScan..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get client
    client = get_client()
    if not client:
        with st.chat_message("assistant"):
            st.error(
                "Please set your Anthropic API key in the sidebar "
                "or as the ANTHROPIC_API_KEY environment variable."
            )
    else:
        # Load knowledge base
        knowledge_base = load_knowledge_base()

        # Build messages for API
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=get_system_prompt(knowledge_base),
                    messages=api_messages,
                )
                assistant_message = response.content[0].text
                st.markdown(assistant_message)

        # Save assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )

# Welcome message if no history
if not st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        - What is the TSR Cellular Monitor?
        - How does radar level measurement work?
        - What industries does TankScan serve?
        """
        )

    with col2:
        st.markdown(
            """
        - How do I select the right monitor for my tanks?
        - What is the Asset Intelligence Platform?
        - How does route optimization save 30%?
        """
        )

    with col3:
        st.markdown(
            """
        - What are C1D1 and C1D2 ratings?
        - How do I integrate TankScan with my ERP?
        - What is the ROI of tank monitoring?
        """
        )
