import matplotlib.pyplot as plt
import random

# Model Variables:
    
#Inventory:
STARTING_INVENTORY_UNITS = 100 #inventory level at the begining of period
BATCH_PRODUCTION_AMOUNT = 1 #units produced during a period
PRODUCTION_INVERVAL = 1 #number of periods separating the output periods
INVENTORY_DRAW_THRESHOLD = 30


PRODUCTION_PERIODS_ON = 30
PRODUCTION_PERIODS_OFF = 30

#Fleet:
FLEET_SIZE = 7 #number of vehicles in the fleet
VEHICLE_CAPACITY = 5 #number of units a vehicle can transport
PICKUP_PERIOD = 5
# VEHICLE_TURNAROUND_TIME = 70

#Turnaround distribution parameters:
LOWER_LIMIT = 40
MU = 90
SIGMA = 17

#Evaluation: 
EVALUATION_INTERVAL = 1000 #number of periods during which the optimization is performed

def inventory_increment(begining_inventory, production, draw): 
    ending_inventory = begining_inventory + production - draw
    return ending_inventory

def batch_produce(period_counter, PRODUCTION_INVERVAL, BATCH_PRODUCTION_AMOUNT):
    '''
    Facility generates product every specified production interval.

    '''
    if period_counter % PRODUCTION_INVERVAL == PRODUCTION_INVERVAL - 1:
        return BATCH_PRODUCTION_AMOUNT
    else:
        return 0
    
def distribution(LOWER_LIMIT, MU, SIGMA):

    flag = True
    
    while flag:
        random_number = random.gauss(MU,SIGMA)
        if random_number < LOWER_LIMIT:
            pass
        else:
            flag = False
    return random_number

def main():
    
    assert INVENTORY_DRAW_THRESHOLD >= VEHICLE_CAPACITY #make sure a vehicle does not draw down more units than are available in inventory


    eop_inventory = [STARTING_INVENTORY_UNITS] # end of period product inventory list
    periods_passed_record = [] # history of periods passed
    available_vehicles = FLEET_SIZE # number of vehicles ready for loading, insantiated with the fleet size number
    in_transit_vehicles = [] # list of vehicles in delivery
    available_vehicle_record = [] #history of available vehile created for plotting purposes
    vehicle_turnaround_record = [] #history of turnaround times each vehicle has clocked
    
    period_counter = 0
    pickup_counter = PICKUP_PERIOD
    
    production_periods_on_counter = 0
    production_periods_off_counter = 0
    
    
    while period_counter < EVALUATION_INTERVAL:
        
        ###___This piece of code makes it so that vehicles pick up material only so often___###
        pickup_counter += 1
        if pickup_counter > PICKUP_PERIOD:
            pickup_counter = 0
        ###____________________________###
    
    
        ### THIS PIECE OF CODE MAKES THE CONTINUOUS PRODUCTION STEPWISE ###
        if production_periods_on_counter < PRODUCTION_PERIODS_ON:
            BATCH_PRODUCTION_AMOUNT_CURRENT = BATCH_PRODUCTION_AMOUNT
            production_periods_on_counter += 1
        else:
            BATCH_PRODUCTION_AMOUNT_CURRENT = 0
            production_periods_off_counter += 1
        
        if production_periods_on_counter + production_periods_off_counter == PRODUCTION_PERIODS_ON + PRODUCTION_PERIODS_OFF:
            production_periods_on_counter = 0
            production_periods_off_counter = 0
        ### _________________________________________# 
        
        
    
    
    
    
        available_vehicle_record.append(available_vehicles) # Records number of vehicles available per period.
    
        PERIOD_PRODUCTION = batch_produce(period_counter, PRODUCTION_INVERVAL, BATCH_PRODUCTION_AMOUNT_CURRENT) #responsible for increasing inventory by material produced.
        
        ###___This piece of code reduces inventory if a pickup is made___###
        if eop_inventory[-1] >= INVENTORY_DRAW_THRESHOLD and available_vehicles > 0 and pickup_counter == PICKUP_PERIOD:
            
            '''# ###___This part handles sending out multiple vehicles___###
            # potential_for_loading = int(eop_inventory[-1] / VEHICLE_CAPACITY) #this many vehicles could potentially be loaded
            # if available_vehicles>=potential_for_loading:
            #     loads  = potential_for_loading #load what is available since there are more vehicles then the product
            # else:
            #     loads = available_vehicles #load only the available vehicles
            # ####_________###'''
            
            loads = 1
            
            eop_inventory.append(inventory_increment(eop_inventory[-1], PERIOD_PRODUCTION, loads*VEHICLE_CAPACITY))
            available_vehicles -= loads  #vehicle leaves  
    
            for load in range(1,loads+1):
    
                in_transit_vehicles.append(load)
    
        else:
            eop_inventory.append(inventory_increment(eop_inventory[-1], PERIOD_PRODUCTION, 0))
        ###_________________________________________###
        
        in_transit_vehicles = [x+1 for x in in_transit_vehicles] #keeps track of how many periods each vehicle in on the road.
        
        ###___adds vehicles back to available vehicle inventory___##
        for index, vehicle in enumerate(in_transit_vehicles): 
            VEHICLE_TURNAROUND_TIME = distribution(LOWER_LIMIT, MU, SIGMA)

            if vehicle > VEHICLE_TURNAROUND_TIME:
                in_transit_vehicles.pop(index)
                available_vehicles += 1
                
                vehicle_turnaround_record.append(VEHICLE_TURNAROUND_TIME)
        ###___________________________###
        
        periods_passed_record.append(period_counter) #adds the current period to the record
        period_counter +=1 #increments time by 1 to move to a new period.
        
    
    plt.plot(eop_inventory)
    plt.xlabel('Period')
    plt.ylabel('Units in Inventory')
    plt.title('End of Period Inventory')
    plt.show()
    
    plt.plot(available_vehicle_record, c='orange')
    plt.title('End of Period Vehicles Available')
    plt.xlabel('Period')
    plt.ylabel('Vehicles Available')
    plt.show()
    
    plt.plot(vehicle_turnaround_record, c='red')
    plt.title('Record of Vehicle Trunaround Times')
    plt.xlabel('Period')
    plt.ylabel('Vehicle Turnaround Times')
    plt.show()



main()




