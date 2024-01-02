# Hecho por Yael Franco T.
import pygame
from sys import exit
from random import randint

def display_score():
    c_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Tiempo: {c_time}', False, (0,0,0))
    score_rect = score_surf.get_rect(center = (640,100))
    screen.blit(score_surf, score_rect)
    return c_time
   
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 595:
                screen.blit(enemy1_surf, obstacle_rect)
            else:
                screen.blit(enemy2_surf, obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -70]
            
        return obstacle_list
    else: return[]

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            # Verifica si el centro del jugador está dentro del obstáculo
            if obstacle_rect.left < player.centerx < obstacle_rect.right and obstacle_rect.top < player.centery < obstacle_rect.bottom:
                return False  

    return True

def player_animation():
    global player_surf, player_index, player_rect, player_gravity

    if player_rect.bottom < 600:  # Si el jugador está en el aire
        player_surf = player_jump
    elif moving_left or moving_right:  # Si el jugador se mueve hacia la izquierda o derecha
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    else:  # Si el jugador no se está moviendo
        player_surf = player_standing

    # Si el jugador está mirando hacia la izquierda
    if moving_left:
        player_surf = pygame.transform.flip(player_surf, True, False)
        
    # Ajusta el tamaño de la imagen según la animación
    player_surf = pygame.transform.scale(player_surf, (94, 96))
    
    return player_surf
    
pygame.init()

size = 1280,720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('MY GAME')
clock = pygame.time.Clock()
font = pygame.font.Font('dogica.ttf',30)
game_active = False
moving_left = False
moving_right = False
start_time = 0
score = 0

#Imagenes
background = pygame.image.load('exterior-parallaxBG1.png').convert_alpha()
background = pygame.transform.scale(background, (1280, 1000))

background_complement = pygame.image.load('exterior-parallaxBG2-removebg-preview.png').convert_alpha()
background_complement = pygame.transform.scale(background_complement, (900, 700))

ground = pygame.image.load('ground.png').convert_alpha()
ground = pygame.transform.scale(ground, (640, 360))
ground2 = pygame.image.load('ground.png').convert_alpha()
ground2 = pygame.transform.scale(ground2, (640, 360))


enemy1_walk1 = pygame.image.load('wolfwalk1.png').convert_alpha()
enemy1_walk1 = pygame.transform.scale(enemy1_walk1, (96, 50))
enemy1_walk2 = pygame.image.load('wolfwalk2.png').convert_alpha()
enemy1_walk2 = pygame.transform.scale(enemy1_walk2, (96, 50))
enemy1_walk = [enemy1_walk1, enemy1_walk2]
enemy1_index = 0
enemy1_surf = enemy1_walk[enemy1_index]

enemy2_fly1 = pygame.image.load('bat-removebg-preview.png').convert_alpha()
enemy2_fly1 = pygame.transform.scale(enemy2_fly1,(79,79))
enemy2_fly2 = pygame.image.load('bat2-removebg-preview.png').convert_alpha()
enemy2_fly2 = pygame.transform.scale(enemy2_fly2,(79,79))
enemy2_fly = [enemy2_fly1,enemy2_fly2]
enemy2_index = 0
enemy2_surf = enemy2_fly[enemy2_index]

obstacle_rect_list = []

player_standing = pygame.image.load('elisa-spritesheetNormal-removebg-preview.png').convert_alpha()
player_walk1 = pygame.image.load('playerwalk1-removebg-preview.png').convert_alpha()
player_walk2 = pygame.image.load('playerwalk2-removebg-preview.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_surf = [player_index]
player_jump = pygame.image.load('playerjump1-removebg-preview.png').convert_alpha()

#dimensiones de imagen
player_standing = pygame.transform.scale(player_standing, (94, 96))
player_walk1 = pygame.transform.scale(player_walk1, (94, 96))
player_walk2 = pygame.transform.scale(player_walk2, (94, 96))
player_jump = pygame.transform.scale(player_jump, (94, 96))

player_rect = player_standing.get_rect(midbottom = (70,600))
player_gravity = 0

#Textos
game_message = font.render('Presiona enter para jugar', False, 'White')
game_message_rect = game_message.get_rect(center = (640,340))

score_message = font.render(f'Tú tiempo fue de: {score} segundos', False, 'White')
score_message_rect = score_message.get_rect(center = (640, 400))
postgame_message = font.render('Presiona enter para volver a jugar', False, 'White')
postgame_message_rect = postgame_message.get_rect(center = (640, 280))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

enemy1_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy1_animation_timer, 250)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 600: 
                    player_gravity = -18
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_LSHIFT and player_rect.bottom >= 600:    
                    player_gravity = -18
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_a:
                    moving_left = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)
                
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(enemy1_walk1.get_rect(bottomright = (randint(1350,1650),595)))
                else:
                    obstacle_rect_list.append(enemy2_fly1.get_rect(bottomright = (randint(1350,1650),505)))
            
           # Timer animación enemigo 1
            if event.type == enemy1_animation_timer:
                enemy1_index = (enemy1_index + 1) % 2  # Cambiar entre 0 y 1
                enemy1_surf = enemy1_walk[enemy1_index]

            # Timer animación enemigo 2
            if event.type == enemy2_animation_timer:
                enemy2_index = (enemy2_index + 1) % 2  # Cambiar entre 0 y 1
                enemy2_surf = enemy2_fly[enemy2_index]
            
                
    if game_active:
        screen.blit(background,(0,-250))
        screen.blit(background_complement,(200, -55))
        screen.blit(ground,(0,595))
        screen.blit(ground2,(640,595))
        
        #Limites de posición del jugador
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 600: 
            player_rect.bottom = 600
        if player_rect.right > 1300: 
            player_rect.right = 1300
        if player_rect.right < 70: 
            player_rect.right = 70
        if moving_left:
            player_rect.x -= 5
        if moving_right:
            player_rect.x += 5
        player_surf = player_animation()
        screen.blit(player_surf, player_rect)
       
        score = display_score()
        
        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
       
        
        game_active = collisions(player_rect,obstacle_rect_list)
        
    else:
        screen.fill('Black')
        obstacle_rect_list.clear()
        player_rect.midbottom = (70,595)
        player_gravity = 0
        
        score_message = font.render(f'Tú tiempo fue de: {score} segundos', False, 'White')
        score_message_rect = score_message.get_rect(center = (640, 400))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(postgame_message, postgame_message_rect)
        
    pygame.display.update()
    clock.tick(60)
