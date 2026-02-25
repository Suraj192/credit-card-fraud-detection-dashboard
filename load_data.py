import pandas as pd
import sqlite3


df = pd.read_csv("data/creditcard.csv")

# connecting to db
conn = sqlite3.connect("fraud.db")

# writing dataframe to sql table
df.to_sql("transactions", conn, if_exists="replace", index=False)

# Verifying insertion
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM transactions")
count = cursor.fetchone()[0]

print(f"Total records inserted: {count}")

conn.close()