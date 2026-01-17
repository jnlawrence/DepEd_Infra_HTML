import csv
import collections

csv_path = 'RegionalProfile.csv'
idx_gov = 28
idx_region = 0
idx_division = 1
idx_province = 18

print("Scanning CSV for Governor Data...")

gov_counts = collections.defaultdict(set)
ncr_govs = set()

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print(f"Header at {idx_gov}: {headers[idx_gov] if len(headers) > idx_gov else 'INDEX OUT OF BOUNDS'}")

        # First pass to count unique governors per region
        rows = list(reader)
        
        for row in rows:
            if len(row) <= idx_gov: continue
            
            reg = row[idx_region]
            gov = row[idx_gov].strip()
            
            if gov:
                gov_counts[reg].add(gov)
                if reg == "NCR":
                    ncr_govs.add(gov)

        print("\nGovernor Data Found per Region:")
        for reg, govs in gov_counts.items():
            print(f"{reg}: {len(govs)} unique governors found. {list(govs)[:3]}")

        print("\nNCR Governors Found:")
        print(ncr_govs)

        print("\nProvinces with Missing/Placeholder Governors:")
       
        prov_govs = {}
        
        for row in rows:
            if len(row) <= idx_gov: continue
            
            reg = row[idx_region]
            div = row[idx_division]
            prov = row[idx_province]
            gov = row[idx_gov].strip()
            
            # Logic matches parse_data.py
            if reg == "NCR":
                p_key = "Metro Manila"
            else:
                p_key = prov if prov else div
            
            if not p_key: p_key = "Unspecified"
            
            if p_key not in prov_govs:
                prov_govs[p_key] = set()
            
            if gov:
                prov_govs[p_key].add(gov)
                
        for p, govs in prov_govs.items():
            if not govs or (len(govs) == 1 and ('' in govs or 'Hon. Governor' in govs or '' in govs)):
                print(f"MISSING: {p} (Found: {govs})")

except Exception as e:
    print(f"Error: {e}")
