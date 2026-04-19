# crew.py
"""
Phase 3: The Orchestrator. 
    This is the most exciting part because it's the "glue" 
    that turns separate files into a living, breathing system.
"""

"""
Phase 3 Roadmap
The Core Loop: A while loop that manages the "Try -> Fail -> Fix" cycle.

The Feedback Bridge: A function that formats the Docker error so the AI can understand it.

The Final Report: A way to show you the successful code.
"""
import os
import re
from crewai import Crew, Process
from agents import get_llm, create_agents
from tasks import define_tasks
from sandbox import execute_sandbox_workflow

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)


def save_code_to_workspace(crew_result: str):
    """
    Extracts the Python code from the AI's output and saves it to workspace/main.py.
    The LLM wraps code in ```python ... ``` blocks — we parse that out.
    This is the missing bridge between what the AI *returns* and what Docker *executes*.
    """
    raw = str(crew_result)

    # Try to extract a ```python ... ``` block first
    match = re.search(r"```python\s*(.*?)```", raw, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        # Fallback: try any ``` ... ``` block
        match = re.search(r"```\s*(.*?)```", raw, re.DOTALL)
        code = match.group(1).strip() if match else raw.strip()

    filepath = os.path.join(WORKSPACE_DIR, "main.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Code saved to {filepath}")
    return filepath


def format_feedback(status, result):
    """
    Takes the sandbox output and turns it into a clear 
    instruction for the AI agents.
    """
    if status == "Success":
        return f"✅ SUCCESS: The code executed perfectly. Output:\n{result}"
    else:
        # We wrap the error in a clear 'Error Report' block
        return f"""❌ CODE EXECUTION FAILED!
        
        TRACEBACK/ERROR:
        {result}
        
        INSTRUCTION: Analyze this traceback, identify the line number and 
        the cause of the error. Rewrite the code in 'workspace/main.py' 
        to fix this specific issue."""


def run_ai_sprint(user_goal, feedback=""):
    """
    Orchestrates one 'Sprint' of the AI team. 
    They will work together to produce one version of 'main.py'.
    """
    # 1. Initialize the Brain (LLM)
    llm = get_llm()
    # 2. Create the Team (Agents)
    architect, debugger = create_agents(llm)

    # 3. Create the Work Orders (Tasks)
    # We pass the feedback here so the Architect knows if they need to fix a bug
    code_task, review_task = define_tasks(architect, debugger, user_goal, feedback)

    # 4. Assemble the Crew
    # 'Process.sequential' means Tasks are done in order: Code first, then Review.
    dev_crew = Crew(
        agents=[architect, debugger],
        tasks=[code_task, review_task],
        process=Process.sequential,
        verbose=True
    )

    # 5. Kickoff the work
    print(f"\n🤖 AI Team is starting work on: {user_goal}")
    result = dev_crew.kickoff()

    # 6. ✅ Extract the code from the AI's output and save it to workspace/main.py
    # This is the missing bridge — the LLM returns text, we write it to disk for Docker
    save_code_to_workspace(str(result))

    return result


def start_self_healing_developer(user_goal, max_retries=3):
    """
    The Grand Finale: This loop connects the Brain to the Sandbox.
    It will give the AI up to 3 chances to get the code working.
    """
    current_feedback = ""
    attempt = 1

    while attempt <= max_retries:
        print(f"\n--- 🛠️ ATTEMPT {attempt} of {max_retries} ---")

        # 1. Run the AI Sprint (Agents write the code)
        run_ai_sprint(user_goal, current_feedback)

        # 2. Run the Sandbox (Docker executes the code)
        status, result = execute_sandbox_workflow("main.py")

        # 3. Check the Result
        if status == "Success":
            print("✅ Code worked perfectly!")
            return result, True  # We stop the loop here!
        else:
            print(f"⚠️ Attempt {attempt} failed. Sending error to AI...")
            # 4. If it failed, we format the error and loop back
            current_feedback = format_feedback(status, result)
            attempt += 1

    print("❌ Max retries reached. The AI couldn't fix the bug.")
    return result, False