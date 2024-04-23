import pygame
import random
import sys

pygame.init()

WIN_SIZE = 800

screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("SNAKE")

x = 400
y = 700

# Farbdefinitionen
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)

# Uhr definieren
clock = pygame.time.Clock()

# Quadratgröße
square_size = 20

# Liste für die Positionen und Geschwindigkeiten der schwarzen Quadrate
black_squares = []
white_squares = []

# Event-Timer für die Erzeugung der Quadrate
ADD_SQUARE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_SQUARE, 1000)  # Event alle 1000 Millisekunden

# Rechtecke für die Schaltflächen "Nochmal spielen" und "Spiel beenden"
retry_rect = pygame.Rect(0, 0, 0, 0)
quit_rect = pygame.Rect(0, 0, 0, 0)

def game_over_screen():
    global retry_rect, quit_rect
    # "Game Over" anzeigen
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, black)
    screen.blit(text, (WIN_SIZE // 2 - text.get_width() // 2, WIN_SIZE // 2 - text.get_height() // 2))

    # "Nochmal spielen" und "Spiel beenden" anzeigen
    font = pygame.font.Font(None, 36)
    text_retry = font.render("Nochmal spielen", True, black)
    text_quit = font.render("Spiel beenden", True, black)

    # Positionen der Texte festlegen
    retry_rect = text_retry.get_rect(center=(WIN_SIZE // 2, WIN_SIZE // 2 + 50))
    quit_rect = text_quit.get_rect(center=(WIN_SIZE // 2, WIN_SIZE // 2 + 100))

    # Rechtecke zeichnen
    pygame.draw.rect(screen, white, retry_rect, 2)
    pygame.draw.rect(screen, white, quit_rect, 2)

    # Texte zeichnen
    screen.blit(text_retry, retry_rect)
    screen.blit(text_quit, quit_rect)

    pygame.display.update()

game_over = False

run = True
points = 0
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == ADD_SQUARE:
            # Zufällige X-Position generieren und zur Liste hinzufügen
            random_x_position = random.randint(0, WIN_SIZE - square_size)
            black_squares.append([random_x_position, 0, 5])  # [x, y, speed]
            random_x_position = random.randint(0, WIN_SIZE - square_size)
            white_squares.append([random_x_position, 0, 5])

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Mausklick-Ereignis verarbeiten, wenn das Spiel vorbei ist
            mouse_pos = pygame.mouse.get_pos()
            if retry_rect.collidepoint(mouse_pos):
                # Nochmal spielen
                game_over = False
                black_squares.clear()
                x = 400
                y = 700
            elif quit_rect.collidepoint(mouse_pos):
                # Spiel beenden
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:  # Das Spiel läuft nur weiter, wenn es nicht vorbei ist
        if keys[pygame.K_RIGHT]:
            x += 5
        if keys[pygame.K_LEFT]:
            x -= 5


        # Überprüfen, ob das rote Rechteck mit einem schwarzen Rechteck kollidiert
        for square in black_squares:
            square[1] += square[2]  # Update y-coordinate using speed
            if y < square[1] + square_size and y + 50 > square[1] and x < square[0] + square_size and x + 50 > square[0]:
                game_over = True

        for square in white_squares:
            square[1] += square[2]  # Update y-coordinate using speed
            if y < square[1] + square_size and y + 50 > square[1] and x < square[0] + square_size and x + 50 > square[0]:
                points = points+1
                square[1] = square[1] + 200

    screen.fill((0, 255, 200))

    # Schwarze Quadrate aktualisieren und zeichnen
    for square in black_squares:
        pygame.draw.rect(screen, black, [square[0], square[1], square_size, square_size])

    for square in white_squares:
        pygame.draw.rect(screen, white, [square[0], square[1], square_size, square_size])

    # Spielerrechteck zeichnen
    pygame.draw.rect(screen, red, (x, y, 50, 50))

    if game_over:
        game_over_screen()

    # Text für die Punkte
    font = pygame.font.Font(None, 64)
    text_points = font.render(f"Deine Punkte {points} " , True, black)
    points_rect = text_points.get_rect(center=(200 , 50))
    screen.blit(text_points, points_rect)

    pygame.display.update()

pygame.quit()
