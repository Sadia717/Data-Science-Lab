
from itertools import groupby

customers = [
    "C1,Kavya,Chennai", "C2,Ravi,Bengaluru",
    "C3,Sana,Chennai", "C4,Tarun,Hyderabad",
    "C5,Uma,Bengaluru"
]

orders = [
    "O1,C1,2500", "O2,C2,1800", "O3,C1,700",
    "O4,C3,4200", "O5,C4,1500", "O6,C2,3100",
    "O7,C5,950", "O8,C3,600", "O9,C9,800"
]

def join_mapper(source, line):
    f = line.split(",")
    return (f[0], ("C", f[1], f[2])) if source == "customers" \
        else (f[1], ("O", f[0], int(f[2])))

def join_reducer(cid, values):
    cust = [v for v in values if v[0] == "C"]
    ords = [v for v in values if v[0] == "O"]
    for c in cust:
        for o in ords:
            yield cid, c[1], c[2], o[1], o[2]

def agg_mapper(row):
    return row[2], row[4]

def agg_reducer(city, amounts):
    return city, sum(amounts), len(amounts), max(amounts)

def shuffle(pairs):
    pairs = sorted(pairs, key=lambda x: x[0])
    return [(k, [v for _, v in g])
            for k, g in groupby(pairs, key=lambda x: x[0])]

print("Sales Analytics: Join and Aggregation using MapReduce")
print("=" * 55)

print("\nJOB 1 - MAP (key = cust_id, value tagged with relation):")
mapped = [join_mapper("customers", x) for x in customers] + \
         [join_mapper("orders", x) for x in orders]
for k, v in mapped:
    print(f" {k} -> {v}")

print("\nJOB 1 - SHUFFLE AND SORT:")
groups = shuffle(mapped)
for k, vals in groups:
    print(f" {k}: {vals}")

print("\nJOB 1 - REDUCE (joined records):")
joined = [r for k, vals in groups for r in join_reducer(k, vals)]
print(f" {'cust':<5}{'name':<7}{'city':<11}{'order':<7}amount")
for r in joined:
    print(f" {r[0]:<5}{r[1]:<7}{r[2]:<11}{r[3]:<7}{r[4]}")
print(" Note: order O9 (cust C9) has no matching customer and is dropped.")

print("\nJOB 2 - MAP (key = city, value = amount):")
mapped2 = [agg_mapper(r) for r in joined]
print(" ", mapped2)

print("\nJOB 2 - SHUFFLE AND SORT:")
groups2 = shuffle(mapped2)
for city, vals in groups2:
    print(f" {city}: {vals}")

print("\nJOB 2 - REDUCE (aggregates per city):")
print(f" {'City':<11}{'Revenue':>8}{'Orders':>8}{'Max':>7}{'Avg':>9}")
results = [agg_reducer(c, v) for c, v in groups2]
for city, total, count, mx in sorted(results, key=lambda x: -x[1]):
    print(f" {city:<11}{total:>8}{count:>8}{mx:>7}{total/count:>9.2f}")

print("\nGrand total revenue:", sum(r[1] for r in results))
