from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

dataset = pd.read_csv('dataset.csv')

if 'relevance_score' not in dataset.columns or 'symptoms' not in dataset.columns:
    raise ValueError("Dataset harus memiliki kolom 'relevance_score' dan 'symptoms'.")
dataset['relevance_score'] = pd.to_numeric(dataset['relevance_score'], errors='coerce')

# Mendapatkan jumlah fitur yang diharapkan oleh model
EXPECTED_FEATURES = model.input_shape[-1]

def extract_features_from_symptoms(symptoms):
    """
    Transformasikan daftar gejala menjadi format yang sesuai dengan model.
    Setiap gejala dipetakan ke indeks fitur menggunakan fungsi hash.
    """
    features = np.zeros(EXPECTED_FEATURES)
    for symptom in symptoms:
        index = hash(symptom.strip().lower()) % EXPECTED_FEATURES
        features[index] = 1
    return features.reshape(1, -1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/herb/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'symptoms' not in data:
            return jsonify({
                "code": 400,
                "message": "Missing symptoms in request data",
                "result data": None
            }), 400

        # Memproses input gejala
        symptoms_input = data['symptoms']
        symptoms_list = [s.strip().lower() for s in symptoms_input.split(',')]
        if len(symptoms_list) > EXPECTED_FEATURES:
            symptoms_list = symptoms_list[:EXPECTED_FEATURES]
        features = extract_features_from_symptoms(symptoms_list)

        if features.shape[1] != EXPECTED_FEATURES:
            return jsonify({
                "code": 400,
                "message": f"Input features must have {EXPECTED_FEATURES} dimensions, but got {features.shape[1]}.",
                "result data": None
            }), 400

        # Melakukan prediksi
        prediction = model.predict(features)
        relevance_score = float(prediction[0][0]) if isinstance(prediction, np.ndarray) and prediction.ndim > 1 else float(prediction[0]) if isinstance(prediction, np.ndarray) else float(prediction)

        print(f"Relevance Score (Predicted): {relevance_score}")

        # Menyaring data berdasarkan kemunculan gejala
        dataset['gejala_list'] = dataset['symptoms'].str.lower().str.split(',')
        dataset['matched_symptoms'] = dataset['gejala_list'].apply(
            lambda gejala: len(set(gejala).intersection(set(symptoms_list)))
        )
        filtered_data = dataset[dataset['matched_symptoms'] > 0].copy()

        filtered_data['score_difference'] = abs(filtered_data['relevance_score'] - relevance_score)
        closest_matches = filtered_data.sort_values(by=['matched_symptoms', 'score_difference'], ascending=[False, True]).head(10)

        if closest_matches.empty:
            return jsonify({
                "code": 404,
                "message": "No matching herbs found",
                "result data": None
            }), 404

        result_data = closest_matches.drop_duplicates(subset=['herbs']).apply(
            lambda row: {
                "herbs": row['herbs'],
                "latin_name": row['latin_name'],
                "image_link": row.get('link_gambar', ''),
                "usage_method": row['usage_method']
            }, axis=1).tolist()

        return jsonify({
            "code": 200,
            "message": "Successful herbs recommendations",
            "prediction score": relevance_score,
            "result data": result_data
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "code": 500,
            "message": str(e),
            "result data": None
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
