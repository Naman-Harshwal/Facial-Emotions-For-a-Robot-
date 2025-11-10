import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#0c0c0c')
ax.set_facecolor('#0c0c0c')
ax.axis('off')

# Global variables
patches_objs = []
eyes_offset = 2.2
reflection_offset = 0.45

# Draw a star shape for sparkles
def draw_star(x, y, size, color):
    return patches.RegularPolygon((x, y), numVertices=5, radius=size, orientation=np.pi/5, color=color)

# Draw an eye with parameters
def draw_eye(cx, cy, blink_factor, look_x, look_y, sparkle):
    components = []
    eye_white = patches.Circle((cx, cy), 1.5, color='#e0f7ff')
    eye_blue = patches.Circle((cx, cy), 1.2, color='#5ab0ff')
    eye_black = patches.Circle((cx + look_x, cy + look_y), 0.8 * blink_factor, color='#121212')
    eye_glint = patches.Circle((cx + reflection_offset, cy + reflection_offset), 0.3 * blink_factor, color='white')

    components += [eye_white, eye_blue, eye_black, eye_glint]
    if sparkle:
        components.append(draw_star(cx + 0.9, cy + 1.1, 0.25, '#b9ffbf'))
    return components

# Draw the mouth with mood-based expressions
def draw_mouth(expression):
    components = []
    if expression == 'smile':
        components.append(patches.Arc((0, -2.5), 3.0, 2.0, angle=0, theta1=0, theta2=180, linewidth=8, color='#c48fff'))
        components.append(patches.Wedge((0, -2.5), 1.0, 0, 180, facecolor='#e0d6ff'))
    elif expression == 'sad':
        components.append(patches.Arc((0, -3.0), 3.0, 2.0, angle=0, theta1=180, theta2=360, linewidth=8, color='#c48fff'))
        components.append(patches.Wedge((0, -3.0), 1.0, 180, 360, facecolor='#e0d6ff'))
    return components

# Add side sparkles to background
def draw_background_sparkles():
    return [
        draw_star(-3.5, 3.2, 0.3, '#b9ffbf'),
        draw_star(3.5, 3.2, 0.2, '#b9ffbf'),
        draw_star(0.0, 3.8, 0.2, '#b9ffbf'),
        draw_star(-4.0, 1.0, 0.15, '#b9ffbf'),
        draw_star(4.0, 1.2, 0.15, '#b9ffbf')
    ]

# Initialize the frame
ax.set_xlim(-6, 6)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

# Animation function
def animate(frame):
    global patches_objs
    for p in patches_objs:
        p.remove()
    patches_objs.clear()

    # Blinking logic
    blink_cycle = (frame // 6) % 50
    blink_factor = 1.0 if blink_cycle < 45 else 0.1

    # Eye direction logic
    direction_phase = (frame // 20) % 4
    if direction_phase == 0:
        look_x, look_y = 0.2, 0
    elif direction_phase == 1:
        look_x, look_y = -0.2, 0
    elif direction_phase == 2:
        look_x, look_y = 0, 0.2
    else:
        look_x, look_y = 0, -0.2

    # Mood logic
    expression = 'smile' if (frame // 100) % 2 == 0 else 'sad'

    # Sparkle effect
    sparkle = (frame % 30) < 5

    # Eyes
    left_eye_center = (-eyes_offset, 0)
    right_eye_center = (eyes_offset, 0)
    eyes = draw_eye(*left_eye_center, blink_factor, look_x, look_y, sparkle) + \
           draw_eye(*right_eye_center, blink_factor, look_x, look_y, sparkle)

    # Mouth
    mouth = draw_mouth(expression)

    # Background sparkles
    background = draw_background_sparkles()

    # Combine and draw
    for element in eyes + mouth + background:
        ax.add_patch(element)
        patches_objs.append(element)
    return patches_objs

# High FPS animation
ani = animation.FuncAnimation(fig, animate, frames=1000, interval=30, blit=True)
plt.show()
