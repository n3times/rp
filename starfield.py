import pygame, random, sys

W, H = 800, 600
MAX_DEPTH = 1000
BG, FG = (0, 0, 0), (255, 255, 255)

MAX_STAR_SIZE = 4
INITIAL_STAR_SPEED = 10
NUM_STARS = 500

class Star:
    def __init__(self):
        self.x = random.uniform(-W, W)
        self.y = random.uniform(-H, H)
        self.z = random.uniform(1, MAX_DEPTH)

    def update(self, star_speed):
        self.z -= star_speed  # Move forward
        
        # Recycle Star object when it gets past the camera
        if self.z < 1:
            self.x = random.uniform(-W, W)
            self.y = random.uniform(-H, H)
            self.z = MAX_DEPTH

    def render(self, screen, star_speed):
        sx, sy = to_screen(self.x, self.y, self.z)

        # Leave a streak
        previous_z = self.z + star_speed
        px, py = to_screen(self.x, self.y, previous_z)
 
        # Closer stars look bigger
        size = max(1, int((1 - self.z/MAX_DEPTH)*MAX_STAR_SIZE))
        
        if 0 <= sx < W and 0 <= sy < H:
            pygame.draw.line(screen, FG, (px,py), (sx,sy), size)

def to_screen(x, y, z):
    # Simple perspective projection: closer objects appear
    # farther from center
    return int((x / z) * W/2 + W/2), int((y / z) * H/2 + H/2)

def update_caption(star_speed):
    pygame.display.set_caption(
        f"left/right to control speed | Speed: {star_speed}"
    )

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
star_speed = INITIAL_STAR_SPEED
update_caption(star_speed)
stars = [Star() for _ in range(NUM_STARS)]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Control speed.
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                star_speed = max(1, star_speed - 1)
            elif e.key == pygame.K_RIGHT:
                star_speed += 1
            update_caption(star_speed)

    screen.fill(BG)
    for star in stars:
        star.update(star_speed)
        star.render(screen, star_speed)
    pygame.display.flip()
    clock.tick(60)
