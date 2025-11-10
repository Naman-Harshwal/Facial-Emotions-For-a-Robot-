import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Face Animation")

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
YELLOW = (255, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Animation functions
def draw_smile():
    # Draw eyes
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (180, 180), 40)
    pygame.draw.circle(screen, DARK_BLUE, (580, 180), 40)
    
    # Draw smiling mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_sad():
    # Draw eyes
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (180, 180), 40)
    pygame.draw.circle(screen, DARK_BLUE, (580, 180), 40)
    
    # Draw sad mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), math.pi, 2*math.pi, 50)

def draw_blink():
    # Draw eyes (closed)
    pygame.draw.rect(screen, LIGHT_BLUE, (130, 130, 140, 140))
    pygame.draw.rect(screen, LIGHT_BLUE, (530, 130, 140, 140))
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_look_left():
    # Draw eyes looking left
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (140, 180), 40)
    pygame.draw.circle(screen, DARK_BLUE, (540, 180), 40)
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_look_right():
    # Draw eyes looking right
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (220, 180), 40)
    pygame.draw.circle(screen, DARK_BLUE, (620, 180), 40)
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_look_up():
    # Draw eyes looking up
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (180, 140), 40)
    pygame.draw.circle(screen, DARK_BLUE, (580, 140), 40)
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_look_down():
    # Draw eyes looking down
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (180, 220), 40)
    pygame.draw.circle(screen, DARK_BLUE, (580, 220), 40)
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

def draw_sparkle():
    # Draw eyes with sparkles
    pygame.draw.circle(screen, LIGHT_BLUE, (200, 200), 70)
    pygame.draw.circle(screen, LIGHT_BLUE, (600, 200), 70)
    pygame.draw.circle(screen, DARK_BLUE, (180, 180), 40)
    pygame.draw.circle(screen, DARK_BLUE, (580, 180), 40)
    
    # Draw sparkles
    pygame.draw.polygon(screen, YELLOW, [(130, 130), (150, 110), (170, 130)])
    pygame.draw.polygon(screen, YELLOW, [(670, 130), (690, 110), (710, 130)])
    
    # Draw mouth
    pygame.draw.arc(screen, PINK, (300, 300, 200, 100), 0, math.pi, 50)

# Animation loop
running = True
animation_sequence = [
    draw_smile, draw_sad, draw_blink, draw_look_left,
    draw_look_right, draw_look_up, draw_look_down, draw_sparkle
]
current_animation = 0
last_switch_time = pygame.time.get_ticks()
switch_interval = 2000  # 2 seconds per animation

while running:
    current_time = pygame.time.get_ticks()
    if current_time - last_switch_time > switch_interval:
        current_animation = (current_animation + 1) % len(animation_sequence)
        last_switch_time = current_time

    screen.fill(WHITE)
    animation_sequence[current_animation]()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)

pygame.quit()
sys.exit()