from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_FILE = BASE_DIR / "data" / "raw" / "supply_chain_data.xlsx"

# Load dataset
df = pd.read_excel(DATA_FILE)

print("================================")
print("SUPPLY CHAIN ANALYSIS")
print("================================")

print("Dataset loaded successfully!")
print()

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print()
print("First 5 records:")
print(df.head())


print()
print("DATASET INFORMATION")
print("====================")

df.info()

print()
print("COLUMN NAMES")
print("============")

for column in df.columns:
    print(column)



print()
print("MISSING VALUES")
print("==============")

print(df.isnull().sum())


print()
print("DUPLICATE RECORDS")
print("=================")

print("Duplicate rows:", df.duplicated().sum())

print()
print("NUMERICAL SUMMARY")
print("=================")

print(df.describe())



df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"],
    errors="coerce"
)

df["Expected_Date"] = pd.to_datetime(
    df["Expected_Date"],
    errors="coerce"
)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"],
    errors="coerce"
)

df["Expected_Date"] = pd.to_datetime(
    df["Expected_Date"],
    errors="coerce"
)

df["Distance_KM"] = pd.to_numeric(
    df["Distance_KM"],
    errors="coerce"
)

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


df["Delay_Reason"] = df["Delay_Reason"].fillna("None")



df["Carrier"] = df["Carrier"].fillna("Unknown")

df["Supplier"] = df["Supplier"].fillna("Unknown")

df["Shipping_Cost"] = df["Shipping_Cost"].fillna(
    df["Shipping_Cost"].median()
)

df["Delivery_Days"] = (
    df["Delivery_Date"] -
    df["Order_Date"]
).dt.days


print(df[[
    "Order_Date",
    "Delivery_Date",
    "Delivery_Days"
]].head())


df["Delay_Days"] = (
    df["Delivery_Date"] -
    df["Expected_Date"]
).dt.days


df["On_Time"] = np.where(
    df["Delivery_Date"] <= df["Expected_Date"],
    "Yes",
    "No"
)

print(df["On_Time"].value_counts())


on_time_rate = (
    df["On_Time"].eq("Yes").mean() * 100
)

print(
    "On-Time Delivery Rate:",
    round(on_time_rate, 2),
    "%"
)


total_shipping_cost = df["Shipping_Cost"].sum()

print(
    "Total Shipping Cost:",
    total_shipping_cost
)


average_delivery_days = df["Delivery_Days"].mean()

print(
    "Average Delivery Days:",
    round(average_delivery_days, 2)
)


delayed_orders = (
    df["On_Time"] == "No"
).sum()

print(
    "Delayed Orders:",
    delayed_orders
)


print()
print("================================")
print("SUPPLY CHAIN KPI SUMMARY")
print("================================")

print("Total Orders:", len(df))

print(
    "Total Shipping Cost:",
    round(df["Shipping_Cost"].sum(), 2)
)

print(
    "Average Delivery Days:",
    round(df["Delivery_Days"].mean(), 2)
)

print(
    "On-Time Delivery Rate:",
    round(on_time_rate, 2),
    "%"
)

print(
    "Delayed Orders:",
    delayed_orders
)


transport_analysis = df.groupby(
    "Transport_Mode"
).agg(
    Orders=("Order_ID", "count"),
    Average_Delivery_Days=("Delivery_Days", "mean"),
    Average_Shipping_Cost=("Shipping_Cost", "mean"),
    On_Time_Rate=("On_Time", lambda x:
        (x == "Yes").mean() * 100
    )
).reset_index()

print()
print("TRANSPORTATION ANALYSIS")
print("=======================")

print(
    transport_analysis.round(2)
)

carrier_analysis = df.groupby(
    "Carrier"
).agg(
    Orders=("Order_ID", "count"),
    Average_Delivery_Days=("Delivery_Days", "mean"),
    Average_Shipping_Cost=("Shipping_Cost", "mean"),
    On_Time_Rate=("On_Time", lambda x:
        (x == "Yes").mean() * 100
    )
).reset_index()

print()
print("CARRIER PERFORMANCE")
print("===================")

print(
    carrier_analysis.round(2)
)

delayed_df = df[df["On_Time"] == "No"]

delay_analysis = (
    delayed_df["Delay_Reason"]
    .value_counts()
    .reset_index()
)

delay_analysis.columns = [
    "Delay_Reason",
    "Delayed_Orders"
]

print()
print("DELAY REASONS")
print("=============")

print(delay_analysis)


df["Month"] = (
    df["Order_Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_analysis = df.groupby(
    "Month"
).agg(
    Orders=("Order_ID", "count"),
    Shipping_Cost=("Shipping_Cost", "sum"),
    Average_Delivery_Days=("Delivery_Days", "mean"),
    On_Time_Rate=("On_Time", lambda x:
        (x == "Yes").mean() * 100
    )
).reset_index()

print()
print("MONTHLY PERFORMANCE")
print("===================")

print(
    monthly_analysis.round(2)
)


plt.figure(figsize=(12, 6))

plt.plot(
    monthly_analysis["Month"],
    monthly_analysis["Orders"],
    marker="o"
)

plt.title("Monthly Order Volume")
plt.xlabel("Month")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "python/charts/monthly_orders.png"
)

plt.show()

plt.figure(figsize=(10, 6))

plt.bar(
    transport_analysis["Transport_Mode"],
    transport_analysis["On_Time_Rate"]
)

plt.title("On-Time Delivery by Transport Mode")
plt.xlabel("Transport Mode")
plt.ylabel("On-Time Delivery %")

plt.tight_layout()

plt.savefig(
    "python/charts/transport_on_time.png"
)

plt.show()

plt.figure(figsize=(10, 6))

plt.bar(
    delay_analysis["Delay_Reason"],
    delay_analysis["Delayed_Orders"]
)

plt.title("Orders Delayed by Reason")
plt.xlabel("Delay Reason")
plt.ylabel("Delayed Orders")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "python/charts/delay_reasons.png"
)

plt.show()


OUTPUT_FILE = (
    BASE_DIR /
    "data" /
    "cleaned" /
    "supply_chain_cleaned.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Cleaned dataset saved successfully!")
print(OUTPUT_FILE)