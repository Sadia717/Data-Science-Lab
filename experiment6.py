#20-11-26
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                            f1_score, confusion_matrix, roc_auc_score, roc_curve)

np.random.seed(3)
n = 400

tenure = np.random.randint(1, 72, n)
monthly = np.round(np.random.uniform(200, 1500, n), 0)
complaints = np.random.poisson(1.2, n)
contract = np.random.choice([0, 1], n, p=[0.55, 0.45])

logit = -1 - 0.06*tenure + 0.002*monthly + 0.7*complaints - 1.3*contract
churn = (np.random.rand(n) < 1/(1+np.exp(-logit))).astype(int)

data = pd.DataFrame({
    "tenure_months": tenure,
    "monthly_bill": monthly,
    "complaints": complaints,
    "yearly_contract": contract,
    "churn": churn
})

print("Telecom Customer Churn Prediction")
print("=" * 50)
print(data.head().to_string(index=False))
print("\nChurn distribution:", data.churn.value_counts().to_dict())

X = data.drop(columns="churn")
y = data["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=0
)

model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)

lr = model.named_steps["logisticregression"]
print("\nCoefficients and Odds Ratios:")
for name, c in zip(X.columns, lr.coef_[0]):
    print(name, round(c, 4), "Odds Ratio =", round(np.exp(c), 3))

pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:, 1]

print("\nModel Evaluation:")
print("Accuracy =", round(accuracy_score(y_test, pred), 4))
print("Precision =", round(precision_score(y_test, pred), 4))
print("Recall =", round(recall_score(y_test, pred), 4))
print("F1-score =", round(f1_score(y_test, pred), 4))
print("ROC-AUC =", round(roc_auc_score(y_test, prob), 4))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred))

cv = cross_val_score(model, X, y, cv=5)
print("\n5-Fold CV Accuracy:", np.round(cv, 4))
print("Mean =", round(cv.mean(), 4))

customer = pd.DataFrame([[4, 1250, 3, 0]], columns=X.columns)
p = model.predict_proba(customer)[0, 1]
print("\nNew Customer Churn Probability =", round(p, 3))

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, prob)
plt.plot(fpr, tpr, label="Logistic Regression")
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("exp06_roc.png")
plt.show()
