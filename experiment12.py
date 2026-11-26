
from collections import Counter, defaultdict

print("University Course Enrolment Analysis: Sets and Dictionaries")
print("=" * 60)

# Sets
python = {"Anu", "Bala", "Chitra", "Dinesh", "Esha", "Farhan"}
ml = {"Chitra", "Dinesh", "Gokul", "Harini", "Esha"}
bigdata = {"Bala", "Esha", "Harini", "Ishaan"}

print("\nPython:", sorted(python))
print("ML:", sorted(ml))
print("Big Data:", sorted(bigdata))
print("Union:", sorted(python | ml | bigdata))
print("Intersection:", sorted(python & ml))
print("Difference:", sorted(python - ml))
print("Symmetric difference:", sorted(python ^ ml))
print("In all three:", sorted(python & ml & bigdata))
print("Subset:", {"Esha", "Bala"}.issubset(python))
print("Disjoint:", ml.isdisjoint(bigdata))

ml.add("Jaya")
ml.discard("Gokul")
print("ML after add/discard:", sorted(ml))

duplicates = ["Anu", "Bala", "Anu", "Chitra", "Bala", "Anu"]
print("Unique names:", sorted(set(duplicates)))

# Dictionaries
marks = {
    "Anu": {"Python": 88, "ML": None},
    "Bala": {"Python": 72, "BigData": 81},
    "Chitra": {"Python": 95, "ML": 91},
    "Dinesh": {"Python": 64, "ML": 70}
}

marks["Anu"]["ML"] = 79
marks["Esha"] = {"Python": 85, "ML": 88, "BigData": 90}

print("\nStudent marks:")
for student, score in marks.items():
    print(student, score)

print("Keys:", list(marks.keys()))
print("Chitra's Python mark:", marks["Chitra"]["Python"])
print("Missing student:", marks.get("Zara", "Not enrolled"))

averages = {
    s: round(sum(v.values()) / len(v), 2)
    for s, v in marks.items()
}
topper = max(averages, key=averages.get)
print("Student averages:", averages)
print("Topper:", topper, averages[topper])

# defaultdict for subject-wise marks
subject_scores = defaultdict(list)
for subjects in marks.values():
    for subject, mark in subjects.items():
        subject_scores[subject].append(mark)

print("\nSubject statistics:")
for subject, scores in subject_scores.items():
    print(subject, "count =", len(scores),
          "avg =", round(sum(scores)/len(scores), 2),
          "max =", max(scores))

removed = marks.pop("Dinesh")
print("\nRemoved Dinesh:", removed, "| students left:", len(marks))
marks.update({"Farhan": {"Python": 77}})
print("After adding Farhan:", sorted(marks))

# Feedback word count
feedback = "good course good faculty excellent labs good projects excellent support"
freq = Counter(feedback.split())
print("\nWord frequency:", dict(freq))
print("Most common 2:", freq.most_common(2))
print("Sorted by frequency:", dict(sorted(freq.items(),
      key=lambda x: x[1], reverse=True)))
