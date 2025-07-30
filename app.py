from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Daftar kata kunci berdasarkan kategori
keywords = {
    "SOCIAL": [
        "community empowerment", "welfare improvement", "community development", "community involvement",
        "tourist education", "cultural respect", "public participation", "tourist health", "tourist safety",
        "cultural education", "cultural preservation", "tradition respect", "cultural development",
        "heritage appreciation", "social equality", "social responsibility", "social development",
        "community engagement"
    ],
    "ECONOMIC": [
        "local economic empowerment", "tourism revenue", "development of local tourism-based enterprises",
        "job opportunities", "employment vacancies", "tourism sector", "employment opportunities",
        "labor absorption", "economic empowerment", "livelihood", "profitability", "income", "investment",
        "economic growth", "competitiveness of tourism business", "market innovation"
    ],
    "ENVIRONMENT": [
        "environmental protection", "environmental preservation", "nature conservation",
        "ecosystem preservation", "ecosystem sustainability", "ecological balance", "nature-based tourism",
        "waste management", "waste disposal", "waste material management", "ecosystem conservation",
        "habitat protection", "water conservation", "tree replanting", "wildlife protection",
        "fauna preservation", "zero-waste practices", "environmental-friendly energy", "pollution prevention",
        "pollution mitigation"
    ]
}

def keyword_ner(text):
    results = []
    text_lower = text.lower()

    for label, phrases in keywords.items():
        for phrase in phrases:
            if phrase.lower() in text_lower:
                # Cari posisi teks aslinya (bukan lowercase-nya)
                match = re.search(re.escape(phrase), text, re.IGNORECASE)
                if match:
                    matched_text = match.group()
                    if not any(r['text'].lower() == matched_text.lower() for r in results):
                        results.append({
                            "label": label,
                            "text": matched_text
                        })

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indonesia')
def indonesia():
    return render_template('indonesia.html')

@app.route('/asean')
def asean():
    return render_template('asean.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/data')
def data ():
    return render_template('data.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    text = data.get("text", "")
    try:
        results = keyword_ner(text)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
