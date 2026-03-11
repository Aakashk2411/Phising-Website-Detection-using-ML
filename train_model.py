import pandas as pd
import numpy as np
import pickle
import tldextract
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def extract_features(url):

    ext = tldextract.extract(url)
    parsed = urlparse(url)

    features = []

    # URL length
    features.append(len(url))

    # number of dots
    features.append(url.count("."))

    # number of hyphens
    features.append(url.count("-"))

    # @ symbol
    features.append(1 if "@" in url else 0)

    # https
    features.append(1 if "https" in url else 0)

    # number of digits
    features.append(sum(c.isdigit() for c in url))

    # number of subdomains
    features.append(len(ext.subdomain.split(".")) if ext.subdomain else 0)

    return features


# load dataset
data = pd.read_csv("dataset.csv")

X = np.array([extract_features(url) for url in data["url"]])
y = data["label"]

# split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

# test accuracy
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved as model.pkl")