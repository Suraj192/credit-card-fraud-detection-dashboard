from flask import Flask, render_template, request
import sqlite3
import joblib
import numpy as np



app = Flask(__name__)

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

@app.route("/")
def index():
    stats = get_fraud_stats()
    return render_template("index.html", normal = stats["normal"],
    fraud= stats["fraud"])


@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None

    if request.method == "POST":
        time = float(request.form["Time"])
        amount = float(request.form["Amount"]) # getting input value from form

        input_data = [time] + [0]*28 + [amount] # out of 30 feature v1 - v28 feature is set to be 0 for input array

        input_array = np.array(input_data).reshape(1,-1)

        result = model.predict(input_array)[0]

        if result == 1:
            prediction = " ⚠️ Fradulent Transaction"
        else:
            prediction = " ✅ Normal Transaction"

    return render_template("predict.html", prediction = prediction)




if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)


