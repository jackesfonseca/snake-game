import pygame, random
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
pygame.init()

# Cria tela
screen = pygame.display.set_mode((600, 600))

# Título e ícone
pygame.display.set_caption('Snake')
icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(icon)

# Fonte
font_message = pygame.font.SysFont('arialblack', 20, bold=False, italic=False)
font_score = pygame.font.SysFont('arial', 20, bold=True, italic=False)
#print(pygame.font.get_fonts())

# Música de fundo
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

my_direction = LEFT

# Limitar o FPS
clock = pygame.time.Clock()

# Gerar maçã dentro do grid
def on_grid_rand():
    x = random.randint(0, 590)
    y = random.randint(30, 590)
    return x//10*10, y//10*10

# Cabeça da cobra e a maçã
def collision(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1]

def out_of_bounds(head):
    if (head[0] <= 0 or head[0] >= 600) or (head[1] <= 0 or head[1] >= 600):
        return True

def suicide(body):
    for i in range(len(body)-1, 0, -1):
        if body[0] == (body[i][0], body[i][1]):
            return True

def score_game_text():
    message = 'Pontuação: '
    score_message = f'{score}'
    formated_message = font_message.render(message, True, (255, 255, 255))
    formated_score_message = font_score.render(score_message, True, (255, 255, 45))
    screen.blit(formated_message, (0, 0))
    screen.blit(formated_score_message, (140, 5))

def over_game_text():
    over_message = "Você perdeu!"
    formated_over_message = font_message.render(over_message, True, (255, 255, 255))
    screen.blit(formated_over_message, (200, 200))


# A cobra é uma lista de segmentos, onde cada segmento é representado por uma tupla (valor de x e y onde está posicionado o quadrado)
snake = [(200, 200), (200, 210), (200, 220)]
snake_skin = pygame.Surface((10, 10))
# Cores RGB
snake_skin.fill((0, 128, 128))

# 590 é a última posição que s epode posicionar algo sem sair da tela
apple_pos = on_grid_rand()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

# Não pode comer
poison_pos = on_grid_rand()
poison = pygame.Surface((10, 10))
poison.fill((255, 255, 255))

speed = 15
score = 0
control_score = 0
running = True

# Loop do jogo
while running:
    clock.tick(speed)

    # Aumentar a velocidade
    if (score-control_score) >= 5:
        speed += 5
        control_score = score

    # Evento de fechar a tela
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            # pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT

    # Testando colisão com a maçã
    if collision(snake[0], apple_pos):
        apple_pos = on_grid_rand()
        poison_pos = on_grid_rand()
        # Nova posição para a cobra
        # OBS.: está em 0 pois ela irá tomar a posição anterior
        coin_sound = pygame.mixer.Sound('coin.wav')
        coin_sound.play()
        snake.append((0, 0))
        score += 1

    # Testando colisão com o veneno
    if collision(snake[0], poison_pos):
#        loser_sound = pygame.mixer.Sound('lose.wav')
#        loser_sound.play()
        over_game_text()

        running = 0

    # Saiu do limite da tela
    if out_of_bounds(snake[0]):
#        loser_sound = pygame.mixer.Sound('lose.wav')
#        loser_sound.play()
        over_game_text()

        running = 0


    # Suicídio
    if suicide(snake):
#        loser_sound = pygame.mixer.Sound('lose.wav')
#        loser_sound.play()
        over_game_text()

        running = 0

    # Movimentar o corpo da cobra (OBS.: Cada posição da cobra ocupará a posição anterior)
    # Começa pelo rabo
    for i in range(len(snake) - 1, 0, -1):  # O 0 não é incluso no range
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    # Movimentar a cabeça da cobra dependendo da direção
    if my_direction == UP:
        # A cabeça da cobre precisa receber uma nova tupla
        snake[0] = (snake[0][0], snake[0][1]-10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1]+10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0]+10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0]-10, snake[0][1])


    # Limpar a tela, pois a mesma será atualizada várias vezes cada vez a cada segundo
    screen.fill((0, 0, 0))

    # Mostrar a pontuação
    score_game_text()

    # Posicionar o objeto na tela
    screen.blit(poison, poison_pos)
    screen.blit(apple, apple_pos)
    # Plotar a cobra na tela
    for pos in snake:
        # O primeiro parâmetro é uma superfície, um desenho ou um sprite e a posição onde se quer plotar
        screen.blit(snake_skin, pos)

    pygame.display.update()