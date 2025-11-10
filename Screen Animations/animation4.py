import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Face")

# Colors (Matching the provided image)
BACKGROUND_COLOR = (245, 245, 245)
ROBOT_FACE_COLOR = (255, 255, 255)
SCREEN_COLOR = (30, 40, 80)
EYE_COLOR = (173, 216, 230)
PUPIL_COLOR = (0, 0, 139)
MOUTH_COLOR = (255, 182, 193)
SPARKLE_COLOR = (200, 255, 200)

# Draw the robot face
def draw_robot_face():
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the robot face outline
    pygame.draw.rect(screen, ROBOT_FACE_COLOR, (100, 50, 600, 500), border_radius=20)
    
    # Draw the screen area
    pygame.draw.rect(screen, SCREEN_COLOR, (150, 100, 500, 400), border_radius=10)
    
    # Draw the eyes
    pygame.draw.circle(screen, EYE_COLOR, (300, 200), 70)
    pygame.draw.circle(screen, EYE_COLOR, (500, 200), 70)
    
    # Draw the pupils
    pygame.draw.circle(screen, PUPIL_COLOR, (280, 180), 40)
    pygame.draw.circle(screen, PUPIL_COLOR, (480, 180), 40)
    
    # Draw the mouth
    pygame.draw.arc(screen, MOUTH_COLOR, (350, 300, 100, 100), 0, math.pi, 50)
    
    # Draw sparkles
    pygame.draw.polygon(screen, SPARKLE_COLOR, [(230, 130), (250, 110), (270, 130)])
    pygame.draw.polygon(screen, SPARKLE_COLOR, [(570, 130), (590, 110), (610, 130)])

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_robot_face()
    pygame.display.flip()

pygame.quit()
sys.exit()