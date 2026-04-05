import pygame, sys

W, H = 600, 600
HALF_W, HALF_H = W // 2, H // 2

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
    x, y = pixel
    dx = (x - HALF_W) / HALF_W
    dy = (HALF_H - y) / HALF_H
    scale = 2 / zoom
    return center + complex(dx * scale, dy * scale * H / W)

def color_for_iter(num_iter, max_iter):
    val = 0 if num_iter == max_iter else 128 + num_iter % 128
    return (val, val, val)

def render_pixel(surface, row, col, center, zoom, max_iter):
    c = pixel_to_complex((col, row), center, zoom)
    num_iter = escape_time(c, max_iter)
    surface.set_at((col, row), color_for_iter(num_iter, max_iter))

def render_ring(surface, ring, center, zoom, max_iter):
    for row in (HALF_H - ring, HALF_H + ring):
        for col in range(HALF_W - ring, HALF_W + ring + 1): 
            render_pixel(surface, row, col, center, zoom, max_iter)
    for row in range(HALF_H - ring, HALF_H + ring):
        for col in (HALF_W - ring, HALF_W + ring): 
            render_pixel(surface, row, col, center, zoom, max_iter)

def reset_view():
    return INITIAL_CENTER, INITIAL_ZOOM, INITIAL_MAX_ITER, 0

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

center, zoom, max_iter, next_ring = reset_view()

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
        if e.type != pygame.KEYDOWN: continue
        # Use brackets to change the "resolution" (max_iter)
        if e.key == pygame.K_LEFTBRACKET:
            max_iter = max(1, max_iter // 2)
        elif e.key == pygame.K_RIGHTBRACKET:
            max_iter *= 2
        # Use arrows to pan half a screen in one direction
        elif e.key == pygame.K_LEFT:
            center = pixel_to_complex((0, HALF_H), center, zoom)
        elif e.key == pygame.K_RIGHT:
            center = pixel_to_complex((W, HALF_H), center, zoom)
        elif e.key == pygame.K_DOWN:
            center = pixel_to_complex((HALF_W, H), center, zoom)
        elif e.key == pygame.K_UP:
            center = pixel_to_complex((HALF_W, 0), center, zoom)
        # Use "R" to reset
        elif e.key == pygame.K_r:
            center, zoom, max_iter, next_ring = reset_view()
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
