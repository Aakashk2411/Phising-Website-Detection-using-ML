import pandas as pd
import re
import tldextract
from urllib.parse import urlparse

def extract_features(url):

    ext = tldextract.extract(url)
    parsed = urlparse(url)

    features = []

    features.append(len(url))
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(url.count('?'))
    features.append(url.count('%'))
    features.append(url.count('='))
    features.append(url.count('http'))
    features.append(url.count('https'))
    features.append(sum(c.isdigit() for c in url))
    features.append(len(ext.domain))
    features.append(len(ext.subdomain))
    features.append(len(parsed.path))

    while len(features) < 31:
        features.append(0)

    return features


# LOAD DATASET
data = pd.read_csv("dataset.csv")

X = []
y = []

for index, row in data.iterrows():

    url = row['url']
    label = row['label']

    features = extract_features(url)

    X.append(features)
    y.append(label)


features_df = pd.DataFrame(X)

features_df['label'] = y

features_df.to_csv("processed_dataset.csv", index=False)

print("Feature extraction completed")