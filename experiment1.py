#18-11-26
import pandas as pd
import json
import os

os.makedirs("data", exist_ok=True)

# 1. Create sample data
pos = pd.DataFrame([
    [101, "Anitha", "Laptop", 1, 54000, "Chennai"],
    [102, "Rahul", "Mouse", 3, 450, "Chennai"],
    [103, "Priya", "Keyboard", 2, 1200, "Chennai"],
    [104, "Karthik", "Monitor", 1, 9500, "Chennai"]
], columns=["order_id", "customer", "product", "qty", "unit_price", "branch"])

pos.to_csv("data/pos.csv", index=False)

web = [
    {"order_id": 201, "customer": "Divya", "product": "Laptop", "qty": 2, "unit_price": 52500, "branch": "Online"},
    {"order_id": 202, "customer": "Arjun", "product": "Headset", "qty": 1, "unit_price": 2300, "branch": "Online"},
    {"order_id": 203, "customer": "Meena", "product": "Mouse", "qty": 5, "unit_price": 430, "branch": "Online"}
]

with open("data/web.json", "w") as f:
    json.dump(web, f)

mobile = """301|Suresh|Monitor|2|9300|Mobile
302|Lakshmi|Keyboard|1|1150|Mobile
303|Vignesh|Laptop|1|55000|Mobile"""

with open("data/mobile.txt", "w") as f:
    f.write(mobile)

# 2. Read data from files
df1 = pd.read_csv("data/pos.csv")

with open("data/web.json") as f:
    df2 = pd.DataFrame(json.load(f))

df3 = pd.read_csv("data/mobile.txt", sep="|", header=None,
                  names=pos.columns)

# 3. Integrate data
orders = pd.concat([df1, df2, df3], ignore_index=True)
orders["amount"] = orders["qty"] * orders["unit_price"]

print("Integrated Dataset:")
print(orders)

# 4. Store data in different formats
orders.to_csv("data/orders.csv", index=False)
orders.to_json("data/orders.json", orient="records")
orders.to_excel("data/orders.xlsx", index=False)

# 5. Retrieve and analyse data
data = pd.read_excel("data/orders.xlsx")

print("\nRevenue by Branch:")
print(data.groupby("branch")["amount"].sum())

print("\nOrders above 10000:")
print(data[data["amount"] > 10000])

# 6. Display file sizes
for file in ["orders.csv", "orders.json", "orders.xlsx"]:
    print(file, os.path.getsize("data/" + file), "bytes")
