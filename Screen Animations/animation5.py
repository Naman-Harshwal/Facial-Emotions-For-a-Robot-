import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.axis('off')

# Function to draw a star
def draw_star(x, y, size, color):
    star = patches.RegularPolygon((x, y), numVertices=4, radius=size, orientation=np.pi/4, color=color)
    ax.add_patch(star)

# Function to draw eye
def draw_eye(center_x, center_y):
    # Outer white ring
    outer_circle = patches.Circle((center_x, center_y), 1.2, color='#d6f0ff')
    ax.add_patch(outer_circle)
    
    # Middle blue ring
    middle_circle = patches.Circle((center_x, center_y), 1.0, color='#66b7ff')
    ax.add_patch(middle_circle)
    
    # Inner black circle
    inner_circle = patches.Circle((center_x, center_y), 0.65, color='black')
    ax.add_patch(inner_circle)
    
    # White reflection
    reflection = patches.Circle((center_x + 0.4, center_y + 0.4), 0.25, color='#e9f6ff')
    ax.add_patch(reflection)

# Function to draw the mouth
def draw_mouth():
    mouth = patches.Wedge(center=(0, -2.5), r=0.9, theta1=0, theta2=180, facecolor='#b893e4')
    ax.add_patch(mouth)
    top_shine = patches.Wedge(center=(0, -2.5), r=0.9, theta1=0, theta2=180, width=0.5, facecolor='#e9e8ff')
    ax.add_patch(top_shine)

# Draw stars
draw_star(-3.2, 2.8, 0.3, '#b9ffbf')
draw_star(3.2, 2.8, 0.2, '#b9ffbf')

# Draw eyes
draw_eye(-2, 0)
draw_eye(2, 0)

# Draw mouth
draw_mouth()

# Set limits
ax.set_xlim(-5, 5)
ax.set_ylim(-4, 4)

plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()