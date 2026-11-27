"""Usage: python clean_train.py train.csv  (the raw file is never modified)"""
import sys
import pandas as pd

from pathlib import Path

here = Path(__file__).parent
source = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\HP\OneDrive\Desktop\Retail Sales Analysis\data\train.csv"
raw = pd.read_csv(source, dtype={"Postal Code": "string"})
df = raw.copy()
df.columns = df.columns.str.lower().str.replace(r"[ -]", "_", regex=True)

# Types: dates are day/month/year, so state the format explicitly
for c in ["order_date", "ship_date"]:
    df[c] = pd.to_datetime(df[c], format="%d/%m/%Y", errors="raise")

# Text: collapse repeated and edge whitespace
text = df.select_dtypes(include=["object", "string"]).columns.drop("postal_code")
for c in text:
    df[c] = df[c].str.replace(r"\s+", " ", regex=True).str.strip()

# Postal codes: fill Burlington, Vermont (05401 is one of its ZIPs, an assumption), restore leading zeros
burlington = df.postal_code.isna() & df.city.eq("Burlington") & df.state.eq("Vermont")
df["postal_code_imputed"] = burlington
df.loc[burlington, "postal_code"] = "05401"
df["postal_code"] = df.postal_code.str.zfill(5)

# Flag for review rather than delete or overwrite
df["possible_duplicate"] = df.duplicated(df.columns.drop(["row_id", "postal_code_imputed"]), keep=False)
df["product_id_conflict"] = df.groupby("product_id").product_name.transform("nunique") > 1
q1, q3 = df.sales.quantile([.25, .75])
df["sales_outlier"] = df.sales > q3 + 1.5 * (q3 - q1)

# Derived column
df["days_to_ship"] = (df.ship_date - df.order_date).dt.days

# Validate
assert len(df) == len(raw)
assert df.row_id.is_unique
assert df.days_to_ship.ge(0).all()
assert df.sales.gt(0).all()
assert df.postal_code.str.fullmatch(r"\d{5}").all()
assert abs(df.sales.sum() - raw.Sales.sum()) < 1e-6

output_folder = here / "data" 
output_folder.mkdir(parents=True, exist_ok=True)
df.to_csv(output_folder / "train_clean.csv", index=False, date_format="%Y-%m-%d")
print(df[["postal_code_imputed", "possible_duplicate", "product_id_conflict", "sales_outlier"]].sum())