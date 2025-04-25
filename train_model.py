import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# 1. Load the dataset
df = pd.read_csv("data/SMSSpamCollection.csv", sep='\t', header=None, names=['label', 'message'], encoding='latin-1')

# Optional: Preview the dataset
print("Sample data:\n", df.head())

# 2. Convert labels to binary (spam = 1, ham = 0)
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# 3. Split features and target
X = df['message']
y = df['label']

# 4. Vectorize the text
vectorizer = TfidfVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# 6. Train the classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 7. Evaluate
y_pred = clf.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# 8. Save the model and vectorizer
model_dir = "backend/model"
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "scam_model.pkl"), "wb") as f:
    pickle.dump(clf, f)

with open(os.path.join(model_dir, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("\n✅ Model and vectorizer saved to backend/model/")
