import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')

# Background color
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

# Draw eyes function
def draw_eye(center_x, center_y):
    eye_outer = patches.Circle((center_x, center_y), 140, color='#E2F1FF')
    ax.add_patch(eye_outer)
    eye_blue = patches.Circle((center_x, center_y), 100, color='#60A4F9')
    ax.add_patch(eye_blue)
    eye_black = patches.Circle((center_x, center_y), 70, color='black')
    ax.add_patch(eye_black)
    sparkle_dot = patches.Circle((center_x + 55, center_y + 55), 25, color='#E2F1FF')
    ax.add_patch(sparkle_dot)

# Draw the two eyes
left_eye_center = (700, 650)
right_eye_center = (1220, 650)
draw_eye(*left_eye_center)
draw_eye(*right_eye_center)

# Draw realistic mouth with teeth, tongue, and inner mouth
# Mouth outer boundary (lips)
lip_outer = patches.Wedge((960, 380), 130, 180, 360, facecolor='#A98DF0')
ax.add_patch(lip_outer)

# Inner mouth (dark red)
mouth_inner = patches.Wedge((960, 370), 100, 180, 360, facecolor='#3B0A18')
ax.add_patch(mouth_inner)

# Tongue (pink ellipse)
tongue = patches.Ellipse((960, 350), 80, 40, facecolor='#F18DB0')
ax.add_patch(tongue)

# Teeth (white rectangle at the top of inner mouth)
teeth = patches.Rectangle((860, 370), 200, 20, facecolor='white')
ax.add_patch(teeth)

# Draw sparkling stars
left_star = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#D8FFC7')[0]
right_star = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#D8FFC7')[0]

# Star animation update
def update(frame):
    alpha = 0.5 + 0.5 * np.sin(frame * 0.6)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)
    return left_star, right_star

# Create high FPS animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=16, blit=True)

plt.show()

