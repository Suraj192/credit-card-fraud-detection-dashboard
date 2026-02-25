from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

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
    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)


