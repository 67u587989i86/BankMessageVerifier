import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def retrain_model():
    print("🔁 Retraining started...")

    feedback_data = pd.read_csv('backend/data/new_training_data.csv')

    X = feedback_data['message']
    y = feedback_data['label']

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    # Save new models
    pickle.dump(model, open('model/scam_model.pkl', 'wb'))
    pickle.dump(vectorizer, open('model/vectorizer.pkl', 'wb'))

    print("✅ Retraining completed and model saved.")

if __name__ == "__main__":
    retrain_model()
