import pygame
import os
pygame.font.init()
pygame.mixer.init()




Width, Height = 1500,800
root = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Learning Pygame")



# someimportant variables for the game like fps width height and all
white = (255,255,255)
fps = 60
vel = 5
bullets_vel = 7
spaceship_width ,spaceship_height  = 64 ,64 
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
border = pygame.Rect(Width/2 - 5, 0, 10, Height)
max_bullets = 5


bullet_hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), r'pygames\explosion.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), r'pygames\hitsound.mp3'))



health_font = pygame.font.SysFont('Fira Code', 40)
winner_font = pygame.font.SysFont('comicsans', 100)





machine1_hit = pygame.USEREVENT + 1 # the numbers are different becasue it like the id's 1 has it own id and 2 has it own if both one then the evnets are same
machine2_hit = pygame.USEREVENT + 2
# images height and width is 64*64 and big villan space ship is 96*96
# Loading images 
villan = pygame.image.load(os.path.join(os.getcwd(), r'pygames\villan_1.png'))
user = pygame.image.load(os.path.join(os.getcwd(), r'pygames\spacship_one.png'))
background = pygame.image.load(os.path.join(os.getcwd(), r'pygames\space.jpg'))



# working on the face and size of the spaceships
villan_spaceship = pygame.transform.rotate(villan,(90))
user_spaceship = pygame.transform.rotate(user,-90)
space_image = pygame.transform.scale(background,(Width, Height))



def draw_window(spaceship1 , spaceship2, machine1_bullets , machine2_bullets, space1health , space2health):
    root.blit(space_image, (0,0))
    pygame.draw.rect(root,black ,border)

    space1health_text = health_font.render("Health: " + str(space1health),1 , white)
    space2health_text = health_font.render("Health: " + str(space2health),1 , white)

    root.blit(space1health_text, (Width -  space1health_text.get_width() -10 , 10))
    root.blit(space2health_text, (10,10))
    root.blit(user_spaceship, (spaceship1.x, spaceship1.y))
    root.blit(villan_spaceship, (spaceship2.x,spaceship2.y))
    
    
    for bullet in machine1_bullets:
        pygame.draw.rect(root,red,bullet)
    
    for bullet in machine2_bullets:
        pygame.draw.rect(root,blue,bullet)



    pygame.display.update()

def moving_spaceship1(spaceship, keys):
    if keys[pygame.K_a] and spaceship.x - vel > 0: #left
        spaceship.x -= vel
    elif keys[pygame.K_d] and spaceship.x + vel + spaceship.width < border.x : #right
        spaceship.x += vel
    elif keys[pygame.K_w] and spaceship.y - vel > 0: #up
        spaceship.y -= vel
    elif keys[pygame.K_s] and spaceship.y + vel + spaceship.height < Height: #down
        spaceship.y += vel
    else:
        pass

def moving_spaceship2(spaceship, keys):
    if keys[pygame.K_LEFT] and spaceship.x - vel > border.x + border.width: #left
        spaceship.x -= vel
    elif keys[pygame.K_RIGHT] and spaceship.x + vel + spaceship.width < Width : #right
        spaceship.x += vel
    elif keys[pygame.K_UP] and spaceship.y - vel > 0: #up
        spaceship.y -= vel
    elif keys[pygame.K_DOWN] and spaceship.y + vel + spaceship.height < Height: #down
        spaceship.y += vel
    else:
        pass


def handle_bullets(shoot1,shoot2 , machine1, machine2):
    for bullet in shoot1:
        bullet.x += bullets_vel
        if machine2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(machine2_hit))
            shoot1.remove(bullet)
        elif bullet.x > Width:
            shoot1.remove(bullet)

    for bullet in shoot2:
        bullet.x -= bullets_vel
        if machine1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(machine1_hit))
            shoot2.remove(bullet)
        elif bullet.x < 0:
            shoot2.remove(bullet)


def draw_winner(text):
    draw_text = winner_font.render(text,1, white )
    root.blit(draw_text, (Width/2 - draw_text.get_width()/2, Height/2 -draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
# making the image to move  x    y  width  height
    spaceship1 = pygame.Rect(300 ,400, spaceship_width , spaceship_height)
    spaceship2 = pygame.Rect(1200 ,400, spaceship_width , spaceship_height)

    space_bullets_1 = []
    space_bullets_2 = []

    spaceship1_health = 10
    spaceship2_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(space_bullets_1) < max_bullets:
                    bullet = pygame.Rect(spaceship1.x + spaceship1.width, spaceship1.y + spaceship1.height/2 - 2 , 10 , 5 )
                    space_bullets_1.append(bullet)
                    bullet_fire_sound.play()


                if event.key == pygame.K_RCTRL and len(space_bullets_2) < max_bullets:
                    bullet = pygame.Rect(spaceship2.x, spaceship2.y + spaceship2.height/2 - 2 , 10 , 5 )
                    space_bullets_2.append(bullet)
                    bullet_fire_sound.play()


            if event.type == machine1_hit:
                spaceship2_health -= 1
                bullet_hit_sound.play()


            if event.type == machine2_hit:
                spaceship1_health -= 1
                bullet_hit_sound.play()



        winner_text = ""
        if spaceship1_health<=0:
            winner_text = "Hero Wins!"

        if spaceship2_health<=0:
            winner_text = "Enemy Wins!"
            
        if winner_text != "":
            draw_winner(winner_text)
            break




        #Moving the spaceship on pressing keys
        keys_press = pygame.key.get_pressed()

        moving_spaceship1(spaceship1, keys_press)

        moving_spaceship2(spaceship2, keys_press)

        handle_bullets(space_bullets_1,space_bullets_2,spaceship1, spaceship2)

        draw_window(spaceship1, spaceship2,space_bullets_1,space_bullets_2 , spaceship1_health, spaceship2_health)

    main()



if __name__ == "__main__":
    main()
