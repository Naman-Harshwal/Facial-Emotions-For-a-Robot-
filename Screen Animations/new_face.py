# Required Libraries
import pygame
import sys
import math

# Initialize
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (230, 243, 255)
BLUE = (102, 169, 255)
LIGHT_BLUE = (229, 243, 255)
LAVENDER = (217, 178, 255)
PURPLE = (225, 179, 255)
STAR_COLOR = (214, 255, 199)

# Functions to draw elements
def draw_star(surface, x, y, size, color):
    points = [(x, y - size), (x + size / 5, y - size / 5), (x + size, y),
              (x + size / 5, y + size / 5), (x, y + size),
              (x - size / 5, y + size / 5), (x - size, y),
              (x - size / 5, y - size / 5)]
    pygame.draw.polygon(surface, color, points)

def draw_eye(surface, cx, cy, blink):
    height = 300 * blink
    pygame.draw.ellipse(surface, LIGHT_BLUE, (cx - 150, cy - height // 2, 300, height))
    pygame.draw.ellipse(surface, BLUE, (cx - 100, cy - (200 * blink) // 2, 200, 200 * blink))
    pygame.draw.ellipse(surface, BLACK, (cx - 60, cy - (120 * blink) // 2, 120, 120 * blink))
    pygame.draw.ellipse(surface, WHITE, (cx - 80, cy - 30 - 30 * (1 - blink), 60, 60))

def draw_mouth(surface):
    pygame.draw.ellipse(surface, PURPLE, (860, 620, 200, 120))
    pygame.draw.ellipse(surface, WHITE, (880, 610, 160, 60))

# Blink logic
def get_blink(frame):
    phase = frame % 120
    if phase < 10:
        return 1 - phase / 10
    elif phase < 20:
        return (phase - 10) / 10
    else:
        return 1

# Main loop
frame = 0
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    blink = get_blink(frame)
    draw_eye(screen, 700, 500, blink)
    draw_eye(screen, 1220, 500, blink)
    draw_star(screen, 420, 180, 40, STAR_COLOR)
    draw_star(screen, 1500, 200, 25, STAR_COLOR)
    draw_mouth(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 1

pygame.quit()
sys.exit()