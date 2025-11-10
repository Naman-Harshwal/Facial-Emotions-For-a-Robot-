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
    for cx, cy in [(700, 650), (1220, 650)]:
        ax.add_patch(patches.Arc((cx, cy), 180, 80, theta1=0, theta2=180, color='#E2F1FF', lw=10))  # Closed eye curve

def draw_mouth():
    ax.add_patch(patches.Wedge((960, 340), 100, 180, 360, facecolor='#FF007F'))  # Neutral sleeping mouth

def draw_zs():
    ax.text(1450, 850, 'Z', fontsize=50, color='#E2F1FF', fontweight='bold')
    ax.text(1500, 900, 'Z', fontsize=40, color='#E2F1FF', fontweight='bold')
    ax.text(1550, 950, 'Z', fontsize=30, color='#E2F1FF', fontweight='bold')

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
draw_zs()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
