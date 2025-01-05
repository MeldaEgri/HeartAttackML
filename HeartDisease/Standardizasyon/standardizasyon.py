import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Veri setini yükle
df = pd.read_csv(r'C:\\Users\\melda\\Desktop\\HeartDisease\\Dataset\\heart.csv')

# Kategorik sütunları tespit et
string_columns = df.select_dtypes(include=['object']).columns
print(f"String sütunlar: {string_columns}")

# LabelEncoder ile kategorik veriyi sayısallaştır
label_encoder = LabelEncoder()

# Kategorik sütunları sayısallaştır
for col in string_columns:
    print(f"'{col}' sütunu sayısallaştırılıyor...")
    df[col] = label_encoder.fit_transform(df[col])

# Sayısal veriye normalizasyon uygula
feature_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                   'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

# Özellikleri seçme (sizin veri setinizdeki doğru sütun adlarına göre)

# MinMaxScaler ile normalizasyon
minmax_scaler = MinMaxScaler()
df_normalized = df.copy()
df_normalized[feature_columns] = minmax_scaler.fit_transform(df[feature_columns])

# Normalleştirilmiş veri setini kaydet
df_normalized.to_csv(r'C:\\Users\\melda\\Desktop\\HeartDisease\\Dataset\\normalized_veriset2.csv', index=False)

print("Veri setine normalizasyon uygulandı ve yeni dosya kaydedildi.")
