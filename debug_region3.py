import csv
import collections

csv_path = 'RegionalProfile.csv'
idx_region = 0
idx_division = 1
idx_province = 18

print("Scanning Region III Data...")

r3_provinces = set()
sjdm_provs = set()
ne_variations = set()
sf_variations = []

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        for row in reader:
            if len(row) <= idx_province: continue
            
            reg = row[idx_region].strip()
            div = row[idx_division].strip()
            prov = row[idx_province].strip()
            
            if reg == "Region III":
                r3_provinces.add(prov)
                if "Nueva Ecija" in prov or "NUEVA ECIJA" in prov:
                    ne_variations.add(prov)
                
                if "San Jose del Monte" in div:
                    sjdm_provs.add(prov)
                    
                if "La Union" in prov:
                    print(f"ALERT: La Union found in Region III! Div: {div}, Prov: {prov}")

            # Check logic for San Fernando collision
            if "San Fernando" in div:
                sf_variations.append((reg, div, prov))

    print(f"\nRegion III Provinces Found: {r3_provinces}")
    print(f"Nueva Ecija Variations: {ne_variations}")
    print(f"San Jose del Monte Provinces: {sjdm_provs}")
    
    print("\nSan Fernando City Entries (All Regions):")
    for item in sf_variations:
        print(item)

except Exception as e:
    print(f"Error: {e}")
