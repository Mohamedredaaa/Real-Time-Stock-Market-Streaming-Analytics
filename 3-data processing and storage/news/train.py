import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

file_path = '/home/student/sicPro/news/news_sentiment_analysis.csv'
data = pd.read_csv(file_path)

data.head()

data.info()

data['Description'] = data['Description'].astype(str)
texts = data['Description']
labels = data['Sentiment']


label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

print(encoded_labels)

X_train, X_test, y_train, y_test = train_test_split(texts, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels)

custom_stop_words = ['the'] + [str(i) for i in range(10)]

vectorizer = TfidfVectorizer(max_features=1000, stop_words=custom_stop_words)

X_train_tfidf  = vectorizer.fit_transform(X_train)
X_test_tfidf  = vectorizer.transform(X_test.astype(str))

model_forest = RandomForestClassifier(n_estimators=100, random_state=42)

model_forest.fit(X_train_tfidf, y_train)

y_pred_forest = model_forest.predict(X_test_tfidf)

accuracy_Forest = accuracy_score(y_test, y_pred_forest)
report_Forest = classification_report(y_test, y_pred_forest, target_names=label_encoder.classes_)

print(f'Accuracy: {accuracy_Forest}')
print('Classification Report:')
print(report_Forest)

# Step 6: Save the model and vectorizer using joblib
joblib.dump(model_forest, 'random_forest_model.pkl')          # Save the trained model
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')        # Save the vectorizer
print("Model and Vectorizer saved successfully!")
