import sys, time
from math import cos, sin

WIDTH, HEIGHT = 65, 35          # Size of terminal "screen"
COLORS = ".=@$-*"               # Characters used to draw faces
N = 20                          # Resolution of each cube face

# ANSI escape codes for smoother animation
CLEAR_SCREEN = "\x1b[2J"
CURSOR_HOME = "\x1b[H"

class Rotation:
    def __init__(self, angle_x, angle_y, angle_z):
        # Precompute cos/sin for rotation angles
        cx, cy, cz = cos(angle_x), cos(angle_y), cos(angle_z)
        sx, sy, sz = sin(angle_x), sin(angle_y), sin(angle_z)

        # Combined 3D rotation matrix (Z * Y * X)
        self.matrix = (
            (cz*cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx),
            (sz*cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx),
            (  -sy,            cy*sx,            cy*cx)
        )

    def apply(self, x, y, z):
        # Apply rotation matrix to a 3D point
        m = self.matrix
        return (
            m[0][0]*x + m[0][1]*y + m[0][2]*z,
            m[1][0]*x + m[1][1]*y + m[1][2]*z,
            m[2][0]*x + m[2][1]*y + m[2][2]*z,
        )

class Face:
    def __init__(self, center, index):
        self.center = center      # Center of the face
        self.index = index        # Used to pick a character

        x, y, z = center

        # Only vary axes on the plane where the face lies.
        # The axis perpendicular to the face stays fixed.
        range_x = range(-N, N + 1) if x == 0 else range(1) 
        range_y = range(-N, N + 1) if y == 0 else range(1) 
        range_z = range(-N, N + 1) if z == 0 else range(1) 

        # Generate grid of points across the face
        self.points = [
            ((x + i / N, y + j / N, z + k / N), index)
            for i in range_x for j in range_y for k in range_z
        ]

    def is_facing_viewer(self, rotation):
        _, _, z = rotation.apply(*self.center)
        return z > 0

def create_cube_faces():
    left, right = Face((-1,0,0), 0), Face((1,0,0), 1)
    down, up = Face((0,-1,0), 2), Face((0,1,0), 3)
    back, front = Face((0,0,-1), 4), Face((0,0,1), 5)
    return (left, right, down, up, back, front)

def render_cube(canvas, cube, rotation):
    # Draw visible faces onto the canvas
    for face in cube:
        if not face.is_facing_viewer(rotation): continue
        for (x, y, z), index in face.points:
            rot_x, rot_y, _ = rotation.apply(x, y, z)
            screen_x = round(WIDTH / 2 + rot_x * WIDTH / 4)
            screen_y = round(HEIGHT / 2 + rot_y * HEIGHT / 4)
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                canvas[screen_y][screen_x] = COLORS[index]

cube = create_cube_faces()
angle = 0

try:
    sys.stdout.write(CURSOR_HOME)
    sys.stdout.write(CLEAR_SCREEN)

    while True:
        rotation = Rotation(angle*0.7, angle*0.4, angle*1.1)

        canvas = [
            [" " for i in range(WIDTH)] for j in range(HEIGHT)
        ]
        render_cube(canvas, cube, rotation)

        frame = "\n".join("".join(row) for row in canvas)
        sys.stdout.write(frame)

        sys.stdout.write(CURSOR_HOME)
        sys.stdout.flush()

        angle += 0.05          # Increase rotation angle
        time.sleep(0.03)       # Control animation speed
except KeyboardInterrupt:
    pass
