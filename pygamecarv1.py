#updated section
import pygame
import random
import time
import sys

'''
notes:
make balls accelerate and decelerate
collision detection in front
stop at random times to simulate drop off
if the object can move forward, make it move forward, otherwise,
if it can move left, moake it move left
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
SPEED = 5
TIMEPERIOD = 50
 
 
class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self, max_acceleration = 5):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.max_acceleration = max_acceleration
 
 
def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    ball.x = 1250
    ball.y = 700
    ball.change_x = SPEED
    ball.change_y = SPEED
 
    return ball
 
 
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

    ball= make_ball()
    ball_list.append(ball)

    #print(ball.y)
    #sys.exit()
 

 
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

        #random spawn
        x = random.randint(1,TIMEPERIOD)
        if (x == 3):
            ball = make_ball()
            ball_list.append(ball)
            
 
        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.y += -ball.change_y
            if ball.y < 100:
                ball.change_x = -SPEED
                ball.x += ball.change_x
                ball.change_y = 0
                
            if ball.x < 125:
                #print('hey')
                ball.change_x= SPEED
                ball.x += ball.change_x
                ball.y += ball.change_y
                ball.change_y = -SPEED
                
                
            if ball.y > (SCREEN_HEIGHT - 50) and ball.x< (200):
              del ball_list[0]

 
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
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what is drawn.
        #print(ball_list)
        pygame.display.flip()
        
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()

