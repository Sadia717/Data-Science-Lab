#24-11-2026
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

np.random.seed(1)
months = pd.date_range("2025-01-01", periods=24, freq="MS")
t = np.arange(24)
sales = pd.DataFrame({
"Electronics":120+4*t+15*np.sin(2*np.pi*t/12)+np.random.normal(0,5,24),
"Clothing":90+1.5*t+25*np.sin(2*np.pi*(t-3)/12)+np.random.normal(0,5,24),
"Groceries":150+0.8*t+np.random.normal(0,4,24)
},index=months).round(1)

print("Monthly Sales Trend Analysis using Line Plots")
print("="*46)
print(sales.head(6).to_string())
print("...")
print("\nYearly totals (Rs. lakhs):")
print(sales.groupby(sales.index.year).sum().round(1).to_string())

peak = sales["Electronics"].idxmax()
print(f"\nPeak Electronics month: {peak:%b %Y} ({sales['Electronics'].max()} lakhs)")
slope,intercept = np.polyfit(t,sales["Electronics"],1)
print(f"Electronics trend line: sales = {intercept:.2f} + {slope:.2f} * month_index")

rolling = sales["Electronics"].rolling(3).mean()
fig,ax = plt.subplots(figsize=(10,5))
styles = [("tab:blue","-","o"),("tab:orange","--","s"),("tab:green",":","^")]
for c,(color,line,marker) in zip(sales.columns,styles):
    ax.plot(months,sales[c],color=color,linestyle=line,marker=marker,label=c)
ax.plot(months,intercept+slope*t,"k-.",label="Electronics trend")
ax.set(title="Monthly Sales by Category (2025-2026)",xlabel="Month",ylabel="Sales (Rs. lakhs)")
ax.set_ylim(40,260)
ax.set_yticks(range(40,261,20))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.grid(True,linestyle="--",alpha=.5)
ax.annotate(f"Peak: {sales['Electronics'].max()}",xy=(peak,sales["Electronics"].max()),
xytext=(peak-pd.Timedelta(days=200),245),arrowprops=dict(arrowstyle="->",color="red"),color="red")
ax.text(months[1],55,"Clothing peaks every summer",fontsize=9,style="italic")
ax.legend(loc="upper left",ncol=2)
plt.tight_layout()
plt.savefig("exp17_line.png",dpi=150)

fig,axes = plt.subplots(2,1,figsize=(10,6),sharex=True)
axes[0].plot(months,sales["Electronics"],label="Monthly",alpha=.6)
axes[0].plot(months,rolling,color="red",label="3-month moving average")
axes[0].set_title("Electronics: Smoothing a Time Series")
axes[0].legend()
axes[0].grid(alpha=.4)
growth = sales.pct_change()*100
axes[1].bar(months,growth["Groceries"],width=20,color="tab:green")
axes[1].axhline(0,color="black",linewidth=.8)
axes[1].set_title("Groceries: Month-on-Month Growth (%)")
axes[1].grid(alpha=.4)
axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b-%y"))
plt.tight_layout()
plt.savefig("exp17_timeseries.png",dpi=150)
plt.show()
print("\nSaved figures: exp17_line.png, exp17_timeseries.png")
