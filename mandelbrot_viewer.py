import pygame, sys

W, H = 800, 600

INITIAL_CENTER = -0.5 + 0j
INITIAL_ZOOM = 1
INITIAL_MAX_ITER = 128

def escape_time(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2: return i
    return max_iter

def pixel_to_complex(pixel, center, zoom):
    i, j = pixel
    j = H - j
    x = center.real - (W // 2 - i) / (W // 2) / zoom * 2
    y = center.imag - (H // 2 - j) / (H // 2) / zoom * 2 * H / W
    return complex(x, y)

def color_for_iter(num_iter, max_iter):
    val = 0 if num_iter == max_iter else 128 + num_iter % 128
    return (val, val, val)

def render_pixel(surface, row, col, center, zoom, max_iter):
    c = pixel_to_complex((col, row), center, zoom)
    num_iter = escape_time(c, max_iter)
    surface.set_at((col, row), color_for_iter(num_iter, max_iter))

def render_ring(surface, ring, center, zoom, max_iter):
    for row in (H // 2 - ring, H // 2 + ring):
        for col in range(W // 2 - ring, W // 2 + ring + 1): 
            render_pixel(surface, row, col, center, zoom, max_iter)
    for row in range(H // 2 - ring, H // 2 + ring + 1):
        for col in (W // 2 - ring, W // 2 + ring): 
            render_pixel(surface, row, col, center, zoom, max_iter)

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

center = INITIAL_CENTER
max_iter = INITIAL_MAX_ITER
zoom = INITIAL_ZOOM
next_ring = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            center = pixel_to_complex(e.pos, center, zoom)
            if e.button == 3:  # right click
                zoom = max(1, zoom // 2)
            else:
                zoom *= 2
            next_ring = 0
        elif e.type == pygame.KEYDOWN:
            # Use brackets to change the "resolution" (max_iter)
            if e.key == pygame.K_LEFTBRACKET:
                max_iter = max(1, max_iter // 2)
            elif e.key == pygame.K_RIGHTBRACKET:
                max_iter *= 2
            # Use arrows to pan half a screen in one direction
            elif e.key == pygame.K_LEFT:
                center = pixel_to_complex((0, H//2), center, zoom)
            elif e.key == pygame.K_RIGHT:
                center = pixel_to_complex((W, H//2), center, zoom)
            elif e.key == pygame.K_DOWN:
                center = pixel_to_complex((W//2, H), center, zoom)
            elif e.key == pygame.K_UP:
                center = pixel_to_complex((W//2, 0), center, zoom)
            # Use "R" to reset
            elif e.key == pygame.K_r:
                center = INITIAL_CENTER
                zoom = INITIAL_ZOOM
                max_iter = INITIAL_MAX_ITER
            next_ring = 0

    # Prepare to draw
    if next_ring == 0:
        screen.fill((255, 255, 255))
        pygame.display.set_caption(
            f"Zoom {zoom:,} -- Iters {max_iter:,}"
        )

    # Draw a few rings at a time
    if next_ring <= max(W, H) // 2:
        for radius in range(next_ring, next_ring + 3):
            render_ring(screen, radius, center, zoom, max_iter)
        next_ring += 3

    pygame.display.flip()
    clock.tick(60)
