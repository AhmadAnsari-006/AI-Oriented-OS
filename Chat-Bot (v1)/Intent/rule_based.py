intent_keywords = {
  "greeting":["hi","hello","hey","yo"],
  "time":["time","clock","hour","minute"],
  "date":["day","date","weeks","months"],
  "exit":["bye","exit","quit","retire"],
  "history":["history"]
}
priority = {
  "greeting":2,
  "time":5,
  "date":4,
  "exit":3,
  "history":1,
  "unknown":0.0
}
score = {
  "greeting":0,
  "time":0,
  "date":0,
  "exit":0,
  "history":0,
  "unknown":0
}
intent_list = []