
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


# Fungsi untuk membuat hiasan bunga pada latar belakang
def drawFlower(x, y, size, petalColor, centerColor):

    # Menggambar kelopak bunga
    for i in range(8):
        angle = math.radians(i * 45)

        petalX = x + int(math.cos(angle) * size)
        petalY = y + int(math.sin(angle) * size)

        pygame.draw.circle(
            screen, petalColor,
            (petalX, petalY), max(2, size // 3)
        )

    # Menggambar bagian tengah bunga
    pygame.draw.circle(
        screen, centerColor, (x, y),
        max(2, size // 3)
    )


# Fungsi untuk menggambar hiasan latar belakang
def drawBackground():

    # Mengisi layar dengan warna oranye muda
    screen.fill(ORANGE)

    # Menggambar lingkaran dekoratif di sudut layar
    pygame.draw.circle(screen, LIGHT_ORANGE, (25, 25), 15)
    pygame.draw.circle(screen, LIGHT_ORANGE, (575, 25), 15)
    pygame.draw.circle(screen, LIGHT_ORANGE, (25, 475), 15)
    pygame.draw.circle(screen, LIGHT_ORANGE, (575, 475), 15)

    # Menggambar hiasan bunga di sisi kiri
    drawFlower(20, 245, 9, PINK, YELLOW)
    drawFlower(25, 330, 8, CREAM, DARK_ORANGE)
    drawFlower(20, 405, 9, PINK, YELLOW)

    # Menggambar hiasan bunga di sisi kanan
    drawFlower(580, 245, 9, CREAM, DARK_ORANGE)
    drawFlower(575, 330, 8, PINK, YELLOW)
    drawFlower(580, 405, 9, CREAM, DARK_ORANGE)

    # Menggambar hiasan bunga kecil di bagian bawah
    drawFlower(210, 465, 6, PINK, YELLOW)
    drawFlower(390, 465, 6, CREAM, DARK_ORANGE)

    # Menggambar hiasan titik-titik dekoratif
    pygame.draw.circle(screen, DARK_ORANGE, (65, 285), 3)
    pygame.draw.circle(screen, DARK_ORANGE, (535, 285), 3)
    pygame.draw.circle(screen, PINK, (65, 365), 3)
    pygame.draw.circle(screen, PINK, (535, 365), 3)


# Fungsi untuk memeriksa tabrakan antara dua objek
def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True

    return False


# Fungsi untuk membuat balok dengan warna kuning dan pink
def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth + horizontalGap):
        for j in range(0, HEIGHT // 2, blockHeight + verticalGap):
            listOfBlocks.append(Block(
                i, j, blockWidth, blockHeight,
                random.choice([YELLOW, PINK])
            ))

    return listOfBlocks


# Fungsi yang dijalankan ketika semua nyawa habis
def gameOver():
    while True:
        drawBackground()

        # Menampilkan tulisan permainan berakhir
        gameOverText = titleFont.render(
            "GAME OVER", True, RED
        )
        gameOverRect = gameOverText.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )

        restartText = font.render(
            "Tekan SPACE untuk bermain lagi", True, BLACK
        )
        restartRect = restartText.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 20)
        )

        screen.blit(gameOverText, gameOverRect)
        screen.blit(restartText, restartRect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


# Kelas untuk mengatur papan pemantul
class Striker:
    def __init__(self, posx, posy, width,
                 height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # Membuat bentuk papan pemantul
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

        self.striker = pygame.draw.rect(
            screen, self.color, self.strikerRect
        )

    # Menampilkan papan pemantul pada layar
    def display(self):
        self.striker = pygame.draw.rect(
            screen, self.color, self.strikerRect,
            border_radius=8
        )

    # Mengatur pergerakan papan pemantul
    def update(self, xFac):
        self.posx += self.speed * xFac

        # Membatasi pergerakan papan agar tidak keluar layar
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    # Mengembalikan posisi papan untuk pemeriksaan tabrakan
    def getRect(self):
        return self.strikerRect