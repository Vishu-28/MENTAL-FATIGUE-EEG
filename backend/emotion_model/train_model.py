import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_excel("../../dataset/emotions.xlsx")

print("Dataset Shape:", df.shape)
print("Columns:", df.columns)

# Features = all columns except label
X = df.drop("label", axis=1)

# Target = emotion label
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", len(X_train))

# Train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model
pickle.dump(model, open("emotion_model.pkl", "wb"))

print("Model saved as emotion_model.pkl")