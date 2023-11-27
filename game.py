import pygame
import random
from sys import exit
import time

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
                butcher_knife_rect.top = 170
                knife_rect.top = 600
                start_time = int(pygame.time.get_ticks() / 1500)

    #game active
    if game_active:
        #background and stuff
        screen.blit(background, (-400,-50))
        screen.blit(side_wall_1_surf, (0,0))
        screen.blit(side_wall_2_surf, (680,0))

        #knives blitting
        butcher_knife_rect.y -= butcher_knife_rect_speed_inc
        butcher_knife_rect_speed_inc +=0.0005
        if butcher_knife_rect.y <= 0:
            butcher_knife_rect.y = 700
        screen.blit(butcher_knife_surf, butcher_knife_rect)

        knife_rect.y -= knife_rect_speed_inc
        knife_rect_speed_inc +=0.0005
        if knife_rect.y <= 0:
            knife_rect.y = 700
        screen.blit(knife_surf, knife_rect)

        #dinosaur stuff
        dinosaur_rect = pygame.transform.rotate(dinosaur_enlarged, dinosaur_rotation)
        dinosaur_image_flipped = pygame.transform.flip(dinosaur_rect, dinosaur_flipped, False)
        dinosaur_rect_2 = dinosaur_image_flipped.get_rect(topleft = (dinosaur_x, dinosaur_y))
        screen.blit(dinosaur_image_flipped, dinosaur_rect_2)

        #score
        current_time = int(pygame.time.get_ticks() / 1500) - start_time
        score_surf = test_font.render(f'{current_time}', False, (255,255,255))
        score_enlarged = pygame.transform.scale_by(score_surf, (5,5))
        score_rect = score_enlarged.get_rect(center =  (400,50))
        screen.blit(score_enlarged,score_rect)

        #energy cube spawning and function
        if current_time % 10 == 0 and current_time != 0:
            energycube_rect_2 = energycube_enlarged.get_rect(topleft = (120,350))
            screen.blit(energycube_enlarged,energycube_rect_2)
            energycuberandom = random.randint(0,5)
            energycubelist = [1,1,2,2,3,4]
            energycubevalue = energycubelist[energycuberandom]
            energycollide = pygame.Rect.colliderect(dinosaur_rect_2, energycube_rect_2)
            if energycollide:
                if not collision_detected:
                    collision_detected = True
                    energycubevalue = energycubelist[energycuberandom]
                    if energycubevalue == 1:
                        print('1')
                    elif energycubevalue == 2:
                        print('2')
                    elif energycubevalue == 3:
                        print('3')
                    elif energycubevalue == 4:
                        print('4')
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

        #collision with knives
        collidewithknife = pygame.Rect.colliderect(dinosaur_rect_2, butcher_knife_rect) or pygame.Rect.colliderect(dinosaur_rect_2, knife_rect)
        if collidewithknife:
            
            score_present = current_time
            game_active = False
    else:
        # end screen
        screen.blit(background,(-400,-50))
        screen.blit(dinosaur_image_enlarged,dinosaur_image_rect)
        screen.blit(text_1_surf, text_1_rect)
        screen.blit(text_2_surf, text_2_rect)
        score_present_surf = test_font.render(f"Score: {score_present}", False, "Black")
        score_present_s = pygame.transform.scale_by(score_present_surf, (5,5))
        score_present_rect = score_present_s.get_rect(center = (400,150))
        screen.blit(score_present_s, score_present_rect)
        butcher_knife_rect_speed_inc = 2
        knife_rect_speed_inc = 2
        energy_y = 500
        
    #mouse_pos = pygame.mouse.get_pos()
    #print(mouse_pos)
    pygame.display.update()
    clock.tick(60)  # limits FPS to 60