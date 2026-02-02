import pandas as pd

# Path to Excel file
excel_path = "../data/excel/AI_Healthcare_Metadata.xlsx"

# Read Excel file
df = pd.read_excel(excel_path)

# Display basic info
print("Excel file read successfully")
print("Number of records:", len(df))
print("\nColumn names:")
print(df.columns)

# Show first 3 rows
print("\nSample data:")
print(df.head(3))
