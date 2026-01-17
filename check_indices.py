import csv

csv_path = 'RegionalProfile.csv'

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        print(f"Total columns: {len(headers)}")
        for i, h in enumerate(headers):
            print(f"{i}: {h}")

except Exception as e:
    print(f"Error: {e}")
