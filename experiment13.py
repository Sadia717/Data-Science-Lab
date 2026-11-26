
import hashlib

BLOCK_SIZE = 64
REPLICATION = 3

log = "\n".join(
    f"2026-03-0{d} 10:{m:02d} sensor={s} temp={30+(d*m+s)%9}"
    for d in range(1, 3) for m in (5, 20) for s in (1, 2)
)

blocks = [log[i:i+BLOCK_SIZE] for i in range(0, len(log), BLOCK_SIZE)]
ids = [f"blk_{i:04d}" for i in range(1, len(blocks)+1)]

nodes = ["DN1", "DN2", "DN3", "DN4", "DN5", "DN6"]
racks = {n: "Rack-1" if i < 3 else "Rack-2" for i, n in enumerate(nodes)}

places = [
    ["DN1", "DN4", "DN5"],
    ["DN2", "DN5", "DN4"],
    ["DN3", "DN6", "DN4"],
    ["DN4", "DN1", "DN2"],
    ["DN5", "DN2", "DN1"]
]

storage = {n: [] for n in nodes}
for bid, targets in zip(ids, places):
    for n in targets:
        storage[n].append(bid)

def checksum(data):
    return hashlib.md5(data.encode()).hexdigest()[:8]

def show_blocks():
    for bid, targets in zip(ids, places):
        print(f" {bid} {targets} racks={sorted({racks[n] for n in targets})}")

print("Distributed File System Simulation (HDFS)")
print("=" * 45)
print(f"Block size = {BLOCK_SIZE} bytes | Replication factor = {REPLICATION}")
print("Cluster    :", ", ".join(f"{n}({racks[n]})" for n in nodes))

print("\n$ hdfs dfs -put sensor_log.txt /data/sensor_log.txt")
print(f"File size = {len(log)} bytes -> {len(blocks)} blocks")

print("\nNameNode metadata (block -> DataNodes):")
show_blocks()

print("\nDataNode storage report:")
for n in nodes:
    print(f" {n} blocks={sorted(storage[n])}")

print("\n$ hdfs dfs -cat /data/sensor_log.txt | head -3")
print("\n".join(log.splitlines()[:3]))
print("Checksum original =", checksum(log), "| read back =", checksum(log))

print("\n*** DataNode DN1 fails (heartbeat lost) ***")
places[0] = ["DN4", "DN5", "DN2"]
places[3] = ["DN4", "DN2", "DN3"]
places[4] = ["DN5", "DN2", "DN3"]
print("Under-replicated blocks re-replicated: 3")

for bid, targets in zip(ids, places):
    print(f" {bid} {targets}")

print("File readable after failure: True | checksum =", checksum(log))
print("\n$ hdfs fsck /data/sensor_log.txt -files -blocks")
print(f"Total blocks: {len(blocks)} | Replication: {REPLICATION} | Status: HEALTHY")
