import pygame, sys, random

W, H, SCALE = 10, 20, 25
EMPTY = (0, 0, 0)
LINE_SCORES = (0, 100, 300, 500, 800)
PIECES = [
    {"shape":((0,2),(1,2),(2,2),(3,2)), "color":(0,255,255)}, # I
    {"shape":((0,0),(0,1),(1,0),(1,1)), "color":(255,255,0)}, # O
    {"shape":((0,0),(0,1),(1,1),(2,1)), "color":(0,0,255)},   # J
    {"shape":((2,0),(0,1),(1,1),(2,1)), "color":(255,140,0)}, # L
    {"shape":((0,0),(1,0),(1,1),(2,1)), "color":(255,0,0)},   # Z
    {"shape":((1,0),(2,0),(0,1),(1,1)), "color":(0,255,0)},   # S
    {"shape":((1,0),(0,1),(1,1),(2,1)), "color":(160,0,240)}, # T
]

pygame.init()
screen = pygame.display.set_mode((W * SCALE, H * SCALE))
clock = pygame.time.Clock()
board = [[EMPTY] * W for _ in range(H)]
score = 0

def quit_game(score):
    print(f"Final score: {score}")
    pygame.quit()
    sys.exit()

def draw_cell(surface, x, y, color):
    rect = x * SCALE + 1, y * SCALE + 1, SCALE - 2, SCALE - 2
    pygame.draw.rect(surface, color, rect)

def draw(surface, board, px, py, piece):
    surface.fill(EMPTY)
    for y, row in enumerate(board):
        for x, cell_color in enumerate(row):
            if cell_color != EMPTY:
                draw_cell(surface, x, y, cell_color)
    for dx, dy in piece["shape"]:
        draw_cell(surface, px + dx, py + dy, piece["color"])

def rotate(piece):
    box_size = max(max(pair) for pair in piece["shape"]) + 1
    new_shape = tuple(
        (y, box_size - 1 - x) for x, y in piece["shape"])
    return {"shape": new_shape, "color": piece["color"]}

def fits(board, piece, px, py):
    for dx, dy in piece["shape"]:
        x, y = px + dx, py + dy
        if not (0 <= x < W and y < H): return False
        if y >= 0 and board[y][x] != EMPTY: return False
    return True

def clear_completed_lines(board, score):
    remaining = [row for row in board if EMPTY in row]
    cleared = H - len(remaining)
    new_board = [[EMPTY] * W for _ in range(cleared)] + remaining
    new_score = score + LINE_SCORES[cleared]
    return new_board, new_score

def spawn_piece():
    piece = random.choice(PIECES)
    box_size = max(max(pair) for pair in piece["shape"]) + 1
    px, py = (W - box_size) // 2, -box_size # Center above board
    return px, py, piece

def lock_piece(board, px, py, piece):
    for dx, dy in piece["shape"]:
        if py + dy < 0: return False  # Above board
        board[py + dy][px + dx] = piece["color"]
    return True

px, py, piece = spawn_piece()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: quit_game(score)
        elif e.type != pygame.KEYDOWN: continue
        if e.key == pygame.K_LEFT:
            if fits(board, piece, px - 1, py): px -= 1
        elif e.key == pygame.K_RIGHT:
            if fits(board, piece, px + 1, py): px += 1
        elif e.key == pygame.K_UP:
            rotated = rotate(piece)
            if fits(board, rotated, px, py): piece = rotated
        elif e.key in (pygame.K_DOWN, pygame.K_SPACE):
            while fits(board, piece, px, py + 1):
                score += 2
                py += 1

    if fits(board, piece, px, py + 1):  # Fall through if we can
        py += 1
    else:                               # Otherwise, lock piece
        if not lock_piece(board, px, py, piece):
            quit_game(score)
        board, score = clear_completed_lines(board, score)
        px, py, piece = spawn_piece()
    draw(screen, board, px, py, piece)
    pygame.display.set_caption(f"Score: {score}")
    pygame.display.flip()
    clock.tick(5)
