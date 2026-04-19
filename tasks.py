# tasks.py
from crewai import Task

def define_tasks(architect, debugger, user_goal, feedback=""):
    """
    Defines the specific work orders for our agents.
    """

    # Task 1: The Coding Task
    code_task = Task(
        description=f"""Analyze the following request: '{user_goal}'. 
        CRITICAL FEEDBACK FROM PREVIOUS ATTEMPT: 
        {feedback if feedback else "None. This is your first attempt."}
        Write a complete, standalone Python script to solve it.
        IMPORTANT: Return ONLY the Python code wrapped in a ```python ... ``` block.
        Do not add explanation outside the code block. Do not include a filename.""",
        expected_output="A complete Python script inside a ```python ... ``` code block.",
        agent=architect
    )

# The Hand-off: Notice that the code_task is assigned to the architect and the review_task is assigned to the debugger.
# This creates the "Chain of Command."
    # Task 2: The Review/Debug Task
    review_task = Task(
        description=f"""Review the Python script written for: '{user_goal}'.
        Look at the previous execution feedback: {feedback if feedback else "None."}
        Verify that the architect has fixed the issue and that the code 
        is now safe and functional.
        If changes are needed, return the COMPLETE corrected script in a ```python ... ``` block.""",
        expected_output="Either approval, or a corrected ```python ... ``` script.",
        agent=debugger
    )

    return code_task, review_task