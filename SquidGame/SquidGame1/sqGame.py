import pygame, sys, random
from random import randrange


pygame.init()
screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)
small_font = pygame.font.Font('04B_19.ttf',10)

bg_surface = pygame.image.load('bk5.png').convert()
man_movement = 0.0
man_status = 0 # 0 stand 1 run
move_speed = 1.0
move_timer = 10

otherman_status = 0
score = 0

man_run1 = pygame.image.load('man/man_1.png').convert_alpha()
man_run2 = pygame.image.load('man/man_2.png').convert_alpha()
man_run3 = pygame.image.load('man/man_3.png').convert_alpha()
man_run4 = pygame.image.load('man/man_4.png').convert_alpha()
man_run5 = pygame.image.load('man/man_5.png').convert_alpha()
man_run6 = pygame.image.load('man/man_6.png').convert_alpha()
man_run7 = pygame.image.load('man/man_7.png').convert_alpha()



pman_surface1 = pygame.image.load('man/man_1.png').convert_alpha()
pman_surface2 = pygame.image.load('man/man_2.png').convert_alpha()
pman_surface3 = pygame.image.load('man/man_3.png').convert_alpha()
pman_surface4 = pygame.image.load('man/man_4.png').convert_alpha()
pman_surface5 = pygame.image.load('man/man_5.png').convert_alpha()
pman_surface6 = pygame.image.load('man/man_6.png').convert_alpha()
pman_surface7 = pygame.image.load('man/man_7.png').convert_alpha()
pman_frames = [man_run1,man_run2,man_run3,man_run4,man_run5,man_run6,man_run7]
pman_index = 0
pmanFLAP = pygame.USEREVENT + 4
pygame.time.set_timer(pmanFLAP,20)


pman_list = []

biggirl_run0 = pygame.image.load('girl/girl_0.png').convert_alpha()
biggirl_run1 = pygame.image.load('girl/girl_1.png').convert_alpha()
biggirl_run2 = pygame.image.load('girl/girl_2.png').convert_alpha()
biggirl_run3 = pygame.image.load('girl/girl_3.png').convert_alpha()
biggirl_run4 = pygame.image.load('girl/girl_4.png').convert_alpha()
biggirl_run5 = pygame.image.load('girl/girl_5.png').convert_alpha()
biggirl_run6 = pygame.image.load('girl/girl_6.png').convert_alpha()



man_frames = [man_run1,man_run2,man_run3,man_run4,man_run5,man_run6,man_run7]
man_index = 0
man_surface = man_frames[0]
man_rect = man_surface.get_rect(center = (100,700))
manFLAP = pygame.USEREVENT + 1
pos_x = 100
pos_y = 700
pygame.time.set_timer(manFLAP,20)
light_status = 0


biggirl_frames = [biggirl_run6,biggirl_run5,biggirl_run4,biggirl_run3,biggirl_run2,
biggirl_run1,biggirl_run0,biggirl_run0,biggirl_run0,biggirl_run1,
biggirl_run2,biggirl_run3,biggirl_run4,biggirl_run5,biggirl_run6]
biggirl_index = 0
biggirl_surface = biggirl_frames[0]
biggirl_rect = biggirl_surface.get_rect(center = (850,100))
biggirlFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(biggirlFLAP,200)

gameover_status = 0

score_sound_countdown = 100

def biggirl_animation():
	new_man = biggirl_frames[biggirl_index]
	new_man_rect = new_man.get_rect(center = (biggirl_rect.centerx,biggirl_rect.centery))
	return new_man,new_man_rect

def man_animation():
	new_man = man_frames[man_index]
	new_man_rect = new_man.get_rect(center = (man_rect.centerx,man_rect.centery))
	return new_man,new_man_rect

def pman_animation():
	new_pman = pman_frames[pman_index]
	return new_pman

def pman_stand():
	new_pman = pman_frames[0]
	return new_pman

def man_stand():
	new_man = man_frames[0]
	new_man_rect = new_man.get_rect(center = (man_rect.centerx,man_rect.centery))
	return new_man,new_man_rect


def redlight_display(game_state):
    if (light_status ==1):
        score_surface = game_font.render("RED LIGHT",True,(255,0,0))
    else:
        score_surface = game_font.render("GREEN LIGHT",True,(0,255,0)) 

    score_rect = score_surface.get_rect(center = (150,50))
    screen.blit(score_surface,score_rect)


def gameover_display(gameover_status):
    if (gameover_status ==1 ):
        gameover_surface = game_font.render("GAME OVER",True,(255,0,0))
        gameover_rect = gameover_surface.get_rect(center = (1024/2,768/2))
        screen.blit(gameover_surface,gameover_rect)

        gameover_surface = game_font.render("Press Space to restart",True,(255,0,0))
        gameover_rect = gameover_surface.get_rect(center = (1024/2,768/2+50))
        screen.blit(gameover_surface,gameover_rect)

    if (gameover_status ==2 ):
        gameover_surface = game_font.render("YOU WIN",True,(255,0,0))
        gameover_rect = gameover_surface.get_rect(center = (1024/2,768/2))
        screen.blit(gameover_surface,gameover_rect)

        gameover_surface = game_font.render("Press Space to restart",True,(255,0,0))
        gameover_rect = gameover_surface.get_rect(center = (1024/2,768/2+50))
        screen.blit(gameover_surface,gameover_rect)





def move_pmans(pmans):
    for pman in pmans:
        if otherman_status ==1 :
            pman.centerx += 2
            pman.centery -= 1

        if pman.centery < -10:
            pmans.remove(pman)
    return pmans
            


def create_pman():
    if gameover_status ==0 :
        bottom_pman = pman_frames[0].get_rect(center = (randrange(1024)-600,800+randrange(500)))
        return bottom_pman


flap_sound = pygame.mixer.Sound('coin.wav')
death_sound = pygame.mixer.Sound('bomb2.wav')
song_sound = pygame.mixer.Sound('song.wav')


SPAWNpman = pygame.USEREVENT
pygame.time.set_timer(SPAWNpman,1200)


gameover_status =0 
pygame.display.set_caption('Squid Game')


while True:

    if ((biggirl_index>=5) & (biggirl_index<=10)):
        light_status = 1
        otherman_status = 0
    else :
        light_status = 0  
        otherman_status = 1 

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                man_status = 1
                flap_sound.play()
            if event.key == pygame.K_a:
                man_status = 0
                flap_sound.play()
            if (event.key == pygame.K_SPACE) &( gameover_status !=0 ):
                man_status = 0
                gameover_status = 0 
                pman_list = [] 
                man_rect.centerx = 100
                man_rect.centery = 700
                pos_x = 100
                pos_y = 700



        elif event.type == SPAWNpman:
            if ((otherman_status == 1) & (gameover_status == 0)):
                for num in range(0,10): 
                    pman_list.append(create_pman())
                print("pile count = ",len(pman_list))


        elif event.type == pmanFLAP:
            if pman_index < 6 :
                pman_index = pman_index + 1
            else:
                pman_index = 0

            if otherman_status==1 :
                pman_surface = pman_animation()
            else:
                pman_surface = pman_stand()
            


        elif event.type == manFLAP:
            if man_index < 6 :
                man_index = man_index + 1
            else:
                man_index = 0
            if man_status==1 :
                man_surface,man_rect = man_animation()
            else:
                man_surface,man_rect = man_stand()



        elif event.type == biggirlFLAP:
            if gameover_status == 0 :
                if biggirl_index < 14 :
                    biggirl_index = biggirl_index + 1
                else:
                    biggirl_index = 0
                    song_sound.play()

            biggirl_surface,biggirl_rect = biggirl_animation()



    if gameover_status == 0:

        screen.blit(bg_surface,(0,0))
        text_surface = game_font.render("Press (D) to Go, (A) Stop",True,(0,0,0))
        text_rect = text_surface.get_rect(center = (1024/2,768-50))
        screen.blit(text_surface,text_rect)


        screen.blit(man_surface, man_rect)


        screen.blit(biggirl_surface, biggirl_rect)
         # pmans
        pman_list = move_pmans(pman_list)
        ##pman_list = remove_pmans(pman_list)

        for pman in pman_list:
            screen.blit(pman_surface,pman)

        if (man_status == 1):
            pos_x = pos_x + move_speed
            pos_y = pos_y - move_speed/2
            man_rect.centerx = pos_x
            man_rect.centery = pos_y

        if ((man_status ==1)and (light_status==1)) :
            gameover_status = 1
            death_sound.play()
            gameover_display(gameover_status)

        if (pos_y < 250):
            gameover_status = 2
            death_sound.play()
            gameover_display(gameover_status)

        redlight_display('main_game')
    else:
        gameover_display(gameover_status)


    pygame.display.update()
    clock.tick(120)
