import csv

# === CONFIGURATION ===
map_file_path = 'deux-couloirs-cegep-septembre25-source.map'   # your input map file
output_map_path = 'deux-couloirs-cegep-septembre25-goals.map'  # output map file
csv_file_path = 'pointsList.csv'         # your CSV file with goals

# === READ GOALS FROM CSV ===
goals = []
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = int(row['x'])
        y = int(row['y'])
        h_str = row.get('h', '').strip()
        heading = float(h_str) if h_str else -90
        name = f'goalx{x}y{y}'
        goals.append(f'Cairn: Goal {x} {y} {heading:.6f} "" ICON "{name}"')

# === INSERT INTO MAP FILE ===
with open(map_file_path, 'r') as f:
    lines = f.readlines()

# Find the line before which to insert (before "LINES" section)
insert_index = None
for i, line in enumerate(lines):
    if line.strip() == "LINES":
        insert_index = i
        break

if insert_index is None:
    raise ValueError("LINES section not found in map file!")

# Insert goal lines before LINES
new_lines = lines[:insert_index] + [g + '\n' for g in goals] + lines[insert_index:]

# Write to new file
with open(output_map_path, 'w') as f:
    f.writelines(new_lines)

print(f"Inserted {len(goals)} goals into: {output_map_path}")
