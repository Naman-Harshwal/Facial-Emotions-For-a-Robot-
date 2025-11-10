import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

parts = {}

# Shared eye coordinates
centers = [(700, 660), (1220, 660)]

def clear_parts():
    for p in parts.values():
        p.remove()
    parts.clear()

def draw_eyes(style='neutral'):
    offset_y = 0
    if style == 'thinking': offset_y = 30
    if style == 'disgusted': offset_y = -20
    if style == 'surprised': offset_y = 0
    if style == 'angry': offset_y = -10
    for i, (cx, cy) in enumerate(centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 140, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy + offset_y), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy + offset_y), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 35, cy + 35), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_eyebrows(style='neutral'):
    coords_map = {
        'thinking': [
            [(630, 780), (730, 770), (730, 760), (630, 770)],
            [(1190, 720), (1290, 740), (1290, 750), (1190, 730)]
        ],
        'disgusted': [
            [(630, 810), (740, 780), (740, 770), (630, 800)],
            [(1210, 780), (1320, 810), (1320, 800), (1210, 770)]
        ],
        'surprised': [
            [(610, 860), (740, 880), (740, 860), (610, 840)],
            [(1180, 880), (1320, 860), (1320, 840), (1180, 860)]
        ]
    }
    coords = coords_map.get(style, [])
    for i, poly in enumerate(coords):
        parts[f'brow_{i}'] = patches.Polygon(poly, closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def draw_mouth(style='neutral'):
    if style == 'thinking':
        parts['mouth'] = mlines.Line2D([920, 1000], [360, 370], color='#E2F1FF', lw=4)
        ax.add_line(parts['mouth'])
    elif style == 'disgusted':
        parts['mouth'] = patches.Arc((960, 330), 160, 90, theta1=10, theta2=170, color='#E2F1FF', lw=4)
        ax.add_patch(parts['mouth'])
    elif style == 'surprised':
        parts['mouth'] = patches.Ellipse((960, 340), 80, 120, facecolor='#E2F1FF')
        ax.add_patch(parts['mouth'])

def set_expression(expr):
    clear_parts()
    draw_eyes(expr)
    draw_eyebrows(expr)
    draw_mouth(expr)

sequence = ['thinking', 'disgusted', 'surprised']
frames_per_expr = 90

# Expression animation
current_expr = {'name': '', 'idx': 0}

def update(frame):
    expr_index = (frame // frames_per_expr) % len(sequence)
    expr_name = sequence[expr_index]
    if expr_name != current_expr['name']:
        current_expr['name'] = expr_name
        set_expression(expr_name)
    return list(parts.values())

ani = FuncAnimation(fig, update, frames=frames_per_expr * len(sequence), interval=16, blit=True)
plt.show()
