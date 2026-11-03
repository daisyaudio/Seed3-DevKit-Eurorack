"""File for renaming fieldnames in kicad centroid to match JLPCBs expected names"""

import os
import csv

fieldname_map = {
    "PosX": "Mid X",
    "PosY": "Mid Y",
    "Ref": "Designator",
    "Rot": "Rotation",
    "Side": "Layer",
}

print("\tpost-processing: renaming fieldnames in centroid...")

production_dir = os.path.join(os.getcwd(), "production")
centroid_file = None
for fname in os.listdir(production_dir):
    if "centroid" in fname and fname.endswith(".csv"):
        centroid_file = os.path.join(production_dir, fname)
        break

if centroid_file is None:
    print("\tNo centroid CSV file found.")
    exit(1)

with open(centroid_file, newline="", encoding="utf-8") as f:
    reader = list(csv.reader(f))
    if not reader:
        print("\tCSV file is empty.")
        exit(1)
    header = reader[0]
    new_header = [fieldname_map.get(col, col) for col in header]
    rows = reader[1:]

with open(centroid_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(new_header)
    writer.writerows(rows)

print("\tpost-processing: done renaming fields.")
