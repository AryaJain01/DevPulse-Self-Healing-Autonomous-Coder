import docker
import os 



#This function ensures that the bridge between Python and Docker is open and stable before we try to pass any code through it.
def get_docker_client():
    """
    Attempts to connect to the Docker Desktop application running on your computer.
    """
    try:
        # from_env() tells Python to look at your system environment variables 
        # to find the Docker Desktop application and connect to it.
        client = docker.from_env()
        return client
    except Exception as e:
        print(f"❌ Sandbox Error: Could not connect to Docker. Is Docker Desktop running?\nDetails: {e}")
        return None
    
   
def run_code_in_container(client, filename="main.py"):
    """
    Takes the connection client and a filename, then runs that file 
    inside an isolated Docker container.
    """
    # 1. Get the absolute path to your local 'workspace' folder
    # This is necessary so Docker knows exactly where to find the file on your Windows drive
    workspace_path = os.path.abspath("workspace")

    try:
        print(f"🚀 Sandbox: Launching {filename}...")
        
        # 2. This is the automated version of the command you ran manually!
        #Everything inside these parentheses is a specific instruction for that container.
        print(f"DEBUG workspace_path: {workspace_path}")
        print(f"DEBUG file exists: {os.path.exists(os.path.join(workspace_path, filename))}")
        filename = filename.strip()  
        output = client.containers.run(
            image="python:3.11-slim",         # The blueprint (recipe)
            command=["python", f"/app/{filename}"],      # This is the command the container will execute the moment it wakes up. It’s just like typing python main.py in your terminal.
            volumes={workspace_path: {'bind': '/app', 'mode': 'rw'}}, # If the AI writes a file called main.py into your Windows workspace folder, it instantly appears inside the container at /app/main.py.
            working_dir="/app",                # Start inside the portal
            remove=True,                       # Self-destruct when finished
            stderr=True,                       # IMPORTANT: Capture crashes
            stdout=True                        # Capture success messages
        )
        
        # If it reaches here, the code worked! 
        # We decode the binary output into a readable string.
        #.decode("utf-8") because Docker sends the output as raw data (bytes), and we need to turn it into a normal Python string.
        #"Black Box" recording—the exact error message that tells the AI why it failed.
        return "Success", output.decode("utf-8")

    except docker.errors.ContainerError as e:
        # 3. If the AI's code crashes, Docker triggers this error.
        # We snatch the error logs (stderr) and return them as the result.
        error_log = e.stderr.decode("utf-8")
        return "Error", error_log

    except Exception as e:
        # For any other system issues (like a missing file)
        return "System Failure", str(e)
    
"""
 This final function in sandbox.py is the one that other parts of your project (like the AI agents) will actually call. 
 It coordinates the first two functions and makes sure the result is clean and ready for the AI to read.
"""   
def execute_sandbox_workflow(filename="main.py"):
    """
    The main entry point for the sandbox. Coordinates connecting to 
    Docker and running the file.
    """
    # 1. Start the engine
    client = get_docker_client()
    
    # If we can't connect, we stop here and report the system error
    if not client:
        return "System Error", "Docker is not responding. Please check if Docker Desktop is open."

    # 2. Execute the code and capture the result
    # This calls our 'Executor' function we just wrote
    status, result = run_code_in_container(client, filename)
    
    # 3. Final cleanup and return
    # We close the connection to the Docker client to save system resources
    client.close()
    
    return status, result

# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    # This part only runs if you run sandbox.py directly.
    # It's perfect for verifying Step 1 is 100% complete.
    print("🧪 Testing Phase 1: Engine Room...")
    s, r = execute_sandbox_workflow("main.py")
    print(f"STATUS: {s}")
    print(f"RESULT:\n{r}")
        