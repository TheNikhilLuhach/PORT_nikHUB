import streamlit as st
import os
from gemini_api import generate_project_ideas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Tech2Idea Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add server configuration for port management
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--server.port":
        port = sys.argv[2]
    else:
        port = 7864  # Use a different port to avoid conflicts

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        border-left: 5px solid;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left-color: #4facfe;
        color: white;
        margin-left: 2rem;
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -2.5rem;
        top: 1rem;
        font-size: 1.2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left-color: #ff6b6b;
        color: white;
        margin-right: 2rem;
        position: relative;
    }
    
    .assistant-message::before {
        content: "🤖";
        position: absolute;
        right: -2.5rem;
        top: 1rem;
        font-size: 1.2rem;
    }
    
    .project-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.8rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .skill-tag {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(255, 154, 158, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }
    
    .input-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .typing-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .chat-bubble {
        position: relative;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .chat-bubble::after {
        content: '';
        position: absolute;
        bottom: 0;
        width: 0;
        height: 0;
        border: 10px solid transparent;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .user-bubble::after {
        right: -10px;
        border-left-color: #764ba2;
        border-bottom-left-radius: 0;
    }
    
    .assistant-bubble {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    .assistant-bubble::after {
        left: -10px;
        border-right-color: #f5576c;
        border-bottom-right-radius: 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'last_topic' not in st.session_state:
        st.session_state.last_topic = None
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False

def extract_name(message):
    """Extract name from message if present."""
    name_keywords = ["my name is", "i am", "i'm", "this is"]
    message_lower = message.lower()
    
    for keyword in name_keywords:
        if keyword in message_lower:
            # Get the part after the keyword
            name_part = message_lower.split(keyword)[1].strip()
            # Take the first word as the name
            name = name_part.split()[0].capitalize()
            return name
    return None

def process_input(message):
    """Process user input and generate project ideas."""
    # Convert message to lowercase for easier matching
    message_lower = message.lower()
    
    # Check for name introduction
    name = extract_name(message)
    if name:
        st.session_state.user_name = name
        response = f"Nice to meet you, {name}! I'm your Tech2Idea assistant. I can help you generate project ideas based on your skills and technologies. What would you like to explore today?"
        return response
    
    # Check for greetings
    greetings = ["hi", "hello", "hey", "greetings", "howdy"]
    if any(greeting in message_lower for greeting in greetings):
        if st.session_state.user_name:
            response = f"Hello again, {st.session_state.user_name}! How can I help you with project ideas today?"
        else:
            response = "Hello! I'm your Tech2Idea assistant. I can help you generate project ideas based on your skills and technologies. What's your name?"
        return response
    
    # Check for help requests
    help_keywords = ["help", "what can you do", "how does this work", "explain"]
    if any(keyword in message_lower for keyword in help_keywords):
        help_response = f"""I can help you with:
1. Generating project ideas based on your skills
2. Suggesting technologies for specific domains
3. Providing guidance on project development

Just tell me about your skills or what kind of project you're interested in, and I'll help you get started!"""
        if st.session_state.user_name:
            help_response = f"Hi {st.session_state.user_name}!\n" + help_response
        return help_response
    
    # Check if the message contains any of the expected keywords
    valid_keywords = ["skills", "technology", "project", "idea", "generate", "build", "create", "develop"]
    if not any(keyword in message_lower for keyword in valid_keywords):
        response = "I'm here to help you with project ideas and technology suggestions! I can assist you with:\n- Generating project ideas based on your skills\n- Suggesting technologies for specific domains\n- Providing guidance on project development\n\nWhat would you like to explore?"
        if st.session_state.user_name:
            response = f"Hi {st.session_state.user_name}!\n" + response
        return response
    
    # Extract skills from the message
    skills = message.strip()
    
    # Generate project ideas
    response = generate_project_ideas(skills, None)
    
    # Add personalization to the response
    if st.session_state.user_name:
        response = f"Here are some project ideas for you, {st.session_state.user_name}:\n\n" + response
    
    return response

# Initialize session state
init_session_state()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Tech2Idea Chatbot</h1>
    <p>Chat with me to transform your technical skills into unique project ideas!</p>
    <p>Just tell me about your skills and technologies, and I'll help you generate project ideas.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user info and quick actions
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">👤 User Information</h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.user_name:
        st.success(f"**Welcome, {st.session_state.user_name}!**")
    else:
        st.info("**Please introduce yourself!**")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">⚡ Quick Actions</h3>
        <h4 style="color: #333; margin-bottom: 0.5rem;">🎯 Popular Skills</h4>
    """, unsafe_allow_html=True)
    
    # Quick skill buttons
    popular_skills = [
        "Python", "JavaScript", "React", "Node.js", "Machine Learning",
        "Data Science", "Web Development", "Mobile Development", "AI/ML"
    ]
    
    for skill in popular_skills:
        if st.button(f"💻 {skill}", key=f"skill_{skill}", use_container_width=True):
            # Add the skill message directly to chat history
            skill_message = f"I know {skill}"
            st.session_state.chat_history.append(("user", skill_message))
            response = process_input(skill_message)
            st.session_state.chat_history.append(("assistant", response))
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">🔧 Tools</h3>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("📊 View Stats", key="view_stats"):
        st.info(f"**Chat Statistics:**")
        st.write(f"• Messages: {len(st.session_state.chat_history)}")
        st.write(f"• User: {st.session_state.user_name or 'Not set'}")
        st.write(f"• Last topic: {st.session_state.last_topic or 'None'}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main chat interface
st.markdown("""
<div class="chat-container">
    <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">💬 Chat Interface</h3>
""", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for i, (role, content) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"""
            <div class="chat-bubble user-bubble">
                <strong>You:</strong><br>
                {content}
                <div class="message-time">Just now</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble assistant-bubble">
                <strong>Assistant:</strong><br>
                {content}
                <div class="message-time">Just now</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input section
st.markdown("""
<div class="input-section">
    <h3 style="text-align: center; color: white; margin-bottom: 1rem;">📝 Send Message</h3>
""", unsafe_allow_html=True)

# Create input columns
col1, col2 = st.columns([4, 1])

with col1:
    # Check if we need to clear the input
    if st.session_state.clear_input:
        user_input = st.text_area(
            "Your Message",
            placeholder="Tell me about your skills and technologies...",
            height=100,
            key="text_input",
            value=""
        )
        st.session_state.clear_input = False
    else:
        user_input = st.text_area(
            "Your Message",
            placeholder="Tell me about your skills and technologies...",
            height=100,
            key="text_input"
        )

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    send_button = st.button("🚀 Send", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Process input when send button is clicked or Enter is pressed
if send_button and user_input.strip():
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))
    
    # Process the message
    response = process_input(user_input)
    
    # Add assistant response to history
    st.session_state.chat_history.append(("assistant", response))
    
    # Set flag to clear input on next render
    st.session_state.clear_input = True
    
    # Rerun to update the display
    st.rerun()

# Handle Enter key press
if user_input and user_input.strip() and not send_button:
    # This will be handled by the button click above
    pass

# Footer with additional information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h4>🎯 How to Use</h4>
    <p>1. <strong>Introduce yourself:</strong> "My name is [Your Name]"</p>
    <p>2. <strong>Share your skills:</strong> "I know Python, JavaScript, and React"</p>
    <p>3. <strong>Get project ideas:</strong> The AI will generate personalized project suggestions</p>
    <p>4. <strong>Ask for help:</strong> Type "help" for more information</p>
</div>
""", unsafe_allow_html=True)

# Display recent project ideas if available
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("💡 Recent Project Ideas")
    
    # Find the last project ideas response
    for role, content in reversed(st.session_state.chat_history):
        if role == "assistant" and ("project ideas" in content.lower() or "project name" in content.lower()):
            st.markdown(f"""
            <div class="project-card">
                <h4>🎯 Latest Suggestions</h4>
                <div style="white-space: pre-line;">{content}</div>
            </div>
            """, unsafe_allow_html=True)
            break

# Add some helpful tips
with st.expander("💡 Tips for Better Results"):
    st.markdown("""
    **🎯 For Best Results:**
    
    1. **Be Specific:** Instead of "I know programming", say "I know Python, JavaScript, and React"
    2. **Mention Domains:** "I'm interested in web development" or "I want to work on AI projects"
    3. **Include Experience Level:** "I'm a beginner in Python" or "I'm advanced in machine learning"
    4. **Specify Interests:** "I want to build mobile apps" or "I'm interested in data visualization"
    
    **🚀 Example Messages:**
    - "My name is Alex and I know Python, JavaScript, and React. I want to build web applications."
    - "I'm a beginner in machine learning and I know Python. I want to work on AI projects."
    - "I know Java, Android development, and I want to create mobile apps."
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #1222;'>
    <p>Tech2Idea Chatbot - Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True) 