"""
This is where we tell the AI who it is and how to think. 
We are going to build this in three distinct parts: the LLM connection, the Agent definitions, and the Task definitions.
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM 
from crewai import Agent


# Load the API key from your .env file
load_dotenv()

def get_llm():
    """
    Sets up the Groq Llama-3 model. 
    We use temperature=0 for coding to ensure the AI is logical and doesn't 'hallucinate'.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found in .env! Did you add it?")

    return LLM(
        model="groq/llama-3.3-70b-versatile",  # ✅ "provider/model" string format
        api_key=api_key,
        temperature=0
    )

    
    
def create_agents(llm):
    """
    Creates the two specialists: The Architect (writes code) 
    and the Debugger (reviews and fixes code).
    """
    #1. The Senior Python developer(The Architect)
    architect=Agent(
        role="Senior Python developer",
        goal="Write clean, efficient, and bug-free Python code based on user requirements.",
        backstory="""You are a world-class Python engineer. Your code is modular, 
        well-documented, and follows PEP 8 standards. You specialize in creating 
        standalone scripts. If you receive error feedback, you analyze it 
        exhaustively to provide a perfect fix.""",
        llm=llm,
        allow_delegation=False, # This agent focuses solely on coding
        verbose=True ,          # This lets us see their 'thought process' in the terminal
        memory=False
    )
    
    # 2. The Senior Debugger (The Quality Gate)
    debugger=Agent(
        role="Senior QA and Debugging Engineer",
        goal='Analyze code execution results and provide clear, actionable feedback to fix any issues.',
        backstory="""You are the master of the Python Traceback. You can spot 
        a Logical Error or a Syntax Error in an instant. Your job is to look at 
        sandbox outputs and tell the Architect exactly what needs to change to 
        make the code run perfectly.""",
        llm=llm,
        allow_delegation=False,# This agent focuses solely on coding
        verbose=True  ,          # This lets us see their 'thought process' in the terminal
        memory=False
    )
    return architect, debugger

#user_goal: This is the prompt you will eventually type into your Streamlit dashboard (e.g., "Make a web scraper").
# We pass it directly into the Architect's instructions.



"""
 now we  have:

LLM Connection (get_llm)

Agent Personas (create_agents)

Task Assignments (define_tasks)
"""