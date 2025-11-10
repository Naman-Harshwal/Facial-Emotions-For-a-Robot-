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
fig.patch.set_facecolor('black')
ax.set_facecolor('#1B1930')

parts = {}
centers = [(700, 660), (1220, 660)]


def clear_parts():
    for p in parts.values():
        p.remove()
    parts.clear()


def draw_eyes(style='neutral'):
    offsets = {
        'thinking': 30, 'disgusted': -20, 'surprised': 0, 'angry': -10,
        'joy': 10, 'crying': -10, 'sleepy': -40, 'shy': 5, 'confused': 5,
        'fear': -5, 'love': 10, 'nervous': -15, 'blushing': 5, 'serious': 0
    }
    offset_y = offsets.get(style, 0)
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
        'thinking': [[(630, 780), (730, 770), (730, 760), (630, 770)], [(1190, 720), (1290, 740), (1290, 750), (1190, 730)]],
        'disgusted': [[(630, 810), (740, 780), (740, 770), (630, 800)], [(1210, 780), (1320, 810), (1320, 800), (1210, 770)]],
        'surprised': [[(610, 860), (740, 880), (740, 860), (610, 840)], [(1180, 880), (1320, 860), (1320, 840), (1180, 860)]],
        'angry': [[(630, 790), (730, 770), (730, 760), (630, 780)], [(1190, 780), (1290, 800), (1290, 810), (1190, 790)]],
        'shy': [[(640, 790), (740, 780), (740, 770), (640, 780)], [(1180, 780), (1280, 790), (1280, 780), (1180, 770)]],
        'confused': [[(620, 800), (740, 800), (740, 790), (620, 790)], [(1200, 790), (1320, 800), (1320, 790), (1200, 780)]],
        'fear': [[(630, 830), (730, 820), (730, 810), (630, 820)], [(1200, 830), (1300, 820), (1300, 810), (1200, 820)]],
        'love': [[(620, 780), (740, 760), (740, 750), (620, 770)], [(1200, 750), (1320, 770), (1320, 760), (1200, 740)]],
        'nervous': [[(640, 770), (740, 770), (740, 760), (640, 760)], [(1200, 770), (1300, 760), (1300, 750), (1200, 760)]],
        'blushing': [[(630, 780), (740, 770), (740, 760), (630, 770)], [(1190, 780), (1290, 790), (1290, 780), (1190, 770)]],
        'serious': [[(630, 800), (740, 800), (740, 790), (630, 790)], [(1190, 800), (1300, 800), (1300, 790), (1190, 790)]]
    }
    coords = coords_map.get(style, [])
    for i, poly in enumerate(coords):
        parts[f'brow_{i}'] = patches.Polygon(poly, closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])


def draw_mouth(style='neutral'):
    mouth_map = {
        'thinking': mlines.Line2D([920, 1000], [360, 370], color='#E2F1FF', lw=4),
        'disgusted': patches.Arc((960, 330), 160, 90, theta1=10, theta2=170, color='#E2F1FF', lw=4),
        'surprised': patches.Ellipse((960, 340), 80, 120, facecolor='#E2F1FF'),
        'angry': patches.Arc((960, 320), 180, 80, theta1=180, theta2=360, color='red', lw=4),
        'joy': patches.Wedge((960, 370), 130, 180, 360, facecolor='#FCD1E3'),
        'crying': patches.Wedge((960, 370), 130, 180, 360, facecolor='#A84D7B'),
        'sleepy': mlines.Line2D([920, 1000], [340, 340], color='#AAAAAA', lw=3),
        'shy': patches.Arc((960, 330), 150, 70, theta1=10, theta2=170, color='#FCA3CC', lw=3),
        'confused': patches.Arc((960, 340), 140, 80, theta1=10, theta2=170, color='#B0D2F1', lw=3),
        'fear': patches.Wedge((960, 340), 100, 180, 360, facecolor='#9D4A7B'),
        'love': patches.Wedge((960, 370), 130, 180, 360, facecolor='#FF69B4'),
        'nervous': patches.Arc((960, 330), 160, 70, theta1=190, theta2=350, color='#CCCCCC', lw=3),
        'blushing': patches.Wedge((960, 370), 130, 180, 360, facecolor='#FFC0CB'),
        'serious': mlines.Line2D([920, 1000], [350, 350], color='#FFFFFF', lw=3)
    }
    mouth = mouth_map.get(style)
    if isinstance(mouth, mlines.Line2D):
        parts['mouth'] = mouth
        ax.add_line(mouth)
    elif mouth:
        parts['mouth'] = mouth
        ax.add_patch(mouth)


def set_expression(expr):
    clear_parts()
    draw_eyes(expr)
    draw_eyebrows(expr)
    draw_mouth(expr)


sequence = [
    'thinking', 'disgusted', 'surprised', 'angry', 'joy', 'crying',
    'sleepy', 'shy', 'confused', 'fear', 'love', 'nervous', 'blushing', 'serious'
]
frames_per_expr = 90
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
