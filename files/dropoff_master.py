#put save states here: 
#while making more edits on most current
#here will be the last fully working most_current.py file

#updated section 4/2/20 10:00AM
#anichau and jeffchen
#signed Jeffrey Chen


'''Things to do:
make cars pull all the way forward
should be a different file for optimized dropoff?
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
do average speed, etc. in mph, work on statistics and testing
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
PERSON_WALK = 175
MAXSPEED = 1.5
ACCEL = 0.5
RANDOMPARAM = 8
INFRONT = 40
SWEEP = 20

#change dt for acceleration change, bigger = faster accel
dt = 0.0006

#set height and width of screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

#pedestrian spawner variables needed
final_ped_time = 0

#things to keep track of during entire program
car_list = []
person_list = []


class Car:
    """
    Class to keep track of a car's location and speed
    """
    def __init__(self):
        self.x = 1250
        self.y = 700
        #if spawning car closer, use x = 150, y = 200
        #self.x = 150
        #self.y = 200

        self.speed = SPEED/2
        self.accel = 0
        self.color = RED

        self.drop_x = 0
        self.drop_y = 0

        self.accel_bool = True
        self.is_dropped = False
        self.start=0
        self.final_time =0 
        self.drop_detect_bool = False

        #time to wait for passengers to get out
        self.wait_time = random.randint(10,15)
        self.in_progress = False
        self.start_time_bool = True
       

    def stop(self, change_color):
        self.speed = 0
        self.accel = 0
        if change_color:
            self.color = YELLOW        

    def detect(self, location):
        
        for sweep in range(-SWEEP, SWEEP):
            for infront in range(20, INFRONT):
                #right
                if location == "right":
                    detect_value = screen.get_at((int(self.x)+sweep, int(self.y)-infront))

                #top
                elif location == "top":
                    detect_value = screen.get_at(((int(self.x)-infront), int(self.y)+sweep))
                    #print("seen")

                #left
                elif location == "left":
                    detect_value = screen.get_at((int(self.x)+sweep, int(self.y)+infront)) 

            #car detection for red, green and yellow    
            if (detect_value==RED) or (detect_value==GREEN) or (detect_value==YELLOW):
                self.accel_bool = False
                self.stop(False)
                return self.accel_bool

        else:
            self.accel_bool = True
            self.accelerate(location)

        return (self.accel_bool)   


    def accelerate(self, location):
        self.ACCEL = self.accel * self.accel * dt
        self.speed = (self.speed + (self.ACCEL))

        if self.speed > MAXSPEED:
            self.speed = MAXSPEED

            #right
            if location == "right":
                self.y += -MAXSPEED
            #top
            elif location == "top":
                self.x += -MAXSPEED
            #left
            elif location == "left":
                self.y += MAXSPEED

        else:
            #right
            if location == "right":
                self.y += -self.speed 
            #top
            elif location == "top":
                self.x += -self.speed
            #left
            elif location == "left":
                self.y += self.speed

        self.accel+= ACCEL

    def drop_detect(self):
        self.drop_detect_bool = False

        for z in range(3, INFRONT):
            for sweep in range(-10, 10):
                detect_val_1 = screen.get_at((int(self.x-z), int(self.y+sweep)))
                detect_val_2 = screen.get_at((int(self.x+sweep), int(self.y) + z))
                if (detect_val_1 == YELLOW) or (detect_val_2 == YELLOW):
                    self.drop_detect_bool = True

        return self.drop_detect_bool



def obj_drop_off(obj):

    if not obj.is_dropped:
        drop_in_front = False

        #If the car is in its intended drop off location and it hasn't dropped and it isn't dropping
        if(not obj.in_progress):  
            obj.stop(True)
            obj.final_time = (pygame.time.get_ticks() / 1000) + obj.wait_time
            obj.in_progress = True

        current_time = pygame.time.get_ticks() / 1000
        if current_time < obj.final_time:
            current_time = pygame.time.get_ticks() / 1000
            obj.stop(True)

        else:
            obj.is_dropped = False
            
    return

#make sure cars do not spawn and overlap
def spawn_detect(x, y):
    car_spawn_bool = True
    #ped_spawn_bool = True

    #if object == "car":
    for width in range(0, 100):
        for height in range(0, 50):
            spawn_value = screen.get_at(( (x + width) , (y + height) ))
            if spawn_value == RED:
                car_spawn_bool = False
                break
                    #return car_spawn_bool
    '''
    elif object == "pedestrian":
        for width in range(-50, 50):
            for height in range(-50, 50):
                spawn_value = screen.get_at(( (x + width) , (y + height) ))
                if spawn_value == GREEN:
                    ped_spawn_bool = False
                    break
                    #return ped_spawn_bool

    #1200, 650
    if object == "car":
        return car_spawn_bool

    elif object == "pedestrian":
        return ped_spawn_bool
    '''
    return car_spawn_bool

class Person:
    """
    Class to make person randomly spawn in 3+ randomly
    generated locations
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = PERSON_SPEED
        self.spawn_point = 0

        #personal_value for WHERE ped will spawn
        self.personal_value = random.randint(0,1)
        self.start_time_bool = True
   
    def stop(self):
        self.speed = 0
 
def pedestrian_spawner(wait, allow):
    global final_ped_time
    
    get_time = True
    ped_current_time = pygame.time.get_ticks() / 1000
    start_spawning = False
    
    if (int(ped_current_time) % wait) == 0:
      
        if get_time:
            start_ped_time = pygame.time.get_ticks() / 1000
            final_ped_time = start_ped_time + allow
            start_spawning = True
            get_time = False

    if (ped_current_time < final_ped_time) and start_spawning:
        person = make_person()
        person_list.append(person)
        ped_current_time = pygame.time.get_ticks() / 1000

    start_spawning = False
    return

def make_car():
    """
    Function to make a new, random car.
    """
    car = Car()
    if random.randint(0,1) == 0:
        car.drop_x = random.randint(77, 250) * 2
    
    else:
        car.drop_y = random.randint(50,150) * 2

    return car


def make_person():
    #person that crosses the street/simulate a sidewalk, 3 possible areas where pedestrians can spawn
    person = Person()

    #top level
    if person.personal_value == 0:
        person.x = 800
        person.y = 230
        person.spawn_point = person.y

    #left side
    elif person.personal_value == 1:
        person.x = 260
        person.y = 450
        person.spawn_point = person.x

    return person
 
def main():

    #rint("input 0 and 0 for no pedestrians, else enter numbers (first entry should be bigger than second)")
    #input_ped_wait = int(input("how long of an interval between pedestrians walking across? "))
    #input_ped_allow = int(input("how long for the flow of pedestrians after interval? "))
    #fix this input later
    input_ped_wait = 20
    input_ped_allow = 3

    pygame.init()
    pygame.display.set_caption("PHS Car Traffic")
 
    # Loop until the user clicks the close button.
    done = False
    hundred_cars_bool = False
    car_count = 0
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    #make first car and person
    car = make_car()
    car_list.append(car)
    first_cross = make_person()
    person_list.append(first_cross)

    #pedestrian spawn variables (for interval purposes)
    #my_seconds = 0
    start_seconds = 0
    start_seconds_bool = True
    end_seconds = 0
    total_seconds = 0
    first_car_bool = True
    initial_time_bool = True
    Ped_walk_bool = False
    ped_time = False
    
 
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
        
        #spawner logic

        #view finding of rectangle to make sure nearest car is out of area to prepare for spawn
        #check if random match and there is a car within rectangular area of start
        
        if ((random.randint(1, RANDOMPARAM)) == 3) and spawn_detect(1200, 650):
            car = make_car()
            car_list.append(car)
        
        pedestrian_spawner(input_ped_wait,input_ped_allow)
 
        # --- car logic
        for car in car_list:
            #Move the car's center, check for position to move car where
            #car.detect function contains acceleration function
            
            #see if car is on right side, will go vertical up
            if car.x > 155 and car.y > 100:
                car.detect("right")

            #see if car is on top side, will go horizontal left 
            elif car.x > 155 and car.y < 100:
                car.detect("top")

                drop_bool = (int(car.x)==car.drop_x) or (int(car.x-1) == car.drop_x)
                should_drop_now = car.drop_detect()
                if drop_bool or (should_drop_now and (car.x > 150 and car.x < 500)):
                    obj_drop_off(car)
                    #cancel the car drop y value if it had it but dropped early
                    car.drop_y = None
                
                
                
                
            #see if car is on left side, will go vertical down
            elif car.x < 156 and car.y > 90:
                car.detect("left")

                drop_bool = (int(car.y)==car.drop_y) or (int(car.y-1) == car.drop_y)
                should_drop_now = car.drop_detect()
                if drop_bool or (should_drop_now and (car.y > 100 and car.y < 350)):
                    obj_drop_off(car)
                
                

                                        
            #get rid of car if it crosses bottom line (memory management)
            if car.y >(SCREEN_HEIGHT - 50) and car.x<(200):
                del car_list[0]
                car_count+=1
                if car_count == 1 and first_car_bool:
                    start_seconds = pygame.time.get_ticks() / 1000
                    first_car_bool = False
                  
                print(str(car_count) + " cars")
                print("Time elapsed " + str(total_seconds))
              
                #currently, on every car pass, write time needed
                #if writing time only for all 100 to pass, change cars_compare to 100
                cars_compare = 130
                if car_count == cars_compare:
                    hundred_cars_bool = True
                    done = True

                #fail safe to check if car going down is still red - not dropped off = bug and need to be fixed
                if car.color == RED:
                    print("car not dropped off, something wrong")
                    done = True
                
        #pedestrian logic
      
            
        for person in person_list:

            person_bool = True
           
            #person coming from top leg
            if person.personal_value == 0:
                for y in range(10,20):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at(((int(person.x) + person_sweep), int(person.y) -y))
                        if person_infront==RED or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.y -= PERSON_SPEED

            #person coming from left leg
            elif person.personal_value == 1:
                for x in range(10,20):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at((int(person.x)-x, int(person.y)+person_sweep))
                        
                        if person_infront==RED or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.x -= PERSON_SPEED

            #always check if person has walked PERSON_WALK pixels, then erase from list (memory management)
            #delete from top leg
            if((person.personal_value == 0) and (abs(person.spawn_point - person.y) > PERSON_WALK)):
                del(person_list[0])

            #delete from right leg
            elif((person.personal_value== 1) and (abs(person.spawn_point - person.x) > PERSON_WALK)):
                del(person_list[0])

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        
        #draw the road
        pygame.draw.rect(screen, BLACK, (100, 50, 1200, 100))
        pygame.draw.rect(screen, BLACK, (1200, 50, 100, 700))
        pygame.draw.rect(screen, BLACK, (100, 50, 100, 700))
        
        #cars will drop off in these zones
        pygame.draw.rect(screen, BLUE, (500, 150, 10, 10))
        pygame.draw.rect(screen, BLUE, (500, 40, 10, 10))
        pygame.draw.rect(screen, BLUE, (200, 300, 10,10))
        pygame.draw.rect(screen, BLUE, (90, 300, 10,10))

        # draw all moving objects
        
        for car in car_list:
            pygame.draw.circle(screen, car.color, [int(car.x), int(car.y)], CAR_SIZE)

        for person in person_list:
            pygame.draw.circle(screen, GREEN, [int(person.x), int(person.y)], 7)
        
 
        # --- Wrap-up, limit to 60 frames per second
        clock.tick(60)
        
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
        #save_path = "/Users/Anirudh/Documents"
        save_path = "/Users/jeffrey/Documents/Github/carsim/files/testing_current"
    
        filestring = "rawdata- " + str(real_time) + ".txt"
        complete_name = os.path.join(save_path, filestring)
        
        f = open(complete_name, "a+")

        #various hundred car trials below
        if input_ped_allow == 0 and input_ped_wait == 0:
            f.write("Time Elapsed for 100 Cars, No Pedestrians")
        

        #do this one later
        #f.write("Time Elapsed for 100 Cars, Randomly Spawned Pedestrians")
        
        else:
            body_text = "Time Elapsed for 100 Cars, %s seconds pedestrian flow, %s seconds interval between flow" %input_ped_allow %input_ped_wait
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 10 Second Intervals")
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 20 Second Intervals")
        #f.write("Time Elapsed for 100 Cars, Pedestrians in 30 Second Intervals")

        f.write(body_print)
        f.write("\n\n=================================================")
        f.close()

 
if __name__ == "__main__":
    main()