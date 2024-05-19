import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Objects")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the Object class
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - 30)
            self.speed = random.randint(5, 10)

# Create a sprite group for objects
objects = pygame.sprite.Group()

# Create the cursor sprite
cursor = pygame.Rect(WIDTH // 2 - 25, HEIGHT * 0.7 - 25, 50, 50)

# Game variables
score = 0
mistakes = 0
level = 1
max_mistakes = 5
objects_per_level = {1: 5, 2: 8, 3: 11}  # Number of objects per level
object_speed_increase = 0.5  # Speed increase per level

# Load font
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # Limit the frame rate

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add new objects based on the current level
    if len(objects) < objects_per_level.get(level, 11):
        objects.add(Object())

    # Update object positions and speeds
    objects.update()

    # Check for collisions
    for obj in objects.copy():
        if obj.rect.colliderect(cursor):
            score += 1
            objects.remove(obj)
        elif obj.rect.y > HEIGHT:
            objects.remove(obj)
            mistakes += 1

    # Check if level up
    if score >= level * 10:
        level += 1
        for obj in objects:
            obj.speed += object_speed_increase

    # Check if game over
    if mistakes >= max_mistakes:
        running = False

    # Restrict cursor movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and cursor.left > 0:
        cursor.left -= 5
    if keys[pygame.K_RIGHT] and cursor.right < WIDTH:
        cursor.right += 5

    # Clear the screen
    screen.fill(BLACK)

    # Draw objects and cursor
    for obj in objects:
        pygame.draw.rect(screen, RED, obj.rect)
    pygame.draw.rect(screen, WHITE, cursor)

    # Draw score, level, and mistakes
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    mistakes_text = font.render(f"Mistakes: {mistakes}/{max_mistakes}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(mistakes_text, (10, 90))

    # Update the display
    pygame.display.flip()

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("Game Over", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 50))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
