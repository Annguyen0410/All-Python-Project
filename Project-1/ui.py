import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.weather_system = None
        self.weather_type = 'clear'

    def set_weather_system(self, weather_system):
        self.weather_system = weather_system
        self.weather_type = weather_system.weather_type

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.toggle_weather('rain')
            elif event.key == pygame.K_s:
                self.toggle_weather('snow')
            elif event.key == pygame.K_d:
                # For simplicity, this example does not implement day/night toggle
                pass

    def toggle_weather(self, weather_type):
        if self.weather_system:
            if self.weather_type == weather_type:
                self.weather_type = 'clear'
            else:
                self.weather_type = weather_type
            self.weather_system.weather_type = self.weather_type

    def draw(self, screen):
        # Draw UI elements
        weather_text = self.font.render(f'Weather: {self.weather_type.capitalize()}', True, (255, 255, 255))
        screen.blit(weather_text, (10, 10))
