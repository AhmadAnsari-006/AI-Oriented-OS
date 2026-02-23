from Core import memory
import string
count = 0

def get_input():
  global count
  message = input("USER: ")
  count += 1
  
  update_memory_unproccessed(message)
  clean_message = remove_punctuation(message.lower())
  clean_message= clean_spaces(clean_message)
  update_memory_processed(clean_message)

def clean_spaces(text):
  clean_message = " ".join(text.split())
  return clean_message  

def remove_punctuation(text):
  translator = str.maketrans('', '', string.punctuation)
  clean_message = text.translate(translator)
  return clean_message

def update_memory_unproccessed(message):
  memory.unproccessed_messages[f"Message{count}"] = message 

def update_memory_processed(clean_message):
  memory.proccessed_messages[f"Message{count}"] = clean_message 

def show_history():
  print("CHAT HISTORY")
  which = input("Do you want proccessed message or unproccessed messages?")
  if which == "proccessed":
    print(memory.proccessed_messages)
  else:
    print(memory.unproccessed_messages)