
print("Pharmacy Inventory Management: Lists and Tuples")
print("=" * 50)

# Tuple: fixed product catalogue
products = (
    ("P101", "Paracetamol", 25.0),
    ("P102", "Amoxicillin", 120.0),
    ("P103", "Cetirizine", 40.0),
    ("P104", "Vitamin D3", 210.0),
    ("P105", "Insulin", 450.0)
)

print("\nProduct catalogue:")
for code, name, price in products:
    print(code, name, "Rs.", price)

print("Number of products:", len(products))
print("Second product:", products[1])
print("First 3 codes:", tuple(p[0] for p in products[:3]))
print("Count / index:", products.count(products[0]), "/", products.index(products[2]))

try:
    products[0][2] = 30.0
except TypeError as e:
    print("Tuple change error:", e)

# List: changing stock
stock = [120, 35, 80, 15, 8]
print("\nInitial stock:", stock)
stock[3] += 50
print("After restocking:", stock)

sold = [20, 10, 5, 12, 3]
stock = [s - d for s, d in zip(stock, sold)]
print("After today's sales:", stock)

# List methods
expiring = ["Amoxicillin", "Insulin"]
expiring.append("Cetirizine")
expiring.extend(["Paracetamol"])
expiring.insert(0, "Vitamin D3")
print("\nList after append/extend/insert:", expiring)

expiring.remove("Paracetamol")
last = expiring.pop()
print("After remove and pop:", expiring, "| popped:", last)
expiring.sort()
print("Sorted:", expiring)
expiring.reverse()
print("Reversed:", expiring)

# Inventory records
inventory = [
    (code, name, price, qty)
    for (code, name, price), qty in zip(products, stock)
]

reorder = [name for _, name, _, qty in inventory if qty < 30]
values = [price * qty for _, _, price, qty in inventory]

print("\nInventory:")
for item, value in zip(inventory, values):
    print(item, "stock value = Rs.", value)

print("Items to reorder:", reorder)
print("Total stock value: Rs.", sum(values))
print("Max / Min quantity:", max(stock), "/", min(stock))

by_value = sorted(inventory, key=lambda t: t[2]*t[3], reverse=True)
print("Highest value item:", by_value[0][1])

# Weekly sales
weekly = [[20, 10, 5, 12, 3], [18, 8, 7, 10, 2], [25, 12, 6, 9, 4]]
totals = [sum(day[i] for day in weekly) for i in range(5)]
print("\nWeekly sales:", weekly)
print("Units sold:", dict(zip([p[1] for p in products], totals)))

copy_list = stock.copy()
copy_list.clear()
print("Copied and cleared:", copy_list, "| original stock:", stock)
