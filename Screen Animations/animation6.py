import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.axis('off')

# Parameters
eye_offset = 2
reflection_offset = 0.4
blink = False

# Eye positions
def eye_center(pos):
    return (-eye_offset + pos[0], pos[1]), (eye_offset + pos[0], pos[1])

# Draw star
def draw_star(x, y, size, color):
    return patches.RegularPolygon((x, y), numVertices=4, radius=size, orientation=np.pi/4, color=color)

# Draw one eye
def draw_eye(cx, cy, blink_factor=1.0, look_x=0, look_y=0, sparkle=False):
    patches_list = []

    # Outer ring
    patches_list.append(patches.Circle((cx, cy), 1.2, color='#d6f0ff'))
    # Blue ring
    patches_list.append(patches.Circle((cx, cy), 1.0, color='#66b7ff'))
    # Pupil adjusted for looking
    patches_list.append(patches.Circle((cx + look_x, cy + look_y), 0.65 * blink_factor, color='black'))
    # Reflection
    patches_list.append(patches.Circle((cx + reflection_offset, cy + reflection_offset), 0.25 * blink_factor, color='#e9f6ff'))

    # Sparkle star
    if sparkle:
        patches_list.append(draw_star(cx + 0.7, cy + 0.8, 0.2, '#b9ffbf'))
    return patches_list

# Draw mouth
def draw_mouth(mood):
    patches_list = []
    if mood == 'smile':
        patches_list.append(patches.Wedge(center=(0, -2.5), r=0.9, theta1=0, theta2=180, facecolor='#b893e4'))
        patches_list.append(patches.Wedge(center=(0, -2.5), r=0.9, theta1=0, theta2=180, width=0.5, facecolor='#e9e8ff'))
    elif mood == 'sad':
        patches_list.append(patches.Wedge(center=(0, -2.8), r=0.9, theta1=180, theta2=360, facecolor='#b893e4'))
        patches_list.append(patches.Wedge(center=(0, -2.8), r=0.9, theta1=180, theta2=360, width=0.5, facecolor='#e9e8ff'))
    return patches_list

# Initialize frame
patches_objs = []
def init():
    global patches_objs
    patches_objs = []
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    return patches_objs

# Animation function
def animate(i):
    global patches_objs
    for patch in patches_objs:
        patch.remove()

    patches_objs.clear()

    blink_factor = 1.0 if (i // 20) % 10 != 0 else 0.1
    mood = 'smile' if (i // 100) % 2 == 0 else 'sad'
    sparkle = (i // 15) % 5 == 0

    # Look directions
    angle = (i % 100) / 100 * 2 * np.pi
    look_x = 0.2 * np.cos(angle)
    look_y = 0.2 * np.sin(angle)

    left_eye_center, right_eye_center = eye_center((0, 0))
    eyes = draw_eye(*left_eye_center, blink_factor, look_x, look_y, sparkle) + \
           draw_eye(*right_eye_center, blink_factor, look_x, look_y, sparkle)

    mouth = draw_mouth(mood)

    stars = [draw_star(-3.2, 2.8, 0.3, '#b9ffbf'), draw_star(3.2, 2.8, 0.2, '#b9ffbf')]

    for patch in eyes + mouth + stars:
        ax.add_patch(patch)
        patches_objs.append(patch)

    return patches_objs

# Animate
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=600, interval=50, blit=True)
plt.show()