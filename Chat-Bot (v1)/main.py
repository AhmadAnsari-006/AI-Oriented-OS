from Core import input_processor
from Response import template_engine as te
print("\n\t\tTHIS IS CHAT-BOT(v1)")
print("______________________________________________________")
print("This is a trial model\n")
#hello time is 2 clock bye hi  date history
while True:
  question = input("Do you want to see Chat History? ")
  if question == "yes":
    input_processor.show_history()
  elif question == 'quit':
    break
  else:
    input_processor.get_input()
    