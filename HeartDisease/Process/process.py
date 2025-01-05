import pandas as pd
from sklearn.model_selection import train_test_split
import torch

# Kaggle veri setini yükle
df = pd.read_csv(r'C:\\Users\\melda\\Desktop\\HeartDisease\\Dataset\\heart_disease_uci.csv')

# Özellikleri seçme (sizin veri setinizdeki doğru sütun adlarına göre)
features = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
labels = df['num']  # Kalp hastalığına sahip olup olmadığını belirten etiket (bu sütun num olmalı)

# Özellikleri ve etiketleri tensöre dönüştür
X = torch.tensor(features.values, dtype=torch.float)
y = torch.tensor(labels.values, dtype=torch.long)

# Eğitim ve test verisi olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
num_nodes = X_train.shape[0]  # Yeni veri setinizin boyutu
print(f"Yeni veri seti boyutu: {num_nodes}")
