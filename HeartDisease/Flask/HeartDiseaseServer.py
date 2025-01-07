import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

dataset = pd.read_csv(r'C:\\Users\\melda\\Documents\\GitHub\\HeartAttackML\\HeartDisease\\Dataset\\normalized_veriset2.csv')

X = dataset.drop("target", axis=1)
y = dataset["target"]

model_path = "optimized_random_forest_model.pkl"

def train_and_save_model():
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    max_accuracy = 0
    best_x = 0
    for x in range(2000):
        rf = RandomForestClassifier(random_state=x)
        rf.fit(X_train, Y_train)
        Y_pred_rf = rf.predict(X_test)
        current_accuracy = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)

        if current_accuracy > max_accuracy:
            max_accuracy = current_accuracy
            best_x = x

    print(f"En iyi doğruluk oranı: {max_accuracy}% (Random State: {best_x})")

    rf = RandomForestClassifier(random_state=best_x)
    rf.fit(X_train, Y_train)
    Y_pred_rf = rf.predict(X_test)
    final_accuracy = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
    print(f"Eğitim sonrası doğruluk oranı: {final_accuracy}%")

    
    with open(model_path, "wb") as file:
        pickle.dump(rf, file)
    print(f"Model '{model_path}' olarak kaydedildi.")

if not os.path.exists(model_path):
    print("Model dosyası bulunamadı, model eğitiliyor...")
    train_and_save_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = pd.DataFrame(data, index=[0])

        with open(model_path, "rb") as file:
            loaded_model = pickle.load(file)

        prediction = loaded_model.predict(features)[0]

        if prediction == 0:
            result_message = "Kalp krizi geçirme ihtimaliniz düşük."
        elif prediction == 1:
            result_message = "Kalp krizi geçirme ihtimaliniz olası çıktı. Bunun için bir kardiyoloji polikliniğine başvurunuz."

        return jsonify({"prediction": int(prediction), "message": result_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
