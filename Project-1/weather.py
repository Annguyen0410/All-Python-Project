import pygame
import random

class WeatherSystem:
    def __init__(self):
        self.weather_type = 'clear'
        self.particles = []

    def update(self):
        if self.weather_type == 'rain':
            self._update_rain()
        elif self.weather_type == 'snow':
            self._update_snow()

    def _update_rain(self):
        if random.random() < 0.1:
            self.particles.append([random.randint(0, 800), 0])

        for particle in self.particles:
            particle[1] += 5

        self.particles = [p for p in self.particles if p[1] < 600]

    def _update_snow(self):
        if random.random() < 0.1:
            self.particles.append([random.randint(0, 800), 0])

        for particle in self.particles:
            particle[1] += 1

        self.particles = [p for p in self.particles if p[1] < 600]

    def draw(self, screen):
        if self.weather_type == 'rain':
            for particle in self.particles:
                pygame.draw.line(screen, (0, 0, 255), particle, (particle[0], particle[1] + 5), 1)
        elif self.weather_type == 'snow':
            for particle in self.particles:
                pygame.draw.circle(screen, (255, 255, 255), particle, 2)
