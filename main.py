import pandas as pd

# read raw dataset
df = pd.read_csv("sales2017_raw.csv", header=None)

# extract headers
headers = df.iloc[2]

# actual data
clean_df = df.iloc[4:].copy()

# set headers
clean_df.columns = headers

# remove fully empty rows
clean_df = clean_df.dropna(how="all")

# clean column names
clean_df.columns = (
    clean_df.columns.astype(str).str.strip().str.lower().str.replace(" ", "_")
)

# replace nothing values with NaN
clean_df = clean_df.replace(["(nothing)", "nothing"], pd.NA)

# clean sales column
clean_df["sales"] = (
    clean_df["sales"].astype(str).str.replace(" sales", "", regex=False).str.strip()
)

# numeric conversion
numeric_cols = ["sales", "revenue", "stock", "price"]

for col in numeric_cols:
    clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

# date conversion
clean_df["order_date"] = pd.to_datetime(clean_df["order_date"], errors="coerce")

# remove duplicates
clean_df = clean_df.drop_duplicates()

# reset index
clean_df = clean_df.reset_index(drop=True)

# drop unwanted columns
clean_df = clean_df.drop(
    columns=[
        "promo_discount_2",
        "promo_bin_2",
        "promo_type_2",
        "column3",
        "promo_discount2",
    ],
    errors="ignore",
)

# rename columns
clean_df = clean_df.rename(
    columns={
        "order_id_(unique)": "order_id",
        "order_date_2": "order_date_alt",
        "delivery_date_format1": "delivery_date_1",
        "delivery_date_format2": "delivery_date_2",
    }
)

# check info
print(clean_df.info())

# check missing values
print(clean_df.isnull().sum())

# save cleaned dataset
clean_df.to_csv("sales_clean.csv", index=False)

print("Cleaning completed successfully!")
