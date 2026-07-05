from Core import memory
from Response import template_engine, llm_engine, action_executor
import re

def process_message(intent_dict, message, voice_user=None, gesture=None, vision_state=None):
    """Processes the intent, performs security checks, handles mode transitions, and dispatches responses."""
    intent = intent_dict["intent"]
    confidence = intent_dict["confidence"]
    
    # Retrieve active environment mode
    active_mode = memory.get_active_mode()
    
    # 1. Security Check: Sensitive system commands require biometric voice verification
    sensitive_intents = ["tool_generation", "app_orchestration"]
    
    # Check if this is a sensitive action
    is_sensitive = intent in sensitive_intents
    
    # Biometric auth registration is also sensitive
    if intent == "biometric_auth" and any(kwd in message.lower() for kwd in ["register", "add"]):
        is_sensitive = True
        
    if is_sensitive:
        if not voice_user:
            print("\n[🛡️ SECURITY WARNING] Privilege escalation blocked.")
            print(">>> Reason: Biometric Voice Verification required for system-scope operations.")
            print(">>> Solution: Prefix command with acoustic print identifier: [VOICE: <username>]")
            return
            
        if not memory.is_voice_authorized(voice_user):
            print(f"\n[🛡️ SECURITY FAILURE] Biometric Voice signature unrecognized.")
            print(f">>> Reason: '{voice_user}' is not registered as an authorized operator voiceprint.")
            print(">>> Solution: Register this voice print or authenticate with a master key.")
            return
            
        # If authorized, print verification badge
        print(f"  [🎙️ VOICE KEY VERIFIED] Authorized operator: {voice_user.upper()} (Continuous Verification Active)")

    # 2. Handle Mode Switching
    if intent == "mode_switch":
        # Scan message for mode keywords
        modes = {
            "coding": "Coding",
            "gaming": "Gaming",
            "medical": "Medical",
            "data": "Data / Statistical",
            "statistical": "Data / Statistical",
            "education": "Education",
            "productivity": "Productivity"
        }
        
        target_mode = None
        for key, mode_name in modes.items():
            if key in message.lower():
                target_mode = mode_name
                break
                
        if target_mode:
            memory.set_active_mode(target_mode)
            print(f"\n[🔄 OS MODE SWITCHED] Transitioning system environment to: {target_mode} Mode.")
            # Trigger mode transition greetings or custom engine responses
            llm_engine.print_mode_intro(target_mode)
            return
        else:
            print("\n[🔄 OS MODE SWITCH] Available environment modes:")
            for m in set(modes.values()):
                print(f"  - {m} Mode")
            print("Please specify which mode you want to activate (e.g., 'switch to coding mode').")
            return

    # 3. Mode adaptation for general queries (if gesture indicates user looking away, alert them)
    if vision_state == "away":
        print("\n[👁️ VISUAL INTERACTION] System paused: Operator gaze detected away from terminal screen.")
        return

    if gesture == "gaze_detected":
        print("  [👁️ VISUAL FEEDBACK] Presence and attention confirmed.")

    # 4. Routing
    # A. System-scope commands go to Action Executor
    action_intents = ["system_status", "tool_generation", "app_orchestration", "biometric_auth", "productivity"]
    if intent in action_intents:
        action_executor.execute_action(intent_dict, message, voice_user, gesture, vision_state)
        
    # B. Basic informational intents go to Template Engine
    elif intent in ["greeting", "time", "date", "exit", "history"]:
        template_engine.get_response(intent_dict)
        
    # C. Dynamic conversational intents (or unknown query in specialized mode) go to LLM Engine
    else:
        llm_engine.generate_response(message, intent_dict, active_mode)
