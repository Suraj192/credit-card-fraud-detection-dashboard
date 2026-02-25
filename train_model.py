import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

conn = sqlite3.connect("fraud.db")

df = pd.read_sql("SELECT * FROM transactions", conn)

conn.close()

print("Data loaded from database")

X = df.drop("Class", axis=1)
y= df["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)

print("Training model ...")

# Training with logistic regressioin 

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nModel Evaluation: \n")
print(classification_report(y_test, y_pred))

# saving model
joblib.dump(model, "models/fraud_model.pkl")

print("\nModel Saved successfully.\n")

