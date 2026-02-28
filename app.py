from flask import Flask, render_template, request
import sqlite3
import joblib
import numpy as np
import os
import pandas as pd



app = Flask(__name__)

def initialize_database():
    if not os.path.exists("fraud.db"):
        print("Database not found. Downloading dataset...")

        url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
        df = pd.read_csv(url)
        df = df.sample(n=50000, random_state=42)

        conn = sqlite3.connect("fraud.db")
        df.to_sql("transactions", conn, if_exists="replace", index=False)
        conn.close()

        print("Database created successfully.")

initialize_database()

model = joblib.load("models/fraud_model.pkl")

def get_fraud_stats():
    conn = sqlite3.connect("fraud.db")
    cursor = conn.cursor()

    query = """
    SELECT Class, COUNT(*)
    FROM transactions
    GROUP BY Class
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()


    stats = {"normal": 0, "fraud": 0}

    for row in results:
        if row[0] == 0:
            stats["normal"] = row[1]
        else:
            stats["fraud"] = row[1]

    return stats


def get_average_amounts():
    conn = sqlite3.connect("fraud.db")
    cursor = conn.cursor()

    query = """
    SELECT Class, AVG(Amount)
    FROM transactions
    GROUP BY Class
    """

    cursor.execute(query)
    results= cursor.fetchall()
    conn.close()

    averages = {"normal_avg": 0, "fraud_avg" : 0}

    for row in results:
        if row[0] == 0:
            averages["normal_avg"] = round(row[1], 2)
        else:
            averages["fraud_avg"] = round(row[1], 2)

    return averages



@app.route("/")
def index():
    stats = get_fraud_stats()
    averages = get_average_amounts()

    
    return render_template("index.html", normal = stats["normal"],
    fraud= stats["fraud"], normal_avg = averages["normal_avg"], fraud_avg=averages["fraud_avg"])


@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    probability = None

    if request.method == "POST":
        time = float(request.form["Time"])
        amount = float(request.form["Amount"]) # getting input value from form

        input_data = [time] + [0]*28 + [amount] # out of 30 feature v1 - v28 feature is set to be 0 for input array

        input_array = np.array(input_data).reshape(1,-1)

        result = model.predict(input_array)[0]

        prob = model.predict_proba(input_array)[0][1] # prabability of fraud
        probability = round(prob*100,2)


        if result == 1:
            prediction = " ⚠️ Fradulent Transaction"
        else:
            prediction = " ✅ Normal Transaction"

    return render_template("predict.html", prediction = prediction, probability=probability)




if __name__ == "__main__":
    #print(app.url_map)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


