import pygame
import random
from screeninfo import get_monitors

pygame.init()

monitor = get_monitors()[0]
windowWidth = monitor.width
windowHeight = monitor.height

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("SNAKE")

x = windowWidth // 2
y = windowHeight - windowHeight // 10

# Farbdefinitionen
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)

# Uhr definieren
clock = pygame.time.Clock()

# Quadratgröße
square_size = windowHeight // 40

# Liste für die Positionen und Geschwindigkeiten der schwarzen Quadrate
black_squares = []

# Event-Timer für die Erzeugung der Quadrate
ADD_SQUARE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_SQUARE, 1000)  # Event alle 1000 Millisekunden

game_over = False

run = True
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == ADD_SQUARE:
            # Zufällige X-Position generieren und zur Liste hinzufügen
            random_x_position = random.randint(0, windowWidth - square_size)
            black_squares.append([random_x_position, 0, 5])  # [x, y, speed]

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        x += windowWidth // 160
    if keys[pygame.K_LEFT]:
        x -= windowWidth // 160

    playerSize = windowHeight // 16

    # Überprüfen, ob das rote Rechteck mit einem schwarzen Rechteck kollidiert
    for square in black_squares:
        square[1] += square[2]  # Update y-coordinate using speed
        if y < square[1] + square_size and y + playerSize > square[1] and x < square[0] + square_size and x + playerSize > square[0]:
            game_over = True

    if game_over:
        # "Game Over" anzeigen
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, black)
        screen.blit(text, (windowWidth // 2 - text.get_width() // 2, windowHeight // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)  # kurz warten, bevor das Spiel beendet wird
        run = False

    screen.fill((0, 255, 200))

    # Schwarze Quadrate aktualisieren und zeichnen
    for square in black_squares:
        pygame.draw.rect(screen, black, [square[0], square[1], square_size, square_size])

    # Spielerrechteck zeichnen
    pygame.draw.rect(screen, red, (x, y, playerSize, playerSize))

    pygame.display.update()

pygame.quit()
