intent_keywords = {
  "greeting": ["hi", "hello", "hey", "yo", "greetings", "sup"],
  "time": ["time", "clock", "hour"],
  "date": ["date", "day", "weeks", "month", "year", "today"],
  "exit": ["bye", "exit", "quit", "shutdown", "logout"],
  "history": ["history", "logs", "chat history", "conversations"],
  "mode_switch": ["switch to", "change mode", "set mode", "mode", "activate mode"],
  "system_status": ["status", "cpu", "memory", "telemetry", "system", "disk", "processes", "stats"],
  "biometric_auth": ["authenticate", "voice print", "master voice", "login", "register voice", "verify identity"],
  "tool_generation": ["generate script", "create tool", "write python code", "build automation", "make script", "generate tool"],
  "app_orchestration": ["open app", "run browser", "browser search", "automate browser", "launch app"],
  "productivity": ["meeting", "checklist", "tasks", "schedule", "meeting summary", "todos"],
  "multilingual": ["translate", "spanish", "french", "german", "language", "chinese", "italian"]
}

priority = {
  "exit": 10,
  "biometric_auth": 9,
  "mode_switch": 8,
  "tool_generation": 7,
  "app_orchestration": 6,
  "system_status": 5,
  "time": 4,
  "date": 4,
  "productivity": 3,
  "multilingual": 3,
  "history": 2,
  "greeting": 1,
  "unknown": 0
}

def get_initial_scores():
  return {intent: 0 for intent in intent_keywords}

intent_list = []