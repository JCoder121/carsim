#anirudh today
#updated section 9/3/19 4:39PM
#anichau and jeffchen
#This update contains the beginning code for pedestrians
import pygame
import random
import math

'''
notes:
make balls accelerate and decelerate
collision detection in front
stop at random times to simulate drop off
Change the colors of the cars
'''

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
 
SCREEN_WIDTH = 1430
SCREEN_HEIGHT = 850
BALL_SIZE = 15
 
 
class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0


def make_person():
    '''
    Makes the people that will cross the street
    '''
    person = Ball()
    person.x = 500
    person.y = 200
    person.change_x = 10
    person.change_y = 10

    return person
 
def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    ball.x = 1250
    ball.y = 700
    ball.change_x = 10
    ball.change_y = 10
 
    return ball
 
def distance(a,b):
    '''
    This function will find the distance between any two balls
    '''
    return math.sqrt((a.y - b.y)**2 + (a.x - b.x)**2)
 
def main():
    """
    This is our main program.
    """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Bouncing Balls")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    ball_list = []
    person_list = []
    #cars
    ball = make_ball()
    ball_list.append(ball)

    #people
    person = make_person()
    person_list.append(person)

 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ball = make_ball()
                    ball_list.append(ball)
                if event.key == pygame.K_RETURN:
                    person = make_person()
                    person_list.append(person)
         
        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.y += -ball.change_y
            if ball.y < 100:
                ball.change_x = -10
                ball.x += ball.change_x
                ball.change_y = 0
                
                
            if ball.x < 125:
                #print('hey')
                ball.change_x= 10
                ball.x += ball.change_x
                ball.y += ball.change_y
                ball.change_y = -10
                
            if ball.y >(SCREEN_HEIGHT - 50) and ball.x<(200):
              del ball_list[0]

        
        # -- Distance ( Object Detection )---
            i =0
            j =0 
            if (len(ball_list) > 1):
                for x in range(len(ball_list)- 1):
                    if (distance(ball_list[i], ball_list[i+1]) < 100):
                        ball_list[i+1].change_y = 0
                    if len(person_list) > 0:
                        for y in range(len(person_list)): 
                            if (distance(ball_list[i], person_list[j]) < 100):
                                    ball_list[i].change_x = 0
                                    ball_list[i].x += 0
                        #print(distance(ball_list[i],ball_list[i+1]))
                    i = i + 1

        # -- Pedestrian Crossing
        for person in person_list:
            person.y += -person.change_y

            if person.y < 20:
                del person_list[0]

                 
            
 
        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        #draw the road

        pygame.draw.rect(screen, BLACK, (100, 50, 1200, 100))
        pygame.draw.rect(screen, BLACK, (1200, 50, 100, 700))
        pygame.draw.rect(screen, BLACK, (100, 50, 100, 700))
        
 
        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, RED, [ball.x, ball.y], BALL_SIZE)

        # Draw the pedestrians
        for person in person_list:
            pygame.draw.circle(screen, GREEN, [person.x, person.y], 7)
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
#        if len(ball_list) > 0:
            #print(ball_list)
        pygame.display.flip()
        '''
        if (len(person_list) > 0):
            #print(person_list)
        '''
            
        if (len(person_list) > 0) and (distance(ball_list[i], person_list[j]) <100) :    
            #print("hey")
            #print(person_list[j].x , person_list[j].y)
            #print(ball_list[i].x , ball_list[i].y)
            ball_list[i].change_x = 0
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()

