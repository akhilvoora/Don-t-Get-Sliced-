import pygame
import random
from sys import exit
import math

#change of speed for the knives as game progresses
changeofspeed = 5

def obstacle_movement(obstacle_list):
    global changeofspeed
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            changeofspeed += 0.00005
            obstacle_rect.y -= changeofspeed

            if obstacle_rect.x == 40:
                screen.blit(butcher_knife_surf,obstacle_rect)
            elif obstacle_rect.x == 520:
                screen.blit(knife_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.y > -100]
        
        return obstacle_list 
    else: return []

def collisions(dinosaur,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            global changeofspeed
            if pygame.Rect.colliderect(dinosaur_rect_2, obstacle_rect):
                score_present = current_time
                obstacle_rect.y = random.randint(750,900)
                changeofspeed = 5
                return False
    return True 

#pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Don't Get Sliced!")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf')
game_active = False
start_time = 0

# play again screen
dinosaur_image = pygame.image.load('dinosaur/dinosaur.png')
dinosaur_image_enlarged = pygame.transform.scale(dinosaur_image, (245,301))
dinosaur_image_rect = dinosaur_image_enlarged.get_rect(center = (400,350))

text_1 = test_font.render("Don't Get Sliced!", False, 'Black')
text_1_surf = pygame.transform.scale_by(text_1, (9,9))
text_1_rect = text_1_surf.get_rect(center = (400,100))
text_2 = test_font.render('Press Any Key To Start', False, 'Black')
text_2_surf = pygame.transform.scale_by(text_2, (6,6))
text_2_rect = text_2_surf.get_rect(center = (400,600))

#score
score_present = 0

#background stuff setup
background = pygame.image.load('assets/metalbackground2.png')
background_surf = pygame.transform.scale(background, (1200,800))
side_wall_1 = pygame.image.load('assets/metalwall2.png')
side_wall_1_surf = pygame.transform.scale(side_wall_1, (120,700))
side_wall_2 = pygame.image.load('assets/metalwall2.png')
side_wall_2_flipped = pygame.transform.flip(side_wall_2, True, False)
side_wall_2_surf = pygame.transform.scale(side_wall_2_flipped, (120,700))

# butcher knife setup
butcher_knife = pygame.image.load('weapons/butcherknife.png')
butcher_knife_surf = pygame.transform.scale(butcher_knife, (228,80))
butcher_knife_rect = butcher_knife_surf.get_rect(topleft=(40,170))
butcher_knife_y_pos = 570
butcher_knife_rect_speed_inc = 2

#knife setup
knife = pygame.image.load('weapons/knife.png').convert_alpha()
knife_boy = pygame.transform.scale(knife, (220,40)).convert_alpha()
knife_surf = pygame.transform.flip(knife_boy, True, False)
knife_rect = knife_surf.get_rect(topleft=(520,600))
knife_y_pos = 570
knife_rect_speed_inc = 2

# list for better enemy logic
obstacle_rect_list = []

#dinosaur setup
dinosaur = pygame.image.load('dinosaur/dinosaur.png')
dinosaur_enlarged = pygame.transform.scale(dinosaur, (87.5,107.5))
dinosaur_rotation = 270
dinosaur_flipped = False
dinosaur_rotated = pygame.transform.rotate(dinosaur_enlarged, dinosaur_rotation)
dinosaur_rect = dinosaur_rotated.get_rect(topleft=(500,-400))
dinosaur_x = 120
dinosaur_y = 300
dinosaur_direction = 1
dinosaur_position = "left"

#energy cube setup
energycube = pygame.image.load('energycube/energycube.png')
energycube_enlarged = pygame.transform.scale(energycube,(64,64))
energycube_rect = energycube_enlarged.get_rect(topleft = (120,350))
energy_y = 500

#collision for energy cube (boolean flag)
collision_detected = False

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

#while loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dinosaur_position == "left":
                        dinosaur_x = 570
                        dinosaur_position = "right"
                    else:
                        dinosaur_x = 120
                        dinosaur_position = "left"
                    dinosaur_rotation = 270
                    dinosaur_flipped = not dinosaur_flipped
        else: 
            # end screen -> starting the game
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1500)
        if event.type == obstacle_timer and game_active == True:
            # append to list using if
            if random.randint(0,1):
                obstacle_rect_list.append(butcher_knife_surf.get_rect(topleft=(40,random.randint(750,900))))
            else:
                obstacle_rect_list.append(knife_surf.get_rect(topleft=(520,random.randint(750,900))))

    #game active
    if game_active:
        #background and stuff
        screen.blit(background, (-400,-50))
        screen.blit(side_wall_1_surf, (0,0))
        screen.blit(side_wall_2_surf, (680,0))

        # dinosaur stuff
        dinosaur_rect = pygame.transform.rotate(dinosaur_enlarged, dinosaur_rotation)
        dinosaur_image_flipped = pygame.transform.flip(dinosaur_rect, dinosaur_flipped, False)
        dinosaur_rect_2 = dinosaur_image_flipped.get_rect(topleft = (dinosaur_x, dinosaur_y))
        screen.blit(dinosaur_image_flipped, dinosaur_rect_2)

        # knives movement
        osbtacle_rect_list = obstacle_movement(obstacle_rect_list)

        # score
        current_time = int(pygame.time.get_ticks() / 1500) - start_time
        score_surf = test_font.render(f'{current_time}', False, (255,255,255))
        score_enlarged = pygame.transform.scale_by(score_surf, (5,5))
        score_rect = score_enlarged.get_rect(center =  (400,50))
        screen.blit(score_enlarged,score_rect)

        # energy cube spawning and function
        if current_time % 5 == 0 and current_time != 0:
            energycube_rect_2 = energycube_enlarged.get_rect(topleft = (120,350))
            screen.blit(energycube_enlarged,energycube_rect_2)
            energycuberandom = random.randint(0,7)
            energycubelist = [1,1,1,2,2,3,3,4]
            energycubevalue = energycubelist[energycuberandom]
            energycollide = pygame.Rect.colliderect(dinosaur_rect_2, energycube_rect_2)
            if energycollide:
                if not collision_detected:
                    collision_detected = True
                    energycubevalue = energycubelist[energycuberandom]
                    if energycubevalue == 1:
                        print('1')
                        current_time = current_time * 1.25
                    elif energycubevalue == 2:
                        print('2')
                        current_time = current_time * 1.5
                    elif energycubevalue == 3:
                        print('3')
                        current_time = current_time * 0.75
                    elif energycubevalue == 4:
                        print('4')
                        current_time = current_time * 0.5
                    else:
                        print('error')
            else:
                collision_detected = False
        
        # score
        current_time = int(pygame.time.get_ticks() / 1500) - start_time
        score_surf = test_font.render(f'{current_time}', False, (255,255,255))
        score_enlarged = pygame.transform.scale_by(score_surf, (5,5))
        score_rect = score_enlarged.get_rect(center =  (400,50))
        screen.blit(score_enlarged,score_rect)

        #collision
        game_active = collisions(dinosaur_rect_2,obstacle_rect_list)

    else:
        # end screen
        timefortext = pygame.time.get_ticks() / 4 % 1000
        yfortext_dino = math.sin(timefortext/60) * 40 + 175
        yfortext_1 = math.sin(timefortext/60) * 40 + 50
        yfortext_2 = math.sin(timefortext/60) * 40 + 550
        yfortext_score = math.sin(timefortext/60) * 40 + 110
        screen.blit(background,(-400,-50))
        screen.blit(dinosaur_image_enlarged,(285,yfortext_dino))
        screen.blit(text_1_surf, (100,yfortext_1))
        screen.blit(text_2_surf, (120,yfortext_2))
        butcher_knife_rect_speed_inc = 2
        knife_rect_speed_inc = 2
        energy_y = 500
        
    #mouse_pos = pygame.mouse.get_pos()
    #print(mouse_pos)
    pygame.display.update()
    clock.tick(60)  # limits FPS to 60