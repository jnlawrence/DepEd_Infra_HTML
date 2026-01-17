import csv
import collections

csv_path = 'RegionalProfile.csv'
idx_division = 1
idx_province = 18

print("Scanning for Divisions with mixed Province values...")

div_provs = collections.defaultdict(set)

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        for row in reader:
            if len(row) <= idx_province: continue
            
            div = row[idx_division].strip()
            prov = row[idx_province].strip()
            
            if div:
                div_provs[div].add(prov)

    print("\nDivisions with multiple Provinces (potential splits):")
    for div, provs in div_provs.items():
        if len(provs) > 1:
            print(f"Division: '{div}' -> Provinces: {provs}")

    print("\nCheck Specific Cities:")
    for city in ["Baguio City", "Davao City", "Zamboanga City", "Iloilo City", "Cebu City"]:
        print(f"{city}: {div_provs.get(city, 'Not Found')}")

except Exception as e:
    print(f"Error: {e}")
