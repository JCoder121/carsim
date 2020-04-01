#put save states here: 
#while making more edits on most current
#here will be the last fully working most_current.py file

#updated section 3/20/20 8:10PM
#anichau and jeffchen
#signed Anirudh Chaudhary
#Update: Sequential Car Dropoff: Cars will dropoff if the car in front of it dropped off

'''Things to do:
1. Sequential car dropping if in the dropoff zone and the car in front is also dropping off
2. Drop off in the vertical and horizontal direction
'''
import pygame
import random
import math  
import os.path
import time
from time import gmtime, strftime

'''
notes:
YELLOW CARS = HAVE DROPPED OFF ALREADY
next step: 
do average speed, etc. in mph
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
SPEED = 0.1
PERSON_SPEED = 1.5
PERSON_WALK = 200
MAXSPEED = 1.5
ACCEL = 0.5
RANDOMPARAM = 8
INFRONT = 40
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
        self.drop = False
        self.time = random.randint(10,15)
        self.dropping = ""
        self.start_time_bool = True


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
                    return (self.accel_bool)         #in the future, experiment with seeing if you can return the detect_value and self.accel_bool


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
    car.drop_x = random.randint(77, 250) * 2

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
    car_count = 0

    car = make_car()
    car_list.append(car)
    #first_cross = make_person()
    #person_list.append(first_cross)
    my_seconds = 0
    start_seconds = 0
    start_seconds_bool = True
    end_seconds = 0
    total_seconds = 0
    first_car_bool = True
    dropping = ""
    initial_time_bool = True
    
    
 
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
        
        #random car spawn
        random_car = random.randint(1,RANDOMPARAM)

        #view finding of rectangle to make sure nearest car is out of area
        spawn_bool = True
        for width in range(0, 100):
            for height in range(0, 50):
                spawn_value = screen.get_at(( (1200 + width) , (650 + height) ))
                if spawn_value == RED:
                    spawn_bool = False
                    break

        #check if random match and there is a car within rectangular area of start
        if (random_car==3) and spawn_bool:
            #- len car list to restrict car number at once on screen
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
            

            #see if car is on right side, will go vertical up
            if car.x > 155 and car.y > 100:
                car.detect(0)
                if car.accel_bool:
                    car.accelerate(0)


            #see if car is on top side, will go horizontal left 
            
            elif car.x > 155 and car.y < 100:
                detect_val = screen.get_at((int(car.x)-INFRONT, int(car.y)))
                current_time = pygame.time.get_ticks() / 1000

                if(((int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x)) and (car.drop == False) and (car.dropping != "In Progress")):  #If the car is in its intended drop off location and it hasn't dropped and it isn't dropping
                   car.stop(True)
                   car.dropping = "In Progress"
                   print(car.dropping)
                   if car.start_time_bool:
                       start = pygame.time.get_ticks() / 1000
                       car.start_time_bool = False
                
                   
                elif (detect_val == YELLOW and (car.x >154 and car.x < 500) and (car.drop == False) and (car.dropping != "In Progress")): #If the car in front is dropping and the present car is not dropping
                   car.stop(True)
                   car.dropping = "In Progress"         #A Consideration: If the car in front of the present car stops only slightly at a turn for example, the present car will signify that it is dropping off. As a result, it sometimes doesn't wait as long as a normal dropoff would. If it is a big deal then we can set a timer for 5 seconds or so for  mandatory waiting
                   print("Car in front stopped")
                   
                
                elif (car.dropping =="In Progress"):
                    car.stop(True)
                    if current_time > start + car.time:
                        car.drop = True
                        car.dropping = ""
                else:
                    car.detect(1)
                    if car.accel_bool: 
                        car.accelerate(1)
                
            elif car.x < 156 and car.y > 90:
                #see if car is on left side, will go vertical down
                car.detect(2)
                if car.accel_bool:
                    car.accelerate(2)

                                        
            #get rid of car if it crosses bottom line (memory management)
            if car.y >(SCREEN_HEIGHT - 50) and car.x<(200):
                del car_list[0]
                car_count+=1
                if car_count == 1 and first_car_bool:
                    start_seconds = pygame.time.get_ticks() / 1000
                    first_car_bool = False
                #print("cars crossed:", car_count)
                print(str(car_count) + " cars")
                print("Time elapsed " + str(total_seconds))
                #cars_compare = 100

                #LOOK HERE ANICHAU
                #currently, on every car pass, write time needed
                #if writing time only for all 100 to pass, change cars_compare to 100
                cars_compare = 130
                if car_count == cars_compare:
                    hundred_cars_bool = True
                    done = True

                #fail safe to check if car going down is still red - not dropped off = bug and need to be fixed
                
                '''
                #will go through this later
                if car.color == RED:
                    print("car not dropped off, something wrong")
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
        #my_seconds+=1
        #mytime = my_seconds/60

        
        #print(int(mytime))
        end_seconds = pygame.time.get_ticks() / 1000
        total_seconds = end_seconds - start_seconds
            
        
        # update screen with newly drawn
        pygame.display.flip()
 
    # Close everything
    pygame.quit()
    if hundred_cars_bool:
        body_print = "\n\nMinutes needed for 100 cars to pass: " + str(float(total_seconds/60)) + " with wait time between 10 and 15 seconds"
        print(body_print)

        real_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
        save_path = "/Users/jeffrey/Documents/Github/carsim/files/testing_current"
    
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
