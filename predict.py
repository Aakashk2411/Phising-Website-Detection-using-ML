from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

# simple feature extractor
def extract_features(url):

    url_length = len(url)
    has_https = 1 if "https" in url else 0
    has_dash = 1 if "-" in url else 0
    dot_count = url.count(".")
    has_at = 1 if "@" in url else 0

    return [[url_length, has_https, has_dash, dot_count, has_at]]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    features = extract_features(url)

    prediction = model.predict(features)

    if prediction[0] == 1:
        result = "⚠️ Phishing Website"
    else:
        result = "✅ Safe Website"

    return result


if __name__ == "__main__":
    app.run(debug=True)