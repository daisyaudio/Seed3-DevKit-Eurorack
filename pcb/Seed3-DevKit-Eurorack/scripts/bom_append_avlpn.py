"""
BOM Post process to generate an "AVLPN" column that is the best-guess
combination of the value + package format we often use.
"""

import csv
import os

# consts based on kicad setup/jobset settings.
FOOTPRINT_COL_NAME = "Footprint"
VALUE_COL_NAME = "Value"

# add to this overtime with other viable mappings to save time
# when resolving to OBSY
FOOTPRINT_TO_PACKAGE_MAP = {
    "Resistor_SMD:R_0603_1608Metric": "R0603",
    "Capacitor_SMD:C_0603_1608Metric": "C0603",
    "Capacitor_SMD:C_0805_2012Metric": "C0805",
    "Capacitor_SMD:C_0402_1005Metric": "C0402",
    "Capacitor_SMD:C_1206_3216Metric": "C1206",
}

print("\tpost-processing: adding best-guess AVLPN column to BOM...")

production_dir = os.path.join(os.getcwd(), "production")
bom_file = None
for fname in os.listdir(production_dir):
    if "bom" in fname and fname.endswith(".csv"):
        bom_file = os.path.join(production_dir, fname)
        break

if not bom_file:
    print("\tNo BOM CSV file found.")
    exit(1)

with open(bom_file, newline="", encoding="utf-8") as f:
    reader = list(csv.reader(f))
    if not reader:
        print("\tCSV File is empty")
    # copy data to modify and then write back to file
    header = reader[0]
    rows = reader[1:]

header.append("AVL_Part_Number")
try:
    footprint_idx = header.index(FOOTPRINT_COL_NAME)
    value_idx = header.index(VALUE_COL_NAME)
except ValueError as err:
    print(f"\tCSV BOM is missing columns: {err}")
    exit(1)

for row in rows:
    fp = row[footprint_idx]
    value = row[value_idx]
    if fp in FOOTPRINT_TO_PACKAGE_MAP:
        avl_pn = f"{value} {FOOTPRINT_TO_PACKAGE_MAP[fp]}"
    else:
        avl_pn = value
    row.append(avl_pn)

with open(bom_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("\tpost-processing: done adding column.")
