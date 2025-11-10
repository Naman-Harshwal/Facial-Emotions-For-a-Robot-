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

def draw_eyes():
    for cx, cy in [(700, 660), (1220, 660)]:  # Slight upward position for wide eyes
        ax.add_patch(patches.Circle((cx, cy), 150, color='#E2F1FF'))  # Enlarged outer
        ax.add_patch(patches.Circle((cx, cy), 110, color='#60A4F9'))
        ax.add_patch(patches.Circle((cx, cy), 75, color='black'))
        ax.add_patch(patches.Circle((cx + 55, cy + 55), 25, color='#E2F1FF'))

def draw_mouth():
    ax.add_patch(patches.Ellipse((960, 380), 120, 160, facecolor="#FF6EC7"))  # Open surprised mouth

left_star = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#D8FFC7')[0]
right_star = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#D8FFC7')[0]

def update(frame):
    alpha = 0.5 + 0.5 * np.sin(frame * 0.1)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)
    return left_star, right_star

draw_eyes()
draw_mouth()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
