import React, { useState } from "react";
import videoBg from "../src/Assets/heart.mp4";
import   '../src/App.css'
function HeartDiseaseForm() {
  const [formData, setFormData] = useState({
    age: "",
    sex: "",
    cp: "",
    trestbps: "",
    chol: "",
    fbs: "",
    restecg: "",
    thalach: "",
    exang: "",
    oldpeak: "",
    slope: "",
    ca: "",
    thal: "",
  });
  const fieldDescriptions = {
    age: "Age = Yaş",
    sex: "Sex = Cinsiyet (0: Erkek, 1: Kadın)",
    cp: "Chest Pain Type: 0 - Typical Angina, 1 - Atypical Angina, 2 - Non-anginal, 3 - Asymptomatic",
    trestbps: "Trestbps = Dinlenme Kan Basıncı (mm Hg)",
    chol: "Chol = Kolesterol (mg/dL)",
    fbs: "FBS = Açlık Kan Şekeri > 120 mg/dL (1: Doğru, 0: Yanlış)",
    restecg: "RestECG = Dinlenme EKG sonuçları (0-2 arasında)",
    thalach: "Thalach = Maksimum Kalp Hızı",
    exang: "Exang = Egzersizle oluşan ST depresyonu dinlenmeye göre (1: Var, 0: Yok)",
    oldpeak: "Oldpeak = ST depresyonu egzersize göre",
    slope: "Slope = ST Segmenti Eğimi (0-2 arasında)",
    ca: "CA = floroskopi ile renklendirilen ana damarların sayıs (0-3 arasında)",
    thal: "Thal = Talasemi Türü  (0 (Normal): Talasemi belirtisi yok, kişinin kanındaki hemoglobin normal durumda ,1 (Fixed Defect - Sabit Defekt): Daha önceki bir kalp krizi nedeniyle kalıcı bir anormallik.,  2 (Reversible Defect - Tersinir Defekt): Stres testi sırasında gözlenen geçici bir kan akış problemi., veya 3 (Severe Defect - Ciddi Defekt): Talasemi veya kalp rahatsızlığı ile ilişkili ciddi bir anormallik.)",
  };

  
  const [predictionMessage, setPredictionMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form verileri gönderiliyor:", formData);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        setPredictionMessage(data.message);
      } else {
        alert(`Hata: ${data.error}`);
      }
    } catch (error) {
      console.error("İstek başarısız:", error);
      alert("Bir hata oluştu, lütfen tekrar deneyin.");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <video className="background-video" src={videoBg} autoPlay loop muted />
      <div className="content">
        <h2>Heart Disease Prediction Form</h2>
        <div className="field-descriptions">
            {Object.entries(fieldDescriptions).map(([key, description]) => (
              <p key={key}>
                <strong>{key.toUpperCase()}</strong>: {description}
              </p>
            ))}
          </div>
        <form onSubmit={handleSubmit}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: "10px",
            }}
          >
            {Object.keys(formData).map((key) => (
              <div key={key}>
                <label
                  style={{
                    display: "block",
                    fontWeight: "bold",
                    marginBottom: "5px",
                  }}
                >
                  {key.charAt(0).toUpperCase() + key.slice(1)}:
                </label>
                <input
                  type="text"
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  style={{
                    width: "100%",
                    padding: "8px",
                    borderRadius: "4px",
                    border: "1px solid #ccc",
                  }}
                />
              </div>
            ))}
          </div>
          <button
            type="submit"
            style={{
              marginTop: "20px",
              padding: "10px 15px",
              backgroundColor: "#007BFF",
              color: "#fff",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Submit
          </button>
        </form>
        {predictionMessage && (
          <div
            style={{
              marginTop: "20px",
              padding: "10px",
              backgroundColor: "#f8f9fa",
              borderRadius: "4px",
              textAlign: "center",
              color:'orangered',

            }}
          >
            <p>{predictionMessage}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default HeartDiseaseForm;
