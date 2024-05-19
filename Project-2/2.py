import pygame
import sys
import math
from pygame.locals import *

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4D Tesseract Visualization")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the vertices of a 4D tesseract
vertices = [
    [-1, -1, -1, -1],
    [1, -1, -1, -1],
    [-1, 1, -1, -1],
    [1, 1, -1, -1],
    [-1, -1, 1, -1],
    [1, -1, 1, -1],
    [-1, 1, 1, -1],
    [1, 1, 1, -1],
    [-1, -1, -1, 1],
    [1, -1, -1, 1],
    [-1, 1, -1, 1],
    [1, 1, -1, 1],
    [-1, -1, 1, 1],
    [1, -1, 1, 1],
    [-1, 1, 1, 1],
    [1, 1, 1, 1]
]

# Define the edges of a 4D tesseract
edges = [
    (0, 1), (1, 3), (3, 2), (2, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),

    (8, 9), (9, 11), (11, 10), (10, 8),
    (12, 13), (13, 15), (15, 14), (14, 12),
    (8, 12), (9, 13), (10, 14), (11, 15),

    (0, 8), (1, 9), (2, 10), (3, 11),
    (4, 12), (5, 13), (6, 14), (7, 15),

    (0, 1), (2, 3), (4, 5), (6, 7),
    (8, 9), (10, 11), (12, 13), (14, 15),

    (0, 2), (1, 3), (4, 6), (5, 7),
    (8, 10), (9, 11), (12, 14), (13, 15),

    (0, 1), (1, 3), (3, 2), (2, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (8, 9), (9, 11), (11, 10), (10, 8),
    (12, 13), (13, 15), (15, 14), (14, 12)
]

# Project a 4D point onto a 3D space
def project(point):
    w = 1 / (2 - point[3])
    return [
        WIDTH / 2 + w * point[0] * 100,
        HEIGHT / 2 - w * point[1] * 100
    ]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Rotate the tesseract in 4D space
    angleX, angleY, angleZ, angleW = pygame.time.get_ticks() / 1000, pygame.time.get_ticks() / 1000, pygame.time.get_ticks() / 1000, pygame.time.get_ticks() / 1000
    rotationX = [
        [1, 0, 0, 0],
        [0, math.cos(angleX), -math.sin(angleX), 0],
        [0, math.sin(angleX), math.cos(angleX), 0],
        [0, 0, 0, 1]
    ]
    rotationY = [
        [math.cos(angleY), 0, math.sin(angleY), 0],
        [0, 1, 0, 0],
        [-math.sin(angleY), 0, math.cos(angleY), 0],
        [0, 0, 0, 1]
    ]
    rotationZ = [
        [math.cos(angleZ), -math.sin(angleZ), 0, 0],
        [math.sin(angleZ), math.cos(angleZ), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    rotationW = [
        [math.cos(angleW), 0, 0, -math.sin(angleW)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [math.sin(angleW), 0, 0, math.cos(angleW)]
    ]
    rotated_vertices = []
    for vertex in vertices:
        rotated = vertex
        for rotation in [rotationX, rotationY, rotationZ, rotationW]:
            rotated = [sum([rotation[i][j] * rotated[j] for j in range(4)]) for i in range(4)]
        rotated_vertices.append(rotated)

    # Project and draw the edges of the tesseract
    for edge in edges:
        start = project(rotated_vertices[edge[0]])
        end = project(rotated_vertices[edge[1]])
        pygame.draw.line(screen, WHITE, start, end, 2)

    pygame.display.flip()
