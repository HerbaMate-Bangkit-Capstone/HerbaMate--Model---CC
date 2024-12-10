# Project Name
Program Backend API untuk Model Machine Learning

## Description
Program ini menggunakan kerangka kerja Flask Python yang dimana akan memberikan rekomendasi tanaman herbal berdasarkan gejala yang di request dan nilai prediction dari Model Machine Learning.
Aplikasi di deploy menggunakan Google Cloud Run melalui Google Cloud Build dan Google Container Registry.

## Key Features
- Herb Recommendations
  
## Instalasi
Langkah-langkah untuk menginstal dan menjalankan proyek ini di lokal.
1. Clone repositori ini:
   ```bash
   git clone https://github.com/HerbaMate-Bangkit-Capstone/HerbaMate--Model---CC.git

2. Extract dan masuk ke folder project:
   ```bash
   cd HerbaMate--Model---CC

3. Jalankan project:
   ```bash
   python app.py

4. Lakukan request menggunakan Postman:
   ```bash
   http://localhost:5000/herb/predict

5. Contoh request:
   ```bash
     {
        "symptoms": "Batuk,Sakit tenggorokan,Perut kembung,Mual"
     }


