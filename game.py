import os
import pygame
from ship import Ship, SHIP_WIDTH, SHIP_HEIGHT

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


# Custom events
RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

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


def handle_bullets(red_ship, blue_ship):
    for bullet in red_ship.bullets:
        bullet.x -= BULLET_VELOCITY
        bounding_box = blue_ship.bounding_box
        if bounding_box.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_ship.remove_bullet(bullet)
        elif bullet.x < 0:
            red_ship.remove_bullet(bullet)
            
    for bullet in blue_ship.bullets:
        bullet.x += BULLET_VELOCITY
        bounding_box = red_ship.bounding_box
        if bounding_box.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_ship.remove_bullet(bullet)
        elif bullet.x > WIDTH:
            blue_ship.remove_bullet(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_ship.bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue_ship.x + SHIP_WIDTH, blue_ship.y + SHIP_HEIGHT // 2 - 2, 10, 5)
                    blue_ship.add_bullet(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_ship.bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red_ship.x, red_ship.y + SHIP_HEIGHT // 2 - 2, 10, 5)
                    red_ship.add_bullet(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_ship.health -= 1
                BULLET_IMPACT_SOUND.play()
            if event.type == BLUE_HIT:
                blue_ship.health -= 1
                BULLET_IMPACT_SOUND.play()
                
        
        winner_text = ""
        if red_ship.health <= 0:
            winner_text = "Blue wins!!!"
        
        if blue_ship.health <= 0:
            winner_text = "Red wins!!!"
            
        if winner_text != "":
            draw_winner(winner_text)
            break
                    
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red_ship)
        blue_handle_movement(keys_pressed, blue_ship)
        handle_bullets(red_ship, blue_ship)
        draw_window(red_ship, blue_ship)
    main()

if __name__ == "__main__":
    main()