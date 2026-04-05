import pygame, sys

W, H = 800, 600

INITIAL_CENTER = -0.5 + 0j
INITIAL_ZOOM = 1
INITIAL_MAX_ITER = 128
RANGE_X_FOR_ZOOM_1 = 4

def mandelbrot_iters(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2: return i
    return max_iter

def pixel_to_complex(pixel, center, zoom):
    x, y = pixel
    dx, dy = x - W//2, H//2 - y
    scale = RANGE_X_FOR_ZOOM_1 / W / zoom
    return center + complex(dx * scale, dy * scale)

def color_for_iter(iters, max_iter):
    if iters == max_iter: return (0, 0, 0)
    val = 128 + int(128 * iters / max_iter)
    return (val, val, val)

def draw_pixel(surface, x, y, center, zoom, max_iter):
    if not(0 <= x < W and 0 <= y < H): return
    c = pixel_to_complex((x, y), center, zoom)
    iters = mandelbrot_iters(c, max_iter)
    surface.set_at((x, y), color_for_iter(iters, max_iter))

def draw_ring(surface, ring, center, zoom, max_iter):
    for y in (H//2 - ring, H//2 + ring):
        for x in range(W//2 - ring, W//2 + ring + 1): 
            draw_pixel(surface, x, y, center, zoom, max_iter)
    for y in range(H//2 - ring, H//2 + ring):
        for x in (W//2 - ring, W//2 + ring): 
            draw_pixel(surface, x, y, center, zoom, max_iter)

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

        # Control zoom, panning, iterations, and reset
        if e.type == pygame.MOUSEBUTTONDOWN:
            center = pixel_to_complex(e.pos, center, zoom)
            if e.button == pygame.BUTTON_RIGHT:
                zoom = max(1, zoom // 2)
            else:
                zoom *= 2
            next_ring = 0
        if e.type != pygame.KEYDOWN: continue
        if e.key == pygame.K_LEFTBRACKET:
            max_iter = max(1, max_iter // 2)
        elif e.key == pygame.K_RIGHTBRACKET:
            max_iter *= 2
        elif e.key == pygame.K_LEFT:
            center += -1 / zoom
        elif e.key == pygame.K_RIGHT:
            center += 1 / zoom
        elif e.key == pygame.K_DOWN:
            center += -1j / zoom
        elif e.key == pygame.K_UP:
            center += 1j / zoom
        elif e.key == pygame.K_r:
            center, zoom, max_iter, next_ring = reset_view()
        else: continue
        next_ring = 0

    # Prepare to draw
    if next_ring == 0:
        screen.fill((255, 255, 255))
        pygame.display.set_caption(
            f"{center} -- Zoom {zoom:,} -- Iters {max_iter:,}")

    # Draw a few rings at a time
    if next_ring <= max(W, H) // 2:
        for _ in range(3):
            draw_ring(screen, next_ring, center, zoom, max_iter)
            next_ring += 1

    pygame.display.flip()
    clock.tick(60)
