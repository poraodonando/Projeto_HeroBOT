import pgzrun
import random
from pgzhelper import *

####################
# Variáveis
####################
velocity = 1 # velocidade que o zumbi se move quando nas direções cima/baixo
gravity = 0.5 # A gravidade vai mudar a velocidade
jump = 2
score = 0
nest_timeout = 0 #esse contador garante que os espinhos apareçam no jogo, mas nao todos de uam vez
game_over = False
deathsound = False
lives = 5

### Musica de fundo
music.play('mix_2')

#Cores
black = (0,0,0)
brown = (71,34,18)
red = (255,0,0)
white = (255,255,255)
blue = (0,0,255)


####################
# Objetos em cena
####################

##### FUNDO

bg = Actor('background')
bg.x = 400
bg.y = 300






# Dimensões da Janela (em pixels)

WIDTH = 800
HEIGHT = 600


####################
# CHARACTERS
####################

##### HEROBOT

robot = Actor('robot/walk_0')
robot.x = 400
robot.y = 450

robot.images = []
for i in range(0,6):
    robot.images.append(f'robot/walk_{i}')


##### BAD BUG

badbug = Actor('bug/badbug_0')
badbug.x = random.randint(900,5000)
badbug.y = random.randint(250,350)
badbug.scale = 0.15

badbug.images = []
for i in range(0,6):
    badbug.images.append(f'bug/badbug_{i}')


##### NEST OF SNAKES

snake = Actor('snake/snake_0')
snake.x = 900
snake.y = 480
snake.scale = 0.3


snake.images = []
for i in range(0,5):
    snake.images.append(f'snake/snake_{i}')


#nest  = []

##### BOMBS

bomb = Actor('bomb')
bomb.x = random.randint(20,780)
bomb.y = 0

##### SKULLS

skull = Actor('skull')
skull.x = random.randint(20,780)
skull.y = 0

##### PYTHON POINTS

py_points = Actor('py_points')
py_points.x = random.randint(20,780)
py_points.y = 0


##### PYTHON GOLDS

py_golds = Actor('py_golds')
py_golds.x = random.randint(20,780)
py_golds.y = 0

##### CONTROL LIVES

contr_lives = Actor('contr_lives')
contr_lives.x = random.randint(20,780)
contr_lives.y = 0



####################
# Função Atualização
####################

def update():

###VARIAVEIS GLOBAIS
    global velocity, jump, score, nest_timeout, game_over,deathsound, lives

    if(keyboard.left):
        robot.animate()
        #sounds.footstep_grass.play()
        velocity += 1
        robot.x -= 3 + score/20
        robot.flip_x = True
        if robot.x < 20:
            robot.x = 20

    if(keyboard.right):
        robot.animate()
        #sounds.footstep_grass.play()
        velocity += 1
        robot.x += 3 + score/20
        robot.flip_x = False
        if robot.x >780:
            robot.x = 780

    if(keyboard.space and jump >= 1):
        robot.y -= 25
        sounds.jump.play()
    robot.y += velocity

    velocity += gravity


    if robot.y > 450:
        velocity = 1
        robot.y = 450

##### BADBUG ANIMATION

    if score > 50: # define o momento que o badbug irá aparece de acordo com o score

        badbug.animate()
        badbug.scale = .15
        badbug.x -= 1 + score/100 # define o aumento de velocidade em relação ao score
        badbug.flip_x = True
        if badbug.x <  -5:
            badbug.x = random.randint(900,2000)
            badbug.y = random.randint(100,500)



##### Quando o robot colide com o badbug

    if badbug.colliderect(robot):
        sounds.splat.play() # som.nome_arquivo_ação()

        #reseta a posição do badbug
        #sounds.insect.play()
        badbug.x =  random.randint(900,3000)
        badbug.y = random.randint(0,500)
        #score -= 5
        lives -= 1

#####SNAKES

    if score >300 : # define o momento que a cobra irá aparecer na cena

        snake.animate()
        snake.scale = 0.3
        snake.x -= 0.5 + score/150 # define o aumento de velocidade em relação ao score

        if snake.x <  -50:
            snake.x = random.randint(900,2000)
            snake.y = 480






#### COLISÃO ENTRE O ROBOT E SNAKE


    if snake.colliderect(robot):
        sounds.snake.play()
        snake.x = random.randint(900,5000)
        snake.y = 480
        score -= 5
        lives = lives - 1


##### BOMBS


    #move down the page
    bomb.y += .5 + score/50

    # Reset the bomb at the top of the page



    if bomb.y > 530:
        bomb.x = random.randint(20, 780)
        bomb.y = 0;

    #Bomb collision with the robot

    if bomb.colliderect(robot):
        sounds.explosion.play()
        bomb.x = random.randint(20, 780)
        bomb.y = 0
        score -= 1



##### SKULLS

    #move down the page
    skull.y += 1  + score/50

    # Reset the skull at the top of the page

    if score > 200: # define o momento que a caveira vai entrar

        if skull.y > 530:
            skull.x = random.randint(20, 780)
            skull.y = -1000

    #skull collision with the ship

    if skull.colliderect(robot):
        sounds.lose.play()
        skull.x = random.randint(20, 780)
        skull.y = -1000
        lives -= 1
        #score -= 10



##### PYTHON POINTS

#move down the page
    py_points.y += 2 + score/100 #define a velocidade que cai as coins

    # Reset the Python points at the top of the page

    if py_points.y > 530:
        py_points.x = random.randint(20, 780)
        py_points.y = 0;

    # Python points  collision with the robot

    if py_points.colliderect(robot):
        sounds.coin.play()
        py_points.x = random.randint(20, 780)
        py_points.y = 0
        score += 2

##### PYTHON GOLDS

#move down the page
    py_golds.y += 3

    # Reset the Python points at the top of the page

    if score >120: #Define o momento que a python gold vai entrar

        if py_golds.y > 530:
            py_golds.x = random.randint(20, 780)
            py_golds.y = 0;

    # Python GOlds collision with the robot

    if py_golds.colliderect(robot):
        sounds.super_coin.play()
        py_golds.x = random.randint(20, 780)
        py_golds.y = -1000
        score += 5

##### CONTROL LIVES

#move down the page
    contr_lives.y += 7

    # Reset the Python points at the top of the page


    if score > 250:

        if contr_lives.y > 530:
            contr_lives.x = random.randint(20, 780)
            contr_lives.y = -5000;

    # Python GOlds collision with the robot

    if contr_lives.colliderect(robot):
        sounds.lives.play()
        contr_lives.x = random.randint(20, 780)
        contr_lives.y = -9000
        lives = lives +1


##### GAME OVER


    if lives == 0:
        game_over = True
        py_points.y = 0
        bomb.y = 0
        skull.y = 0
        py_golds.y = 0
        badbug.y = 0
        if deathsound == False:
            sounds.epicover.play()
        deathsound = True

####################
# Função Desenhar
####################

def draw():
    #screen.draw.filled_rect(Rect(0, 0, 800, 500),(black)) #céu
    #screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #Solo
    bg.draw()
    robot.draw()
    badbug.draw()

    if game_over:
        screen.draw.text('Game Over', centerx = 380, centery = 150, color = (red),fontname= 'creepster', fontsize = 80 )
        screen.draw.text('Score: ' + str(score), centerx = 300, centery = 300, color = (black),fontname= 'creepster', fontsize = 80 )
        music.stop()
    else:
        robot.draw()
        badbug.draw()
        bomb.draw()


        if score > 30:
            py_golds.draw()
            contr_lives.draw()
            skull.draw()
            snake.draw()

        py_points.draw()

        screen.draw.text('Score: ' + str(score),(20,20),color = (red),fontname='creepster',
            fontsize = 30)
        screen.draw.text( 'Lives: ' + str(lives),(650,20), color = red, fontname ='creepster', fontsize = 30  )




pgzrun.go()


