intent_keywords = {
  "greeting":["hi","hello","hey","yo",],# intent_name : keywords_list
  "time":["time","clock",],
  "date":["day","date","weeks"],
  "exit":["bye","exit","quit"],
  "history":["history"]
}
priority = {
  "greeting":2,
  "time":5,
  "date":4,
  "exit":3,
  "history":1,
  "unknown":0.1
}
score = { #intent_name : score_values
  "greeting":0, 
  "time":0,
  "date":0,
  "exit":0,
  "history":0,
  "unknown":0
}
intent_list = []