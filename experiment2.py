#18-11-26
import sqlite3
import pandas as pd
import json

# 1. Create database and tables
con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.executescript("""
CREATE TABLE doctors(id INTEGER PRIMARY KEY, name TEXT, dept TEXT);
CREATE TABLE patients(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, city TEXT);
CREATE TABLE visits(id INTEGER PRIMARY KEY, pid INTEGER, did INTEGER, date TEXT, fee REAL);
""")

# 2. Insert records
cur.executemany("INSERT INTO doctors VALUES(?,?,?)", [
    (1,"Dr. Ramesh","Cardiology"),
    (2,"Dr. Kavitha","Orthopaedics"),
    (3,"Dr. Imran","General Medicine")
])

cur.executemany("INSERT INTO patients VALUES(?,?,?,?,?)", [
    (1,"Ajay",45,"M","Chennai"), (2,"Bhavana",32,"F","Madurai"),
    (3,"Charles",67,"M","Chennai"), (4,"Deepa",29,"F","Coimbatore"),
    (5,"Elango",54,"M","Madurai"), (6,"Fathima",38,"F","Chennai")
])

cur.executemany("INSERT INTO visits VALUES(?,?,?,?,?)", [
    (1,1,1,"2026-01-05",800), (2,2,2,"2026-01-06",600),
    (3,3,1,"2026-01-08",800), (4,4,3,"2026-01-09",300),
    (5,5,1,"2026-01-12",800), (6,1,3,"2026-01-15",300),
    (7,6,2,"2026-01-18",600), (8,3,3,"2026-01-20",300),
    (9,2,2,"2026-01-22",600), (10,5,3,"2026-01-25",300)
])

con.commit()

# 3. SQL queries
queries = [
    "SELECT * FROM patients WHERE age > 40",
    """SELECT p.name, d.name, v.fee FROM visits v
       JOIN patients p ON v.pid=p.id
       JOIN doctors d ON v.did=d.id""",
    """SELECT d.dept, COUNT(*), SUM(v.fee) FROM visits v
       JOIN doctors d ON v.did=d.id GROUP BY d.dept""",
    """SELECT p.name, COUNT(*) FROM visits v
       JOIN patients p ON v.pid=p.id
       GROUP BY p.name HAVING COUNT(*) > 1"""
]

for q in queries:
    print("\n", pd.read_sql_query(q, con))

# 4. Update and delete
cur.execute("UPDATE doctors SET dept='Internal Medicine' WHERE id=3")
cur.execute("DELETE FROM visits WHERE id=10")
con.commit()

print("\nUpdated Doctors:")
print(pd.read_sql_query("SELECT * FROM doctors", con))
print("Remaining visits:", cur.execute("SELECT COUNT(*) FROM visits").fetchone()[0])

# 5. Pandas analysis
df = pd.read_sql_query(
    "SELECT p.city, v.fee FROM visits v JOIN patients p ON v.pid=p.id", con)
print("\nCity-wise average fee:")
print(df.groupby("city")["fee"].agg(["count", "mean"]))

# 6. NoSQL JSON documents
df = pd.read_sql_query("""
SELECT p.id, p.name, p.age, p.city, d.dept, v.date, v.fee
FROM patients p JOIN visits v ON p.id=v.pid
JOIN doctors d ON d.id=v.did ORDER BY p.id
""", con)

docs = []
for pid, g in df.groupby("id"):
    r = g.iloc[0]
    docs.append({
        "_id": int(pid), "name": r["name"],
        "age": int(r["age"]), "city": r["city"],
        "visits": [{"dept": x.dept, "date": x.date, "fee": x.fee}
                   for x in g.itertuples()]
    })

with open("patients_nosql.json", "w") as f:
    json.dump(docs, f, indent=2)

print("\nNoSQL Documents:")
print(json.dumps(docs, indent=2))

con.close()
