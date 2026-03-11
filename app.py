from flask import Flask, render_template, request
import pickle
import numpy as np
import tldextract
from urllib.parse import urlparse

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

def extract_features(url):

    ext = tldextract.extract(url)
    parsed = urlparse(url)

    features = []

    features.append(len(url))
    features.append(url.count("."))
    features.append(url.count("-"))
    features.append(1 if "@" in url else 0)
    features.append(1 if "https" in url else 0)
    features.append(sum(c.isdigit() for c in url))
    features.append(len(ext.subdomain.split(".")) if ext.subdomain else 0)

    return np.array(features).reshape(1,-1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    url = request.form["url"]

    features = extract_features(url)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    risk = round(probability * 100,2)

    if prediction == 1:
        result = "⚠️ Phishing Website Detected"
    else:
        result = "✅ Legitimate Website"

    return render_template(
        "result.html",
        result=result,
        url=url,
        risk=risk
    )


if __name__ == "__main__":
    app.run(debug=True)