import os
import pygame
from ship import Ship

pygame.font.init()
pygame.mixer.init()

# Screen Specifications
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Game Settings
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SHIP_WIDTH = 55
SHIP_HEIGHT = 40

# Assets
BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "Ship_1.png"))
BLUE_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "Ship_2.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH, HEIGHT))


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

# Border between the ships
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# Load Sounds
BULLET_IMPACT_SOUND = pygame.mixer.Sound("impact sound.wav")
BULLET_FIRE_SOUND = pygame.mixer.Sound("laser shot.wav")
START_SOUND = pygame.mixer.Sound('start sound.wav')

# Load Fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)


# Draw window with all its elements
def draw_window(red_ship, blue_ship):
    # draw background
    WIN.blit(SPACE, (0,0))
    
    # draw border between the ships
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    # draw health of players
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_ship.health), 1, WHITE
    )
    blue_health_text = HEALTH_FONT.render(
        "Health: " + str(blue_ship.health), 1, WHITE
    )
    
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10,10))
    
    # draw players
    WIN.blit(RED_SPACESHIP, (red_ship.x, red_ship.y))
    WIN.blit(BLUE_SPACESHIP, (blue_ship.x, blue_ship.y))
    
    # draw bullets    
    for bullet in red_ship.bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in blue_ship.bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
        
    # update
    pygame.display.update()


def red_handle_movement(keys_pressed, red_ship):
    if keys_pressed[pygame.K_LEFT] and red_ship.x - VELOCITY > BORDER.x + BORDER.width:
        red_ship.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red_ship.x + VELOCITY + SHIP_WIDTH < WIDTH:
        red_ship.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red_ship.y - VELOCITY > 0:
        red_ship.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red_ship.y + VELOCITY + SHIP_HEIGHT < HEIGHT - 15:
        red_ship.y += VELOCITY
        

def blue_handle_movement(keys_pressed, blue_ship):
    if keys_pressed[pygame.K_a] and blue_ship.x - VELOCITY > 0:
        blue_ship.x -= VELOCITY
    if keys_pressed[pygame.K_d] and blue_ship.x + VELOCITY + SHIP_WIDTH < BORDER.x:
        blue_ship.x += VELOCITY
    if keys_pressed[pygame.K_w] and blue_ship.y - VELOCITY > 0:
        blue_ship.y -= VELOCITY
    if keys_pressed[pygame.K_s] and blue_ship.y + VELOCITY + SHIP_HEIGHT < HEIGHT - 15:
        blue_ship.y += VELOCITY

def main():
    red_ship = Ship(x=700, y=300, health=6, bullets=[])
    blue_ship = Ship(x=100, y=300, health=6, bullets=[])
    START_SOUND.play()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red_ship)
        blue_handle_movement(keys_pressed, blue_ship)
        draw_window(red_ship, blue_ship)


if __name__ == "__main__":
    main()