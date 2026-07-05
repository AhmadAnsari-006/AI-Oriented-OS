from Intent import rule_based
from datetime import datetime
import random

intent  = rule_based.intent_list.value()

def get_time():
  return(datetime.now().strftime("%H:%M:%S"))
def get_date():
  return(datetime.now().date())        
time = get_time()
date = get_date()
responses = {
  "greeting":[
          "Hello! 👋 How can I help you? ",
          "Hi there! What can I do for you?",
          "Hey! 😊 What’s up?",
          "Hello! Nice to talk to you."
          ],
  "time":[
          "The current time is {time}.",
          "It’s {time} right now.",
          "Right now, the time is {time}."
          ],
  "date":[
          "Today is {date}.",
          "It’s {date} today.",
          "Today’s date is {date}."
          ],
  "exit":[
          "Goodbye! 👋 Have a great day.",
          "See you soon! 😊",
          "Bye! Take care.",
          "Exiting now. Talk to you later!"
          ],
  "history":["history"],
  "unknown" : [
          "I am not sure I understood that.",
          "Can you rephrase that?",
          "Sorry, I do not understand yet.",
          "I am still learning. Try asking something else."
          ]
  } 
def get_response(intent): 
  response = random.choice(responses[intent['intent']])
  print( response.format(time=get_time(), date=get_date()) )

response = get_response(intent)
