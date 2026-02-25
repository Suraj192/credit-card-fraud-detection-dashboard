import sqlite3
import pandas as pd

conn = sqlite3.connect("fraud.db")

query = """
SELECT Class, COUNT(*) as total
FROM transactions
GROUP BY Class
"""

df= pd.read_sql(query, conn)
print(df)

conn.close()