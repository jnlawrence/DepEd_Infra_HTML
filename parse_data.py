import csv
import json
import os

csv_path = 'RegionalProfile.csv'
output_path = 'dashboard_data.js'

try:
    with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Hardcoded indices

        
        # Hardcoded indices
        # Hardcoded indices - ADJUSTED FOR RegionalProfile.csv (IDENTIFIER at 0)
        idx_region = 1
        idx_division = 2
        idx_school_id = 3
        idx_school_name = 4
        idx_muni = 5
        idx_enrol = 7
        idx_instruct = 8
        idx_cl_req = 9
        idx_cl_short = 10 
        idx_dist = 16
        idx_minor = 21
        idx_major = 22
        idx_const = 23
        idx_cong = 28
        idx_province = 19

        idx_gov = 29
        idx_mayor = 30

        idx_nc_target_23 = 31
        idx_nc_completed_23 = 32
        idx_nc_remaining_23 = 33
        idx_nc_lapsed_23 = 34

        idx_nc_target_24 = 35
        idx_nc_completed_24 = 36
        idx_nc_remaining_24 = 37
        idx_nc_lapsed_24 = 38

        idx_nc_target = 39
        idx_nc_completed = 40
        idx_nc_remaining = 41
        idx_nc_lapsed = 42

        # Unfinished / Loss proxy columns?
        idx_loss_total_prior = 43
        idx_loss_fire_prior = 44
        idx_loss_earthquake_prior = 45
        idx_loss_typhoon_prior = 46 # Overlap/Check?
        idx_loss_repaired_prior = 47 # Check?

        idx_loss_total = 48 # Check?
        idx_loss_fire = 49
        idx_loss_earthquake = 50
        idx_loss_typhoon = 51
        idx_loss_repaired = 52 # Likely invalid

        # New QRF Indices (Shifted +1 from previous valid checks)
        idx_qrf_total_24 = 46
        idx_qrf_major_24 = 47
        idx_qrf_minor_24 = 48
        idx_qrf_total_19_23 = 49
        idx_qrf_major_19_23 = 50
        idx_qrf_minor_19_23 = 51

        # New Columns AZ to BH mapping
        # 52: No. of Sites
        # 53: No. of Storeys
        # 54: With Site Ownership
        # 55: With Buildable Space
        # 56: With Geotech Report
        # 57: No. of CLs
        # 58: INDEX
        
        idx_noSites = 52
        idx_noStoreys = 53
        idx_siteOwnership = 54
        idx_buildableSpace = 55
        idx_geotechReport = 56
        idx_noCLs = 57
        
        # Missing/Removed Columns
        idx_masterlist2026 = -1
        idx_lms = 15
        idx_lmsCLs = -1

        # Note: Previous regular Loss indices might be invalid now if CSV structure changed
        # We will keep reading them but also read new ones.
        # Actually, let's just add the new ones.

        def format_official_name(name):
            if not name: return ""
            if "Governor" in name and "Hon." in name: return name 
            cased = name.title()
            replacements = {
                " Vi": " VI", " Vii": " VII", " Viii": " VIII", " Iv": " IV", " Iii": " III", " Ii": " II",
                " Jr.": " Jr.", " Sr.": " Sr.", " Ma.": " Ma." 
            }
            for old, new in replacements.items():
                if cased.endswith(old):
                    cased = cased[:-len(old)] + new
                elif old + " " in cased:
                     cased = cased.replace(old + " ", new + " ")
            if not cased.startswith("Hon."):
                 cased = f"Hon. {cased}"
            
            # Simple fix for casing
            return cased.strip()

        # External file loading removed/deprecated in favor of CSV columns
        governors = {}
        mayors = {}

        db = {}

        # Pre-scan for Division to Province Mapping
        rows = list(reader)
        div_to_prov_map = {}
        
        for row in rows:
            if len(row) > idx_province:
                r_val = row[idx_region].strip()
                d_val = row[idx_division].strip()
                p_val = row[idx_province].strip()
                if d_val and p_val:
                    # Capture the first non-empty province for a division, scoped by REGION
                    key = (r_val, d_val)
                    if key not in div_to_prov_map:
                        div_to_prov_map[key] = p_val.title() # Store Title Case
        
        # Hardcoded Province Overrides (Fixing San Jose del Monte, etc.)
        PROVINCE_OVERRIDES = {
            "San Jose del Monte City": "Bulacan",
            "Himamaylan City": "Negros Occidental",
            "Sagay City": "Negros Occidental",
            "San Carlos City": "Negros Occidental",
            "Sipalay City": "Negros Occidental",
            "Negros Occidental": "Negros Occidental",
            "Bacolod City": "Negros Occidental" 
        }

        # Reset reader logic (using rows list now)
        for row in rows:
            if len(row) < 5: continue

            def get_val(idx):
                if idx < 0: return ""
                if idx < len(row): return row[idx]
                return ""

            region = get_val(idx_region)
            division = get_val(idx_division)
            district = get_val(idx_dist)
            muni_name = get_val(idx_muni)
            cong = get_val(idx_cong)
            province_name = get_val(idx_province).strip().title() # Normalize Casing
            
            raw_gov = get_val(idx_gov)
            raw_mayor = get_val(idx_mayor)

            gov_name = format_official_name(raw_gov)
            mayor_name = format_official_name(raw_mayor)

            def parse_int(val):
                try: return int(float(val.replace(',', '')))
                except: return 0

            enrol = parse_int(row[idx_enrol])
            instruct = parse_int(row[idx_instruct])
            cl_req = parse_int(row[idx_cl_req])
            cl_short = parse_int(row[idx_cl_short])
            minor = parse_int(row[idx_minor])
            major = parse_int(row[idx_major])
            cons = parse_int(row[idx_const])

            nc_target_23 = parse_int(row[idx_nc_target_23])
            nc_completed_23 = parse_int(row[idx_nc_completed_23])
            nc_remaining_23 = parse_int(row[idx_nc_remaining_23])
            nc_lapsed_23 = parse_int(row[idx_nc_lapsed_23])

            nc_target_24 = parse_int(row[idx_nc_target_24])
            nc_completed_24 = parse_int(row[idx_nc_completed_24])
            nc_remaining_24 = parse_int(row[idx_nc_remaining_24])
            nc_lapsed_24 = parse_int(row[idx_nc_lapsed_24])
            
            nc_target = parse_int(row[idx_nc_target])
            nc_completed = parse_int(row[idx_nc_completed])
            nc_remaining = parse_int(row[idx_nc_remaining])
            nc_lapsed = parse_int(row[idx_nc_lapsed])

            loss_total_prior = parse_int(get_val(idx_loss_total_prior))
            loss_fire_prior = parse_int(get_val(idx_loss_fire_prior))
            loss_earthquake_prior = parse_int(get_val(idx_loss_earthquake_prior))
            loss_typhoon_prior = parse_int(get_val(idx_loss_typhoon_prior))
            loss_repaired_prior = parse_int(get_val(idx_loss_repaired_prior))

            loss_total = parse_int(get_val(idx_loss_total))
            loss_fire = parse_int(get_val(idx_loss_fire))
            loss_earthquake = parse_int(get_val(idx_loss_earthquake))
            loss_typhoon = parse_int(get_val(idx_loss_typhoon))
            loss_repaired = parse_int(get_val(idx_loss_repaired))

            # QRF Data
            qrf_total_24 = parse_int(get_val(idx_qrf_total_24))
            qrf_major_24 = parse_int(get_val(idx_qrf_major_24))
            qrf_minor_24 = parse_int(get_val(idx_qrf_minor_24))
            
            qrf_total_19_23 = parse_int(get_val(idx_qrf_total_19_23))
            qrf_major_19_23 = parse_int(get_val(idx_qrf_major_19_23))
            qrf_minor_19_23 = parse_int(get_val(idx_qrf_minor_19_23))

            # New Columns Extraction
            masterlist2026 = parse_int(get_val(idx_masterlist2026))
            noSites = parse_int(get_val(idx_noSites))
            noStoreys = parse_int(get_val(idx_noStoreys))
            noCLs = parse_int(get_val(idx_noCLs))
            siteOwnership = parse_int(get_val(idx_siteOwnership))
            buildableSpace = parse_int(get_val(idx_buildableSpace))
            geotechReport = parse_int(get_val(idx_geotechReport))
            lms = parse_int(get_val(idx_lms))
            lmsCLs = parse_int(get_val(idx_lmsCLs))


            sc_name = row[idx_school_name]
            sc_id = row[idx_school_id]

            if region not in db:
                db[region] = {'name': region, 'provinces': {}}
            
            # --- PROVINCE GROUPING ---
            if region == "NCR":
                prov_key = "Metro Manila"
            else:
                # 1. Prefer Province Column
                if province_name:
                    prov_key = province_name
                # 2. Check Overrides (e.g. San Jose del Monte)
                elif division in PROVINCE_OVERRIDES:
                     prov_key = PROVINCE_OVERRIDES[division]
                # 3. If empty, check Inferred Map (Scoped by Region)
                elif (region, division) in div_to_prov_map:
                    prov_key = div_to_prov_map[(region, division)]
                # 4. Fallback to Division Name
                else: 
                    prov_key = division.title()
            
            if not prov_key: prov_key = "Unspecified"

            if prov_key not in db[region]['provinces']:
                db[region]['provinces'][prov_key] = {
                    'name': prov_key,
                    'governor': "", # Will populate below
                    'divisions': {},
                    'districts': {},
                    'municipalities': {},
                    'stats': {
                        'schools': 0, 'enrolment': 0, 'classroomReq': 0, 'classroomShortage': 0,
                        'totalClassrooms': 0, 'construction': 0, 'minorRepairs': 0, 'majorRepairs': 0,
                        'ncTarget': 0, 'ncCompleted': 0, 'ncRemaining': 0, 'ncLapsed': 0,
                        'ncTarget24': 0, 'ncCompleted24': 0, 'ncRemaining24': 0, 'ncLapsed24': 0,
                        'ncTarget23': 0, 'ncCompleted23': 0, 'ncRemaining23': 0, 'ncLapsed23': 0,
                        'lossTotal': 0, 'lossFire': 0, 'lossEarthquake': 0, 'lossTyphoon': 0, 'lossRepaired': 0,
                        'lossTotalPrior': 0, 'lossFirePrior': 0, 'lossEarthquakePrior': 0, 'lossTyphoonPrior': 0, 'lossRepairedPrior': 0,
                        'qrfTotal24': 0, 'qrfMajor24': 0, 'qrfMinor24': 0,
                        'qrfTotal19_23': 0, 'qrfMajor19_23': 0, 'qrfMinor19_23': 0,
                        'masterlist2026': 0, 'noSites': 0, 'noStoreys': 0, 'noCLs': 0,
                        'siteOwnership': 0, 'buildableSpace': 0, 'geotechReport': 0,
                        'lms': 0, 'lmsCLs': 0,
                        'singleStorey': 0, 'multiStorey': 0,
                        'siteReadiness': 0
                    }
                }
            
             
            # Hardcoded Governor Overrides
            MANUAL_GOVERNORS = {
                "Zamboanga del Sur": "Victor Yu",
                "Zamboanga del Norte": "Rosalina Jalosjos",
                "Mt. Province": "Bonifacio Lacwasan",
                "North Cotabato": "Emmylou Mendoza",
                "Lanao del Norte": "Imelda Dimaporo",
                "Agusan del Sur": "Santiago Cane Jr.",
                "Surigao del Norte": "Robert Lyndon Barbers",
                "Surigao del Sur": "Alexander Pimentel",
                "Nueva Ecija": "Aurelio Umali",
                "Davao del Norte": "Edwin Jubahib",
                "Davao del Sur": "Yvonne Roña Cagas",
                "Compostela Valley": "Dorothy Montejo-Gonzaga",
                "Siquijor": "Jake Vincent Villa",
                "Dinagat Island": "Nilo Demerey Jr.",
                "Sulu": "Abdusakur Tan",
                "Maguindanao": "Bai Mariam Mangudadatu",
                "Masbate": "Antonio Kho",
                "La Union": "Raphaelle Veronica Ortega-David",
                "Negros Occidental": "Hon. Eugenio Jose Lacson"
            }

            p_obj = db[region]['provinces'][prov_key]
            
            # Fallback Mayor Logic REMOVED (Was overriding formatted name)

            # Update Governor if available and not yet set (or overwrite)
            if gov_name and (not p_obj['governor'] or p_obj['governor'] == "Hon. Governor"):
                 p_obj['governor'] = gov_name
            
            # Logic for "Blanks"
            if not p_obj['governor'] or p_obj['governor'] == "Hon. Governor":
                # 1. Check Manual Overrides
                if prov_key in MANUAL_GOVERNORS:
                    p_obj['governor'] = MANUAL_GOVERNORS[prov_key]
                # 2. If it's a City/Division acting as Province, use Mayor
                elif mayor_name:
                    p_obj['governor'] = f"{mayor_name}" 
                # 3. Last Resort
                else:
                    p_obj['governor'] = "Hon. Governor"

            # Aggregations
            p_obj['stats']['schools'] += 1
            p_obj['stats']['enrolment'] += enrol
            p_obj['stats']['classroomReq'] += cl_req
            p_obj['stats']['classroomShortage'] += cl_short
            p_obj['stats']['totalClassrooms'] += instruct
            p_obj['stats']['construction'] += cons
            p_obj['stats']['minorRepairs'] += minor
            p_obj['stats']['majorRepairs'] += major
            p_obj['stats']['ncTarget'] += nc_target
            p_obj['stats']['ncCompleted'] += nc_completed
            p_obj['stats']['ncRemaining'] += nc_remaining
            p_obj['stats']['ncLapsed'] += nc_lapsed

            p_obj['stats']['ncTarget24'] += nc_target_24
            p_obj['stats']['ncCompleted24'] += nc_completed_24
            p_obj['stats']['ncRemaining24'] += nc_remaining_24
            p_obj['stats']['ncLapsed24'] += nc_lapsed_24

            p_obj['stats']['ncTarget23'] += nc_target_23
            p_obj['stats']['ncCompleted23'] += nc_completed_23
            p_obj['stats']['ncRemaining23'] += nc_remaining_23
            p_obj['stats']['ncLapsed23'] += nc_lapsed_23

            p_obj['stats']['lossTotal'] += loss_total
            p_obj['stats']['lossFire'] += loss_fire
            p_obj['stats']['lossEarthquake'] += loss_earthquake
            p_obj['stats']['lossTyphoon'] += loss_typhoon
            p_obj['stats']['lossRepaired'] += loss_repaired

            p_obj['stats']['lossTotalPrior'] += loss_total_prior
            p_obj['stats']['lossFirePrior'] += loss_fire_prior
            p_obj['stats']['lossEarthquakePrior'] += loss_earthquake_prior
            p_obj['stats']['lossTyphoonPrior'] += loss_typhoon_prior
            p_obj['stats']['lossRepairedPrior'] += loss_repaired_prior

            p_obj['stats']['qrfTotal24'] += qrf_total_24
            p_obj['stats']['qrfMajor24'] += qrf_major_24
            p_obj['stats']['qrfMinor24'] += qrf_minor_24
            
            p_obj['stats']['qrfTotal19_23'] += qrf_total_19_23
            p_obj['stats']['qrfMajor19_23'] += qrf_major_19_23
            p_obj['stats']['qrfMinor19_23'] += qrf_minor_19_23

            p_obj['stats']['masterlist2026'] += masterlist2026
            p_obj['stats']['noSites'] += noSites
            p_obj['stats']['noStoreys'] += noStoreys
            p_obj['stats']['noCLs'] += noCLs
            p_obj['stats']['siteOwnership'] += siteOwnership
            p_obj['stats']['buildableSpace'] += buildableSpace
            p_obj['stats']['geotechReport'] += geotechReport
            p_obj['stats']['lms'] += lms
            p_obj['stats']['lmsCLs'] += lmsCLs

            if noStoreys == 1:
                p_obj['stats']['singleStorey'] += 1
            elif noStoreys > 1:
                p_obj['stats']['multiStorey'] += 1

            if siteOwnership == 1 and buildableSpace == 1 and geotechReport == 1:
                p_obj['stats']['siteReadiness'] += 1


            # Division Nesting
            if division not in p_obj['divisions']:
                p_obj['divisions'][division] = {
                    'name': division,
                    'stats': {'schools': 0, 'enrolment': 0}
                }
            p_obj['divisions'][division]['stats']['schools'] += 1
            p_obj['divisions'][division]['stats']['enrolment'] += enrol

            # District Nesting
            if district not in p_obj['districts']:
                 p_obj['districts'][district] = {
                    'name': district,
                    'division': division,
                    'stats': {'schools': 0, 'enrolment': 0}
                }
            p_obj['districts'][district]['stats']['schools'] += 1
            p_obj['districts'][district]['stats']['enrolment'] += enrol

            # Municipality Nesting
            if muni_name not in p_obj['municipalities']:
                p_obj['municipalities'][muni_name] = {
                    'name': muni_name,
                    'congressman': cong,
                    'mayor': mayor_name if mayor_name else "Hon. Mayor", 
                    'district': district,
                    'division': division,
                    'schools': 0, 'enrolment': 0, 'classroomReq': 0, 'classroomShortage': 0,
                    'totalClassrooms': 0, 'construction': 0, 'minorRepairs': 0, 'majorRepairs': 0,
                    'ncTarget': 0, 'ncCompleted': 0, 'ncRemaining': 0, 'ncLapsed': 0,
                    'ncTarget24': 0, 'ncCompleted24': 0, 'ncRemaining24': 0, 'ncLapsed24': 0,
                    'ncTarget23': 0, 'ncCompleted23': 0, 'ncRemaining23': 0, 'ncLapsed23': 0,
                    'lossTotal': 0, 'lossFire': 0, 'lossEarthquake': 0, 'lossTyphoon': 0, 'lossRepaired': 0,
                    'lossTotalPrior': 0, 'lossFirePrior': 0, 'lossEarthquakePrior': 0, 'lossTyphoonPrior': 0, 'lossRepairedPrior': 0,
                    'qrfTotal24': 0, 'qrfMajor24': 0, 'qrfMinor24': 0,
                    'qrfTotal19_23': 0, 'qrfMajor19_23': 0, 'qrfMinor19_23': 0,
                    'masterlist2026': 0, 'noSites': 0, 'noStoreys': 0, 'noCLs': 0,
                    'siteOwnership': 0, 'buildableSpace': 0, 'geotechReport': 0,
                    'lms': 0, 'lmsCLs': 0,
                    'singleStorey': 0, 'multiStorey': 0,
                    'siteReadiness': 0,
                    'schoolList': []
                }
            
            m_obj = p_obj['municipalities'][muni_name]
            m_obj['schools'] += 1
            m_obj['enrolment'] += enrol
            m_obj['classroomReq'] += cl_req
            m_obj['classroomShortage'] += cl_short
            m_obj['totalClassrooms'] += instruct
            m_obj['construction'] += cons
            m_obj['minorRepairs'] += minor
            m_obj['majorRepairs'] += major
            m_obj['ncTarget'] += nc_target
            m_obj['ncCompleted'] += nc_completed
            m_obj['ncRemaining'] += nc_remaining
            m_obj['ncLapsed'] += nc_lapsed

            m_obj['ncTarget24'] += nc_target_24
            m_obj['ncCompleted24'] += nc_completed_24
            m_obj['ncRemaining24'] += nc_remaining_24
            m_obj['ncLapsed24'] += nc_lapsed_24

            m_obj['ncTarget23'] += nc_target_23
            m_obj['ncCompleted23'] += nc_completed_23
            m_obj['ncRemaining23'] += nc_remaining_23
            m_obj['ncLapsed23'] += nc_lapsed_23

            m_obj['lossTotal'] += loss_total
            m_obj['lossFire'] += loss_fire
            m_obj['lossEarthquake'] += loss_earthquake
            m_obj['lossTyphoon'] += loss_typhoon
            m_obj['lossRepaired'] += loss_repaired

            m_obj['lossTotalPrior'] += loss_total_prior
            m_obj['lossFirePrior'] += loss_fire_prior
            m_obj['lossEarthquakePrior'] += loss_earthquake_prior
            m_obj['lossTyphoonPrior'] += loss_typhoon_prior
            m_obj['lossRepairedPrior'] += loss_repaired_prior

            m_obj['qrfTotal24'] += qrf_total_24
            m_obj['qrfMajor24'] += qrf_major_24
            m_obj['qrfMinor24'] += qrf_minor_24
            
            m_obj['qrfTotal19_23'] += qrf_total_19_23
            m_obj['qrfMajor19_23'] += qrf_major_19_23
            m_obj['qrfMinor19_23'] += qrf_minor_19_23

            m_obj['masterlist2026'] += masterlist2026
            m_obj['noSites'] += noSites
            m_obj['noStoreys'] += noStoreys
            m_obj['noCLs'] += noCLs
            m_obj['siteOwnership'] += siteOwnership
            m_obj['buildableSpace'] += buildableSpace
            m_obj['geotechReport'] += geotechReport
            m_obj['lms'] += lms
            m_obj['lmsCLs'] += lmsCLs

            if noStoreys == 1:
                m_obj['singleStorey'] += 1
            elif noStoreys > 1:
                m_obj['multiStorey'] += 1

            if siteOwnership == 1 and buildableSpace == 1 and geotechReport == 1:
                m_obj['siteReadiness'] += 1

            
            m_obj['schoolList'].append({
                'id': sc_id, 'name': sc_name, 'muni': muni_name,
                'enrolment': enrol, 'classroomReq': cl_req, 'totalClassrooms': instruct,
                'classroomShortage': cl_short, 'construction': cons,
                'minorRepairs': minor, 'majorRepairs': major,
                'ncTarget': nc_target, 'ncCompleted': nc_completed, 'ncRemaining': nc_remaining, 'ncLapsed': nc_lapsed,
                'ncTarget24': nc_target_24, 'ncCompleted24': nc_completed_24, 'ncRemaining24': nc_remaining_24, 'ncLapsed24': nc_lapsed_24,
                'ncTarget23': nc_target_23, 'ncCompleted23': nc_completed_23, 'ncRemaining23': nc_remaining_23, 'ncLapsed23': nc_lapsed_23,
                'lossTotal': loss_total, 'lossFire': loss_fire, 'lossEarthquake': loss_earthquake, 'lossTyphoon': loss_typhoon, 'lossRepaired': loss_repaired,
                'lossTotalPrior': loss_total_prior, 'lossFirePrior': loss_fire_prior, 'lossEarthquakePrior': loss_earthquake_prior, 'lossTyphoonPrior': loss_typhoon_prior, 'lossRepairedPrior': loss_repaired_prior,
                'qrfTotal24': qrf_total_24, 'qrfMajor24': qrf_major_24, 'qrfMinor24': qrf_minor_24,
                'qrfTotal19_23': qrf_total_19_23, 'qrfMajor19_23': qrf_major_19_23, 'qrfMinor19_23': qrf_minor_19_23,
                'masterlist2026': masterlist2026, 'noSites': noSites, 'noStoreys': noStoreys, 'noCLs': noCLs,
                'siteOwnership': siteOwnership, 'buildableSpace': buildableSpace, 'geotechReport': geotechReport,
                'lms': lms, 'lmsCLs': lmsCLs,
                'singleStorey': 1 if noStoreys == 1 else 0,
                'multiStorey': 1 if noStoreys > 1 else 0,
                'siteReadiness': 1 if (siteOwnership == 1 and buildableSpace == 1 and geotechReport == 1) else 0
            })
            
            # Update Mayor/Gov if current row has data and existing is placeholder or empty
            if mayor_name and (not m_obj['mayor'] or "Hon. Mayor" in m_obj['mayor']):
                m_obj['mayor'] = mayor_name

    # Transform to JSON
    final_data = []
    found_regions = []
    
    for r_key in sorted(db.keys()):
        r_val = db[r_key]
        found_regions.append(r_key)
        
        region_entry = {
            'name': r_val['name'],
            'provinces': []
        }

        for p_key in sorted(r_val['provinces'].keys()):
            p_val = r_val['provinces'][p_key]
            
            # Sorted lists
            divisions_list = sorted(p_val['divisions'].values(), key=lambda x: x['name'])
            districts_list = sorted(p_val['districts'].values(), key=lambda x: x['name'])
            munis_list = sorted(p_val['municipalities'].values(), key=lambda x: x['name'])
            
            prov_entry = {
                'name': p_val['name'],
                'governor': p_val['governor'],
                'stats': p_val['stats'],
                'divisions': divisions_list,
                'districts': districts_list,
                'municipalities': munis_list
            }
            region_entry['provinces'].append(prov_entry)
        
        final_data.append(region_entry)

    print(f"Regions found in CSV: {found_regions}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const parsedDatabase = ")
        json.dump(final_data, f, indent=2)
        f.write(";")

    print("JS data file generated successfully.")

except Exception as e:
    print(f"Error: {e}")
