#updated section 9/12/19 2:25PM
#anichau and jeffchen

#working version
#decelerating is still a question
#can move on to simulating the actual passenger drop off
#remember on drop off to associate a boolean
#if dropped off already, can't do it again
import pygame
import random
import math
import sys


'''
notes:
do wait time later, see if can implement it
'''

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
 
SCREEN_WIDTH = 1430
SCREEN_HEIGHT = 850
BALL_SIZE = 15
SPEED = 1
PERSON_SPEED = 1.5
MAXSPEED = 2
ACCEL = 0.03
RANDOMPARAM = 25
INFRONT = 35
WAITTIME = 1000
#change dt for acceleration change, bigger = faster accel
dt = 0.008

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dropping Cars")

class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.y_accel = 0
        self.drop_bool = False
        self.x_accel = 0
        self.drop_val = 100
        self.accel_bool = True

    def stop(self):
        self.speed = 0
        self.y_accel = 0
        self.x_accel = 0
    
    
    def dropoff(self, drop_val):
        #drop off from top

        if drop_val == 0:
            self.drop_bool = True
            #this means that its stopping at top to drop off
            drop_x = random.randint(150, 800)
            if self.x == drop_x and self.y < 300:
                for x in range(0, WAITTIME):
                    self.reset()
                print('dropped off 1')
            self.drop_bool = False

        elif drop_val == 1:
            self.drop_bool = True
            #this means that its stopping at left side going down to d.o.
            drop_y = random.randint(125, 600)
            if self.y == drop_y and self.x < 200:
                for x in range(0, WAITTIME):
                    self.reset()
                print('dropped off 2')
            self.drop_bool = False

        elif drop_val == 100:
            print('something wrong')
    
    def detect(self, detect_var):
        #left 
        if detect_var == 0:
            for infront in range(20,INFRONT):
                    value3 = screen.get_at((int(self.x), int(self.y)+infront))  

                    if (value3 == RED) or (value3 == GREEN):
                        self.accel_bool = False   
                        #ball.decelerate(2)
                        self.stop()

        #right
        elif detect_var == 1:
            for infront in range(20, INFRONT):
                        value1 = screen.get_at((int(self.x), int(self.y)-infront))
                        if (value1 == RED) or (value1 == GREEN):
                            self.accel_bool = False
                            #ball.decelerate(0)
                            self.stop()

        #top
        elif detect_var == 2:
            for infront in range(20, INFRONT):
                        value2 = screen.get_at(((int(self.x)-infront), int(self.y)))
                        
                        if (value2 == RED) or (value2 == GREEN):
                            self.accel_bool = False
                            #ball.decelerate(1)
                            self.stop()

        return self.accel_bool


    def accelerate(self, var1):
        self.Y_ACCEL = self.y_accel*self.y_accel * dt
        self.X_ACCEL = self.x_accel*self.x_accel * dt
    
        #from right side
        if var1 == 0:
            self.speed = (self.speed + (self.Y_ACCEL))      
            if self.speed > MAXSPEED:
                self.speed = MAXSPEED
                self.y -= MAXSPEED
            else:   
                self.y -= self.speed
            self.y_accel += ACCEL

        #from top side
        elif var1 == 1:
            self.speed = (self.speed + (self.X_ACCEL))
            if self.speed > MAXSPEED:
                self.speed = MAXSPEED
                self.x -= MAXSPEED
            else:
                self.x -= self.speed
            self.x_accel += ACCEL

        #from left side
        elif var1 == 2:    
            self.speed = (self.speed + (self.Y_ACCEL))
            if self.speed > MAXSPEED:
                self.speed = MAXSPEED
                self.y += MAXSPEED
            else:
                self.y += self.speed
            self.y_accel += ACCEL

        else:
            print('error accelerate')
            print(var1)
            sys.exit()

    '''
    def decelerate(self, var1):
        self.Y_ACCEL = self.y_accel*self.y_accel * dt
        self.X_ACCEL = self.x_accel*self.x_accel * dt

        #from right side
        if var1 == 0:
            self.speed = (self.speed - (self.Y_ACCEL))    
            if self.speed < 0:
                self.speed = 0
                self.y -= 0
            else:
                self.y -= self.speed
            self.y_accel += ACCEL

        #from top side
        elif var1 == 1:
            self.speed = (self.speed - (self.X_ACCEL))
            if self.speed < 0:
                self.speed = 0
                self.x -= 0
            else:
                self.x -= self.speed
            self.x_accel += ACCEL
            
        #from left side
        elif var1 == 2:
            self.speed = (self.speed - (self.Y_ACCEL))
            if self.speed < 0:
                self.speed = 0
                self.y += 0
            else:
                self.y += self.speed
            self.y_accel += ACCEL

        else:
            print('error decelerate')
            sys.exit()
    '''
    
        
class Person:
    """
    Class to make person randomly spawn in 3+ randomly
    generated locations
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = PERSON_SPEED
        self.initial = 0
        #self.personal_value = random.randint(0,2)
        self.personal_value = 0

 
def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()                                                                      
    # Starting position of the ball.
    ball.x = 1250
    ball.y = 700
    ball.speed = SPEED
    ball.drop_val = random.randint(0,1)
    return ball

def make_person():
    #make person function that crosses the street and simulate a sidewalk
    #3 possible segments where pedestrians can spawn
    person = Person()

    #right side
    if person.personal_value == 0:
        person.x = 1350
        person.initial = person.x
        person.y = 400

    #top level
    elif person.personal_value == 1:
        person.x = 800
        person.initial = person.y
        person.y = 40

    #left side
    elif person.personal_value == 2:
        person.x = 60
        person.initial = person.y
        person.y = 450

    else:
        print('error personal value')
        sys.exit()    

    return person
 
def distance(a,b):
    '''
    This function will find the distance between any two balls
    '''
    return math.sqrt((a.y - b.y)**2 + (a.x - a.y)**2)
 
def main():
    '''
    This is our main program.
    '''
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dropping Cars")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    ball_list = []
    person_list = []

    ball = make_ball()
    ball_list.append(ball)
    first_cross = make_person()
    person_list.append(first_cross)
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
    
        #on sublime, use below    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN and ball.y<680:
                ball = make_ball()
                ball_list.append(ball)

            if event.type == pygame.KEYDOWN:
                person = make_person()
                person_list.append(person)

            #on IDLE, use below
            '''
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                print('something')
                #Space bar spawn a new ball.
                #prevent rapid firing spawn
                if event.key == pygame.K_SPACE and ball.y < 680:
                    print('hello')
                    ball = make_ball()
                    ball_list.append(ball)
                if event.key == pygame.K_RETURN:
                    person = make_person()
                    person_list.append(person)
            '''
        
        #random car spawn
        x = random.randint(1,RANDOMPARAM)
        #check if random match and there is a ball above
        if (x==3) and (ball.y < 680):
            ball = make_ball()
            ball_list.append(ball)


        #random pedestrian spawn
        another_random = random.randint(1, RANDOMPARAM + 100)
        #another_random = 3
        if (another_random == 3):
            person = make_person()
            person_list.append(person)
 
        # --- Logic
        for ball in ball_list:

            #Move the ball's center, check for position to move ball where
            #DECELERATING IS BIG KEY - STAY OR NO?

            #see if ball is on left side, will go vertical motion down
            ball.accel_bool = True


            if ball.x < 155 and ball.y > 90:
                '''
                if ball.drop_val == 1:
                    ball.drop_off(drop_val)
                '''
                #see if ball is on left side, will go down
                #get value above detect and use that
                ball.detect(0)
            

                if ball.accel_bool:
                    ball.accelerate(2)
                
            else:
                #see if ball is on right side, will go vertical motion up
                if ball.y > 100:
                    ball.detect(1)
                            
                    if ball.accel_bool:
                        ball.accelerate(0)
                    
                #see if ball is on top side, will go horizontal motion left
                elif ball.y < 100:
                    ball.detect(2)

                    if ball.accel_bool:    
                        ball.accelerate(1)
        
            #get rid of ball if it crosses 
            if ball.y >(SCREEN_HEIGHT - 50) and ball.x<(200):
                del ball_list[0]


        #pedestrian crossing
        for person in person_list:
            #person coming from right leg
            if person.personal_value == 0:
                person.x -= PERSON_SPEED

            #person coming from top
            elif person.personal_value == 1:
                person.y += PERSON_SPEED

            #person coming from left leg
            elif person.personal_value == 2:
                person.x += PERSON_SPEED

            else:
                print('error personlist')
                sys.exit()

            #always check if person has walked 200 pixels, then erase
            if((person.personal_value == 0 or person.personal_value== 2)
               and (abs(person.initial - person.x) > 200)):
                del(person_list[0])

            elif((person.personal_value == 1)
                 and abs(person.initial - person.y) > 200):
                del(person_list[0])

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        #draw the road
        pygame.draw.rect(screen, BLACK, (100, 50, 1200, 100))
        pygame.draw.rect(screen, BLACK, (1200, 50, 100, 700))
        pygame.draw.rect(screen, BLACK, (100, 50, 100, 700))
        
        # draw everything
        
        for ball in ball_list:
            if ball.drop_bool == True:
                pygame.draw.circle(screen, YELLOW, [int(ball.x), int(ball.y)], BALL_SIZE)

            else:
                pygame.draw.circle(screen, RED, [int(ball.x), int(ball.y)], BALL_SIZE)

        

        for person in person_list:
            pygame.draw.circle(screen, GREEN, [int(person.x), int(person.y)], 7)
 
        # --- Wrap-up, limit to 60 frames per second
        clock.tick(60)
 
        # update screen with newly drawn
        pygame.display.flip()
 
    # Close everything 
    pygame.quit()
 
if __name__ == "__main__":
    main()

