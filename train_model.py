import pickle
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample healthcare dataset
data = {
    "question": [
        "What are the symptoms of flu?",
        "How to treat a cold?",
        "What are the side effects of antibiotics?",
        "What is COVID-19?",
        "How to improve immunity?",
        "blackheads pimples face pimples neck pimples shoulder pimples",
        "impulsivity hyperactivity lack of focus messy worksrestlessness",
        "sneezing itchy eyes coughing watery eyes itchy nose",
        "forgetful confusion with time poor judgement",
        "loss of appetite weight loss difficulty walking pain in heels pain in hips pain in jaw decreased energy heart failure heart block pain in lower back stiffness",
        "terrifies of gaining weight hard to sleep through night dizziness hair is falling out constipation swollen arms swollen legs fainting underweight",
        "rapid heartbeat fast heartbeat sweating shaking shortness of breath fear of death chest pain faintness",
        "lack of movement sored area joint pain",
        "jaundice yellow skin coughing up blood yellow urine",
        "dark shadows under eyes be pale have little energy feeling drowsy unable to eat",
        "trouble swallowing trouble breathing bad taste gum redness sensitivity bad odor in mouth"
        
    ],
    "response": [
        "Flu symptoms include fever, cough, and fatigue.",
        "Cold treatment includes rest, hydration, and medication.",
        "Side effects of antibiotics include nausea and diarrhea.",
        "COVID-19 is a viral disease affecting the respiratory system.",
        "To improve immunity, eat a balanced diet and exercise regularly.",
        "According to your symptoms you might have Acne",
        "According to your symptoms you might have Attention Deficit Disorder",
        "According to your symptoms you might have Allergies",
        "According to your symptoms you might have Alzheimers",
        "You have Ankylosing Spondylitis",
        "According to your symptoms you might have Anorexia",
        "According to your symptoms you might have Anxiety or Panic Disorder",
        "According to your symptoms you might have any type of Arthritis",
        "According to your symptoms you might have Antitrypsin Deficiency",
        "According to your symptoms you might have Abdominal Migraine",
        "sudden weight loss feeling of fullness shortness of breath tongue swelling severe fatigue severe weakness irregular heartbeat"
    ]
}

df = pd.DataFrame(data)

# NLP Preprocessing
nltk.download('punkt')
vectorizer = TfidfVectorizer(tokenizer=word_tokenize)
X = vectorizer.fit_transform(df['question'])
y = df['response']

# Train Model
model = LogisticRegression()
model.fit(X, y)

# Save Model & Vectorizer
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
