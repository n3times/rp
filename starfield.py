import pygame, random, sys

W, H = 800, 600
MAX_DEPTH = 1000
BG, FG = (0, 0, 0), (255, 255, 255)

MAX_STAR_SIZE = 4
STAR_SPEED = 20
NUM_STARS = 500

class Star:
    def __init__(self):
        self.x = random.uniform(-W, W)
        self.y = random.uniform(-H, H)
        self.z = random.uniform(1, MAX_DEPTH)

    def update(self):
        self.z -= STAR_SPEED  # Move forward
        
        # Recycle Star object when it gets past the camera
        if self.z < 1:
            self.x = random.uniform(-W, W)
            self.y = random.uniform(-H, H)
            self.z = MAX_DEPTH

    def render(self, screen):
        sx, sy = to_screen(self.x, self.y, self.z)

        # Leave a streak
        previous_z = self.z + STAR_SPEED
        px, py = to_screen(self.x, self.y, previous_z)
 
        # Closer stars look bigger
        size = round((1 - self.z / MAX_DEPTH) * MAX_STAR_SIZE)
        
        if 0 <= sx < W and 0 <= sy < H:
            pygame.draw.line(screen, FG, (px,py), (sx,sy), size)

def to_screen(x, y, z):
    # Simple perspective projection: closer objects appear
    # farther from center
    return round((x / z) * W/2 + W/2), round((y / z) * H/2 + H/2)

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
stars = [Star() for _ in range(NUM_STARS)]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)
    for star in stars:
        star.update()
        star.render(screen)
    pygame.display.flip()
    clock.tick(60)
