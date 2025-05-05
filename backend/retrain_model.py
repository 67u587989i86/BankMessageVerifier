import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

def retrain_model():
    print("🚀 Starting model retraining...")

    # Load original data
    original_data = pd.read_csv("data/SMSSpamCollection.csv", sep='\t', header=None, names=['label', 'message'], encoding='latin-1')
    print(f"✅ Loaded original data: {original_data.shape[0]} records")

    # Load new data (assumes same format: label,message)
    new_data = pd.read_csv("backend/data/new_training_data.csv", header=None, names=["label", "message"])
    print(f"✅ Loaded new training data: {new_data.shape[0]} records")

    # Normalize labels to binary (ham = 0, spam = 1)
    for df in [original_data, new_data]:
        df['label'] = df['label'].str.lower().map({'ham': 0, 'spam': 1})

    # Combine both
    combined_data = pd.concat([original_data, new_data], ignore_index=True).dropna()
    combined_data = combined_data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save combined dataset (optional)
    os.makedirs("backend/data", exist_ok=True)
    combined_data.to_csv("backend/data/combined_data.csv", index=False)

    print(f"📁 Combined dataset saved with {combined_data.shape[0]} records")

    # Vectorize and train
    X = combined_data['message']
    y = combined_data['label'].astype(int)

    vectorizer = TfidfVectorizer(stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    # Save model and vectorizer
    os.makedirs("backend/model", exist_ok=True)
    pickle.dump(model, open("backend/model/scam_model.pkl", 'wb'))
    pickle.dump(vectorizer, open("backend/model/vectorizer.pkl", 'wb'))

    print("✅ Retraining completed and model saved.")

if __name__ == "__main__":
    retrain_model()
