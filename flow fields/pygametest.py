import pygame
import sys

pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 0)
CIRCLE_RADIUS = 50
INITIAL_OPACITY = 25  # 10% opacity
OPACITY_INCREMENT = 10  # Increase opacity by 10% each time

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fading Circle")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create a surface for the circle
circle_surface = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, CIRCLE_COLOR, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
circle_alpha = INITIAL_OPACITY


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Set the alpha value of the circle surface
    circle_surface.set_alpha(circle_alpha)

    # Draw the circle onto the screen
    screen.blit(circle_surface, (WIDTH // 2 - CIRCLE_RADIUS, HEIGHT // 2 - CIRCLE_RADIUS))

    # Increase the alpha value for the next frame
    circle_alpha += OPACITY_INCREMENT

    # Limit the frame rate
    clock.tick(2)

    # Update the display
    pygame.display.flip()
