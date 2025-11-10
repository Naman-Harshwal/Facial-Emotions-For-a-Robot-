import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
ax.axis('off')

ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')

patches_objs = []

def draw_star(x, y, size, color):
    return patches.RegularPolygon((x, y), numVertices=5, radius=size, orientation=np.pi/5, color=color)

def draw_eye(cx, cy, blink, blink_progress):
    
    eye_elements = []
    # Eye whites and iris
    eye_elements.append(patches.Circle((cx, cy), 1.8, color='#e6f9ff'))
    eye_elements.append(patches.Circle((cx, cy), 1.5, color='#5ab0ff'))
    eye_elements.append(patches.Circle((cx, cy), 0.9, color='#121212'))
    eye_elements.append(patches.Circle((cx + 0.45, cy + 0.45), 0.3, color='white'))

    if blink:
        eye_elements.append(patches.Rectangle((cx - 2, cy + 1.8 - blink_progress), 4, blink_progress * 2, color='black'))

    return eye_elements

def draw_realistic_smile():
    mouth_elements = []
    # Create a realistic cartoon-style smile with a flipped vertical orientation
    mouth_elements.append(patches.Arc((0, -2.5), 4.5, 2.5, theta1=180, theta2=360, lw=6, color='#d1a6f9'))  # Flipped smile
    return mouth_elements

def draw_stars(frame):
    stars = []
    twinkle = 1 if (frame % 20 < 10) else 0.4
    stars.append(draw_star(2.5 + 1.1, 0.5 + 1.1, 0.25 * twinkle, '#b9ffbf'))
    stars.append(draw_star(-2.5, 4.0, 0.3 * twinkle, '#b9ffbf'))
    stars.append(draw_star(2.5, 4.0, 0.3 * twinkle, '#b9ffbf'))
    return stars

def animate_smile(frame):
    global patches_objs
    for p in patches_objs:
        p.remove()
    patches_objs.clear()

    blink_phase = (frame % 60)
    if blink_phase < 10:
        blink = True
        blink_progress = (10 - blink_phase) * 0.3
    elif blink_phase > 50:
        blink = True
        blink_progress = (blink_phase - 50) * 0.3
    else:
        blink = False
        blink_progress = 0

    left_eye_center = (-2.5, 0.5)
    right_eye_center = (2.5, 0.5)
    eyes = draw_eye(*left_eye_center, blink, blink_progress) + \
           draw_eye(*right_eye_center, blink, blink_progress)

    mouth = draw_realistic_smile()
    stars = draw_stars(frame)

    for item in eyes + mouth + stars:
        ax.add_patch(item)
        patches_objs.append(item)
    return patches_objs

ani = animation.FuncAnimation(fig, animate_smile, frames=1000, interval=16, blit=True)
plt.show()