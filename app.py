import streamlit as st
import os
from crew import start_self_healing_developer

# Set up the Page Config
st.set_page_config(page_title="DevPulse AI", page_icon="🤖", layout="wide")

# Custom CSS to make it look like a developer tool
st.markdown("""
    <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Fira+Code:wght@400;500&display=swap');
        
        .stApp {
            background-color: #050505;
            font-family: 'Inter', sans-serif;
        }

        /* The Neon Header */
        h1 {
            color: #00ff88;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
            letter-spacing: -1px;
            font-weight: 700;
        }

        /* Glassmorphism Card Effect for Text Areas */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #00ff88 !important;
            border-radius: 12px !important;
            padding: 15px !important;
            font-family: 'Fira Code', monospace !important;
        }

        /* Glowing Button */
        .stButton>button {
            width: 100%;
            background: linear-gradient(90deg, #00C853 0%, #B2FF59 100%);
            color: #000 !important;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 200, 83, 0.3);
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 200, 83, 0.5);
            color: #000 !important;
        }

        /* Code Block Styling */
        .stCodeBlock {
            border-radius: 12px !important;
            border: 1px solid #1E1E1E !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        /* Sidebar Glass Effect */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.8) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
    """, unsafe_allow_html=True)
st.title("🚀 DevPulse: Self-Healing Autonomous Coder")
st.info("Input a task, and watch the AI write, test, and fix code using Docker.")

# 1. User Input
user_prompt = st.text_area("What should the AI build today?", 
                           placeholder="e.g., Create a script that scrapes the top news from HackerNews and saves it to a CSV.")

if st.button("Generate & Self-Heal"):
    if user_prompt:
        # 2. Visual Placeholders
        #st.status: This is a great Streamlit feature.
        # It creates a dropdown "spinner" that shows the user exactly what the AI is doing in real-time.
        with st.status("🤖 AI Agents are thinking and coding...", expanded=True) as status:
            st.write("Connecting to Docker Sandbox...")
            
            # 3. Call the Master Loop (From Phase 3)
            #final_result: We display the output from the Docker container (the text your code printed).
            final_result, success = start_self_healing_developer(user_prompt)
            
            if success:
                status.update(label="✅ Code Working Perfectly!", state="complete", expanded=False)
            else:
                status.update(label="❌ Failed after 3 attempts.", state="error", expanded=True)

        # 4. Display Results
        st.subheader("Final Execution Result:")
        #t.code: We open the workspace/main.py file and display the actual code the AI wrote.
        # This allows you to verify it immediately.
        st.code(final_result, language="bash")

        # 5. Show the Code
        if os.path.exists("workspace/main.py"):
            st.subheader("Generated Code (workspace/main.py):")
            with open("workspace/main.py", "r") as f:
                code = f.read()
                st.code(code, language="python")
    else:
        st.warning("Please enter a goal first!")