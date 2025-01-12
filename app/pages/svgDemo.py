from app.tools.svg_tools import Canvas, Style
import math
import numpy as np


class Matrix3D:
    @staticmethod
    def rotation_y(angle):
        """Create rotation matrix around Y axis"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return np.array([
            [cos_a, 0, -sin_a, 0],
            [0, 1, 0, 0],
            [sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_x(angle):
        """Create rotation matrix around X axis"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, cos_a, sin_a, 0],
            [0, -sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ])


def project_point(point, focal_length=2):
    """Project 3D point to 2D using perspective projection"""
    x, y, z = point
    # Move points forward so they're in front of the camera
    z += 3  # Offset to ensure points are in front of camera
    scale = focal_length / z
    return np.array([x * scale, y * scale])


# Create canvas
WIDTH, HEIGHT = 800, 800
canvas = Canvas(WIDTH, HEIGHT)
canvas.background("white")

# Configuration
NUM_SLICES = 25
NUM_POINTS = 100  # Points per circle
RADIUS = 1.0
ROTATION_Y = math.radians(30)
ROTATION_X = math.radians(15)

# Create transformation matrix
transform = Matrix3D.rotation_y(ROTATION_Y) @ Matrix3D.rotation_x(ROTATION_X)

# Calculate center for screen space transformation
center_x = WIDTH / 2
center_y = HEIGHT / 2
scale = 300  # Scale factor for final rendering

# Generate circles at different heights
for i in range(NUM_SLICES):
    # Calculate height position (-1 to 1)
    height = 1 - (2 * i / (NUM_SLICES - 1))

    # Calculate radius at this height using sphere equation
    circle_radius = RADIUS * math.sqrt(1 - height * height)

    # Generate points for this circle
    points_2d = []
    for j in range(NUM_POINTS):
        angle = (j / NUM_POINTS) * 2 * math.pi

        # Create 3D point on circle
        point = np.array([
            circle_radius * math.cos(angle),
            height,
            circle_radius * math.sin(angle),
            1
        ])

        # Transform point
        transformed = transform @ point

        # Project to 2D
        projected = project_point(transformed[:3])

        # Convert to screen space
        screen_x = center_x + projected[0] * scale
        screen_y = center_y + projected[1] * scale
        points_2d.append((screen_x, screen_y))

    # Draw the projected circle
    canvas.stroke("black")
    canvas.fill("none")
    canvas.begin_shape()
    for x, y in points_2d:
        canvas.vertex(x, y)
    canvas.end_shape(close=True)

# Save and display the result
output_path = "sphere_slices.svg"
canvas.save(output_path)

# Open in default browser
import os
import platform

system = platform.system().lower()
try:
    if system == 'windows':
        os.system(f"start {output_path}")
    elif system == 'darwin':  # macOS
        os.system(f"open {output_path}")
    elif system == 'linux':
        os.system(f"xdg-open {output_path}")
    else:
        print(f"Unsupported operating system: {system}")
        print(f"SVG saved to: {output_path}")
except Exception as e:
    print(f"Error opening SVG: {str(e)}")
    print(f"SVG saved to: {output_path}")