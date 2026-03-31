import pygame, sys

WIDTH, HEIGHT = 800, 600
BG_COLOR, CELL_COLOR = (0, 0, 0), (255, 255, 255)
DEFAULT_CELL_SIZE, DEFAULT_FPS = 5, 3
NEIGHBORS = ((-1,-1), (0,-1), (1,-1),
             (-1, 0),         (1, 0),
             (-1, 1), (0, 1), (1, 1))

# B = birth counts, S = survival counts (e.g. Conway is B3/S23)
RULE = "B3/S23"

# Set the initial state here: 'o' = alive, '.' = dead
INITIAL_STATE = (
    ".o.",
    "..o",
    "ooo",
)

def parse_rule(rule):
    birth, survival = rule.split("/")
    birth_set = {int(n) for n in birth[1:]}
    survival_set = {int(n) for n in survival[1:]}
    return (birth_set, survival_set)

def parse_state(state):
    live_cells = set()
    row_count = len(state)
    col_count = max((len(row) for row in state), default=0)
    # Center the pattern around (0, 0)
    offset_x, offset_y = -(col_count // 2), -(row_count // 2)
    for y, row in enumerate(state):
        for x, char in enumerate(row):
            if char == "o":
                live_cells.add((x + offset_x, y + offset_y))
    return live_cells

def evolve_state(live_cells, rule):
    # Count neighbors.
    # Include all current cells even if they end up with 0
    # neighbors, so survival rules like S0 can be applied
    neighbor_counts = {}
    for cell in live_cells:
        neighbor_counts[cell] = 0
    for x, y in live_cells:
        for dx, dy in NEIGHBORS:
            neighbor = (x + dx, y + dy)
            previous_count = neighbor_counts.get(neighbor, 0)
            neighbor_counts[neighbor] = previous_count + 1

    # Apply birth/survival rule to all neighbors
    birth_set, survival_set = rule
    next_cells = set()
    for cell, count in neighbor_counts.items():
        if ((cell in live_cells and count in survival_set) or
            (cell not in live_cells and count in birth_set)):
            next_cells.add(cell)
    return next_cells

def render_state(screen, live_cells, cell_size):
    screen.fill(BG_COLOR)
    cols, rows = WIDTH // cell_size, HEIGHT // cell_size
    offset_x, offset_y = cols // 2, rows // 2
    gap = 1 if cell_size > 2 else 0
    rect_size = cell_size - gap
    for x, y in live_cells:
        # Center coordinates around (0, 0)
        x, y = x + offset_x, y + offset_y
        if x < 0 or x >= cols or y < 0 or y >= rows: continue
        pygame.draw.rect(screen, CELL_COLOR,
            (x * cell_size, y * cell_size, rect_size, rect_size))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cell_size, fps = DEFAULT_CELL_SIZE, DEFAULT_FPS
rule = parse_rule(RULE)
live_cells = parse_state(INITIAL_STATE)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control zoom and speed.
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: cell_size += 1
            elif e.key == pygame.K_DOWN: cell_size -= 1
            elif e.key == pygame.K_RIGHT: fps += 1
            elif e.key == pygame.K_LEFT: fps -= 1
            cell_size, fps = max(cell_size, 1), max(fps, 1)
            
    render_state(screen, live_cells, cell_size)
    pygame.display.set_caption(f"FPS {fps} - Zoom {cell_size}")
    live_cells = evolve_state(live_cells, rule)
    pygame.display.flip()
    clock.tick(fps)
