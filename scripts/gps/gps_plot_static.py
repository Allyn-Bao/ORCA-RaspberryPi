import math
import matplotlib.pyplot as plt

METERS_PER_DEGREE_LAT = 111320

'''Function to get the deta NS and EW between 2 comnsecutive gps points'''
def gps_delta(pt1, pt2):
    # average latitude
    avg_lat = math.radians((pt1[0] + pt2[0])/2)

    delta_lat = pt2[0] - pt1[0]
    delta_lon = pt2[1] - pt1[1]

    delta_y = delta_lat * METERS_PER_DEGREE_LAT
    delta_x = delta_lon * METERS_PER_DEGREE_LAT * math.cos(avg_lat)

    return [delta_x, delta_y]


def plot_path(points):
    locations = [[0,0]]
    for i in range(len(points) - 1):
        delta = gps_delta(points[i], points[i+1])
        xy = [delta[0] + locations[i][0], delta[1] + locations[i][1]]
        locations.append(xy)
    
    # Extract x and y coordinates for plotting
    x_vals = [p[0] for p in locations]
    y_vals = [p[1] for p in locations]

    # Plot the path
    plt.figure(figsize=(6, 6))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue')
    plt.title('GPS Path (Projected XY in Meters)')
    plt.xlabel('X (East) [meters]')
    plt.ylabel('Y (North) [meters]')
    plt.grid(True)
    plt.axis('equal')
    #plt.show()
    plt.savefig('gps_plot.png')

    return locations


# === TEST ===
# Convert your DMM points to decimal degrees
points = [
    [43 + 28.22996 / 60, 80 + 32.42608 / 60],  # Point A
    [43 + 28.22284 / 60, 80 + 32.42694 / 60]   # Point B
]

# Run and plot
path = plot_path(points)

# Print path coordinates
for i, (x, y) in enumerate(path):
    print(f"Point {i}: X = {x:.3f} m, Y = {y:.3f} m")
