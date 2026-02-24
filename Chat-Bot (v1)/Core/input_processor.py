from Intent import rule_based
import string
count = 0
max_score = 0
unproccessed_messages = {}
proccessed_messages = {}
temp = {}

def get_input():
  global count, unproccessed_messages, proccessed_messages, temp
  message = input("USER: ")
  count += 1
  
  update_memory_unproccessed(message)
  clean_message = remove_punctuation(message.lower())
  clean_message= clean_spaces(clean_message)
  update_memory_processed(clean_message)
  detect_intent(clean_message)
  update_score(rule_based.score)
  get_priority(temp)
  print(rule_based.score)

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
  print("\n\t\tCHAT HISTORY")
  print("______________________________________________________")
  which = input("Do you want proccessed message or unproccessed messages?")
  if which == "proccessed":
    print("\n",proccessed_messages)
    print("______________________________________________________")
  else:
    print("\n",unproccessed_messages)
    print("______________________________________________________")

def detect_intent(clean_message):
  for intent_name, keywords_list in rule_based.intent_keywords.items():
    for keyword in keywords_list:
      if keyword in clean_message:
        rule_based.score[intent_name] += 1
  return rule_based.score

def update_score(score):
  global temp
  for intent_name, score_value in score.items():
    if score_value !=0:
      temp[intent_name] = score_value
    else:
      continue
  return temp

def get_priority(temp):
  max_intents = []
  for intent_name, score_value in temp.items():
    if temp:
      max_score = max(temp.values())
      if score_value == max_score :
        max_intents.append(intent_name)
      else:
        max_intents.append("unknown")
  return max_intents