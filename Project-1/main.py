import pygame
from terrain import generate_terrain
from weather import WeatherSystem
from ui import UI

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Terrain Generator")

# Terrain settings
TERRAIN_WIDTH, TERRAIN_HEIGHT = 100, 75
SCALE = 8

# Generate terrain
terrain = generate_terrain(TERRAIN_WIDTH, TERRAIN_HEIGHT)

# Initialize weather system
weather = WeatherSystem()

# Initialize UI
ui = UI()
ui.set_weather_system(weather)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ui.handle_event(event)

    # Update weather
    weather.update()

    # Draw terrain
    for y in range(TERRAIN_HEIGHT):
        for x in range(TERRAIN_WIDTH):
            height = terrain[y][x]
            color = (0, int(255 * (height + 0.5)), 0)  # Green scale
            pygame.draw.rect(screen, color, (x * SCALE, y * SCALE, SCALE, SCALE))

    # Draw weather effects
    weather.draw(screen)

    # Draw UI
    ui.draw(screen)

    pygame.display.flip()

pygame.quit()
