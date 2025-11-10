import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

# Draw expressive, realistic joyful eyes with eyebrows
def draw_eyes():
    for cx, cy in [(700, 700), (1220, 700)]:
        ax.add_patch(patches.Circle((cx, cy), 140, color='#E2F1FF'))
        ax.add_patch(patches.Circle((cx, cy), 100, color='#60A4F9'))
        ax.add_patch(patches.Circle((cx, cy), 70, color='black'))
        ax.add_patch(patches.Circle((cx + 55, cy + 55), 25, color='white'))
        ax.add_patch(patches.Arc((cx, cy + 160), 160, 50, theta1=0, theta2=180, color='white', lw=5))  # eyebrow

# Draw more realistic joyful smiling mouth with expressive curves and dimples
def draw_mouth():
    ax.add_patch(patches.Wedge((960, 380), 180, 180, 360, facecolor='#A98DF0'))  # lips
    ax.add_patch(patches.Wedge((960, 375), 140, 180, 360, facecolor='#3B0A18'))  # mouth cavity
    ax.add_patch(patches.Rectangle((820, 375), 280, 25, facecolor='white'))  # teeth
    ax.add_patch(patches.Ellipse((960, 340), 100, 50, facecolor='#F18DB0'))  # tongue
    ax.add_patch(patches.Circle((820, 375), 15, facecolor='#A98DF0'))  # dimples
    ax.add_patch(patches.Circle((1100, 375), 15, facecolor='#A98DF0'))

# Stars for sparkle effect
left_star = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#FFD4FA')[0]
right_star = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#FFD4FA')[0]

def update(frame):
    alpha = 0.6 + 0.4 * np.sin(frame * 0.15)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)
    return left_star, right_star

draw_eyes()
draw_mouth()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
