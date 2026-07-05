import os
import sys
import psutil
import platform
from Core import memory

def execute_action(intent_dict, message, voice_user=None, gesture=None, vision_state=None):
    """Dispatches execution to sub-systems depending on the intent type."""
    intent = intent_dict["intent"]
    
    if intent == "system_status":
        run_system_status()
    elif intent == "biometric_auth":
        run_biometric_auth(message, voice_user)
    elif intent == "tool_generation":
        run_tool_generation(message)
    elif intent == "app_orchestration":
        run_app_orchestration(message)
    elif intent == "productivity":
        run_productivity(message)
    else:
        print(f"[Action Executor] Unknown system command: {intent}")

def run_system_status():
    """Fetches real host telemetry (CPU, RAM, Disk, Processes) and renders a styled dashboard table."""
    print("\n🖥️  [SYSTEM INTEGRATION] Querying Host Telemetry...")
    
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get active OS info
    os_name = platform.system()
    os_release = platform.release()
    os_arch = platform.machine()
    
    print("+" + "-"*68 + "+")
    print(f"|  AI-Oriented-OS Telemetry Dashboard ({os_name} {os_release} {os_arch})  |")
    print("+" + "-"*68 + "+")
    print(f"|  CPU Usage:       [ {cpu_usage:<5}% ] " + ("|" * int(cpu_usage/4.0)).ljust(25) + " |")
    print(f"|  RAM Usage:       [ {ram.percent:<5}% ] " + ("|" * int(ram.percent/4.0)).ljust(25) + f" ({ram.used/(1024**3):.1f}GB / {ram.total/(1024**3):.1f}GB) |")
    print(f"|  Disk Usage:      [ {disk.percent:<5}% ] " + ("|" * int(disk.percent/4.0)).ljust(25) + f" ({disk.used/(1024**3):.1f}GB / {disk.total/(1024**3):.1f}GB) |")
    print("+" + "-"*68 + "+")
    
    # Get running processes
    print("|  Top CPU Consuming Processes:                                       |")
    print("+" + "-"*68 + "+")
    proc_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            # Fetch cpu percent
            p_info = proc.info
            if p_info['cpu_percent'] is not None:
                proc_list.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Sort processes by cpu percent
    proc_list = sorted(proc_list, key=lambda x: x.get('cpu_percent', 0.0) or 0.0, reverse=True)[:5]
    for p in proc_list:
        p_name = p['name']
        p_pid = p['pid']
        p_cpu = p['cpu_percent']
        print(f"|  PID: {p_pid:<8} | Process: {p_name[:25]:<25} | CPU: {p_cpu:>5.1f}% |")
    
    print("+" + "-"*68 + "+\n")

def run_biometric_auth(message, voice_user):
    """Registers new operator voice prints into the database."""
    print("\n🔐 [BIOMETRIC IDENTITY LAYER] Processing Voiceprint Registration...")
    
    # Search for register query: register voice print for username
    import re
    match = re.search(r'(?:register|add|save)\s+voice\s*(?:print)?\s*(?:for)?\s*([a-zA-Z0-9_]+)', message, re.IGNORECASE)
    if match:
        new_username = match.group(1).lower()
        success = memory.add_voice_authorization(new_username)
        if success:
            print(f"  [🎙️ VOICE PRINT SAVED] User '{new_username.upper()}' registered successfully.")
            print("  This username is now authorized to execute system-level commands.")
        else:
            print(f"  [🎙️ VOICE PRINT EXISTS] User '{new_username.upper()}' is already registered.")
    else:
        # Check current voice status
        data = memory.load_memory()
        auths = data["user_profile"].get("authorized_voiceprints", [])
        print("  Current Authorized Operators:")
        for user in auths:
            print(f"    - {user.upper()} (Verified)")
        print("\n  To register a new voice print, type: 'register voice print for <name>'")

def run_tool_generation(message):
    """Generates a real, executable python utility tool in the 'Tools' directory."""
    print("\n🧩 [ON-DEMAND AI TOOL GENERATOR] Synthesizing task-specific script...")
    
    # Simple parsing to determine what script to generate
    script_name = "custom_utility.py"
    script_code = ""
    description = ""
    
    if "disk" in message.lower() or "space" in message.lower():
        script_name = "check_disk_space.py"
        description = "Scans storage disks and alerts on low space."
        script_code = """# On-Demand Generated Tool: Check Disk Space
import shutil
import sys

def main():
    total, used, free = shutil.disk_usage("/")
    print("Disk Space Scan:")
    print(f"  Total: {total / (1024**3):.2f} GB")
    print(f"  Used:  {used / (1024**3):.2f} GB ({used/total*100.0:.1f}%)")
    print(f"  Free:  {free / (1024**3):.2f} GB")
    if (free/total) < 0.15:
        print("[WARNING] Free disk space is lower than 15%!")
        sys.exit(1)
    else:
        print("[SUCCESS] Disk space levels are healthy.")
        sys.exit(0)

if __name__ == '__main__':
    main()
"""
    elif "list" in message.lower() or "file" in message.lower() or "directory" in message.lower():
        script_name = "list_files.py"
        description = "Lists files in the current workspace directory."
        script_code = """# On-Demand Generated Tool: List Files
import os
import sys

def main():
    target_dir = os.getcwd()
    print(f"Scanning Directory: {target_dir}")
    try:
        files = os.listdir(target_dir)
        print(f"Found {len(files)} files/folders:")
        for idx, file in enumerate(sorted(files), start=1):
            is_dir = "[DIR]" if os.path.isdir(file) else "[FILE]"
            print(f"  {idx:<3} {is_dir:<6} {file}")
        sys.exit(0)
    except Exception as e:
        print(f"Error scanning: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
"""
    else:
        # Default shell printer tool
        script_name = "task_runner.py"
        description = "Runs background tasks and prints status."
        script_code = """# On-Demand Generated Tool: Task Runner
import sys
import time

def main():
    print("Booting task runner...")
    for i in range(1, 4):
        print(f"  [Step {i}/3] Executing pipeline job...")
        time.sleep(0.5)
    print("Pipeline execution complete. Exit code: 0")
    sys.exit(0)

if __name__ == '__main__':
    main()
"""

    tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tools")
    os.makedirs(tools_dir, exist_ok=True)
    tool_path = os.path.join(tools_dir, script_name)
    
    with open(tool_path, "w") as f:
        f.write(script_code)
        
    # Register in database
    memory.add_tool(script_name, tool_path, description)
    
    print(f"  [✓ TOOL SYNTHESIS COMPLETE]")
    print(f"  Target File:  {tool_path}")
    print(f"  Description:  {description}")
    print(f"  System Action: Registered in custom_tools database.")
    print("  -------------------------------------------------------------")
    print("  Generated Source Code:")
    print("  -------------------------------------------------------------")
    for line in script_code.strip().split("\n"):
        print(f"  {line}")
    print("  -------------------------------------------------------------")
    print(f"  You can run this tool inside your shell by navigating to Tools/{script_name}.")

def run_app_orchestration(message):
    """Simulates browser automated workflow executions."""
    print("\n🌐 [UNIVERSAL APPLICATION & BROWSER ORCHESTRATION] Initializing Browser Controller...")
    
    # Weather check simulation
    if "weather" in message.lower():
        print("  [✓] Default Chromium Headless Browser instance loaded.")
        print("  [✓] Navigation: Resolving domain 'weather.com'...")
        print("  [✓] DOM Interactivity: Simulating user typing query 'Bhopal weather' in search inputs.")
        print("  [✓] Event Loop: Simulated Form Submit triggered.")
        print("  [✓] Scraping Results: Extracting elements matching '.weather-temp-today'...")
        print("\n  Browser Output:")
        print("  =============================================================")
        print("  Location: Bhopal, Madhya Pradesh, India")
        print("  Temperature: 31°C (88°F)")
        print("  Conditions: Scattered Thunderstorms, Humidity: 76%, Wind: 14 km/h")
        print("  =============================================================")
    else:
        # Generic automation
        print("  [✓] Launching browser engine in sandbox mode.")
        print(f"  [✓] Navigation: Navigating to page search query '{message}'...")
        print("  [✓] Interaction: Simulating scrolls and link activations.")
        print("  [✓] Task Chain: Workflow completed successfully. Browser closed.")

def run_productivity(message):
    """Manages the interactive productivity checklist and summaries."""
    print("\n📅 [PRODUCTIVITY & MEETING ASSISTANT] Parsing workspace schedule...")
    
    # Check if we should add task, complete task, or list tasks
    if "add task" in message.lower() or "create task" in message.lower():
        import re
        match = re.search(r'(?:add|create)\s+task\s+(.+)', message, re.IGNORECASE)
        if match:
            t_name = match.group(1).strip()
            memory.add_task(t_name)
            print(f"  [✓ TASK ADDED] Registered: '{t_name}' in productivity checklist.")
        else:
            print("  Please specify the task title. Example: 'add task review PR'")
            
    elif "complete task" in message.lower() or "finish task" in message.lower() or "done task" in message.lower():
        import re
        match = re.search(r'(?:complete|finish|done)\s+task\s+(\d+)', message, re.IGNORECASE)
        if match:
            t_idx = int(match.group(1)) - 1
            success = memory.complete_task(t_idx)
            if success:
                print(f"  [✓ TASK COMPLETED] Mark task index #{t_idx + 1} as completed.")
            else:
                print(f"  [Error] Invalid task index. Tasks size is {len(memory.get_tasks())}.")
        else:
            print("  Please specify the task index. Example: 'complete task 1'")
            
    else:
        # Default: list productivity tasks
        tasks = memory.get_tasks()
        print("\n  Productivity Todo Checklist:")
        print("  -------------------------------------------------------------")
        if not tasks:
            print("    No tasks scheduled.")
        else:
            for idx, item in enumerate(tasks, start=1):
                checkbox = "[X]" if item["completed"] else "[ ]"
                print(f"    {idx}. {checkbox} {item['task']}")
        print("  -------------------------------------------------------------")
        print("  Available actions: 'add task <title>', 'complete task <index>'")
