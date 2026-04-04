import pygame, sys

W, H = 800, 600

INITIAL_CENTER = 0 + 0j
INITIAL_ZOOM = 1
INITIAL_MAX_ITER = 128

def escape_time(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2: return i
    return max_iter

def translate(screen_pos, center, zoom):
    i, j = screen_pos
    j = H - j
    x = center.real - (W // 2 - i) / (W // 2) / zoom * 2
    y = center.imag - (H // 2 - j) / (H // 2) / zoom * 2 * H / W
    return complex(x, y)

def get_color(escape_time, max_iter):
    # Black for the Mandelbrot set and white to mid gray outside
    val = 0 if escape_time == max_iter else 128 + escape_time%128
    return (val, val, val)

def render_column(surface, col, center, zoom, max_iter):
    for row in range(H):
        c = translate((col, row), center, zoom)
        time = escape_time(c, max_iter)
        surface.set_at((col, row), get_color(time, max_iter))

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

center = INITIAL_CENTER
max_iter = INITIAL_MAX_ITER
zoom = INITIAL_ZOOM
next_col = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            center = translate(e.pos, center, zoom)
            if e.button == 3:  # right click
                zoom = max(1, zoom // 2)
            else:
                zoom *= 2
            next_col = 0
        elif e.type == pygame.KEYDOWN:
            # Use brackets to change the "resolution" (max_iter)
            if e.key == pygame.K_LEFTBRACKET:
                max_iter = max(1, max_iter // 2)
            elif e.key == pygame.K_RIGHTBRACKET:
                max_iter *= 2
            # Use arrows to pan half a screen in one direction
            elif e.key == pygame.K_LEFT:
                center = translate((0, H//2), center, zoom)
            elif e.key == pygame.K_RIGHT:
                center = translate((W, H//2), center, zoom)
            elif e.key == pygame.K_DOWN:
                center = translate((W//2, H), center, zoom)
            elif e.key == pygame.K_UP:
                center = translate((W//2, 0), center, zoom)
            # Use "R" to reset
            elif e.key == pygame.K_r:
                center = INITIAL_CENTER
                zoom = 1
                max_iter = 128
            next_col = 0

    # Prepare to draw
    if next_col == 0:
        screen.fill((255, 255, 255))
        pygame.display.set_caption(
            f"Zoom {zoom:,} -- Iters {max_iter:,}"
        )

    # Draw a few columns at a time
    if next_col < W:
        for col in range(next_col, min(next_col + 3, W)):
            render_column(screen, col, center, zoom, max_iter)
        next_col += 3

    pygame.display.flip()
    clock.tick(60)
