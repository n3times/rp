import pygame, random, math, sys
from math import sin, cos, atan2
from pygame.math import Vector2

W, H = 1000, 800
ALIGN_RADIUS, COH_RADIUS, SEP_RADIUS = 50, 75, 25
K_ALIGN, K_COH, K_SEP = 0.3, 0.1, 0.2
MAX_SPEED = 4
MAX_FORCE = 0.1
NUM_BOIDS = 100

class Boid:
    def __init__(self):
        x, y = random.uniform(0, W), random.uniform(0, H)
        self.pos = Vector2(x, y)
        theta = random.uniform(0, 2 * math.pi)
        speed = random.uniform(MAX_SPEED / 2, MAX_SPEED)
        vx, vy = speed * cos(theta), speed * sin(theta)
        self.vel = Vector2(vx, vy)

    def compute_steering(self, boids):
        align_sum = Vector2()
        coh_sum = Vector2()
        sep_sum = Vector2()
        align_count = coh_count = sep_count = 0

        for boid in boids:
            if boid is self: continue
            offset = boid.pos - self.pos
            dist = offset.length()

            if dist <= ALIGN_RADIUS:
                align_sum += boid.vel
                align_count += 1
            if dist <= COH_RADIUS:
                coh_sum += boid.pos
                coh_count += 1
            if 0 < dist <= SEP_RADIUS:
                sep_sum -= offset / dist ** 2
                sep_count += 1

        steering = Vector2()
        if align_count > 0:
            avg_vel = align_sum / align_count
            if avg_vel.length_squared() > 0:
                desired = avg_vel.normalize() * MAX_SPEED
                steering += (desired - self.vel) * K_ALIGN
        if coh_count > 0:
            center = coh_sum / coh_count
            desired = center - self.pos
            if desired.length_squared() > 0:
                desired = desired.normalize() * MAX_SPEED
                steering += (desired - self.vel) * K_COH
        if (sep_count > 0) and (sep_sum.length_squared() > 0):
            desired = sep_sum.normalize() * MAX_SPEED
            steering += (desired - self.vel) * K_SEP
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        return steering

    def update(self, steering):
        self.vel += steering
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        # Wrap around screen
        self.pos.x %= W 
        self.pos.y %= H

    def draw(self, screen):
        a = atan2(self.vel.y, self.vel.x)
        tip = self.pos + Vector2(cos(a), sin(a)) * 10
        l = self.pos + Vector2(cos(a + 2.5), sin(a + 2.5)) * 7
        r = self.pos + Vector2(cos(a - 2.5), sin(a - 2.5)) * 7
        pygame.draw.polygon(screen, (255, 255, 255), [tip, l, r])

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
boids = [Boid() for _ in range(NUM_BOIDS)]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    steerings = [boid.compute_steering(boids) for boid in boids]
    for boid, steering in zip(boids, steerings):
        boid.update(steering)

    screen.fill((0, 0, 0))
    for boid in boids:
        boid.draw(screen)
    pygame.display.flip() 
    clock.tick(60)
