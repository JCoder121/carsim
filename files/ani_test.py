#updated section 9/16/19 4:50PM
#anichau and jeffchen

#decelerating is still a question

import pygame
import random
import math
import sys

'''
notes:
YELLOW CARS = HAVE DROPPED OFF ALREADY
deceleration function?
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
SPEED = 1
PERSON_SPEED = 1.5
MAXSPEED = 2
ACCEL = 0.5
RANDOMPARAM = 10
INFRONT = 35
SWEEP = 20
WAITTIME = 10000
#change dt for acceleration change, bigger = faster accel
dt = 0.006

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
        self.speed = SPEED/2
        self.y_accel = 0
        self.x_accel = 0
        self.color = RED

        self.drop_val = -1
        self.drop_x = 0
        self.drop_y = 0

        self.drop_bool = True
        self.accel_bool = True
        self.is_dropped = False


    def stop(self, the_drop_bool):
        self.speed = 0
        self.y_accel = 0
        self.x_accel = 0
        if the_drop_bool == True:
            self.color = YELLOW        


    def detect(self, detect_var):
        #right 
        if detect_var == 0:
            for sweep in range(-SWEEP, SWEEP):
                for infront in range(20, INFRONT):
                    value1 = screen.get_at((int(self.x)+sweep, int(self.y)-infront))
                    
                    if (value1 == RED) or (value1 == GREEN) or (value1 == YELLOW):
                        self.accel_bool = False
                        self.stop(False)
                        return self.accel_bool
 
        #top
        elif detect_var == 1:
            for sweep in range(-SWEEP, SWEEP):
                for infront in range(20, INFRONT):    
                    value1 = screen.get_at(((int(self.x)-infront), int(self.y) + sweep))
                    
                    if (value1 == RED) or (value1 == GREEN) or (value1 == YELLOW):
                        self.accel_bool = False
                        self.stop(False)
                        return self.accel_bool

        #left
        elif detect_var == 2:
            #sweep allows for it to be a rectangle object detection
            for sweep in range(-SWEEP, SWEEP):
                for infront in range(20,INFRONT):
                    value1 = screen.get_at((int(self.x)+sweep, int(self.y)+infront))  

                    if (value1 == RED) or (value1 == GREEN) or (value1 == YELLOW):
                        self.accel_bool = False   
                        self.stop(False)
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
    car.drop_val = random.randint(0,1)

    if car.drop_val == 0:
        car.drop_x = random.randint(77, 400) * 2

    elif car.drop_val == 1:
        car.drop_y = random.randint(62, 300) *2

    return car


def make_person():
    #make person function that crosses the street and simulate a sidewalk
    #3 possible areas where pedestrians can spawn
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

class Passenger:
    """
    Class to make person randomly spawn from cars
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = PERSON_SPEED
        self.initial = 0

def make_passenger(car):
    #make passenger function that will get dropped off in Dropoff zone
    passenger = Passenger()
    if ((car.drop_val == 0)):
        passenger.x =  car.x +20
        passenger.initial = passenger.x
        passenger.y = car.y
    if (car.drop_val == 1):
        passenger.x = car.x
        passenger.y = car.y +20
        passenger.initial = car.y

    return passenger
 
def drop_off(car, person):
    drop_off_bool = False
    rand = random.randint(1,4)
    print("This is car x cord " + str(car.x))
    passenger_list = []
    for i in range(rand):
        passenger = make_passenger(car)
        passenger_list.append(passenger)
        if (car.drop_val == 0) :
            passenger.x =  car.x +20
            print("This is passenger x cord " + str(passenger.x))
            passenger.y = car.y
            print("This is passenger initial cord " + str(passenger.initial))
            passenger.initial = passenger.y
            print("This is passenger.y " + str(passenger.y))
        if (car.drop_val == 1):
            passenger.x = car.x
            passenger.y = car.y +20
            passenger.initial = car.y

        print("in dropoff function")
        pygame.draw.circle(screen, GREEN, (int(passenger.x), int(passenger.y)),7)
        if(car.drop_val == 0):  # Could change to correspond to drop off zone
            print("in")
            print("Diff: " + str(abs(passenger.initial - passenger.y)))
            while (abs(passenger.initial - passenger.y) < 50):
                for passenger in passenger_list:
                    pygame.draw.circle(screen, GREEN, [int(passenger.x), int(passenger.y)],7)
                passenger.y = passenger.y - 1.5
                print("in passenger")
                print("This is passenger initial cord " + str(passenger.y))
                print("Diff: " + str(abs(passenger.initial - passenger.y)))
        if (car.drop_val ==1):
            while (abs(passenger.initial - passenger.x) < 50):
                pygame.draw.circle(screen, GREEN, [int(passenger.x), int(passenger.y)],7)
                passenger.x -= 1.5
        
            
def main():
    '''
    This is our main program.
    '''
    pygame.init()
    pygame.display.set_caption("PHS Car Traffic")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    car_list = []
    person_list = []
   

    car = make_car()
    car_list.append(car)
    first_cross = make_person()
    person_list.append(first_cross)
 
    # -------- Main Program Loop -----------
    print(car.drop_val)
    
    while not done:
        # --- Event Processing
    
        
        for event in pygame.event.get():

             #on sublime, use below
            '''
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
'''
            #on IDLE, use below
            
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
        '''if (random_car==3) and spawn_bool:
        #and len(car_list)<4: - len car list to restrict car number at once on screen
            car = make_car()
            car_list.append(car)
'''
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

            #see if car is on right side, will go vertical up
            if car.x > 155 and car.y > 100:
                car.detect(0)
                if car.accel_bool:
                    car.accelerate(0)


            #see if car is on top side, will go horizontal left 
            elif car.x > 155 and car.y < 100:
                if car.drop_val == 0:
                    #print(car.x, car.drop_x)
                    #if int(car.x) == car.drop_x:
                    if(int(car.x)==car.drop_x) or (int(car.x-1)==car.drop_x) or (int(car.x+1)==car.drop_x):          
                        car.stop(True)
                        drop_off(car, person)
                        print("Dropoff")
                        car.x -= 4

                car.detect(1) 
                if car.accel_bool:                    
                    car.accelerate(1)


            elif car.x < 155 and car.y > 90:
                #see if car is on left side, will go vertical down
                
                if car.drop_val == 1:
                    #print(car.y, car.drop_y)
                    #print('dropped(car)')
                    if(int(car.y)==car.drop_y) or (int(car.y-1)==car.drop_y) or (int(car.y+1)==car.drop_y):          
                        car.stop(True)
                        drop_off(car,person)
                        print("Dropoff")

                        car.y +=4

                car.detect(2)
                if car.accel_bool:
                    car.accelerate(2)

                                        
            #get rid of car if it crosses bottom line (memory management)
            if car.y >(SCREEN_HEIGHT - 50) and car.x<(200):
                del car_list[0]


        #pedestrian logic
        for person in person_list:

            person_bool = True

            if person.personal_value == 0:
                #simple personobj detection:
                #coming from right
                for x in range(10, 25):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at(((int(person.x)-x), int(person.y) + person_sweep))
                        if person_infront==RED or person_infront==GREEN:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.x -= PERSON_SPEED

            #person coming from top
            elif person.personal_value == 1:
                for y in range(10,25):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at(((int(person.x) + person_sweep), int(person.y) +y))
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.y += PERSON_SPEED

            #person coming from left leg
            elif person.personal_value == 2:
                for x in range(10,25):
                    for person_sweep in range(-4, 4):
                        person_infront = screen.get_at((int(person.x)+x, int(person.y)+person_sweep))
                        if person_infront==RED or person_infront==GREEN or person_infront==YELLOW:
                            person.stop()
                            person_bool = False

                if person_bool:
                    person.x += PERSON_SPEED
            
            #always check if person has walked 225 pixels, then erase from list (memory management)
            if((person.personal_value == 0 or person.personal_value== 2)
               and (abs(person.initial - person.x) > 225)):
                del(person_list[0])

            elif((person.personal_value == 1)
                 and abs(person.initial - person.y) > 225):
                del(person_list[0])

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
        #draw the road
        pygame.draw.rect(screen, BLACK, (100, 50, 1200, 100))
        pygame.draw.rect(screen, BLACK, (1200, 50, 100, 700))
        pygame.draw.rect(screen, BLACK, (100, 50, 100, 700))
        
        # draw everything
        
        for car in car_list:
            pygame.draw.circle(screen, car.color, [int(car.x), int(car.y)], CAR_SIZE)

        for person in person_list:
            pygame.draw.circle(screen, GREEN, [int(person.x), int(person.y)], 7)
 
        # --- Wrap-up, limit to 60 frames per second
        clock.tick(60)
        #print(car.x,car.y)
        #print(car.drop_val)
 
        # update screen with newly drawn
        pygame.display.flip()
 
    # Close everything 
    pygame.quit()
 
if __name__ == "__main__":
    main()

