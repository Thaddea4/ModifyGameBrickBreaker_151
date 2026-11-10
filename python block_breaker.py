
import pygame
import random
import math

pygame.init()

# Mengatur ukuran layar permainan
WIDTH, HEIGHT = 600, 500

# Menentukan warna yang digunakan dalam permainan
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Warna latar belakang dan hiasan
ORANGE = (255, 205, 145)
DARK_ORANGE = (235, 135, 55)
LIGHT_ORANGE = (255, 225, 180)
CREAM = (255, 242, 210)

# Mengatur jenis dan ukuran tulisan
font = pygame.font.Font('freesansbold.ttf', 15)
titleFont = pygame.font.Font('freesansbold.ttf', 22)

# Membuat layar permainan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Flower Theme")

# Mengatur kecepatan permainan
clock = pygame.time.Clock()
FPS = 30