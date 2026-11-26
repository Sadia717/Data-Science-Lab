#19-11-26
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 200

df = pd.DataFrame({
    "customer_id": range(1001, 1001+n),
    "age": np.random.randint(18, 70, n).astype(float),
    "income": np.random.normal(45000, 12000, n).round(),
    "city": np.random.choice(
        ["Chennai", "chennai ", "Madurai", "Coimbatore"], n),
    "purchases": np.random.poisson(6, n).astype(float),
    "churn": np.random.choice(["Yes", "No"], n, p=[0.3, 0.7])
})

# Add missing values, outliers and duplicates
df.loc[np.random.choice(n, 15, replace=False), "age"] = np.nan
df.loc[np.random.choice(n, 10, replace=False), "income"] = np.nan
df.loc[[5, 50, 120], "income"] = [450000, 520000, -3000]
df = pd.concat([df, df.iloc[[10, 20, 30, 40, 50]]], ignore_index=True)

print("Customer Data: Cleaning and Sampling for Modeling")
print("=" * 50)
print("Raw shape:", df.shape)

# 1. Missing values
print("\n[1] Missing values:")
print(df.isnull().sum())

# 2. Remove duplicates
dups = df.duplicated().sum()
df = df.drop_duplicates()
print("\n[2] Duplicates removed:", dups, "-> shape", df.shape)

# 3. Correct city names
print("\n[3] Cities before:", sorted(df.city.unique()))
df["city"] = df.city.str.strip().str.title()
print("Cities after:", sorted(df.city.unique()))

# 4. Handle invalid values and outliers
df.loc[df.income < 0, "income"] = np.nan
q1, q3 = df.income.quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5*iqr, q3 + 1.5*iqr

out = df[(df.income < low) | (df.income > high)]
print("\n[4] Income bounds:", round(low), "to", round(high))
print("Outliers found:", len(out))
print(out[["customer_id", "income"]].to_string(index=False))

df["income"] = df.income.clip(low, high)

# 5. Fill missing values
df["age"] = df.age.fillna(df.age.median())
df["income"] = df.income.fillna(df.income.mean()).round()
print("\n[5] Missing values after cleaning:",
      int(df.isnull().sum().sum()))

# 6. Encoding and scaling
df["churn"] = df.churn.map({"No": 0, "Yes": 1})
df = pd.get_dummies(df, columns=["city"], drop_first=True, dtype=int)

scaler = StandardScaler()
cols = ["age", "income", "purchases"]
df[cols] = scaler.fit_transform(df[cols])

print("\n[6] Cleaned data (first 5 rows):")
print(df.head().round(3).to_string(index=False))

# 7. Sampling
X = df.drop(columns=["customer_id", "churn"])
y = df["churn"]

sample = df.sample(frac=0.2, random_state=1)
print("\n[7] Random sample:", len(sample),
      "rows, churn rate =", round(sample.churn.mean(), 3))

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=1)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=1)

print("\nTrain / Validation / Test split (70/15/15):")
for name, part in [
    ("Overall", y), ("Train", y_train),
    ("Validation", y_val), ("Test", y_test)
]:
    print(name, "rows =", len(part),
          "churn rate =", round(part.mean(), 3))
