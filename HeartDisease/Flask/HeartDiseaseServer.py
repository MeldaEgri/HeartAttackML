import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)
CORS(app)

df = pd.read_csv(r'C:\\Users\\melda\\Documents\\GitHub\\HeartAttackML\\HeartDisease\\Dataset\\normalized_veriset2.csv')
X = df.drop("target",axis=1)  
y = df["target"] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  
X_test = scaler.transform(X_test)       

model = RandomForestClassifier(n_estimators=250, random_state=50, class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Modelin Doğruluk Oranı: {accuracy * 100:.2f}%")

model_path = "random_forest_model.pkl"
with open(model_path, "wb") as file:
    pickle.dump((model, scaler), file)
print(f"Model '{model_path}' olarak kaydedildi.")


@app.route('/predict', methods=['POST'])
def predict():
    """
    Gelen JSON verisiyle tahmin yapar.
    """
    try:
        data = request.get_json()
        features = pd.DataFrame(data, index=[0]) 
        with open(model_path, "rb") as file:
            loaded_model, loaded_scaler = pickle.load(file)

        scaled_features = loaded_scaler.transform(features)
        prediction = loaded_model.predict(scaled_features)
        
        return jsonify({"prediction": int(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
