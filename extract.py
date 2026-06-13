import pandas as pd
import json
from datetime import datetime, timezone, timedelta

file_name = r"d:\Dad Business\E-commerce\Business Data 2.xlsx"
sheet_name = 'Stock Keeping'

# 1. Read the sheet, skipping the first row to grab the correct column names
df = pd.read_excel(file_name, sheet_name=sheet_name, header=1)

# 2. Drop the empty divider column (Column E)
df = df.dropna(axis=1, how='all')

# 3. Rename columns. Since the typo is fixed, Pandas will read the Return 
# columns as 'Amazon.1' and 'Meesho.1' natively.
df.rename(columns={
    'Amazon': 'Sold_Amazon',
    'Meesho': 'Sold_Meesho', 
    'Amazon.1': 'Return_Amazon',
    'Meesho.1': 'Return_Meesho',
    'Damaged/Lost/Others': 'Damaged_Lost_Others'
}, inplace=True)

# 4. Find and remove the "Date" column(s) automatically
cols_to_drop = [col for col in df.columns if 'Date' in col]
df.drop(columns=cols_to_drop, inplace=True, errors='ignore')

# 5. Clean up bottom empty rows and replace empty number cells with 0
df = df.dropna(subset=['ITEM'])
df = df.fillna(0)

# 6. Calculate the current Indian Standard Time (IST)
ist_offset = timedelta(hours=5, minutes=30)
ist_time = datetime.now(timezone.utc) + ist_offset
formatted_time = ist_time.strftime("%d-%m-%Y %I:%M %p IST")

# 7. Create the new JSON structure with the timestamp at the top
output_data = {
    "last_updated": formatted_time,
    "inventory": df.to_dict(orient='records')
}

# 8. Save the JSON
with open('data.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Data successfully extracted at {formatted_time} and saved!")