# import critical modules
import copy
import random
import pygame
import time


pygame.init()

# initialize game variables
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Water Sort PyGame')
font = pygame.font.Font('freesansbold.ttf', 24)
fps = 60
timer = pygame.time.Clock()
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']
tubes = 10
new_game = True
selected = False
tube_rects = []
select_rect = 100
win = False

def generate_start():
    tubes_number = random.randint(10, 14)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    return tubes_number, tubes_colors

def draw_tubes(tubes_num, tube_cols):
    tube_boxes = []
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True
    spacing = WIDTH / tubes_per_row
    for i in range(tubes_per_row):
        for j in range(len(tube_cols[i])):
            pygame.draw.rect(screen, color_choices[tube_cols[i][j]], [5 + spacing * i, 200 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [5 + spacing * i, 50, 65, 200], 3, 5)
        tube_boxes.append(box)
    if offset:
        for i in range(tubes_per_row - 1):
            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]],
                                 [(spacing * 0.5) + 5 + spacing * i, 450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)
    else:
        for i in range(tubes_per_row):
            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]], [5 + spacing * i,
                                                                                          450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)
    return tube_boxes

def calc_move(colors, selected_rect, destination):
    chain = True
    color_on_top = 100
    length = 1
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    return colors

def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won
# initialize game variables
start_time = None
elapsed_time = 0
score = 0

# function to start the timer
def start_timer():
    global start_time
    start_time = time.time()

# function to update and display the timer
def update_timer():
    global elapsed_time
    if start_time:
        elapsed_time = int(time.time() - start_time)
        timer_text = font.render(f"Time: {elapsed_time // 60:02d}:{elapsed_time % 60:02d}", True, 'white')
        screen.blit(timer_text, (10, 40))

# function to update and display the score
def update_score(moves):
    global score
    score += 100 - moves
    score_text = font.render(f"Score: {score}", True, 'white')
    screen.blit(score_text, (10, 70))

run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
        start_timer()  # start the timer when a new game begins
    else:
        tube_rects = draw_tubes(tubes, tube_colors)
    win = check_victory(tube_colors)
    update_timer()  # update and display the timer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
                start_timer()  # reset the timer for a new game
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        moves = len(tube_colors[select_rect]) - len(tube_colors[dest_rect])
                        tube_colors = calc_move(tube_colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100
                        update_score(moves)  # update the score based on the number of moves
    if win:
        victory_text = font.render('You Won! Press Enter for a new board!', True, 'white')
        screen.blit(victory_text, (30, 265))
    restart_text = font.render('Stuck? Space-Restart, Enter-New Board!', True, 'white')
    screen.blit(restart_text, (10, 10))
    pygame.display.flip()

pygame.quit()
