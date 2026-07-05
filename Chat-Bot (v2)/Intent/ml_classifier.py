import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Predefined dataset for training the ML Intent Classifier
TRAINING_DATA = [
    # greeting
    ("hello there", "greeting"),
    ("hi, how are you?", "greeting"),
    ("hey computer", "greeting"),
    ("yo!", "greeting"),
    ("greetings OS", "greeting"),
    ("good morning", "greeting"),
    ("hey", "greeting"),
    ("sup buddy", "greeting"),
    
    # time
    ("what time is it?", "time"),
    ("can you tell me the time?", "time"),
    ("do you have the clock?", "time"),
    ("what's the current hour?", "time"),
    ("current time please", "time"),
    ("tell me the time", "time"),
    
    # date
    ("what's the date today?", "date"),
    ("show me the day", "date"),
    ("what is today's date?", "date"),
    ("what week is it?", "date"),
    ("tell me the date", "date"),
    ("what is today", "date"),
    
    # exit
    ("bye now", "exit"),
    ("exit the system", "exit"),
    ("quit application", "exit"),
    ("shutdown OS", "exit"),
    ("close down", "exit"),
    ("turn off", "exit"),
    ("quit", "exit"),
    ("logout", "exit"),
    
    # history
    ("show me the history", "history"),
    ("retrieve conversation logs", "history"),
    ("what did we talk about?", "history"),
    ("print chat history", "history"),
    ("show history", "history"),
    ("logs of conversation", "history"),
    
    # mode_switch
    ("switch to coding mode", "mode_switch"),
    ("change the environment to gaming", "mode_switch"),
    ("activate medical mode", "mode_switch"),
    ("set active mode to productivity", "mode_switch"),
    ("toggle data mode", "mode_switch"),
    ("change operating mode to education", "mode_switch"),
    ("switch mode", "mode_switch"),
    ("activate productivity mode", "mode_switch"),
    
    # system_status
    ("check system status", "system_status"),
    ("cpu utilization", "system_status"),
    ("memory usage metrics", "system_status"),
    ("show telemetry", "system_status"),
    ("list running processes", "system_status"),
    ("how much disk space is left?", "system_status"),
    ("system stats", "system_status"),
    ("hardware telemetry", "system_status"),
    
    # biometric_auth
    ("authenticate my voiceprint", "biometric_auth"),
    ("register master voice key", "biometric_auth"),
    ("log in with voice print", "biometric_auth"),
    ("verify my identity", "biometric_auth"),
    ("secure authentication", "biometric_auth"),
    ("register my voice", "biometric_auth"),
    
    # tool_generation
    ("generate a python script to parse files", "tool_generation"),
    ("create tool for directory listing", "tool_generation"),
    ("write code to automate this", "tool_generation"),
    ("build an automation script", "tool_generation"),
    ("make an ephemeral utility helper", "tool_generation"),
    ("generate a python tool", "tool_generation"),
    
    # app_orchestration
    ("open browser window", "app_orchestration"),
    ("run search in browser", "app_orchestration"),
    ("automate the default browser", "app_orchestration"),
    ("launch system application", "app_orchestration"),
    ("open default browser", "app_orchestration"),
    ("launch web browser", "app_orchestration"),
    
    # productivity
    ("summarize our last meeting", "productivity"),
    ("show my productivity checklist", "productivity"),
    ("add task to schedule", "productivity"),
    ("what are my todos today?", "productivity"),
    ("create meeting notes", "productivity"),
    ("todo list schedule", "productivity"),
    
    # multilingual
    ("translate this sentence to spanish", "multilingual"),
    ("how do you say hello in german", "multilingual"),
    ("french translation support", "multilingual"),
    ("translate this to chinese", "multilingual"),
    ("run multilingual assistant", "multilingual"),
    ("translate to german", "multilingual")
]

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Models", "intent_model.pkl")

loaded_model = None

def train_model():
    """Trains a TF-IDF Vectorizer and a MultinomialNB classifier and saves them to Models/intent_model.pkl."""
    global loaded_model
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]
    
    vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    classifier = MultinomialNB()
    classifier.fit(X, labels)
    
    # Ensure Models directory exists
    models_dir = os.path.dirname(MODEL_PATH)
    if not os.path.exists(models_dir):
        os.makedirs(models_dir, exist_ok=True)
        
    model_data = {
        "vectorizer": vectorizer,
        "classifier": classifier
    }
    
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_data, f)
        
    loaded_model = model_data
    print(f"[ML Classifier] Model trained and saved to {MODEL_PATH}")

def load_model():
    """Loads the model from disk if it exists, otherwise trains a new one."""
    global loaded_model
    if loaded_model is not None:
        return loaded_model
        
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
        try:
            with open(MODEL_PATH, "rb") as f:
                loaded_model = pickle.load(f)
            return loaded_model
        except Exception as e:
            print(f"[ML Classifier] Error loading model: {e}. Re-training...")
            
    train_model()
    return loaded_model

def predict_intent(clean_message):
    """Predicts intent and returns a dictionary with the intent name and confidence score."""
    model = load_model()
    if not model:
        return {"intent": "unknown", "confidence": 0.0}
        
    vectorizer = model["vectorizer"]
    classifier = model["classifier"]
    
    X_test = vectorizer.transform([clean_message])
    
    # Check if vocabulary overlaps at all
    if X_test.nnz == 0:
        # No known words in the message
        return {"intent": "unknown", "confidence": 0.0}
        
    predicted_intent = classifier.predict(X_test)[0]
    probabilities = classifier.predict_proba(X_test)[0]
    classes = classifier.classes_
    
    # Find matching class index
    class_idx = list(classes).index(predicted_intent)
    confidence = float(probabilities[class_idx])
    
    return {
        "intent": predicted_intent,
        "confidence": confidence
    }
