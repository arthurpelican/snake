import pygame
import random as rd
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by Arthur")

TEXTS_FONT = pygame.font.SysFont("lucidaconsole", 80)
SCORE_FONT = pygame.font.SysFont("lucidasans", 40)
FPS = 60

LGREEN = (65, 232, 87)
DGREEN = (16, 102, 28)
RED = (200, 0, 0)
BROWN = (160, 100, 80)
DBLUE = (26, 60, 163)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
GOLD = (191, 143, 0)
WHITE = (255, 255, 255)

class Snake() :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.length = 1
        self.last = []
        self.x_vel = 100
        self.y_vel = 0

    def draw(self, win, head_color, body_color) :
        pygame.draw.circle(win, head_color, (self.x + 50, self.y + 50), 30)
        for i in range(len(self.last)) :
            if i % 2 == 0 :
                pygame.draw.circle(win, body_color, (self.last[i][0] + 50, self.last[i][1] + 45), 25)
            else :
                pygame.draw.circle(win, body_color, (self.last[i][0] + 50, self.last[i][1] + 55), 25)

class Apple() :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    
    def draw(self, win, color) :
        pygame.draw.circle(win, color, (self.x + 50, self.y + 50), 30)

def add_apple(apples, snake) :
    if len(snake.last) < 97 :
        positions = set()
        positions.add((snake.x, snake.y))
        for v in snake.last :
            positions.add(v)
        for v in apples :
            positions.add((v.x, v.y))
        x, y = rd.randrange(0, 10) * 100, rd.randrange(0, 10) * 100
        while (x, y) in positions :
            x = rd.randrange(0, 10) * 100
            y = rd.randrange(0, 10) * 100

        apples.append(Apple(x, y))

def snake_update(snake, apples) :
    adding = False
    eated = []
    for v in apples :
        if snake.x == v.x and snake.y == v.y :
            adding = True
            eated.append(v)
    for v in eated :
        apples.remove(v)
        add_apple(apples, snake)
    snake.last.append((snake.x, snake.y))
    if len(snake.last) > 0 and not adding:
        snake.last.pop(0)
    snake.x += snake.x_vel
    snake.y += snake.y_vel

def snake_controlling(snake, keys) :
    if keys[pygame.K_UP] : 
        snake.x_vel = 0
        snake.y_vel = -100
    elif keys[pygame.K_RIGHT] : 
        snake.x_vel = 100
        snake.y_vel = 0
    elif keys[pygame.K_DOWN] : 
        snake.x_vel = 0
        snake.y_vel = 100
    elif keys[pygame.K_LEFT] : 
        snake.x_vel = -100
        snake.y_vel = 0

def lose(win, snake, apples, score) :

    draw(win, snake, (BLACK, GREY), apples, score, True , False)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

def won(win, snake, apples, score) :

    draw(win, snake, (GOLD, GOLD), apples, score, False , True)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()

def draw(win, snake, snake_colors, apples, score,  lose = False, won = False) :
    
    # dallage
    pygame.draw.rect(win, LGREEN, (0, 0, WIDTH, HEIGHT))

    for i in range(0, WIDTH, 200) :
        for j in range(0, HEIGHT, 200) :
                pygame.draw.rect(win, DGREEN, (i, j, 100, 100))
    for i in range(100, WIDTH, 200) :
        for j in range(100, HEIGHT, 200) :
                pygame.draw.rect(win, DGREEN, (i, j, 100, 100))

    # elements
    for v in apples :
        v.draw(win, RED)
    head_color, body_color = snake_colors[0], snake_colors[1]
    snake.draw(win, head_color, body_color)
    
    if lose :
        losing_text = TEXTS_FONT.render("Game Over", 1, BLACK)
        win.blit(losing_text, (WIDTH // 2 - losing_text.get_width() // 2, HEIGHT // 2 - losing_text.get_height() // 2))
    
    if won :
        winning_text = TEXTS_FONT.render("You won !", 1, GOLD)
        win.blit(winning_text, (WIDTH // 2 - winning_text.get_width() // 2, HEIGHT // 2 - winning_text.get_height() // 2))

    score_text = SCORE_FONT.render(str(score), 1, BLACK)
    win.blit(score_text, (1, 1))

    pygame.display.update()

def main() :
    running = True
    clock = pygame.time.Clock()
    snake = Snake(400, 400)
    current_tick = 0

    score = 0

    apples = []
    for _ in range(3) :
        add_apple(apples, snake)

    while running :
        current_tick += 1
        if current_tick == 60 :
            current_tick = 0

        clock.tick(FPS)
        draw(WIN, snake, (BROWN, DBLUE), apples, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        keys = pygame.key.get_pressed()

        snake_controlling(snake, keys)

        if current_tick in {0, 20, 40} :
            snake_update(snake, apples)
            for v in snake.last :
                if v[0] == snake.x and v[1] == snake.y :
                    lose(WIN, snake, apples, score)
                    running = False
            score = len(snake.last)

        if snake.x > WIDTH or snake.x < 0 or snake.y < 0 or snake.y > HEIGHT :
            lose(WIN, snake, apples, score)
            running = False

        if score == 99 :
            won(WIN, snake, apples, score)

if __name__ == "__main__" :
    main()