from Core import input_processor
print("\n\t\tTHIS IS CHAT-BOT(v1)")
print("______________________________________________________")
print("This is a trial model\n")
while True:
  question = input("Do you want to see Chat History? ")
  if question == "yes":
    input_processor.show_history()
  else:
    input_processor.get_input()
    