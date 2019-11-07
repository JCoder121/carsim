#updated section 9/24/19 6:00PM
#anichau and jeffchen
#signed jeffrey chen

import pygame
import random
import math
import sys
import tkinter

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

PASSENGERS ARE STILL NOT WORKING - CAR NEEDS TO BE ABLE TO WAIT
2 options - have make_passenger inside the main loop make it however many times OR
have make_passenger in def function have the number of passengers to make

output things to a file to make more realisitc - at this point in time, make timestamp and write a line about car

future plans: film directly translate to simulation - read in and reflect (through drone)
'''

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)

#define other variables 
CAR_SIZE = 15
SPEED = 1
PERSON_SPEED = 1.5
PERSON_WALK = 200
MAXSPEED = 2
ACCEL = 0.03
RANDOMPARAM = 10
INFRONT = 35
SWEEP = 20

# wait time is currently unncessary
#WAITTIME = 10000
#change dt for acceleration change, bigger = faster accel
dt = 0.004
#dt = 1
car_list = []
person_list = []
passenger_list = []

#get screen size with tkinter
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#print(screen_width)

#subtract on the height because there are borders and everything
size = [screen_width, int(screen_height*0.95)]
screen = pygame.display.set_mode(size)


class Car:
    """
    Class to keep track of a car's location and speed
    """
    def __init__(self):
        self.x = screen_width *0.865
        self.y = screen_height * 0.75
        #testing for self.y = 300
        self.speed = SPEED/2
        self.accel = 0
        self.color = RED
        self.passenger_num = random.randint(2,4)
        self.passenger_check = 0

        '''
        self.waiting_time = 0
        self.now_time = 0
        '''

        self.drop_val = -1
        self.drop_x = 0
        self.drop_y = 0
        self.accel_bool = True
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

class Passenger:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.initial = -1
        self.passenger_value = -1
        self.speed = PERSON_SPEED
        self.color = BLUE
        self.top = True

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
        car.drop_x = random.randint(int(screen_width*.14), int(screen_width*.5))

    elif car.drop_val == 1:
        car.drop_y = random.randint(int(screen_height*0.17), int(screen_height)*0.6)

    return car


def make_person():
    #person that crosses the street/simulate a sidewalk, 3 possible areas where pedestrians can spawn
    person = Person()

    #right side
    if person.personal_value == 0:
        person.x = screen_width*0.79
        person.initial = person.x
        person.y = screen_height*0.4

    #top level
    elif person.personal_value == 1:
        #person.x = 800
        person.x = screen_width * 0.4
        person.y = screen_height*0.3
        person.initial = person.y

    #left side
    elif person.personal_value == 2:
        person.x = screen_width*0.2
        person.initial = person.x
        person.y = screen_height*0.5

    return person
 

#make_passenger(car.drop_x, car.y -15)
def make_passenger(x, y):
    passenger = Passenger()
    passenger.x = x
    passenger.y = y
    passenger.initial = y
    passenger.top = True
    passenger_list.append(passenger)

    return passenger

    #make passenger students that exit from the dropped off cars
 
def main():
    '''
    This is our main program.
    '''
    #start program and give name
    pygame.init()
    pygame.display.set_caption("PHS Car Traffic")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    wait_list = [10,200000,30000000]

    car = make_car()
    car_list.append(car)
    first_cross = make_person()
    person_list.append(first_cross)
 
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
                        spawn_value = screen.get_at(( int(screen_width*0.835) , int(screen_height*0.75) ))
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
            person = make_person()
            person_list.append(person)
        
 
        # --- car logic
        for car in car_list:
            #Move the car's center, check for position to move car where
            car.accel_bool = True
            car.pass_bool = True

            car.waiting_time = pygame.time.get_ticks()

            #print(passenger_list)
            #cooldown?

            #print(car.waiting_time)
            #see if car is on right side, will go vertical up

            turn_left_val = 0.17
            if car.x > screen_width/2 and car.y > screen_height*turn_left_val:
                car.detect(0)
                if car.accel_bool:
                    car.accelerate(0)


            #see if car is on top side, will go horizontal left 
            elif car.x > screen_width*0.14 and car.y < screen_height*turn_left_val:
                if car.drop_val ==0:
                    #while(int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x) or (int(car.x+1)==car.drop_x):  
                    if(int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x) or (int(car.x+1)==car.drop_x):  
                        #car.stop(True)
                        

                        for x in range(0, car.passenger_num):
                            car.stop(True)
                            make_passenger(int(car.x), int(car.y))
                            #passenger.top = True

                        car.x -= 4
                        
                #car.x-=4
                #^current dropoff function no passenger spawn

                #further passenger spawn testing below

                
                '''
                if car.drop_val == 0:
                    if(int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x) or (int(car.x+1)==car.drop_x):  
                        
                        car.stop(True)
                        #make_passenger(int(car.x), int(car.y)-10, car.passenger_num)
                        #print('entered')
                        
                        #for x in range(0, car.passenger_num):
                        quick_val = 0
                        pass_bool = True
                        #print(pass_bool)
                        while (quick_val <= car.passenger_num):
                            car.stop(True)
                            for width in range(-5, 5):
                                for y in range(0, 30):
                                    if screen.get_at((int(car.x) + width, int(car.y) - y)) != BLUE:
                                        pass_bool = True
                            
                            if(pass_bool):
                                car.stop(True)
                                passenger = make_passenger(int(car.x), int(car.y)-10)
                                passenger.passenger_value = 0
                                passenger_list.append(passenger)
                                quick_val +=1
                            
                    
                        car.x -=4
                '''
                
                car.detect(1) 
                if car.accel_bool:                    
                    car.accelerate(1)


            elif car.x < screen_width*0.14 and car.y > screen_height*0.02:

                #see if car is on left side, will go vertical down
                if car.drop_val == 1:
                    if(int(car.y)==car.drop_y) or (int(car.y-1)==car.drop_y):   
                        car.stop(True) 
                        #passenger.top = False
                        car.y+=4
                        #^working dropoff no passenger spawn

                #passenger drop-off testing goes below

                        #for y in range(0, wait_list[random.randint(0,2)]):
                        #car.now = pygame.time.get_ticks()

                    
                        #for x in range(0, )

                
                '''
                if car.pass_bool:
                    passenger = make_passenger(car.x-15, car.drop_y)
                    passenger.initial = car.x
                    passenger_list.append(passenger)
                    passenger.passenger_value = car.drop_val
                    car.pass_bool = False


                '''

                car.detect(2)
                if car.accel_bool:
                    car.accelerate(2)
                                        
            #get rid of car if it crosses bottom line (memory management)
            if car.y >(screen_height*0.85) and car.x<(screen_width/2):
                del car_list[0]
                #fail safe to check if car going down is still red - not dropped off = bug and need to be fixed
                if car.color == RED:
                    print("car not dropped off, something wrong")
                    done = True


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
                    for person_sweep in range(-10, 10):
                        person_infront = screen.get_at(((int(person.x) + person_sweep), int(person.y) -y))
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.y -= PERSON_SPEED

            #person coming from left leg
            elif person.personal_value == 2:
                for x in range(10,20):
                    for person_sweep in range(-10, 10):
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


        #exiting passenger logic
        for passenger in passenger_list:
            #need distance check to erase
            
            #top leg passenger
            if passenger.top:
                passenger.y += -PERSON_SPEED/2
            '''
            if passenger.y<(screen_height*0.02):
                passenger.y += -PERSON_SPEED/2
            '''

            '''
            if passenger.passenger_value == 0:
                passenger.y += -PERSON_SPEED/2
                if (abs(passenger.initial - passenger.y) > 60):
                    del(passenger_list[0])
                
            #left leg passenger
            elif passenger.passenger_value == 1:
                passenger.x += -PERSON_SPEED/2
                if(abs(passenger.initial - passenger.x) > 60):
                    del(passenger_list[0])
            '''

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        
        road_width = 100
        road_vert = screen_height*0.70
        #draw the road
        #template: (x, y, width, height)
        #top side of road
        pygame.draw.rect(screen, BLACK, (screen_width*0.1, 100, screen_width*0.75, road_width))
        #right side of road
        pygame.draw.rect(screen, BLACK, ((screen_width*0.9-road_width), 100, road_width, road_vert))
        #left side of road
        pygame.draw.rect(screen, BLACK, (screen_width*0.1, 100, road_width, road_vert))
        
        # draw all moving objects
        for car in car_list:
            pygame.draw.circle(screen, car.color, [int(car.x), int(car.y)], CAR_SIZE)

        for person in person_list:
            pygame.draw.circle(screen, GREEN, [int(person.x), int(person.y)], 7)

        for passenger in passenger_list:
            pygame.draw.circle(screen, passenger.color, [int(passenger.x), int(passenger.y)], 8)
        
        # --- Wrap-up, limit to 60 frames per second
        clock.tick(60)
 
        # update screen with newly drawn
        pygame.display.flip()
 
    # Close everything 
    pygame.quit()
 
if __name__ == "__main__":
    main()