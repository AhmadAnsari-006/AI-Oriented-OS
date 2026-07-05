import random

def print_mode_intro(mode):
    """Prints a premium transition banner when entering a new mode environment."""
    headers = {
        "Coding": "💻 CODING MODE ACTIVE - CORE COGNITIVE COMPLIANCE INSTRUCTIONS LOADED",
        "Gaming": "🎮 GAMING MODE ACTIVE - PERFORMANCE POLICIES & FRAME SCHEDULERS ENGAGED",
        "Medical": "🏥 MEDICAL MODE ACTIVE - HEALTH INFORMATICS & DIAGNOSTICS PLATFORM ENABLED",
        "Data / Statistical": "📊 DATA / STATISTICAL MODE ACTIVE - NUMERICAL ENGINE & TELEMETRY READY",
        "Education": "🎓 EDUCATION MODE ACTIVE - ACADEMIC ASSISTANT & CONCEPT EXPLAINER READY",
        "Productivity": "🧑‍💼 PRODUCTIVITY MODE ACTIVE - WORKFLOW AUTOMATIONS & CALENDAR INTEGRATIONS ACTIVE"
    }
    
    intros = {
        "Coding": "System optimized for low-latency code syntax parsing, script synthesis, and documentation reading.\nTool generators and file modification APIs are fully unlocked for verified voiceprints.",
        "Gaming": "Overclocking telemetry engaged. CPU scheduling priorities boosted. Ambient background services minimized.\nLet me know what games or hardware configurations you want to monitor.",
        "Medical": "System connected to the medical ontology databases.\nWARNING: All outputs are generated for educational and simulator purposes. Consult professional physicians for critical clinical decisions.",
        "Data / Statistical": "Statistical processing modules loaded. Ready to parse CSVs, summarize data arrays, and calculate variance, mean, or standard deviations.",
        "Education": "Curriculum-oriented parsing active. Responses will focus on structural breakdowns, summaries, and self-test quizzes.",
        "Productivity": "Workspace automation engines initialized. Ready to record meeting minutes, manage task lists, and write emails."
    }
    
    header = headers.get(mode, "🌟 ADAPTIVE MODE ACTIVE")
    intro = intros.get(mode, "System parameters configured.")
    
    print("\n" + "="*70)
    print(header)
    print("="*70)
    print(intro)
    print("="*70 + "\n")

def generate_response(message, intent_dict, mode):
    """Generates realistic LLM answers, adapting the tone and layout according to the active mode."""
    print(f"\n[🧠 LLM ENGINE] (Processing query in {mode} Mode...)")
    
    # 1. Coding Mode Responses
    if mode == "Coding":
        if "python" in message.lower() or "code" in message.lower() or "write" in message.lower() or "how" in message.lower():
            print("```python\n# Adaptive generated script inside Coding Mode\n")
            print("def reverse_list(data_list):\n    \"\"\"Reverses a given list in-place and returns it.\"\"\"\n    left, right = 0, len(data_list) - 1\n    while left < right:\n        data_list[left], data_list[right] = data_list[right], data_list[left]\n        left += 1\n        right -= 1\n    return data_list\n\n# Example usage:\nprint(reverse_list([1, 2, 3, 4, 5]))  # Output: [5, 4, 3, 2, 1]\n```")
            print("\nThis script runs in O(N) time complexity and uses O(1) extra space. You can request tool execution with a verified voiceprint (e.g. '[VOICE: ahmad] generate script to reverse a list').")
        else:
            print("System is ready for coding queries. You can ask for code examples, algorithms, or script generations. \nExample: 'Write a python script to check disk space'.")
            
    # 2. Gaming Mode Responses
    elif mode == "Gaming":
        if "fps" in message.lower() or "performance" in message.lower() or "boost" in message.lower():
            print("🎮 [Gaming Optimizer Toolkit] Recommended Steps for Maximum FPS:")
            print("  1. Enable Windows Hardware-Accelerated GPU Scheduling (HAGS).")
            print("  2. Force '.venv/Scripts/python.exe' and game processes to use the Discrete GPU via Graphics Settings.")
            print("  3. Set Windows Power Plan to 'Ultimate Performance'.")
            print("  4. Limit background telemetry apps. The current AI-Oriented-OS gaming mode has suspended 3 background threads.")
        else:
            print("Gaming mode is active. System resources are diverted to peak application performance. Ask me about game optimization, frame times, or system configs.")
            
    # 3. Medical Mode Responses
    elif mode == "Medical":
        print("🩺 [Medical Simulator Node] Diagnostic Synthesis:")
        print("  Based on clinical symptoms parser, potential factors have been mapped. However, clinical diagnoses require doctor examination.")
        print("\n  > [!WARNING]")
        print("  > Medical advice disclaimer: AI outputs do not replace professional medical evaluations. Please visit a certified doctor for health concerns.")
        
    # 4. Data / Statistical Mode Responses
    elif mode == "Data / Statistical":
        words = message.split()
        word_count = len(words)
        char_count = len(message)
        print("📊 [Data Analytics Engine] Text Analysis Summary:")
        print(f"  - Word Count: {word_count}")
        print(f"  - Character Count (including spaces): {char_count}")
        print(f"  - Vocabulary Density: {len(set(words))/word_count:.2f}" if word_count > 0 else "0.0")
        print("\nYou can paste CSV strings or numerical datasets here to calculate statistical distributions.")
        
    # 5. Education Mode Responses
    elif mode == "Education":
        print("📚 [Academic Study Assistant]")
        print(f"  Topic Breakdown: Explain '{message}'")
        print("  -------------------------------------------------------------")
        print("  Core Concept: AI-Oriented-OS shifts the computing paradigm from graphical user interfaces (GUI) to intent-based interaction models.")
        print("  Key Vocabulary: Intent Parsing, Signal Fusion, Biometric Authentication, Agent Orchestration.")
        print("\n📝 Quick Quiz: What is the primary channel of command in AI-Oriented-OS?")
        print("  (Type your answer or ask for more details!)")
        
    # 6. Productivity Mode (Default) Responses
    else:
        # Check translation keywords for multilingual support
        if intent_dict["intent"] == "multilingual":
            translations = {
                "spanish": "Hola! ¿Cómo puedo ayudarte hoy? El sistema AI-Oriented-OS está listo.",
                "german": "Hallo! Wie kann ich Ihnen heute helfen? Das AI-Oriented-OS System ist bereit.",
                "french": "Bonjour! Comment puis-je vous aider aujourd'hui? Le système AI-Oriented-OS est prêt.",
                "italian": "Ciao! Come posso aiutarti oggi? Il sistema AI-Oriented-OS è pronto."
            }
            target_lang = "spanish"
            for lang in translations:
                if lang in message.lower():
                    target_lang = lang
                    break
            print(f"\n🌐 [Multilingual Translator Engine] Translated output ({target_lang.capitalize()}):")
            print(f"  \"{translations[target_lang]}\"")
        else:
            print("Welcome operator. I am the cognitive interface of AI-Oriented-OS (v2).")
            print("I process natural language, authenticate operators, and orchestrate underlying operating systems.")
            print("Try checking my telemetry by typing 'check system status' or switch environments with 'switch to coding mode'.")
            
    print("="*70)
