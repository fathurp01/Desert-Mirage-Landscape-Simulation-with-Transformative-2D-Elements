import pygame
import math
import random

# f Inisailisasi Pygame
pygame.init()

# f Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Mirage: Landscape Simulation")

# f pengaturan warna
SKY_COLOR = (185, 235, 250)
DESERT_COLOR = (237, 201, 175)
SUN_COLOR = (255, 223, 0)
TUMBLEWEED_COLOR = (139, 69, 19)
SHADOW_COLOR = (50, 50, 50)
CACTUS_COLOR = (34, 139, 34)
MIRAGE_COLOR = (135, 206, 250, 100)
PYRAMID_COLOR1 = (139, 69, 19)
PYRAMID_COLOR2 = (160, 82, 45)
PYRAMID_COLOR3 = (205, 133, 63)

# f time clock untuk mengatur frame rate
clock = pygame.time.Clock()

# f atribut tumbleweed
tumbleweed_pos = [-50, HEIGHT - 100]  # Initial position (x, y)
tumbleweed_translation = [2, 0]  # Translation values (tx, ty)
tumbleweed_angle = 0

# f atribut refleksi tumbleweed
shadow_offset = -454
horizontal_offset = 30

# f perhitungan posisi tumbleweed awal untuk mengenerate circle
tumbleweed_layers = []
layer_count = 7
for i in range(layer_count):
    radius = 25 - i * 2.5
    layer = []
    for _ in range(8):
        offset_angle = random.uniform(0, 2 * math.pi)
        offset_x = int(math.cos(offset_angle) * radius)
        offset_y = int(math.sin(offset_angle) * radius)
        layer.append((offset_x, offset_y))
    tumbleweed_layers.append(layer)

# f atribut awan
cloud_translation = [1, 0]  # Translation values (tx, ty) for clouds
clouds = [
    {
        "x": -200,
        "y_offsets": [120, 110, 120],
        "sizes": [35, 40, 35],
        "color": (255, 255, 255, 180),
    },
    {
        "x": -500,
        "y_offsets": [150, 160, 170],
        "sizes": [45, 50, 45],
        "color": (255, 255, 255, 150),
    },
    {
        "x": -800,
        "y_offsets": [65, 55, 45],
        "sizes": [30, 35, 30],
        "color": (255, 255, 255, 200),
    },
]

# atribut matahari
sun_pos = [WIDTH // 2 - 300, HEIGHT // 4 - 50]
sun_radius = 50
sun_scale_factor = 0.15
sun_scale_direction = 1

# atribut kaktus
cactus_pos = (100, HEIGHT - 200)
cactus_pos1 = (700, HEIGHT - 125)

# atribut mirage
mirage_height = 30
mirage_pos = [0, HEIGHT // 2 - mirage_height // 2]
layer_count = 20
adjusted_mirage_height = 80
spacing = 8

# atribut gelombang angin
wind_particles = []
num_particles = 50
wind_translation = [3, 0]  # Translation values (tx, ty) for wind
wind_amplitude = 20
wind_frequency = 0.05

# inisialisasi partikel angin
for _ in range(num_particles):
    particle = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(HEIGHT // 2, HEIGHT),
        "size": random.randint(2, 4),
        "phase": random.uniform(0, 2 * math.pi),
    }
    wind_particles.append(particle)


# Functions untuk menggambar objek-objek di layar
def draw_background(surface):
    pygame.draw.rect(surface, SKY_COLOR, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(surface, DESERT_COLOR, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))


def draw_dunes(surface):
    pygame.draw.ellipse(surface, (210, 180, 140), (250, HEIGHT - 350, 500, 100))
    pygame.draw.ellipse(surface, (200, 170, 130), (450, HEIGHT - 400, 400, 150))


def draw_dunes1(surface):
    pygame.draw.ellipse(surface, (220, 180, 150), (550, HEIGHT - 300, 300, 120))


def draw_sun(surface):
    global sun_radius, sun_scale_direction
    sun_radius += sun_scale_direction * sun_scale_factor
    if sun_radius > 50 or sun_radius < 40:
        sun_scale_direction *= -1
    pygame.draw.circle(surface, SUN_COLOR, sun_pos, int(sun_radius))


# f
def draw_clouds(surface):
    for cloud in clouds:
        for i in range(len(cloud["sizes"])):
            y_offset = cloud["y_offsets"][i]
            pygame.draw.circle(
                surface,
                cloud["color"],
                (cloud["x"] + i * cloud["sizes"][i], y_offset),
                cloud["sizes"][i],
            )


# f
def move_clouds():
    for cloud in clouds:
        # translation formula
        cloud["x"] = cloud["x"] + cloud_translation[0]  # x' = x + tx
        if cloud["x"] > WIDTH:
            cloud["x"] = -max(cloud["sizes"]) * 3


# f
def draw_tumbleweed(surface, center, angle, color):
    for layer in tumbleweed_layers:
        for offset_x, offset_y in layer:
            rotated_x = (
                center[0] + offset_x * math.cos(angle) - offset_y * math.sin(angle)
            )
            rotated_y = (
                center[1] + offset_x * math.sin(angle) + offset_y * math.cos(angle)
            )
            pygame.draw.circle(surface, color, (int(rotated_x), int(rotated_y)), 10, 1)


# f
def draw_shadow(surface, tumbleweed_pos, angle):
    shadow_pos = [
        tumbleweed_pos[0] + horizontal_offset,
        tumbleweed_pos[1] + shadow_offset,
    ]
    shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shadow_surface.set_alpha(150)
    draw_tumbleweed(shadow_surface, shadow_pos, angle, SHADOW_COLOR)
    reflection_surface = pygame.transform.flip(shadow_surface, False, True)
    surface.blit(
        pygame.transform.smoothscale(reflection_surface, (WIDTH, HEIGHT)), (0, 0)
    )


def draw_cactus(surface):
    pygame.draw.rect(surface, CACTUS_COLOR, (*cactus_pos, 20, 100))
    pygame.draw.ellipse(
        surface, CACTUS_COLOR, (cactus_pos[0] - 15, cactus_pos[1] - 30, 50, 50)
    )
    pygame.draw.rect(
        surface, CACTUS_COLOR, (cactus_pos[0] - 10, cactus_pos[1] - 50, 15, 50)
    )
    pygame.draw.rect(
        surface, CACTUS_COLOR, (cactus_pos[0] + 15, cactus_pos[1] - 40, 15, 40)
    )


def draw_cactus1(surface):
    pygame.draw.rect(surface, CACTUS_COLOR, (*cactus_pos1, 20, 120))
    pygame.draw.ellipse(
        surface, CACTUS_COLOR, (cactus_pos1[0] - 12, cactus_pos1[1] - 30, 50, 60)
    )
    pygame.draw.rect(
        surface, CACTUS_COLOR, (cactus_pos1[0] - 10, cactus_pos1[1] - 50, 15, 60)
    )
    pygame.draw.rect(
        surface, CACTUS_COLOR, (cactus_pos1[0] + 20, cactus_pos1[1] - 55, 15, 50)
    )


def draw_mirage(surface):
    mirage_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(layer_count):
        alpha = int(255 * (1 - i / layer_count))
        rect_height = max(adjusted_mirage_height - i * spacing, 0)
        pygame.draw.rect(
            mirage_surface,
            (MIRAGE_COLOR[0], MIRAGE_COLOR[1], MIRAGE_COLOR[2], alpha),
            (mirage_pos[0], mirage_pos[1] + i * spacing, WIDTH, rect_height),
        )
    surface.blit(mirage_surface, (0, 0))


def draw_pyramid(surface, x, y, width, height, color):
    pyramid_points = [
        (x - width // 2, y + height),
        (x + width // 2, y + height),
        (x, y),
    ]
    pygame.draw.polygon(surface, color, pyramid_points)


def draw_wind_waves(surface):
    """Draw wind effect particles using translation formula: x' = x + tx, y' = y + ty"""
    for particle in wind_particles:
        # Apply translation formula
        particle["x"] = particle["x"] + wind_translation[0]  # x' = x + tx

        # Create wave motion
        wave_offset = (
            math.sin(particle["phase"] + particle["x"] * wind_frequency)
            * wind_amplitude
        )

        pygame.draw.circle(
            surface,
            (DESERT_COLOR[0] - 20, DESERT_COLOR[1] - 20, DESERT_COLOR[2] - 20),
            (int(particle["x"]), int(particle["y"] + wave_offset)),
            particle["size"],
        )

        particle["phase"] += 0.01

        if particle["x"] > WIDTH:
            particle["x"] = 0
            particle["y"] = random.randint(HEIGHT // 2, HEIGHT)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background(screen)
    draw_mirage(screen)
    draw_dunes(screen)

    pyramid1_width, pyramid1_height = 400, 200
    pyramid2_width, pyramid2_height = 350, 150
    pyramid3_width, pyramid3_height = 250, 100

    pyramid1_pos = (WIDTH // 1.7, HEIGHT - 400 - 40)
    pyramid2_pos = (WIDTH // 2.3, HEIGHT - 350 - 40)
    pyramid3_pos = (WIDTH // 3.1, HEIGHT - 290 - 40)

    draw_pyramid(
        screen,
        pyramid2_pos[0],
        pyramid2_pos[1],
        pyramid2_width,
        pyramid2_height,
        PYRAMID_COLOR2,
    )
    draw_pyramid(
        screen,
        pyramid1_pos[0],
        pyramid1_pos[1],
        pyramid1_width,
        pyramid1_height,
        PYRAMID_COLOR1,
    )
    draw_pyramid(
        screen,
        pyramid3_pos[0],
        pyramid3_pos[1],
        pyramid3_width,
        pyramid3_height,
        PYRAMID_COLOR3,
    )

    draw_dunes1(screen)

    draw_sun(screen)

    # f
    draw_clouds(screen)
    move_clouds()
    draw_shadow(screen, tumbleweed_pos, tumbleweed_angle)

    draw_cactus(screen)

    # f Update posisi tumbleweed dengan menggunakan formula translasi : x' = x + tx, y' = y + ty
    tumbleweed_pos[0] = tumbleweed_pos[0] + tumbleweed_translation[0]  # x' = x + tx
    tumbleweed_pos[1] = tumbleweed_pos[1] + tumbleweed_translation[1]  # y' = y + ty
    tumbleweed_angle += 0.1
    if tumbleweed_pos[0] > WIDTH + 50:
        tumbleweed_pos[0] = -50
    draw_tumbleweed(screen, tumbleweed_pos, tumbleweed_angle, TUMBLEWEED_COLOR)

    draw_cactus1(screen)
    draw_wind_waves(screen)

    # f
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
