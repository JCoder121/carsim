#put save states here: 
#while making more edits on most current
#here will be the last fully working most_current.py file

#updated section 9/16/19 8:00PM
#anichau and jeffchen
#signed jeffrey chen

import pygame
import random
import math  
import os.path
import time
from time import gmtime, strftime

'''
notes:
YELLOW CARS = HAVE DROPPED OFF ALREADY
deceleration function?

next step: 
exiting cars range from 1 to 3 passengers
count number of student flow?
can definitely start doing actual statistics
count number of cars that got deleted in x amount of time = flow
do average speed, etc. in mph

Exiting students should be blue, roughly same circle size
travel about 50 pix
work on passenger

drop off list of times to wait - access that through the rand int


COMMON LOCATIONS
'''

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)

#define other variables 
SCREEN_WIDTH = 1430
SCREEN_HEIGHT = 850
CAR_SIZE = 15
SPEED = 0.01
PERSON_SPEED = 1.5
PERSON_WALK = 200
MAXSPEED = 1.5
#MAXSPEED = 10
#ACCEL = 1
ACCEL = 0.1
RANDOMPARAM = 8
INFRONT = 35
SWEEP = 20

WAITTIME = 100000
#change dt for acceleration change, bigger = faster accel
dt = 0.0006

#set height and width of screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

class Car:
    """
    Class to keep track of a car's location and speed
    """
    def __init__(self):
        self.x = 1250
        self.y = 700
        #below is spawn cars close to bottom
        #self.x = 150
        #self.y = 600
        self.speed = SPEED/2
        self.accel = 0
        self.color = RED

        self.drop_val = -1
        self.drop_x = 0
        self.drop_y = 0

        self.drop_bool = True
        self.accel_bool = True
        self.is_dropped = False
        self.pass_bool = True


    def stop(self, the_drop_bool):
        self.speed = 0
        self.accel = 0
        if the_drop_bool:
            self.color = YELLOW        

    def detect(self, detect_var):
        
        for sweep in range(-SWEEP, SWEEP):
            for infront in range(20, INFRONT):
                #right
                if detect_var == 0:
                    detect_value = screen.get_at((int(self.x)+sweep, int(self.y)-infront))

                #top
                elif detect_var == 1:
                    detect_value = screen.get_at(((int(self.x)-infront), int(self.y)+sweep))

                #left
                elif detect_var == 2:
                    detect_value = screen.get_at((int(self.x)+sweep, int(self.y)+infront)) 

                if (detect_value==RED) or (detect_value==GREEN) or (detect_value==YELLOW):
                    self.accel_bool = False
                    self.stop(False)
                    return self.accel_bool


    def accelerate(self, var1):
        self.ACCEL = self.accel * self.accel * dt
        self.speed = (self.speed + (self.ACCEL))

        if self.speed > MAXSPEED:
            self.speed = MAXSPEED

            #right
            if var1 == 0:
                self.y += -MAXSPEED
            #top
            elif var1 == 1:
                self.x += -MAXSPEED
            #lieft
            elif var1 == 2:
                self.y += MAXSPEED

        else:
            #right
            if var1 == 0:
                self.y += -self.speed 
            #top
            elif var1 == 1:
                self.x += -self.speed
            #left
            elif var1 == 2:
                self.y += self.speed

        self.accel+= ACCEL

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
        self.personal_value = random.randint(0,2)
        #self.personal_value = 1
   
    def stop(self):
        self.speed = 0
 
def make_car():
    """
    Function to make a new, random car.
    """
    car = Car()                                                                      
    #car.drop_val = random.randint(0,1)
    car.drop_val = 0

    if car.drop_val == 0:
        car.drop_x = random.randint(77, 400) * 2

    elif car.drop_val == 1:
        car.drop_y = random.randint(62, 300) *2

    return car


def make_person():
    #person that crosses the street/simulate a sidewalk, 3 possible areas where pedestrians can spawn
    person = Person()

    #right side
    if person.personal_value == 0:
        #pass
        person.x = 1130
        person.initial = person.x
        person.y = 400

    #top level
    elif person.personal_value == 1:
        person.x = 800
        person.y = 230
        person.initial = person.y

    #left side
    elif person.personal_value == 2:
        person.x = 260
        person.initial = person.x
        person.y = 450

    return person
 
def main():
    '''
    This is our main program.
    '''
    pygame.init()
    pygame.display.set_caption("PHS Car Traffic")
 
    # Loop until the user clicks the close button.
    done = False
    hundred_cars_bool = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    car_list = []
    person_list = []
    wait_list = [100,200,3000000]
    car_count = 0

    car = make_car()
    car_list.append(car)
    #first_cross = make_person()
    #person_list.append(first_cross)
    my_seconds = 0
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
    
        for event in pygame.event.get():

            #on sublime, use below    
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                spawn_bool = True

                for width in range(0, 100):
                    for height in range(0, 100):
                        spawn_value = screen.get_at(( (1200 + width) , (650 + height) ))
                        
                        if spawn_value == RED:
                            spawn_bool = False
                            break

                if spawn_bool:
                    car = make_car()
                    car_list.append(car)

            if event.type == pygame.KEYDOWN:
                person = make_person()
                person_list.append(person)

            #on IDLE, use below
            '''
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                print('something')
                #Space bar spawn a new car.
                #prevent rapid firing spawn
                if event.key == pygame.K_SPACE and car.y < 680:
                    print('hello')
                    car = make_car()
                    car_list.append(car)
                if event.key == pygame.K_RETURN:
                    person = make_person()
                    person_list.append(person)
            '''
        
        #random car spawn
        random_car = random.randint(1,RANDOMPARAM)

        #view finding of rectangle to make sure nearest car is out of area
        spawn_bool = True
        for width in range(0, 100):
            for height in range(0, 100):
                spawn_value = screen.get_at(( (1200 + width) , (650 + height) ))
                if spawn_value == RED:
                    spawn_bool = False
                    break

        #check if random match and there is a car within rectangular area of start
        if (random_car==3) and spawn_bool:
        #and len(car_list)<4: - len car list to restrict car number at once on screen
            car = make_car()
            car_list.append(car)

        
        #random pedestrian spawn
        random_ped = random.randint(1, RANDOMPARAM+100)
        #random_ped = 3
        if (random_ped == 3):
            pass
            #see how this goes 
            #person = make_person()
            #person_list.append(person)
        
 
        # --- car logic
        for car in car_list:
            #Move the car's center, check for position to move car where
            car.accel_bool = True
            #car.is_dropped_off = False
            

            #see if car is on right side, will go vertical up
            if car.x > 155 and car.y > 100:
                car.detect(0)
                if car.accel_bool:
                    car.accelerate(0)


            #see if car is on top side, will go horizontal left 
            
            elif car.x > 155 and car.y < 100:
                if car.drop_val == 0:
                    if(int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x): 
                        car.stop(True)
                        car.x -= 4
                        '''
                        #while small_timer < 5:         
                        for x in range(0, WAITTIME):
                            car.stop(True)
                            #print(small_timer)
                            #small_timer+=1
                        '''

                        #car.x -= 4



                car.detect(1) 
                if car.accel_bool:                    
                    car.accelerate(1)


            elif car.x < 155 and car.y > 90:
                #see if car is on left side, will go vertical down
                if car.drop_val == 1:
                    if(int(car.y)==car.drop_y) or (int(car.y-1)==car.drop_y):    

                        for y in range(0, wait_list[random.randint(0,2)]):
                            car.stop(True)

                        #car.y +=4

                car.detect(2)
                if car.accel_bool:
                    car.accelerate(2)

                                        
            #get rid of car if it crosses bottom line (memory management)
            if car.y >(SCREEN_HEIGHT - 50) and car.x<(200):
                del car_list[0]
                car_count+=1
                print("cars crossed:", car_count)
                cars_compare = 100
                if car_count == cars_compare:
                    hundred_cars_bool = True
                    done = True

                #fail safe to check if car going down is still red - not dropped off = bug and need to be fixed
                
                '''
                #will go through this later
                if car.color == RED:
                    print("car not dropped off, something wrong")
                    done = True
                '''

        #pedestrian logic
        for person in person_list:

            person_bool = True

            if person.personal_value == 0:
                #simple personobj detection:
                #coming from right leg
                for x in range(10, 25):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at(((int(person.x)+x), int(person.y) + person_sweep))
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.x += PERSON_SPEED

            #person coming from top leg
            elif person.personal_value == 1:
                for y in range(10,25):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at(((int(person.x) + person_sweep), int(person.y) -y))
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.y -= PERSON_SPEED

            #person coming from left leg
            elif person.personal_value == 2:
                for x in range(10,20):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at((int(person.x)-x, int(person.y)+person_sweep))
                        
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.x -= PERSON_SPEED

            
            #always check if person has walked PERSON_WALK pixels, then erase from list (memory management)

            #delete from left leg
            if((person.personal_value == 0) and (abs(person.initial - person.x) > PERSON_WALK)):
                
                del(person_list[0])

            #delete from top leg
            elif((person.personal_value == 1) and (abs(person.initial - person.y) > PERSON_WALK)):

                del(person_list[0])

            #delete from right leg
            elif((person.personal_value== 2) and (abs(person.initial - person.x) > PERSON_WALK)):
                del(person_list[0])


        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        
        #draw the road
        pygame.draw.rect(screen, BLACK, (100, 50, 1200, 100))
        pygame.draw.rect(screen, BLACK, (1200, 50, 100, 700))
        pygame.draw.rect(screen, BLACK, (100, 50, 100, 700))
        
        # draw all moving objects
        
        for car in car_list:
            pygame.draw.circle(screen, car.color, [int(car.x), int(car.y)], CAR_SIZE)

        for person in person_list:
            pygame.draw.circle(screen, GREEN, [int(person.x), int(person.y)], 7)
        
 
        # --- Wrap-up, limit to 60 frames per second
        clock.tick(60)
        my_seconds+=1
        mytime = my_seconds/60
        #print(int(mytime))
        
 
        # update screen with newly drawn
        pygame.display.flip()
 
    # Close everything
    pygame.quit()
    if hundred_cars_bool:
        body_print = "\n\nseconds needed for all " + str(car_count) + " cars to pass: %0.2f seconds" % mytime
        print(body_print)

        real_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
        save_path = "/Users/jeffrey/Documents/Github/carsim/files/testing"
        filestring = "rawdata- " + str(real_time) + ".txt"
        complete_name = os.path.join(save_path, filestring)
        
        f = open(complete_name, "a+")
        #f = open(complete_name, "w")
        #f = open("text.txt", "a+")

        #various hundred car trials below
        #f.write("\nthis is first go")
        f.write("Time Elapsed for 100 Cars, No Pedestrians")
        #write in the date or something else as well
        #f.write("Time Elapsed for 100 Cars, Randomly Spawned Pedestrians")
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 10 Second Intervals")
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 20 Second Intervals")
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 30 Second Intervals")

        f.write(body_print)
        f.write("\n\n=================================================")
        f.close()

 
if __name__ == "__main__":
    main()