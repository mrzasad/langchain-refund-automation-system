import pandas as pd

# Load the file
df = pd.read_excel("data/customer_complaints.xlsx")

# Print current columns
print("Current columns:")
print(df.columns.tolist())

# Rename columns (adjust based on your actual column names)
df.columns = df.columns.str.lower().str.strip()

# Map to expected names
column_mapping = {
    'customer_name': 'customer_name',
    'order_id': 'order_id',
    'complaint_text': 'complaint_text',
    'complaint_date': 'complaint_date',
    # Add more mappings if your columns have different names
    # Example: 'customer': 'customer_name'
}

df = df.rename(columns=column_mapping)

# Verify
print("\nNew columns:")
print(df.columns.tolist())

# Save back to Excel
df.to_excel("customer_complaints.xlsx", index=False)
print("\n✅ File fixed and saved!")