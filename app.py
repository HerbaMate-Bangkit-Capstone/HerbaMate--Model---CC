from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Membaca dataset CSV
df = pd.read_csv('dataset.csv')

@app.route('/herb/predict', methods=['POST'])
def recommend_plants():
    selected_symptoms = request.json.get('symptoms', [])

    if not selected_symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400

    recommended_plants = []

    # Loop melalui setiap baris di dataset dan periksa apakah gejala cocok
    for index, row in df.iterrows():
        plant_symptoms = row['symptoms'].split(',')
        if any(symptom in plant_symptoms for symptom in selected_symptoms):
            recommended_plants.append({
                'tanaman': row['herbs'],
                'cara_pembuatan': row['usage_method'],
                'gejala': plant_symptoms,
                'relevance_score': row['relevance_score']
            })

    if not recommended_plants:
        return jsonify({'message': 'No plants match the selected symptoms'}), 404

    # Mengurutkan berdasarkan relevance_score secara menurun
    recommended_plants.sort(key=lambda x: x['relevance_score'], reverse=True)

    return jsonify({'recommended_plants': recommended_plants})


if __name__ == '__main__':
    app.run(debug=True)