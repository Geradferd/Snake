import pygame
import time
import random
from tkinter import *


"https://www.youtube.com/watch?v=PHdZdrMCKuY&t=372s"


screen_state = True

"setting up the menu"
menu = Tk()
menu.title("Snake Menu")
menu.geometry("300x500")
menu.resizable(False, False)

"gadgets"
tele_var = IntVar()
moving_var = IntVar()
target_num_var = IntVar()

start_button = Button(menu, text = "START", command = lambda:(menu.withdraw(), run_game()))
start_button.pack()

options = Frame(menu)
tele_info = Label(options, text = "Wraparound: ")
teleport_option = Checkbutton(options, variable = tele_var)
move_info = Label(options, text = "Movable Coins: ")
moving_option = Checkbutton(options, variable = moving_var)
target_info = Label(menu, text = "Number of Coins")
target_num_option = Scale(menu, from_ = 1, to = 10, orient = HORIZONTAL, variable = target_num_var)

tele_info.pack(side='left')
teleport_option.pack(side='left')
move_info.pack(side='left', padx = 10)
moving_option.pack(side='left')
options.pack(pady = 20)
target_info.pack()
target_num_option.pack()

leave_button = Button(menu, text = "QUIT", command = lambda:(pygame.quit(), quit()))
leave_button.pack(pady = 20)

pygame.init()


"RGB values"
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
width, height = 600, 400
coin_sound = pygame.mixer.Sound("collectcoin-6075.mp3")

"setting up the display screen"
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("NeuralNine Snake Game")
clock = pygame.time.Clock()
snake_size = 10
snake_speed = 15
"defining font styles and sizes"
message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 25)

def print_score(score):
    text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(text, [0,0])

def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, [pixel[0], pixel[1], snake_size, snake_size])

def run_game():
    global tele_var, moving_var, target_num_var, menu
    
    "game effects"
    screen_teleport = (True if tele_var.get() == 1 else False)
    moving_target = (True if moving_var.get() == 1 else False)
    target_num = target_num_var.get()
    
    game_over = False
    game_close = False
    
    x = width/2
    y = height/2
    
    x_speed = 0
    y_speed = 0
    
    snake_pixels = []
    snake_length = 1
    

    targets_x = [round(random.randrange(0, width-snake_size) / 10.0) * 10.0 for x in range(target_num)]
    targets_y = [round(random.randrange(0, height-snake_size) / 10.0) * 10.0 for y in range(target_num)]
    
    target_max_spd = 1
    if moving_target:
        targets_speed = [[round(random.randrange(-10, 10)),round(random.randrange(-10, 10))] for i in range(target_num)]
    hit_box = snake_size
    
    while not game_over:
        
        "game over code"
        while game_close:
            game_display.fill(black)
            game_over_message = message_font.render("Game Over!", True, red)
            game_display.blit(game_over_message, [width / 3, height / 3])
            game_over_messages = message_font.render("type '1' for menu and '2' for restart", True, red)
            game_display.blit(game_over_messages, [width / 6, height / 6])
            print_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_over = True
                        game_close = False
                        menu.deiconify()
                    if event.key == pygame.K_2:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        
        "controls"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            length_check = snake_length > 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not (length_check and x_speed > 0):
                    x_speed = -snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT and not (length_check and x_speed < 0):
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP and not (length_check and y_speed > 0):
                    x_speed = 0
                    y_speed = -snake_size
                if event.key == pygame.K_DOWN and not (length_check and y_speed < 0):
                    x_speed = 0
                    y_speed = snake_size
        
        if (x >= width or x < 0 or y >= height or y < 0) and screen_teleport == False:
            game_close = True
        
        x += x_speed
        y += y_speed
        
        if moving_target:
            counter = 0
            for spd in targets_speed:
                counter += 1
                if targets_x[counter-1] > width or targets_x[counter-1] < 0:
                    targets_speed[counter-1][0] *= -1
                if targets_y[counter-1] > height or targets_y[counter-1] < 0:
                    targets_speed[counter-1][1] *= -1
                targets_x[counter-1] += targets_speed[counter-1][0]
                targets_y[counter-1] += targets_speed[counter-1][1]
        
        
        game_display.fill(black)

        for i in range(target_num):
            pygame.draw.rect(game_display, orange, [targets_x[i], targets_y[i], snake_size, snake_size])
        
        if screen_teleport:
            if x < 0:
                x = width-1
            elif x > width:
                x = 1
            if y < 0:
                y = height-1
            elif y > height:
                y = 1
        snake_pixels.append([x, y])
        
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        
        "Checks if the snake hit itself"
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True
        
        draw_snake(snake_size, snake_pixels)
        print_score(snake_length - 1)
        
        pygame.display.update()
        
        "checks if the player is touching the coin"
        for i in range((target_num)):
            if targets_x[i]-hit_box < x < targets_x[i]+hit_box and targets_y[i]-hit_box < y < targets_y[i]+hit_box:
                print("hit")
                if moving_target:
                    targets_speed[i][0] = round(random.randrange(-10, 10))
                    targets_speed[i][1] = round(random.randrange(-10, 10))
                pygame.mixer.Sound.play(coin_sound)
                targets_x[i] = round(random.randrange(0, width-snake_size) / 10.0) * 10.0
                targets_y[i] = round(random.randrange(0, height-snake_size) / 10.0) * 10.0
                snake_length += 1
        
        
        "checks if coin is tounching the player"
        if moving_target:
            for pixel in snake_pixels[:-1]:
                for i in range(target_num):
                    if pixel[0]-hit_box*1.5 < targets_x[i] < pixel[0]+hit_box*1.5 and pixel[1]-hit_box*1.5 < targets_y[i] < pixel[1]+hit_box*1.5:
                        if targets_x[i] < pixel[0]-hit_box or targets_x[i] > pixel[0]+hit_box:
                            targets_speed[i][0] *= -1
                        if targets_y[i] < pixel[1]-hit_box or targets_y[i] > pixel[1]+hit_box:
                            targets_speed[i][1] *= -1
        
        "checks if coint is touching another coin"
        if moving_target:
            for p in range(target_num):
                for p_other in list(range(target_num))[0:p] + list(range(target_num))[p+1:]:
                    if targets_x[p_other]-hit_box*1.5 < targets_x[p] < targets_x[p_other]+hit_box*1.5 and targets_y[p_other]-hit_box*1.5 < targets_y[p] < targets_y[p_other]+hit_box*1.5:
                        if targets_x[p] < targets_x[p_other]-hit_box or targets_x[p] > targets_x[p_other]+hit_box:
                            targets_speed[p][0] *= -1
                        if targets_y[p] < targets_y[p_other]-hit_box or targets_y[p] > targets_y[p_other]+hit_box:
                            targets_speed[p][1] *= -1
        
        clock.tick(snake_speed)
    

menu.mainloop()
