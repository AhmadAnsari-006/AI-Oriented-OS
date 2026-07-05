from datetime import datetime
import random
from Core import memory

def get_time():
  return datetime.now().strftime("%H:%M:%S")

def get_date():
  return datetime.now().strftime("%Y-%m-%d")        

responses = {
  "greeting": [
      "Hello! 👋 How can I help you today?",
      "Hi there! What can I do for you?",
      "Hey! 😊 What’s up?",
      "Hello! Nice to talk to you."
  ],
  "time": [
      "The current time is {time}.",
      "It’s {time} right now.",
      "Right now, the time is {time}."
  ],
  "date": [
      "Today is {date}.",
      "It’s {date} today.",
      "Today’s date is {date}."
  ],
  "exit": [
      "Goodbye! 👋 Have a great day.",
      "See you soon! 😊",
      "Bye! Take care.",
      "Exiting now. Talk to you later!"
  ],
  "history": [
      "Retrieving chat history from local database..."
  ],
  "unknown": [
      "I am not sure I understood that.",
      "Can you rephrase that?",
      "Sorry, I do not understand yet.",
      "I am still learning. Try asking something else."
  ]
}

def get_response(intent_dict): 
  intent_name = intent_dict.get('intent', 'unknown')
  
  if intent_name not in responses:
      intent_name = 'unknown'
      
  # Special override for history intent to integrate with input_processor's history prompt
  if intent_name == "history":
      from Core import input_processor
      input_processor.show_history()
      return
      
  response_template = random.choice(responses[intent_name])
  formatted_response = response_template.format(time=get_time(), date=get_date())
  print(formatted_response)
  return formatted_response
