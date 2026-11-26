
import re
import sys
from itertools import groupby

def mapper(lines):
    for line in lines:
        for word in re.findall(r"[a-z]+", line.lower()):
            yield f"{word}\t1"

def reducer(lines):
    pairs = (line.rstrip().split("\t") for line in lines)
    for word, group in groupby(pairs, key=lambda x: x[0]):
        yield f"{word}\t{sum(int(c) for _, c in group)}"

if len(sys.argv) > 1:
    func = mapper if sys.argv[1] == "map" else reducer
    for out in func(sys.stdin):
        print(out)
    sys.exit()

splits = {
    "split-1 (node1)": [
        "Data science uses data to create value",
        "Big data needs distributed storage"
    ],
    "split-2 (node2)": [
        "Hadoop stores big data in HDFS",
        "MapReduce processes data in parallel"
    ],
    "split-3 (node3)": [
        "Spark and Hadoop process big data",
        "Data drives science"
    ]
}

print("MapReduce Word Count on News Headlines")
print("=" * 42)

print("\n--- MAP PHASE ---")
mapped = {}
for split, lines in splits.items():
    mapped[split] = list(mapper(lines))
    out = mapped[split]
    print(f"{split}: {len(out)} pairs ->",
          ", ".join(x.replace("\t", ":") for x in out[:6]), "...")

print("\n--- COMBINER (local aggregation on each mapper) ---")
combined = []
for split, out in mapped.items():
    local = list(reducer(sorted(out)))
    combined.extend(local)
    print(f"{split}: {len(out)} pairs reduced to {len(local)}")

print("\n--- SHUFFLE AND SORT ---")
shuffled = sorted(combined)
for word, group in groupby(shuffled, key=lambda x: x.split("\t")[0]):
    values = [x.split("\t")[1] for x in group]
    if len(values) > 1:
        print(f" {word:<12} -> {values}")
print(" (keys appearing on only one mapper are not shown)")

print("\n--- REDUCE PHASE ---")
result = [x.split("\t") for x in reducer(shuffled)]
result.sort(key=lambda x: (-int(x[1]), x[0]))

print(f"{'WORD':<12}COUNT")
for word, count in result:
    print(f"{word:<12}{count}")

print("\nDistinct words :", len(result))
print("Total words    :", sum(int(c) for _, c in result))
print("Top 3 words    :", [w for w, _ in result[:3]])
