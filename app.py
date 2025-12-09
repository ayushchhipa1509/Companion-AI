"""
Companion AI - Memory & Personality Engine Demo

Streamlit app demonstrating:
1. Memory extraction from chat history
2. Personality-based response transformation
3. Before/After comparison
"""

import streamlit as st
import json
from pathlib import Path
from modules.memory import MemoryExtractor
from modules.personality import PersonalityEngine

# Page configuration
st.set_page_config(
    page_title="Companion AI - Memory & Personality",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def load_sample_chats():
    """Load sample chat messages from JSON file."""
    try:
        with open("data/sample_chats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def main():
    st.title("🧠 Companion AI: Memory & Personality Engine")
    st.markdown("""
    This demo shows how an AI companion can:
    - **Extract memory** from chat history (preferences, emotions, facts)
    - **Transform responses** based on personality style + user memory
    - **Personalize interactions** using extracted insights
    """)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # API Key input
        # Check if running on Streamlit Cloud (secrets available)
        try:
            api_key_from_secrets = st.secrets.get("OPENAI_API_KEY", "")
        except:
            api_key_from_secrets = ""
        
        if api_key_from_secrets:
            st.success("✅ API key loaded from Secrets (Streamlit Cloud)")
            api_key = api_key_from_secrets
        else:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key. For Streamlit Cloud, configure in Secrets.",
                value=""
            )
        
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key to use this app.")
            st.info("💡 On Streamlit Cloud: Add your key in App Settings → Secrets")
            st.stop()
        
        st.divider()
        
        # Personality selector
        st.subheader("🎭 Personality Style")
        personality_options = {
            "neutral": "Standard AI (Neutral)",
            "calm_mentor": "Calm Mentor",
            "witty_friend": "Witty Friend",
            "therapist_style": "Therapist-Style"
        }
        
        selected_personality = st.selectbox(
            "Choose personality for transformed responses:",
            options=list(personality_options.keys()),
            format_func=lambda x: personality_options[x]
        )
        
        st.info(f"Selected: **{personality_options[selected_personality]}**")
        
        st.divider()
        
        # Memory extraction button
        st.subheader("📊 Memory Extraction")
        if st.button("🔍 Extract Memory from Chats", type="primary", use_container_width=True):
            if st.session_state.chat_messages:
                with st.spinner("Analyzing chat history and extracting memory..."):
                    try:
                        extractor = MemoryExtractor(api_key=api_key)
                        st.session_state.memory = extractor.extract_memory(st.session_state.chat_messages)
                        st.success("✅ Memory extracted successfully!")
                    except Exception as e:
                        st.error(f"Error extracting memory: {str(e)}")
            else:
                st.warning("Please add chat messages first!")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📝 Chat Input", "💾 Memory Display", "🔄 Before/After Demo"])
    
    # Tab 1: Chat Input
    with tab1:
        st.header("Enter Chat Messages")
        st.markdown("Add 30 chat messages (or use sample data) to extract memory from.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Load sample chats
            sample_chats = load_sample_chats()
            if sample_chats:
                if st.button("📥 Load Sample Chats (30 messages)", use_container_width=True):
                    st.session_state.chat_messages = sample_chats
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Messages", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.memory = None
                st.rerun()
        
        # Text area for chat messages
        chat_input = st.text_area(
            "Chat Messages (one per line, or paste multiple):",
            value="\n".join(st.session_state.chat_messages),
            height=300,
            help="Enter chat messages, one per line. These will be analyzed for memory extraction."
        )
        
        if st.button("💾 Save Messages", type="primary"):
            messages = [msg.strip() for msg in chat_input.split("\n") if msg.strip()]
            st.session_state.chat_messages = messages
            st.success(f"✅ Saved {len(messages)} messages!")
            st.rerun()
        
        if st.session_state.chat_messages:
            st.info(f"📊 Currently loaded: **{len(st.session_state.chat_messages)}** messages")
    
    # Tab 2: Memory Display
    with tab2:
        st.header("Extracted Memory")
        
        if st.session_state.memory:
            memory = st.session_state.memory
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🎯 Preferences")
                if memory.get("preferences"):
                    for pref in memory["preferences"]:
                        st.markdown(f"- {pref}")
                else:
                    st.info("No preferences extracted yet.")
            
            with col2:
                st.subheader("😊 Emotional Patterns")
                if memory.get("emotional_patterns"):
                    st.markdown(memory["emotional_patterns"])
                else:
                    st.info("No emotional patterns detected.")
            
            with col3:
                st.subheader("📌 Key Facts")
                if memory.get("facts"):
                    for fact in memory["facts"]:
                        st.markdown(f"- {fact}")
                else:
                    st.info("No facts extracted yet.")
            
            st.divider()
            
            # Raw JSON view
            with st.expander("🔍 View Raw JSON"):
                st.json(memory)
        else:
            st.info("👆 Go to 'Chat Input' tab, add messages, and click 'Extract Memory' in the sidebar.")
    
    # Tab 3: Before/After Demo
    with tab3:
        st.header("Before/After Personality Comparison")
        st.markdown("""
        Ask a question and see how the response changes:
        - **Before**: Standard neutral AI response
        - **After**: Personality-transformed response (using memory if available)
        """)
        
        # User question input
        user_question = st.text_input(
            "Ask a question:",
            placeholder="e.g., How do I fix this bug?",
            help="Enter a question to see the before/after comparison"
        )
        
        if user_question:
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar.")
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🤖 Standard AI Response")
                    with st.spinner("Generating standard response..."):
                        try:
                            engine = PersonalityEngine(api_key=api_key)
                            standard_response = engine.get_standard_response(user_question, api_key)
                            st.markdown(standard_response)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                with col2:
                    personality_name = PersonalityEngine.PERSONALITIES[selected_personality]["name"]
                    st.subheader(f"🎭 {personality_name} Response")
                    
                    if st.session_state.memory:
                        st.caption("✨ Using extracted memory for personalization")
                    else:
                        st.caption("⚠️ No memory extracted yet (using personality only)")
                    
                    with st.spinner(f"Transforming to {personality_name} style..."):
                        try:
                            engine = PersonalityEngine(api_key=api_key)
                            standard_response = engine.get_standard_response(user_question, api_key)
                            transformed_response = engine.transform_response(
                                user_question=user_question,
                                standard_response=standard_response,
                                personality=selected_personality,
                                memory=st.session_state.memory
                            )
                            st.markdown(transformed_response)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                # Show memory context if available
                if st.session_state.memory:
                    with st.expander("📋 Memory Context Used"):
                        st.json(st.session_state.memory)
        else:
            st.info("👆 Enter a question above to see the before/after comparison.")
    
    # Footer
    st.divider()
    st.markdown("""
    ### 📚 How It Works
    
    1. **Memory Extraction**: Uses LLM with structured output parsing to extract:
       - User preferences (likes, dislikes, habits)
       - Emotional patterns (mood trends, triggers)
       - Key facts (name, role, constraints, goals)
    
    2. **Personality Engine**: Transforms responses by:
       - Applying personality style (tone, delivery, word choice)
       - Incorporating user memory for personalization
       - Maintaining factual accuracy while changing style
    
    3. **Structured Output**: All memory is extracted as clean JSON for easy use
    
    ### 🚀 Deployment
    - **GitHub**: [Your repo link]
    - **Streamlit Cloud**: [Your hosted link]
    """)


if __name__ == "__main__":
    main()

