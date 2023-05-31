import pygame 
from Fighters import Fighter

pygame.init()

clock = pygame.time.Clock()
fps = 60

intro_count = 3
last_count_update = pygame.time.get_ticks()
round_over = False
score = [0,0]
round_over_cooldown = 2000
round_no = 1


Warrior_size = 162
Warrior_scale = 4
Warrior_offset = [72,56]

Wizard_size = 250
Wizard_scale = 3
Wizard_offset = [112,107]

Warrior_data = [Warrior_size,Warrior_scale, Warrior_offset]
Wizard_data = [Wizard_size, Wizard_scale, Wizard_offset]

Screen_width = 1000
Screen_height = 600

screen = pygame.display.set_mode((Screen_width,Screen_height))
pygame.display.set_caption("Fighter")

bg = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

count_fonts = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_fonts = pygame.font.Font("assets/fonts/turok.ttf",30)

def draw_text(text, font, color, x, y):
    img = font.render(text, font, color)
    screen.blit(img , (x , y))


Warrior_animation_steps = [10,8,1,7,7,3,7]
Wizard_animation_steps = [8,8,1,8,8,3,7]

def health_bars(health,x,y):
    ratio = health/100
    health_b = pygame.Rect((x,y,400 * ratio, 30))
    pygame.draw.rect(screen,(255,255,255),(x-2,y-2,404,34))
    pygame.draw.rect(screen,(255,0,0),(x,y,400,30))
    pygame.draw.rect(screen,(255,255 ,0),health_b)



def put_bg():
    resized = pygame.transform.scale(bg,(Screen_width,Screen_height))
    screen.blit(resized,(0,0))

run = True

fighter_1 = Fighter(1,200,310,False,Warrior_data, warrior_sheet, Warrior_animation_steps,round_over)
fighter_2 = Fighter(2,700,310,True,Wizard_data,wizard_sheet,Wizard_animation_steps,round_over)

while run:

    clock.tick(fps)

    put_bg()

    health_bars(fighter_1.health, 20,20)
    health_bars(fighter_2.health, 580,20)

    draw_text("P1 : " + str(score[1]), score_fonts, (255,0,0), 20,60)
    draw_text("P2 : " + str(score[0]), score_fonts, (255,0,0), 580,60)
    draw_text(str(round_no), count_fonts , (255,0,0), (Screen_width/2.1) + 10  , 0)

    if intro_count <= 0:
        fighter_1.move(Screen_width, Screen_height, screen , fighter_2)
        fighter_2.move(Screen_width, Screen_height, screen, fighter_1)
    else:
        draw_text(str(intro_count), count_fonts, (255,0,0), Screen_width / 2.1 , Screen_height / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            
            

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over == False:
        if fighter_1.alive == False:
            score[0] += 1
            round_no += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[1] += 1
            round_over = True
            round_no += 1
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360,150))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1,200,310,False,Warrior_data, warrior_sheet, Warrior_animation_steps, round_over)
            fighter_2 = Fighter(2,700,310,True,Wizard_data,wizard_sheet,Wizard_animation_steps, round_over)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
pygame.quit()