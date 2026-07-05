from Intent import rule_based, ml_classifier
from Core import memory, dialogue_manager
import string
import re

count = 0
unproccessed_messages = {}
proccessed_messages = {}
temp = {}
max_intents = []
temp_intent = []

def init_processor():
    """Syncs in-memory message history with disk storage."""
    global count, unproccessed_messages, proccessed_messages
    try:
        mem_data = memory.load_memory()
        unproc_list = mem_data["chat_history"]["unprocessed"]
        proc_list = mem_data["chat_history"]["processed"]
        count = len(unproc_list)
        unproccessed_messages.clear()
        proccessed_messages.clear()
        for idx, (unproc, proc) in enumerate(zip(unproc_list, proc_list), start=1):
            unproccessed_messages[f"Message{idx}"] = unproc
            proccessed_messages[f"Message{idx}"] = proc
    except Exception as e:
        pass

# Initialize history on module load
init_processor()

def get_input(user_input_string=None):
  global count, unproccessed_messages, proccessed_messages, temp, max_intents, temp_intent
  
  # Reset state per invocation to prevent cross-talk leaks
  temp.clear()
  max_intents.clear()
  temp_intent.clear()
  
  if user_input_string is not None:
      message = user_input_string
  else:
      message = input("USER: ")
      
  if not message.strip():
      return
      
  count += 1
  
  # Extract multi-modal tags if simulated (e.g. [VOICE: ahmad], [GESTURE: point_finger], [VISION: user_present])
  voice_user = None
  gesture = None
  vision_state = None
  
  tags = re.findall(r'\[(VOICE|GESTURE|VISION):\s*([^\]]+)\]', message, re.IGNORECASE)
  cleaned_text = message
  for tag, val in tags:
      cleaned_text = cleaned_text.replace(f"[{tag}: {val}]", "").replace(f"[{tag}:{val}]", "")
      if tag.upper() == "VOICE":
          voice_user = val.strip().lower()
      elif tag.upper() == "GESTURE":
          gesture = val.strip().lower()
      elif tag.upper() == "VISION":
          vision_state = val.strip().lower()
  cleaned_text = cleaned_text.strip()
  
  update_memory_unproccessed(message)
  clean_message = remove_punctuation(cleaned_text.lower())
  clean_message = clean_spaces(clean_message)
  update_memory_processed(clean_message)
  
  # Record to disk storage
  memory.add_chat_log(message, clean_message)
  
  # 1. Rule-based Intent scoring
  rule_scores = detect_intent(clean_message)
  update_score(rule_scores)
  get_priority(temp)
  check_confidence(max_intents)
  
  # 2. ML-based Intent prediction
  ml_res = ml_classifier.predict_intent(clean_message)
  
  # 3. Resolve Intent
  chosen_intent = None
  winning_confidence = 0.0
  
  # If we have matches in rule-based
  if temp_intent:
      rule_max_conf = max([d['confidence'] for d in temp_intent])
      rule_matches = [d for d in temp_intent if d['confidence'] == rule_max_conf]
      
      # Select the match with the highest priority weight
      best_intent = rule_matches[0]['intent']
      best_priority = rule_based.priority.get(best_intent, 0)
      for item in rule_matches:
          p = rule_based.priority.get(item['intent'], 0)
          if p > best_priority:
              best_priority = p
              best_intent = item['intent']
              rule_max_conf = item['confidence']
      
      chosen_intent = best_intent
      winning_confidence = rule_max_conf
  
  # Override with ML if it has strong confidence (> 0.5) or if rule-based failed
  if (chosen_intent is None) or (ml_res["intent"] != "unknown" and ml_res["confidence"] > 0.5 and rule_based.priority.get(ml_res["intent"], 0) >= rule_based.priority.get(chosen_intent, 0)):
      chosen_intent = ml_res["intent"]
      winning_confidence = ml_res["confidence"]
      
  if not chosen_intent:
      chosen_intent = "unknown"
      winning_confidence = 0.0
      
  intent_dict = {"intent": chosen_intent, "confidence": winning_confidence}
  
  # Record habits and intent list
  rule_based.intent_list.append(intent_dict)
  memory.record_intent_usage(chosen_intent)
  
  # Send to Dialogue Manager for routing and output rendering
  dialogue_manager.process_message(intent_dict, cleaned_text, voice_user, gesture, vision_state)

def clean_spaces(text):
  clean_message = " ".join(text.split())
  return clean_message  

def remove_punctuation(text):
  translator = str.maketrans('', '', string.punctuation)
  clean_message = text.translate(translator)
  return clean_message

def update_memory_unproccessed(message):
  global unproccessed_messages, count
  unproccessed_messages[f"Message{count}"] = message 

def update_memory_processed(clean_message):
  global proccessed_messages, count
  proccessed_messages[f"Message{count}"] = clean_message 

def show_history():
  global unproccessed_messages, proccessed_messages
  print("\n\t\tCHAT HISTORY")
  print("______________________________________________________")
  which = input("Do you want proccessed message or unproccessed messages (p/u)? ").strip().lower()
  if which in ["p", "processed", "proccessed"]:
    for k, v in proccessed_messages.items():
        print(f"[{k}] {v}")
    print("______________________________________________________")
  else:
    for k, v in unproccessed_messages.items():
        print(f"[{k}] {v}")
    print("______________________________________________________")

def detect_intent(clean_message):
  scores = rule_based.get_initial_scores()
  for intent_name, keywords_list in rule_based.intent_keywords.items():
    for keyword in keywords_list:
      if keyword in clean_message:
        scores[intent_name] += 1
  return scores

def update_score(score):
  global temp
  temp.clear()
  for intent_name, score_value in score.items():
    if score_value != 0:
      temp[intent_name] = score_value
  return temp

def get_priority(temp_dict):
  global max_intents
  max_intents.clear()
  if temp_dict:
    max_val = max(temp_dict.values())
    for intent_name, score_value in temp_dict.items():
      if score_value == max_val:
        max_intents.append(intent_name)
  return max_intents

def check_confidence(maximum_intents):
  global temp_intent
  temp_intent.clear()
  for intents in maximum_intents:
    matches = temp.get(intents, 0)
    total_keywords_for_intent = len(rule_based.intent_keywords[intents])
    confidence = matches/total_keywords_for_intent
    temp_intent.append({
      "intent": intents,
      "confidence": confidence
    })  