import csv

csv_path = 'RegionalProfile.csv'
idx_region = 0
idx_division = 1
idx_province = 18
idx_school_name = 3

print("Scanning CSV for Baguio City Data...")

baguio_division_count = 0
baguio_province_count = 0
baguio_province_vals = set()

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        for i, row in enumerate(reader):
            if len(row) <= idx_province: continue
            
            div = row[idx_division].strip()
            prov = row[idx_province].strip()
            name = row[idx_school_name].strip()
            
            if "Baguio" in div:
                baguio_division_count += 1
                baguio_province_vals.add(prov)
                if i < 5: # Print first few for sample
                    print(f"Sample School (Div={div}): {name}, Prov='{prov}'")
            
            if "Baguio" in prov:
                baguio_province_count += 1

    print(f"\nTotal rows with Division 'Baguio City': {baguio_division_count}")
    print(f"Total rows with Province 'Baguio City': {baguio_province_count}")
    print(f"Provinces found for Baguio City Division: {baguio_province_vals}")

except Exception as e:
    print(f"Error: {e}")
