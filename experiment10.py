
import array
import re
import numpy as np

reviews = [
    " Excellent product! Battery life is GREAT and delivery was fast. ",
    "Poor quality. The battery drained in 2 hours. Very disappointed!!",
    "Good value for money, but the charger is slow.",
    "Delivery was late; product is average. Contact: support@shopmart.in",
    "Great camera, great display, great price!"
]

print("Customer Review and Sensor Analytics: Strings and Arrays")
print("=" * 58)

# String operations
r = reviews[0].strip()
print("\nString operations:")
print("Original:", r)
print("Lower:", r.lower())
print("Upper:", r.upper())
print("Length:", len(r))
print("Slice:", r[0:17])
print("Reverse:", r[::-1][:25], "...")
print("Find Battery:", r.find("Battery"))
print("Count a:", r.lower().count("a"))
print("Replace:", r.replace("GREAT", "good"))
print("Split:", r.split()[:5])
print("Starts with Exc:", r.startswith("Exc"))

# Sentiment analysis
positive = {"excellent", "great", "good", "fast"}
negative = {"poor", "disappointed", "slow", "late", "drained"}

print("\nReview sentiment:")
for i, text in enumerate(reviews, 1):
    words = re.findall(r"[a-z]+", text.lower())
    score = sum(w in positive for w in words) - sum(w in negative for w in words)
    label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    print(i, "words =", len(words), "score =", score, "->", label)

# Regex and formatting
emails = re.findall(r"[\w.]+@[\w.]+", " ".join(reviews))
print("\nEmails:", emails)
print("Joined keywords:", " | ".join(sorted(positive)))
print("Formatted:", "{:<10}|{:^10}|{:>10}".format("left", "centre", "right"))

# Array module
temps = array.array("f", [31.5, 32.0, 33.8, 35.2, 34.1, 30.9, 36.4])
temps.append(37.0)
temps.insert(0, 30.2)
print("\nArray after append/insert:", [round(t, 1) for t in temps])
print("Index of max:", temps.index(max(temps)), "| typecode:", temps.typecode)

# NumPy 2-D array
week = np.array([
    [31.5, 32.0, 33.8, 35.2, 34.1, 30.9, 36.4],
    [29.8, 30.5, 31.2, 33.0, 32.7, 29.5, 34.0],
    [33.1, 34.2, 35.6, 37.1, 36.0, 32.8, 38.2]
])

print("\nSensor array:")
print(week)
print("Shape, dimensions, size:", week.shape, week.ndim, week.size)
print("Sensor means:", week.mean(axis=1).round(2))
print("Daily maximum:", week.max(axis=0))
print("Readings above 35:", week[week > 35])
print("Sensor 2, days 2-4:", week[1, 1:4])
print("Fahrenheit:")
print((week * 9 / 5 + 32).round(1))
print("Reshaped:", week.reshape(7, 3).shape)
print("Sorted sensor 1:", np.sort(week[0]))
