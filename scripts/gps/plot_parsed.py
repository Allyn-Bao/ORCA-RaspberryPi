from gps_plot_static import plot_path  # your plot_path and gps_delta code

gps_points = []

# Read file with pre-parsed lat/lon lines
with open('gps_data_parsed.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith("Latitude:"):
            try:
                # Extract numbers from the line
                parts = line.split(',')
                lat_str = parts[0].split(':')[1].strip()
                lon_str = parts[1].split(':')[1].strip()
                lat = float(lat_str)
                lon = float(lon_str)
                gps_points.append([lat, lon])
            except (IndexError, ValueError):
                continue  # skip bad lines

# Optional: Remove duplicate consecutive points
unique_points = []
for pt in gps_points:
    if len(unique_points) == 0 or pt != unique_points[-1]:
        unique_points.append(pt)

# Plot the path
xy_path = plot_path(unique_points)

# Print XY coordinates
for i, (x, y) in enumerate(xy_path):
    print(f"Point {i}: X = {x:.3f} m, Y = {y:.3f} m")
