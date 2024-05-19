import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (160, 82, 45)
LIGHT_BROWN = (235, 209, 166)

# Define board dimensions
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE[0] // BOARD_SIZE

# Define piece characters
PIECE_CHARS = {
    "wK": "♔", "wQ": "♕", "wR": "♖", "wB": "♗", "wN": "♘", "wP": "♙",
    "bK": "♚", "bQ": "♛", "bR": "♜", "bB": "♝", "bN": "♞", "bP": "♟"
}

# Define font for piece characters
FONT = pygame.font.Font(None, SQUARE_SIZE // 2)

# Define board and current state
BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]
TURN = "w"
SELECTED_PIECE = None
LEGAL_MOVES = []

# Helper functions
def is_on_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def get_piece(row, col):
    return BOARD[row][col]

def set_piece(row, col, piece):
    BOARD[row][col] = piece

def is_opposite_color(piece1, piece2):
    if not piece1 or not piece2:
        return False
    return piece1[0] != piece2[0]

def is_king(piece):
    return piece[1] == "K"

# Move functions for each piece
def get_pawn_moves(row, col, piece):
    moves = []
    direction = -1 if piece[0] == "w" else 1
    start_row = 6 if piece[0] == "w" else 1

    # One square forward
    new_row = row + direction
    if is_on_board(new_row, col) and get_piece(new_row, col) == "":
        moves.append((new_row, col))

        # Two squares forward from start row
        if row == start_row and get_piece(row + 2 * direction, col) == "":
            moves.append((row + 2 * direction, col))

    # Capture diagonally
    for offset in [-1, 1]:
        new_row = row + direction
        new_col = col + offset
        if is_on_board(new_row, new_col) and is_opposite_color(piece, get_piece(new_row, new_col)):
            moves.append((new_row, new_col))

    return moves

def get_rook_moves(row, col, piece):
    moves = []
    # Move horizontally and vertically
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for step in range(1, BOARD_SIZE):
            new_row = row + step * direction[0]
            new_col = col + step * direction[1]
            if not is_on_board(new_row, new_col):
                break
            new_piece = get_piece(new_row, new_col)
            if new_piece == "":
                moves.append((new_row, new_col))
            elif is_opposite_color(piece, new_piece):
                moves.append((new_row, new_col))
                break
            else:
                break
    return moves

def get_bishop_moves(row, col, piece):
    moves = []
    # Move diagonally
    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for step in range(1, BOARD_SIZE):
            new_row = row + step * direction[0]
            new_col = col + step * direction[1]
            if not is_on_board(new_row, new_col):
                break
            new_piece = get_piece(new_row, new_col)
            if new_piece == "":
                moves.append((new_row, new_col))
            elif is_opposite_color(piece, new_piece):
                moves.append((new_row, new_col))
                break
            else:
                break
    return moves

def get_knight_moves(row, col, piece):
    moves = []
    offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for offset in offsets:
        new_row = row + offset[0]
        new_col = col + offset[1]
        if is_on_board(new_row, new_col) and (get_piece(new_row, new_col) == "" or is_opposite_color(piece, get_piece(new_row, new_col))):
            moves.append((new_row, new_col))
    return moves

def get_queen_moves(row, col, piece):
    moves = get_rook_moves(row, col, piece) + get_bishop_moves(row, col, piece)
    return moves

def get_king_moves(row, col, piece):
    moves = []
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for offset in offsets:
        new_row = row + offset[0]
        new_col = col + offset[1]
        if is_on_board(new_row, new_col) and (get_piece(new_row, new_col) == "" or is_opposite_color(piece, get_piece(new_row, new_col))):
            moves.append((new_row, new_col))
    return moves

# Get all legal moves for the current player
def get_legal_moves(piece):
    row, col = SELECTED_PIECE
    piece_type = piece[1]
    if piece_type == "P":
        return get_pawn_moves(row, col, piece)
    elif piece_type == "R":
        return get_rook_moves(row, col, piece)
    elif piece_type == "B":
        return get_bishop_moves(row, col, piece)
    elif piece_type == "N":
        return get_knight_moves(row, col, piece)
    elif piece_type == "Q":
        return get_queen_moves(row, col, piece)
    elif piece_type == "K":
        return get_king_moves(row, col, piece)

# Check if the king is in check
def is_in_check(color):
    king_row, king_col = None, None
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = get_piece(row, col)
            if piece != "" and piece[0] == color and is_king(piece):
                king_row, king_col = row, col
                break
        if king_row is not None:
            break

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = get_piece(row, col)
            if piece != "" and piece[0] != color:
                moves = []
                if piece[1] == "P":
                    moves = get_pawn_moves(row, col, piece)
                elif piece[1] == "R":
                    moves = get_rook_moves(row, col, piece)
                elif piece[1] == "B":
                    moves = get_bishop_moves(row, col, piece)
                elif piece[1] == "N":
                    moves = get_knight_moves(row, col, piece)
                elif piece[1] == "Q":
                    moves = get_queen_moves(row, col, piece)
                elif piece[1] == "K":
                    moves = get_king_moves(row, col, piece)

                if (king_row, king_col) in moves:
                    return True

    return False

# Check if the game is over
def is_game_over():
    if is_in_check(TURN):
        # Check for checkmate
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = get_piece(row, col)
                if piece != "" and piece[0] == TURN:
                    LEGAL_MOVES = get_legal_moves(piece)
                    if LEGAL_MOVES:
                        return False  # There is a legal move, so not checkmate
        return True  # No legal moves, so it's checkmate
    else:
        return False

# Draw the board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(
                screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

# Draw the pieces
def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = BOARD[row][col]
            if piece != "":
                piece_char = FONT.render(PIECE_CHARS[piece], True, BLACK)
                screen.blit(
                    piece_char, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4)
                )

def handle_mouse_events(pos):
    global SELECTED_PIECE, LEGAL_MOVES, TURN  # Move TURN here
    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
    if SELECTED_PIECE is None:
        piece = get_piece(row, col)
        if piece != "" and piece[0] == TURN:
            SELECTED_PIECE = (row, col)
            LEGAL_MOVES = get_legal_moves(piece)
    else:
        if (row, col) in LEGAL_MOVES:
            old_row, old_col = SELECTED_PIECE
            set_piece(row, col, get_piece(old_row, old_col))
            set_piece(old_row, old_col, "")
            SELECTED_PIECE = None
            LEGAL_MOVES = []
            TURN = "b" if TURN == "w" else "w"
        else:
            SELECTED_PIECE = None
            LEGAL_MOVES = []
# Game loop
running = True
TURN = "w"  # Initialize TURN outside the loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_events(event.pos)

    screen.fill(WHITE)
    draw_board()
    draw_pieces()

    if SELECTED_PIECE:
        row, col = SELECTED_PIECE
        pygame.draw.rect(
            screen, (255, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2
        )
        for move in LEGAL_MOVES:
            row, col = move
            pygame.draw.circle(
                screen, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10
            )

    if is_game_over():
        if is_in_check(TURN):
            print(f"Checkmate! {TURN.upper()} player wins!")
        else:
            print("Stalemate!")
        running = False

    pygame.display.flip()

pygame.quit()
