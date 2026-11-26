
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(11)
departments = ["Cardiology","Orthopaedics","Neurology","Paediatrics","General"]
budget = [28,18,22,12,20]
p25 = [820,640,410,930,1500]
p26 = [910,700,455,880,1620]
wait = {d:np.random.gamma(k,6,120) for d,k in zip(departments,[3,2.5,4,1.8,5])}
ages = np.concatenate([np.random.normal(8,4,300),np.random.normal(45,12,700),np.random.normal(70,8,300)])
ages = ages[(ages>0)&(ages<100)]

print("Hospital Operations Dashboard: Choosing the Right Graph")
print("="*56)
print("\nBudget share (%)       :",dict(zip(departments,budget)))
print("Patients 2025 vs 2026 :")
for d,a,b in zip(departments,p25,p26):
    print(f" {d:<13} {a:>5} {b:>5} change = {100*(b-a)/a:+.1f}%")
print("\nPatient age: n = {}, mean = {:.1f}, median = {:.1f}, std = {:.1f}".format(
len(ages),ages.mean(),np.median(ages),ages.std()))
print("\nWaiting time (minutes) summary by department:")
print(pd.DataFrame(wait).describe().T[["mean","25%","50%","75%","max"]].round(1).to_string())

fig,ax = plt.subplots(2,2,figsize=(12,9))
ax[0,0].pie(budget,labels=departments,autopct="%1.0f%%",startangle=90,
explode=[.08 if s==max(budget) else 0 for s in budget],shadow=True)
ax[0,0].set_title("Parts of a Whole: Budget Share")

x=np.arange(5); w=.38
b1=ax[0,1].bar(x-w/2,p25,w,label="2025")
b2=ax[0,1].bar(x+w/2,p26,w,label="2026")
ax[0,1].bar_label(b2,fontsize=8)
ax[0,1].set_xticks(x,departments,rotation=20)
ax[0,1].set_ylabel("Patients")
ax[0,1].legend()
ax[0,1].set_title("Comparison: Patients per Department")

ax[1,0].hist(ages,bins=25,edgecolor="white")
ax[1,0].axvline(ages.mean(),color="red",linestyle="--",label=f"Mean = {ages.mean():.1f}")
ax[1,0].set_xlabel("Age (years)")
ax[1,0].set_ylabel("Number of patients")
ax[1,0].set_title("Distribution: Patient Age")
ax[1,0].legend()

ax[1,1].boxplot(wait.values(),tick_labels=[d[:5] for d in departments],patch_artist=True,
boxprops=dict(facecolor="#edc948"))
ax[1,1].set_ylabel("Waiting time (minutes)")
ax[1,1].set_title("Groups: Waiting Time by Department")
plt.tight_layout()
plt.savefig("exp18_dashboard.png",dpi=150)
plt.show()

order=np.argsort(p26)
plt.figure(figsize=(7,3.5))
plt.barh(np.array(departments)[order],np.array(p26)[order],color="#76b7b2")
plt.xlabel("Patients in 2026")
plt.title("Ranked Comparison (Horizontal Bar)")
plt.tight_layout()
plt.savefig("exp18_barh.png",dpi=150)
print("\nSaved figures: exp18_dashboard.png, exp18_barh.png")
