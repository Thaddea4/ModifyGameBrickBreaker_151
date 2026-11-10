
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


# Kelas untuk mengatur balok
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        # Balok pink membutuhkan dua kali benturan
        # Balok kuning membutuhkan satu kali benturan
        if color == PINK:
            self.health = 200
        else:
            self.health = 100

        # Membuat bentuk balok
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

        self.block = pygame.draw.rect(
            screen, self.color, self.blockRect
        )

    # Menampilkan balok selama ketahanannya masih ada
    def display(self):
        if self.health > 0:
            self.block = pygame.draw.rect(
                screen, self.color, self.blockRect,
                border_radius=4
            )

    # Mengurangi ketahanan balok ketika terkena bunga
    def hit(self):
        self.health -= self.damage

    # Mengembalikan posisi balok
    def getRect(self):
        return self.blockRect

    # Mengembalikan sisa ketahanan balok
    def getHealth(self):
        return self.health


# Kelas untuk mengatur bunga sebagai pengganti bola
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, -1

        # Membuat area tabrakan bunga
        self.ballRect = pygame.Rect(0, 0, 0, 0)

    # Menampilkan bunga pada layar
    def display(self):

        # Menggambar delapan kelopak bunga berwarna merah
        for i in range(8):
            angle = math.radians(i * 45)

            petalX = self.posx + int(math.cos(angle) * self.radius)
            petalY = self.posy + int(math.sin(angle) * self.radius)

            pygame.draw.circle(
                screen, self.color,
                (petalX, petalY), 8
            )

        # Menggambar bagian tengah bunga berwarna kuning
        pygame.draw.circle(
            screen, YELLOW,
            (self.posx, self.posy), 7
        )

        # Memperbarui area tabrakan bunga
        self.ballRect = pygame.Rect(
            self.posx - self.radius - 8,
            self.posy - self.radius - 8,
            (self.radius + 8) * 2,
            (self.radius + 8) * 2
        )

    # Mengatur pergerakan bunga
    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Membalik arah bunga ketika menyentuh sisi layar
        if self.posx <= self.radius + 8 or self.posx >= WIDTH - self.radius - 8:
            self.xFac *= -1

        # Membalik arah bunga ketika menyentuh bagian atas
        if self.posy <= self.radius + 8:
            self.yFac *= -1

        # Memperbarui area tabrakan sesuai posisi bunga
        self.ballRect = pygame.Rect(
            self.posx - self.radius - 8,
            self.posy - self.radius - 8,
            (self.radius + 8) * 2,
            (self.radius + 8) * 2
        )

        # Mengurangi nyawa ketika bunga jatuh ke bawah
        if self.posy >= HEIGHT:
            return True

        return False

    # Mengembalikan bunga ke posisi awal
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac, self.yFac = 1, -1

    # Mengubah arah gerak bunga ketika terjadi benturan
    def hit(self):
        self.yFac *= -1

    # Mengembalikan area tabrakan bunga
    def getRect(self):
        return self.ballRect


# Fungsi utama untuk menjalankan permainan
def main():
    running = True
    lives = 3
    score = 0

    # Mengatur tampilan tulisan skor dan nyawa
    scoreTextRect = pygame.Rect(25, HEIGHT - 25, 100, 20)
    livesTextRect = pygame.Rect(145, HEIGHT - 25, 100, 20)

    # Membuat papan pemantul berwarna ungu dan lebih lebar
    striker = Striker(
        (WIDTH - 130) // 2,
        HEIGHT - 50,
        130, 20, 10, PURPLE
    )

    strikerXFac = 0

    # Membuat bunga merah dengan ukuran lebih besar
    ball = Ball(WIDTH // 2, HEIGHT - 150, 12, 5, RED)

    # Mengatur ukuran dan jarak antarbalok
    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    # Membuat kumpulan balok
    listOfBlocks = populateBlocks(
        blockWidth, blockHeight,
        horizontalGap, verticalGap
    )

    # Perulangan utama permainan
    while running:

        # Menggambar latar belakang dan hiasan
        drawBackground()

        # Memperbarui tampilan skor dan nyawa
        scoreText = font.render(
            "Score : " + str(score), True, BLACK
        )

        livesText = font.render(
            "Lives : " + str(lives), True, BLACK
        )

        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        # Membuat kembali balok jika semuanya telah hancur
        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight,
                horizontalGap, verticalGap
            )

        # Memeriksa kondisi ketika semua nyawa habis
        if lives <= 0:
            running = gameOver()

            if not running:
                break

            lives = 3
            score = 0
            ball.reset()

            listOfBlocks = populateBlocks(
                blockWidth, blockHeight,
                horizontalGap, verticalGap
            )

        # Mengatur perintah dari keyboard
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1

                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Memeriksa tabrakan antara bunga dan papan pemantul
        if collisionChecker(striker.getRect(), ball.getRect()):
            if ball.yFac > 0:
                ball.hit()

        # Memeriksa tabrakan antara bunga dan balok
        for block in listOfBlocks[:]:
            if collisionChecker(block.getRect(), ball.getRect()):
                ball.hit()
                block.hit()

                # Menghapus balok jika ketahanannya habis
                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5

        # Memperbarui posisi papan pemantul dan bunga
        striker.update(strikerXFac)
        lifeLost = ball.update()

        # Mengurangi nyawa jika bunga jatuh
        if lifeLost:
            lives -= 1
            ball.reset()

        # Menampilkan papan pemantul
        striker.display()

        # Menampilkan semua balok
        for block in listOfBlocks:
            block.display()

        # Menampilkan bunga
        ball.display()

        # Memperbarui tampilan layar
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
