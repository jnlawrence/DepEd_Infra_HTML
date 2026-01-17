import csv

csv_path = 'RegionalProfile.csv'
idx_region = 0
idx_division = 1
idx_province = 18

print("Scanning Region VI Data...")

r6_raw_provinces = set()
r6_divisions_empty_prov = set()
div_to_prov_map = {}

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        
        # 1. Build Map (simulating parse_data.py logic)
        for row in rows:
            if len(row) > idx_province:
                r_val = row[idx_region].strip()
                d_val = row[idx_division].strip()
                p_val = row[idx_province].strip()
                
                if d_val and p_val:
                    key = (r_val, d_val)
                    if key not in div_to_prov_map:
                        div_to_prov_map[key] = p_val.title()

        # 2. Analyze Region VI
        for row in rows:
            if len(row) <= idx_province: continue
            
            reg = row[idx_region].strip()
            div = row[idx_division].strip()
            prov = row[idx_province].strip().title() # Normalize
            
            if reg == "Region VI":
                if prov:
                    r6_raw_provinces.add(prov)
                else:
                    r6_divisions_empty_prov.add(div)
        
    print(f"\nCreate Region VI Raw Provinces (from CSV column):")
    for p in sorted(list(r6_raw_provinces)):
        print(f" - '{p}'")

    print(f"\nRegion VI Divisions with Empty Province:")
    for d in sorted(list(r6_divisions_empty_prov)):
        mapped_prov = div_to_prov_map.get(("Region VI", d), "NO MAPPING FOUND -> Will fallback to Division Name")
        print(f" - Div: '{d}' -> Maps to: '{mapped_prov}'")

except Exception as e:
    print(f"Error: {e}")
