import pygame
import heapq
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Set up the maze grid
maze_width = 20
maze_height = 20
maze = [[0 for _ in range(maze_width)] for _ in range(maze_height)]

# Initialize Pygame
pygame.init()

# Set up the display
cell_size = 20
screen_width = maze_width * cell_size
screen_height = maze_height * cell_size + 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Pathfinding")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 24)

# Start and end points
start = (1, 1)
end = (maze_width - 2, maze_height - 2)

# Pathfinding algorithm
algorithm = "A*"

# Function to draw the maze
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def draw_buttons():
    button_font = pygame.font.Font(None, 20)
    a_star_button = button_font.render("A*", True, BLACK)
    bfs_button = button_font.render("BFS", True, BLACK)
    pygame.draw.rect(screen, GRAY, (0, screen_height - 50, screen_width // 2, 50))
    pygame.draw.rect(screen, GRAY, (screen_width // 2, screen_height - 50, screen_width // 2, 50))
    screen.blit(a_star_button, (screen_width // 4 - a_star_button.get_width() // 2, screen_height - 35))
    screen.blit(bfs_button, (3 * screen_width // 4 - bfs_button.get_width() // 2, screen_height - 35))

# Function to calculate Manhattan distance
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Function to calculate the shortest path using A* algorithm
def a_star(start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < maze_width and 0 <= neighbor[1] < maze_height and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

# Function to calculate the shortest path using BFS algorithm
def bfs(start, end):
    queue = [(start, [])]
    visited = set()

    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path + [current]

        if current in visited:
            continue

        visited.add(current)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < maze_width and 0 <= neighbor[1] < maze_height and maze[neighbor[1]][neighbor[0]] == 0:
                queue.append((neighbor, path + [current]))

    return None

# Define constants
DIAGONAL_COST = 1.4

# Function to calculate the shortest path using A* algorithm with diagonal movement
def a_star_diagonal(start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < maze_width and 0 <= neighbor[1] < maze_height and maze[neighbor[1]][neighbor[0]] == 0:
                if dx == 0 or dy == 0:
                    new_g_score = g_score[current] + 1
                else:
                    new_g_score = g_score[current] + DIAGONAL_COST

                if neighbor not in g_score or new_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = new_g_score
                    f_score[neighbor] = new_g_score + manhattan_distance(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

# Function to generate a random maze
def generate_maze(density):
    maze = [[0 for _ in range(maze_width)] for _ in range(maze_height)]
    for y in range(maze_height):
        for x in range(maze_width):
            if random.random() < density:
                maze[y][x] = 1
    maze[start[1]][start[0]] = 0
    maze[end[1]][end[0]] = 0
    return maze

# Main loop
running = True
drawing = False
density = 0.3
algorithm = "A* Diagonal"
maze = generate_maze(density)

# Pathfinding variables
current_algorithm = None
current_path = []

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if pos[1] < screen_height - 50:
                x = pos[0] // cell_size
                y = pos[1] // cell_size
                if (x, y) == start or (x, y) == end:
                    drawing = True
                else:
                    maze[y][x] = 1 - maze[y][x]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze = generate_maze(density)
                current_path = []
            elif event.key == pygame.K_UP:
                density = min(1, density + 0.05)
                maze = generate_maze(density)
                current_path = []
            elif event.key == pygame.K_DOWN:
                density = max(0, density - 0.05)
                maze = generate_maze(density)
                current_path = []
            elif event.key == pygame.K_RETURN:
                current_algorithm = a_star_diagonal if algorithm == "A* Diagonal" else a_star
                current_path = current_algorithm(start, end)

    # Update screen
    screen.fill(WHITE)
    draw_maze()
    draw_buttons()

    # Draw current path
    if current_path:
        for x, y in current_path:
            pygame.draw.rect(screen, YELLOW, (x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, GREEN, (start[0] * cell_size, start[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, RED, (end[0] * cell_size, end[1] * cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
