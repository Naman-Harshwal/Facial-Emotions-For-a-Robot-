import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bellabot Robot Animation")

# Colors
BACKGROUND = (10, 20, 30)
PRIMARY = (0, 180, 216)
SECONDARY = (238, 242, 255)
ACCENT = (252, 163, 17)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class BellabotFace:
    def __init__(self):
        self.eye_y_offset = 0
        self.eye_move_direction = 1
        self.mouth_openness = 0
        self.mouth_change = 1
        self.antenna_angle = 0

    def draw(self, surface):
        # Clear screen
        surface.fill(BACKGROUND)
        
        # Draw face outline - FIXED: removed extra parameters
        pygame.draw.ellipse(surface, PRIMARY, (WIDTH//2-150, 80, 300, 300))
        pygame.draw.ellipse(surface, SECONDARY, (WIDTH//2-140, 90, 280, 280))
        
        # Draw antennas
        self.antenna_angle = (self.antenna_angle + 0.03) % (2 * math.pi)
        antenna_offset = math.sin(self.antenna_angle) * 5
        pygame.draw.line(surface, PRIMARY, (WIDTH//2-40, 80), (WIDTH//2-70, 20 + antenna_offset), 8)
        pygame.draw.line(surface, PRIMARY, (WIDTH//2+40, 80), (WIDTH//2+70, 20 - antenna_offset), 8)
        pygame.draw.circle(surface, ACCENT, (WIDTH//2-70, 20 + antenna_offset), 10)
        pygame.draw.circle(surface, ACCENT, (WIDTH//2+70, 20 - antenna_offset), 10)
        
        # Draw eyes
        self.eye_y_offset += 0.1 * self.eye_move_direction
        if abs(self.eye_y_offset) > 5:
            self.eye_move_direction *= -1
            
        # Left eye
        pygame.draw.ellipse(surface, BACKGROUND, (WIDTH//2-100, 150 + self.eye_y_offset, 60, 80))
        pygame.draw.circle(surface, PRIMARY, (WIDTH//2-70, 180 + self.eye_y_offset), 15)
        
        # Right eye
        pygame.draw.ellipse(surface, BACKGROUND, (WIDTH//2+40, 150 - self.eye_y_offset, 60, 80))
        pygame.draw.circle(surface, PRIMARY, (WIDTH//2+70, 180 - self.eye_y_offset), 15)
        
        # Draw mouth
        self.mouth_openness += 0.2 * self.mouth_change
        if self.mouth_openness > 10 or self.mouth_openness < 0:
            self.mouth_change *= -1
            
        pygame.draw.ellipse(surface, BACKGROUND, (WIDTH//2-70, 280, 140, 40))
        pygame.draw.arc(surface, ACCENT, (WIDTH//2-70, 280 - self.mouth_openness//2, 
                                          140, 40 + self.mouth_openness), 
                                          0, math.pi, 5)
        
        # Draw status text
        font = pygame.font.SysFont(None, 36)
        status = font.render("STATUS: OPERATIONAL", True, PRIMARY)
        surface.blit(status, (WIDTH//2 - status.get_width()//2, 380))

# Create face instance
bot_face = BellabotFace()

# Main animation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update and draw face
    bot_face.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()