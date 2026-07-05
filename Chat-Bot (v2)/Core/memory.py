import os
import json

MEMORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "user_memory.json")

DEFAULT_MEMORY = {
    "user_profile": {
        "username": "Ahmad",
        "authorized_voiceprints": ["ahmad"],
        "active_mode": "Productivity",
        "learned_habits": {
            "frequent_intents": {}
        }
    },
    "chat_history": {
        "unprocessed": [],
        "processed": []
    },
    "custom_tools": [],
    "productivity_tasks": [
        {"task": "Initialize AI-Oriented-OS", "completed": True},
        {"task": "Train ML intent classifier", "completed": True},
        {"task": "Configure voice verification", "completed": False}
    ]
}

def load_memory():
    """Loads memory from Data/user_memory.json. Initializes with defaults if file doesn't exist or is invalid."""
    if not os.path.exists(MEMORY_PATH) or os.path.getsize(MEMORY_PATH) == 0:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY
        
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
            # Ensure key structures exist
            for key in DEFAULT_MEMORY:
                if key not in data:
                    data[key] = DEFAULT_MEMORY[key]
            return data
    except Exception as e:
        print(f"[Memory] Error loading memory file: {e}. Resetting to defaults.")
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY

def save_memory(data):
    """Saves memory to Data/user_memory.json."""
    try:
        os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
        with open(MEMORY_PATH, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[Memory] Error saving memory: {e}")

def add_chat_log(message, clean_message):
    """Appends messages to raw and cleaned history lists."""
    data = load_memory()
    data["chat_history"]["unprocessed"].append(message)
    data["chat_history"]["processed"].append(clean_message)
    save_memory(data)

def get_history(processed_type=True):
    """Retrieves chat logs."""
    data = load_memory()
    key = "processed" if processed_type else "unprocessed"
    return data["chat_history"][key]

def clear_history():
    """Clears history."""
    data = load_memory()
    data["chat_history"]["processed"] = []
    data["chat_history"]["unprocessed"] = []
    save_memory(data)

def get_active_mode():
    """Returns the current active system mode."""
    data = load_memory()
    return data["user_profile"].get("active_mode", "Productivity")

def set_active_mode(mode):
    """Updates the active system mode."""
    data = load_memory()
    data["user_profile"]["active_mode"] = mode
    save_memory(data)

def is_voice_authorized(username):
    """Checks if the voice username is registered in authorized_voiceprints."""
    data = load_memory()
    auth_list = data["user_profile"].get("authorized_voiceprints", [])
    return username.lower() in [name.lower() for name in auth_list]

def add_voice_authorization(username):
    """Adds a new voice signature authorization."""
    data = load_memory()
    auth_list = data["user_profile"].setdefault("authorized_voiceprints", [])
    if username.lower() not in [name.lower() for name in auth_list]:
        auth_list.append(username)
        save_memory(data)
        return True
    return False

def record_intent_usage(intent):
    """Tracks frequency of intents for user habits."""
    data = load_memory()
    habits = data["user_profile"].setdefault("learned_habits", {}).setdefault("frequent_intents", {})
    habits[intent] = habits.get(intent, 0) + 1
    save_memory(data)

def get_tasks():
    """Returns the productivity tasks list."""
    data = load_memory()
    return data.get("productivity_tasks", [])

def add_task(task_name):
    """Adds a task."""
    data = load_memory()
    data.setdefault("productivity_tasks", []).append({"task": task_name, "completed": False})
    save_memory(data)

def complete_task(task_idx):
    """Marks task at index as completed."""
    data = load_memory()
    tasks = data.setdefault("productivity_tasks", [])
    if 0 <= task_idx < len(tasks):
        tasks[task_idx]["completed"] = True
        save_memory(data)
        return True
    return False

def get_tools():
    """Returns custom generated tools."""
    data = load_memory()
    return data.get("custom_tools", [])

def add_tool(name, path, description):
    """Registers a generated tool."""
    data = load_memory()
    data.setdefault("custom_tools", []).append({
        "name": name,
        "path": path,
        "description": description
    })
    save_memory(data)
