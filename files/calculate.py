#take in data and calculate using number praser
#no passengers
#will need to take in first line and print tha ONtCE (no ped, 1 ped every second, etc)

import glob
import os

#NEED A TITLE

data_list = []
path = "/Users/jeffrey/Documents/Github/carsim/files/testing_current/*.txt"

files = glob.glob(path)

#find integers in all folders: seconds for cars to pass
for name in files:
    with open(name) as f:
    	
    	for line in f:
    		try:
    			value = int(line)
    			data_list.append(value)
    		except ValueError:
    			pass

    	f.close()


#caluculate statistics
average = 0
car_sum = 0
for item in data_list:
	car_sum += item

average = car_sum / (len(data_list))

with open
print("\naverage seconds needed: %0.2f" % average)


print("done")