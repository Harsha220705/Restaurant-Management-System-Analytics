import pandas as pd

# Replace with your Excel file name
excel_file = 'database_data.xlsx'

# Load all sheets
sheets = pd.read_excel(excel_file, sheet_name=None)

# Convert each sheet to CSV
for sheet_name, data in sheets.items():
    csv_file = f"{sheet_name}.csv"
    data.to_csv(csv_file, index=False)
    print(f"Saved: {csv_file}")