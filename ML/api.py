from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# load model and vectorizer
with open("log_reg_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # get news text
    news_text = data.get("news", "")

    if not news_text:
        return jsonify({"error": "No news text provided"}), 400

    # text → vector
    text_vector = vectorizer.transform([news_text])

    # prediction
    pred = model.predict(text_vector)[0]
    prob = model.predict_proba(text_vector)[0]

    return jsonify({
        "prediction": "true" if pred == 1 else "false",
        "probability": float(max(prob))
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
