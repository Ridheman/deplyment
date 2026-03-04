from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix

app = Flask(__name__)

@app.route('/')
def home():
    return "Gaussian Naive Bayes Classifier API is running"

@app.route('/train', methods=['POST'])
def train_model():
    
    file = request.files['file']
    target_col = request.form['target']

    df = pd.read_csv(file)

    # Features and Target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model Training
    model = GaussianNB()
    model.fit(X_train, y_train)

    # Predictions
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    # Accuracy
    train_acc = accuracy_score(y_train, train_preds)
    test_acc = accuracy_score(y_test, test_preds)

    # Confusion Matrix
    cm = confusion_matrix(y_test, test_preds).tolist()

    return jsonify({
        "training_accuracy": train_acc,
        "testing_accuracy": test_acc,
        "confusion_matrix": cm
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)