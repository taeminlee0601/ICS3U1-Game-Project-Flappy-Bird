# Import pygame, os, random, and time modules
import pygame
import os
import random
import time

# initialize the font module
pygame.font.init()

#set the width and height of the window
WIDTH, HEIGHT = 900,500

# make the window and set the title of the window
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")

# set the FPS
# set the speed of the bird and the pipes
FPS = 60
VEL_OF_FALL = 5
VEL_OF_PIPES = 2

# set the rgb values for the colours that will be used
WHITE = 255,255,255
BLACK = 0,0,0
GREEN = 29,206,42

# make a rectangle for the player
# scale the background to fit the width and height of the window
# scale the bird to fit the width and height of the player rectangle
PLAYER = pygame.Rect(WIDTH / 4, HEIGHT/2 - 15, 50, 35)
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.jfif')), (WIDTH, HEIGHT))
BIRD = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Bird.png')), (50,35))

# set the clock variable to control the FPS
clock = pygame.time.Clock()

# set the fonts and the size of the fonts
START_FONT = pygame.font.Font('assets\FlappyBirdLetters.ttf', 50)
END_FONT = pygame.font.Font('assets\FlappyBirdLetters.ttf', 80)
TITLE_FONT = pygame.font.Font('assets\FlappyBirdLetters.ttf', 150)
SCORE_FONT = pygame.font.Font('assets\FlappyBirdNumbers.ttf', 30)
SCORE_FONT_TWO = pygame.font.Font('assets\FlappyBirdNumbers.ttf', 100)

# make a method that makes the pipes work
# get the score and the two lists created for the pipes
def handle_pipes(top_pipe, bottom_pipe, score):
    # move the pipes, and check if the pipes hit the player or are out of the window
    for pipe in top_pipe:
        # move the pipe towards the player
        pipe.x -= VEL_OF_PIPES

        # check if the player has collided/hit the pipe
        # if so make the game end
        if PLAYER.colliderect(pipe):
            end_game(score)
        # check if the pipe is out of the window
        # if so remove the pipe from the list
        elif pipe.x < -100:
            top_pipe.remove(pipe)

    # move the pipes, and check if the pipes hit the player or are out of the window
    for pipe in bottom_pipe:
        # move the pipe towards the player
        pipe.x -= VEL_OF_PIPES
        
        # check if the player has collided/hit the pipe
        # if so make the game end
        if PLAYER.colliderect(pipe):
            end_game(score)
        # check if the pipe is out of the window
        # if so remove the pipe from the list
        elif pipe.x < -100:
            bottom_pipe.remove(pipe)

# make a method that draws on the window when the game is played
# get the score and the two lists for the pipes
def game_window(top_pipe, bottom_pipe, score):
    # draw the background on the window
    # draw the bird on the window
    screen.blit(BG, (0,0))
    screen.blit(BIRD, (PLAYER.x, PLAYER.y))

    # make a variable that will draw the score 
    # make the variable say the score 
    # make the colour of the score black
    scoreboard = SCORE_FONT.render(str(score), 1, BLACK)

    # draw the top pipes in the list
    for pipe in top_pipe:
        pygame.draw.rect(screen, GREEN, pipe)
    
    # draw the bottom pipes in the list
    for pipe in bottom_pipe:
        pygame.draw.rect(screen, GREEN, pipe)
    
    # draw the scoreboard in the middle of the width and near the top of the window
    screen.blit(scoreboard, (WIDTH / 2 - scoreboard.get_width() / 2, HEIGHT / 2 - scoreboard.get_height()/2 - 200))

    # update the screen so the objects are all drawn
    pygame.display.update()

# make a function that runs the game
def play_game():
    # set the player height at the beginning of the game
    PLAYER.y = HEIGHT / 2 - 15

    # make a list for the top pipes
    # make a list for the bottom pipes
    # make the starting pipes have a whole in the middle of the screen
    # make the pipes have a 200px gap
    top_pipe = []
    bottom_pipe = []
    pipe_top = pygame.Rect(900, -200, 100, 150 + 200)
    pipe_bottom = pygame.Rect(900, HEIGHT - 150, 100, 150)

    # add the pipes to the lists
    top_pipe.append(pipe_top)
    bottom_pipe.append(pipe_bottom)

    # make a score variable and set it to 0
    score = 0

    # make run to true to run the while loop
    run = True

    # make a while loop to run the game
    while run:
        # make the game refresh at 60 frames per second
        clock.tick(FPS)
        
        # end the game if the player/bird hits the ground
        # run the game over window
        if PLAYER.y > 450:
            end_game(score)

        # check for the events that happen in pygame
        for event in pygame.event.get():
            # if the pygame is quit, close the window
            if event.type == pygame.QUIT:
                exit()

            # if the player is within the height of the map, make them jump
            # the player cannot go over -50 pxl
            if event.type == pygame.KEYDOWN and PLAYER.y + 100 > -50:
                PLAYER.y -= 100

        # check if a new pipe is needed
        for pipe in top_pipe:
            # if a pipe is at 700 and the length of the list is under 7
            # generate a random number from 75 to 225 (a number to determine where the gap is)
            # make 2 pipes using the random number generated
            # add the 2 pipes to the list
            if pipe.x == 700 and len(top_pipe) < 7:
                number = random.randint(75, 225)
                pipes_top = pygame.Rect(900, -200, 100, number + 200)
                pipes_bottom = pygame.Rect(900, number + 200, 100, HEIGHT - 200 - number)
                top_pipe.append(pipes_top)
                bottom_pipe.append(pipes_bottom)
            # check if the player has past the pipe
            # if so increase the score by one
            if pipe.x + 50 > PLAYER.x - 2 and pipe.x + 50 < PLAYER.x:
                score += 1

        # run the functions so that pipes mechanics will work
        # run the game window function to draw the game window
        handle_pipes(top_pipe, bottom_pipe, score)
        game_window(top_pipe, bottom_pipe, score)

        # make the player fall at a set velocity
        PLAYER.y += VEL_OF_FALL

# make a function to draw the start window
def start_window():
    # draw the background on the window
    screen.blit(BG, (0,0))
    
    # make a variable that will say the instructions in black
    # make a variable that will say the title
    start_text = START_FONT.render("Press Any Key To Start", 1, BLACK)
    title = TITLE_FONT.render("FLAPPY BIRD", 1, BLACK)

    # draw the title and instructions on the window
    screen.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - start_text.get_height()/2 + 100))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height()/2 - 50))

    # update the screen so the objects are all drawn
    pygame.display.update()

# make a function that will start when the game is first run
def start():
    # make run to True to run the while loop
    run = True

    # make a while loop to run the start screen
    while run:
        # make the game refresh at 60 frames per second
        clock.tick(FPS)

        # run the function to draw the start window
        start_window()

        # check for events in pygame
        for event in pygame.event.get():
            # if the pygame is quit, close the window
            if event.type == pygame.QUIT:
                exit()

            # if the user presses any key, run the game
            if event.type == pygame.KEYDOWN:
                play_game()

# make a function to draw the game over screen
def end_window(score):
    # draw the background on the window
    screen.blit(BG, (0,0))

    # make a variable that will say the word score
    # make a variable that will say the score
    # make a variable that will say the instructions
    end_text = END_FONT.render("Score ", 1, BLACK)
    score_text = SCORE_FONT_TWO.render(str(score), 1, BLACK)
    instructions = START_FONT.render("Press Any Key To Play Again", 1, BLACK)
    
    # draw the word score, score and instructions on the screen
    screen.blit(end_text, (WIDTH / 2 - end_text.get_width() / 2, HEIGHT / 2 - end_text.get_height()/2 - 200))
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height()/2 - 75))
    screen.blit(instructions, (WIDTH / 2 - instructions.get_width() / 2, HEIGHT / 2 - instructions.get_height() / 2 + 50))

    # update the screen so the objects are all drawn
    pygame.display.update()

# make a functions that will occur after the player loses the game
def end_game(score):
    # make run to True to run the while loop
    run = True

    # make a while loop to run the end screen
    while run:
        # make the game refresh 60 frames per second
        clock.tick(FPS)

        # run the function to draw the end window
        end_window(score)

        # check for events in pygame
        for event in pygame.event.get():
            # if pygame is quit, close the window
            if event.type == pygame.QUIT:
                exit()

            # if a key is pressed, run the game 
            if event.type == pygame.KEYDOWN:
                time.sleep(0.2)
                play_game()

# check if the imported modules are imported correctly
# if so run the game 
if __name__ == "__main__":
    start()