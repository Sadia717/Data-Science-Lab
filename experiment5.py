#19-11-26
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

np.random.seed(10)
n = 150

area = np.random.randint(500, 3000, n)
bedrooms = np.random.randint(1, 5, n)
age = np.random.randint(0, 30, n)
distance = np.round(np.random.uniform(1, 25, n), 1)

price = (15 + 0.045*area + 4*bedrooms - 0.6*age
          - 1.2*distance + np.random.normal(0, 6, n))

houses = pd.DataFrame({
    "area_sqft": area,
    "bedrooms": bedrooms,
    "age_years": age,
    "distance_km": distance,
    "price_lakhs": price.round(2)
})

print("House Price Prediction using Linear Regression")
print("=" * 50)
print(houses.head().to_string(index=False))
print("\nCorrelation with price:")
print(houses.corr()["price_lakhs"].drop("price_lakhs").round(3))

X = houses.drop(columns="price_lakhs")
y = houses["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1
)

# Simple Linear Regression (area only)
simple = LinearRegression().fit(X_train[["area_sqft"]], y_train)
print("\nSimple Linear Regression:")
print("Intercept =", round(simple.intercept_, 4))
print("Slope =", round(simple.coef_[0], 4))
print("R2 =", round(r2_score(y_test, simple.predict(X_test[["area_sqft"]])), 4))

# Multiple Linear Regression
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)

print("\nMultiple Regression Coefficients:")
print("Intercept =", round(model.intercept_, 4))
for name, c in zip(X.columns, model.coef_):
    print(name, "=", round(c, 4))

mse = mean_squared_error(y_test, pred)
print("\nModel Evaluation:")
print("MAE =", round(mean_absolute_error(y_test, pred), 4))
print("MSE =", round(mse, 4))
print("RMSE =", round(np.sqrt(mse), 4))
print("R2 =", round(r2_score(y_test, pred), 4))

new_house = pd.DataFrame([[1800, 3, 5, 8.0]], columns=X.columns)
print("\nPredicted price =", round(model.predict(new_house)[0], 2), "lakhs")

# Graphs
xs = np.linspace(500, 3000, 100).reshape(-1, 1)

plt.subplot(1, 2, 1)
plt.scatter(X_train["area_sqft"], y_train)
plt.plot(xs, simple.predict(pd.DataFrame(xs, columns=["area_sqft"])), color="red")
plt.xlabel("Area (sqft)")
plt.ylabel("Price (lakhs)")
plt.title("Simple Linear Regression")

plt.subplot(1, 2, 2)
plt.scatter(pred, y_test - pred, color="purple")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Predicted price")
plt.ylabel("Residual")
plt.title("Residual Plot")

plt.tight_layout()
plt.savefig("exp05_regression.png")
plt.show()
