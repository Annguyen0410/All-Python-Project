import noise
import numpy as np

def generate_terrain(width, height, scale=20, octaves=6, persistence=0.5, lacunarity=2.0):
    terrain = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            nx = x / width - 0.5
            ny = y / height - 0.5
            terrain[y][x] = noise.pnoise2(nx * scale, ny * scale, octaves=octaves,
                                          persistence=persistence, lacunarity=lacunarity,
                                          repeatx=1024, repeaty=1024, base=42)
    return terrain
