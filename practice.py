import pandas as pd

# Load your Excel file
file_path = "data/customer_complaints.xlsx"  # Replace with your file path
df = pd.read_excel(file_path)

print("Column names in your file:")
print(df.columns.tolist())
print("\nFirst row:")
print(df.head(1))
print("\nData types:")
print(df.dtypes)