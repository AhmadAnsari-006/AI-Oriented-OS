import os
import sys

# Ensure Chat-Bot (v2) root directory is in python search path for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core import input_processor, memory
from Intent import ml_classifier

def print_welcome_dashboard():
    active_mode = memory.get_active_mode()
    data = memory.load_memory()
    auths = data["user_profile"].get("authorized_voiceprints", [])
    
    print("\n" + "="*70)
    print("      👾 AI-ORIENTED-OS (v2): COGNITIVE COMPUTING CONSOLE 👾")
    print("="*70)
    print(f"  System Scope   : Full Environment Integration Layer")
    print(f"  Active Mode    : {active_mode} Mode")
    print(f"  Master Operator: Ahmad (Authorized Voiceprints: {', '.join([u.upper() for u in auths])})")
    print(f"  Model Engine   : ML Intent Classifier (MultinomialNB) & LLM Engine")
    print("="*70)
    print("  SIMULATION TIPS:")
    print("    - To simulate voice authentication, prefix with: [VOICE: ahmad]")
    print("    - To simulate gesture controls, prefix with: [GESTURE: gaze_detected]")
    print("    - To change modes, type: 'switch to coding mode' or 'switch to gaming'")
    print("    - To run telemetry, type: 'check system status'")
    print("    - To generate a script, type: '[VOICE: ahmad] generate script list_files'")
    print("    - To manage checklist, type: 'add task study' or 'complete task 1'")
    print("="*70 + "\n")

def main():
    # Make sure ML Model is trained and loaded
    ml_classifier.load_model()
    
    print_welcome_dashboard()
    
    while True:
        # Prompt as per legacy code structure
        question = input("Do you want to see Chat History? (yes/quit/no): ").strip().lower()
        if question == "yes":
            input_processor.show_history()
        elif question in ["quit", "exit"]:
            print("\nExiting AI-Oriented-OS Console. Goodbye! 👋")
            break
        else:
            # Runs get_input() which prompts 'USER: ' to read the system command
            input_processor.get_input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSystem interrupted. Exiting OS console.")