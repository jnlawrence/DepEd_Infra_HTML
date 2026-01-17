import csv

csv_path = 'RegionalProfile.csv'
idx_region = 0

print("Scanning for Unique Regions...")

regions = set()

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        for row in reader:
            if len(row) > idx_region:
                reg = row[idx_region].strip()
                if reg:
                    regions.add(reg)

    print("\nUnique Regions Found:")
    for r in sorted(list(regions)):
        print(f" - '{r}'")

except Exception as e:
    print(f"Error: {e}")
