# Copyright Sebastian Puchalski 2022

#Import required libraries:
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import webbrowser

plt.rcParams.update({'font.size': 8})


def inventory_increment(begining_inventory, production, draw): 
    '''
    Increments the inventory accounting for production and drawdown.
    '''
    
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
    
    '''
    Creates a random vehicle turnaround time.
    '''

    flag = True
    
    while flag:
        random_number = random.gauss(MU,SIGMA)
        if random_number < LOWER_LIMIT:
            pass
        else:
            flag = False
    return random_number


def main(STARTING_INVENTORY_UNITS, BATCH_PRODUCTION_AMOUNT, PRODUCTION_INVERVAL, INVENTORY_DRAW_THRESHOLD, FLEET_SIZE, VEHICLE_CAPACITY, PICKUP_PERIOD, LOWER_LIMIT=0, MU=0, SIGMA=0, EVALUATION_INTERVAL=0, PRODUCTION_PERIODS_ON=1, PRODUCTION_PERIODS_OFF=0):
       
    
    PICKUP_PERIOD = PICKUP_PERIOD - 1 #adjusts the variable so that input of 1 translates into pickup every period.
    
    #assert INVENTORY_DRAW_THRESHOLD >= VEHICLE_CAPACITY #make sure a vehicle does not draw down more units than are available in inventory

    if LOWER_LIMIT > MU: #avoids issues created by entering a lower number for average vehicle turnaround than the lower turnaround limit
        pass
    
    else:

        eop_inventory = [STARTING_INVENTORY_UNITS] # end of period product inventory list
        periods_passed_record = [] # history of periods passed
        available_vehicles = FLEET_SIZE # number of vehicles ready for loading, insantiated with the fleet size number
        in_transit_vehicles = [] # list of vehicles in delivery
        available_vehicle_record = [] #history of available vehicle created for plotting purposes
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
            
            # if INVENTORY_DRAW_THRESHOLD < VEHICLE_CAPACITY:
            #     INVENTORY_DRAW_THRESHOLD = VEHICLE_CAPACITY

                
            # else:
                # pass
            
            # if eop_inventory[-1] >= INVENTORY_DRAW_THRESHOLD and available_vehicles > 0 and pickup_counter == PICKUP_PERIOD:
            if eop_inventory[-1] >= INVENTORY_DRAW_THRESHOLD+VEHICLE_CAPACITY and available_vehicles > 0 and pickup_counter == PICKUP_PERIOD:
                
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
        
    
        
    return eop_inventory, available_vehicle_record, vehicle_turnaround_record


def plot(data):
    
    '''Plots the emvs in the GUI window'''
        
    data_a = data[0] #eop_inventory
    data_b = data[1] #available_vehicle_record
    data_c = data[2] #vehicle_turnaround_record

    figure1 = plt.Figure(figsize=(.4*WIDTH,4), dpi=90)
    ax1 = figure1.add_subplot(111)
    ax1.grid()
    ax1.locator_params(axis="both", integer=True, tight=True)
    ax1.text(len(data_a), data_a[-1], data_a[-1], size=10) #labels the last point on the graph
    ax1.plot(data_a, color = '#E6A700' )
    
    
    figure2 = plt.Figure(figsize=(.4*WIDTH,4), dpi=90)
    ax2 = figure2.add_subplot(111)
    ax2.grid()
    ax2.locator_params(axis="both", integer=True, tight=True)
    ax2.plot(data_b, color = '#DD2E1F')

    figure3 = plt.Figure(figsize=(.4*WIDTH,4), dpi=90)
    ax3 = figure3.add_subplot(111)
    ax3.grid()
    ax3.locator_params(axis="x", integer=True, tight=True)
    if len(data_c)>0:
        ax3.text(len(data_c), data_c[-1], len(data_c), size=10) #labels the last point on the graph
    else:
        pass
    ax3.plot(range(1, len(data_c)+1), data_c, color = '#7C5BBB')
    

             
    if len(frame_plot_1.winfo_children())==0:
        pass
    else:
        for item in frame_plot_1.winfo_children():
            item.destroy()
            
            
    if len(frame_plot_2.winfo_children())==0:
        pass
    else:
        for item in frame_plot_2.winfo_children():
            item.destroy()
 
    if len(frame_plot_3.winfo_children())==0:
        pass
    else:
        for item in frame_plot_3.winfo_children():
            item.destroy()
 

    scatter = FigureCanvasTkAgg(figure1, frame_plot_1)    
    scatter.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
    
    scatter = FigureCanvasTkAgg(figure2, frame_plot_2)    
    scatter.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
  
    scatter = FigureCanvasTkAgg(figure3, frame_plot_3)    
    scatter.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)

    ax1.set_xlabel('Period')
    ax1.set_title('End of Period Inventory')


    ax2.set_xlabel('Period')
    ax2.set_title('Vehicles Available at the End of Period')

    ax3.set_xlabel('Completed Turnarounds')
    ax3.set_ylabel('Recorded Time [periods]')
    ax3.set_title('Record of Vehicle Turnaround Times')




'''_________________GUI START___________________________'''


FONT_SIZE = 40

#Canvas Dimensions:
HEIGHT = 650
WIDTH = 1200

#Frame Dimensions:
FRAME_HEIGHT = 35
FRAME_HEIGHT_INCREMENT=.1
FRAME_Y_POSITION = 120
FRAME_WIDTH = 282/WIDTH
FRAME_X_POSITION = 152/WIDTH


#Fonts:
FONT='Helvetica 10 bold'


#Colors:
CANVAS_COLOR = '#CFEDFB'
FRAME_COLOR = "#68C7EC"
LABEL_COLOR = '#00A0DC'
FG_LABEL_COLOR = 'white'
BUTTON_COLOR='#fedb00'
TEXT_BUTTON_COLOR='#003a7e'
ALTERNATIVE_FRAME_COLOR='#D8CCF4'
ALTERNATIVE_LABEL_COLOR = '#A589D9'


#Plot positions:
PLOT_1_X_POSITION = .17
PLOT_2_X_POSITION = .5
PLOT_3_X_POSITION = .83
PLOT_RELATIVE_WIDTH = 385/WIDTH
PLOT_RELATIVE_HEIGHT = .45
# PLOT_RELATIVE_HEIGHT = 280/HEIGHT





root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg=CANVAS_COLOR)
canvas.pack(fill="both", expand=True)


'''_________Title_________'''
second_frame = tk.Frame(root, bg=CANVAS_COLOR, bd=5)
second_frame.place(relx = 0.5, y=10, relwidth=.4, height=80, anchor='n')

label = tk.Label(second_frame, text='Why Work Weak?\nFleet Sizing Made Easy',bg=CANVAS_COLOR,fg= FRAME_COLOR,font='Helvetica 25 bold')
label.place(relx=0, relwidth=1, relheight=1)


'''_________Credit_________'''

second_frame = tk.Frame(root, bg=CANVAS_COLOR, bd=5)
second_frame.place(relx = 0.5, rely=0.96, relwidth=.4, height=30, anchor='n')

label = tk.Label(second_frame, text='Copyright belongs to Sebastian Puchalski, 2022',bg=CANVAS_COLOR,fg=FRAME_COLOR, font='Helvetica 10 bold')
label.place(relx=0, relwidth=1, relheight=.9)





#INVENTORY INPUT:



ORDER = 1

X_POSITION = FRAME_X_POSITION
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Inventory Input:',bg=FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)



ORDER = 2

X_POSITION = FRAME_X_POSITION
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Starting inventory level [units]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r1 = tk.Entry(second_frame, font = FONT_SIZE)
c1r1.place(relx=0.72, relwidth=0.28, relheight=.9)


ORDER = 3

X_POSITION = FRAME_X_POSITION
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Minimum inventory level [units]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r4 = tk.Entry(second_frame, font = FONT_SIZE)
c1r4.place(relx=0.72, relwidth=0.28, relheight=.9)









#PRODUCTION INPUT

ORDER = 1

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Production Rate Input:',bg=FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)



ORDER = 2

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Production amount [units]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r2 = tk.Entry(second_frame, font = FONT_SIZE)
c1r2.place(relx=0.72, relwidth=0.28, relheight=.9)



ORDER = 3

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Production interval [periods]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r3 = tk.Entry(second_frame, font = FONT_SIZE)
c1r3.place(relx=0.72, relwidth=0.28, relheight=.9)



ORDER = 4

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Optional Production Input:',bg=ALTERNATIVE_FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)



ORDER = 5

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Production on [periods]',bg=ALTERNATIVE_LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r5 = tk.Entry(second_frame, font = FONT_SIZE)
c1r5.insert(-1, '1')
c1r5.place(relx=0.72, relwidth=0.28, relheight=.9)




ORDER = 6

X_POSITION = 1.1*FRAME_X_POSITION + FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Production off [periods]',bg=ALTERNATIVE_LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c1r6 = tk.Entry(second_frame, font = FONT_SIZE)
c1r6.insert(-1, '0')
c1r6.place(relx=0.72, relwidth=0.28, relheight=.9)






#DELIVERY INPUT:
ORDER = 1

X_POSITION = 1.2*FRAME_X_POSITION + 2*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Delivery Fleet Input:',bg=FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)




ORDER = 2

X_POSITION = 1.2*FRAME_X_POSITION + 2*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Delivery fleet size [vehicles]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c2r1 = tk.Entry(second_frame, font = FONT_SIZE)
c2r1.place(relx=0.72, relwidth=0.28, relheight=.9)




ORDER = 3

X_POSITION = 1.2*FRAME_X_POSITION + 2*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Vehicle capacity [units/vehicle]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c2r2 = tk.Entry(second_frame, font = FONT_SIZE)
c2r2.place(relx=0.72, relwidth=0.28, relheight=.9)




ORDER = 4

X_POSITION = 1.2*FRAME_X_POSITION + 2*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Vehicle dispatch interval [periods]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c2r3 = tk.Entry(second_frame, font = FONT_SIZE)
c2r3.place(relx=0.72, relwidth=0.28, relheight=.9)




ORDER = 5

X_POSITION = 1.2*FRAME_X_POSITION + 2*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Vehicle turnaround time, avg.[periods]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c3r2 = tk.Entry(second_frame, font = FONT_SIZE)
c3r2.place(relx=0.72, relwidth=0.28, relheight=.9)



ORDER = 1

X_POSITION = 1.3*FRAME_X_POSITION + 3*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Optional Vehicle Turnaround Time Input:',bg=ALTERNATIVE_FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)




ORDER = 2

X_POSITION = 1.3*FRAME_X_POSITION + 3*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Minimum time [periods]',bg=ALTERNATIVE_LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c3r1 = tk.Entry(second_frame, font = FONT_SIZE)
c3r1.insert(-1, '0')
c3r1.place(relx=0.72, relwidth=0.28, relheight=.9)




ORDER = 3

X_POSITION = 1.3*FRAME_X_POSITION + 3*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=ALTERNATIVE_FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Standard deviation [periods]',bg=ALTERNATIVE_LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c3r3 = tk.Entry(second_frame, font = FONT_SIZE)
c3r3.insert(-1, '0')
c3r3.place(relx=0.72, relwidth=0.28, relheight=.9)




#EVALUATION PERIOD INPUT:
ORDER = 5

X_POSITION = FRAME_X_POSITION
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='Evaluation timeframe:',bg=FRAME_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=1, relheight=.9)



ORDER = 6

X_POSITION = FRAME_X_POSITION
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

second_frame = tk.Frame(root, bg=FRAME_COLOR, bd=5)
second_frame.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

label = tk.Label(second_frame, text='[periods]',bg=LABEL_COLOR,fg= FG_LABEL_COLOR,font=FONT)
label.place(relx=0, relwidth=0.7, relheight=.9)

c3r4 = tk.Entry(second_frame, font = FONT_SIZE)
c3r4.place(relx=0.72, relwidth=0.28, relheight=.9)



#RUN ESTIMATION BUTTON
ORDER = 5

X_POSITION = 1.3*FRAME_X_POSITION + 3*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)
frame_b = tk.Frame(root, bg=FRAME_COLOR, bd=1)
frame_b.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

button = tk.Button(frame_b,fg=TEXT_BUTTON_COLOR, bg=BUTTON_COLOR, text="Run Estimation", font = FONT_SIZE, command=lambda: [plot(main(float(c1r1.get()),float(c1r2.get()),float(c1r3.get()),float(c1r4.get()),float(c2r1.get()),float(c2r2.get()),float(c2r3.get()),float(c3r1.get()),float(c3r2.get()),float(c3r3.get()),float(c3r4.get()),float(c1r5.get()) ,float(c1r6.get())))])

button.place(relx=0, y=0, relwidth=1, relheight=1)



#HELP BUTTON
ORDER = 6

X_POSITION = 1.3*FRAME_X_POSITION + 3*FRAME_WIDTH
Y_POSITION = FRAME_Y_POSITION + FRAME_HEIGHT*(ORDER-1)

frame_b = tk.Frame(root, bg=FRAME_COLOR, bd=1)
frame_b.place(relx = X_POSITION, y=Y_POSITION, relwidth=FRAME_WIDTH, height=FRAME_HEIGHT, anchor='n')

button = tk.Button(frame_b,fg=TEXT_BUTTON_COLOR, bg=BUTTON_COLOR, text="Help", font = FONT_SIZE, command=lambda: webbrowser.open('https://whyworkweak.com/?page_id=24517'))

button.place(relx=0, y=0, relwidth=1, relheight=1)



#PLOTS:
'''___________PLOT_1 FRAME___________'''
frame_plot_1 = tk.Frame(root, bg=FRAME_COLOR, bd=5)
frame_plot_1.place(relx = PLOT_1_X_POSITION, y=0.52*HEIGHT, relwidth=PLOT_RELATIVE_WIDTH, relheight=PLOT_RELATIVE_HEIGHT, anchor='n')



'''___________PLOT_2 FRAME___________'''
frame_plot_2 = tk.Frame(root, bg=FRAME_COLOR, bd=5)
frame_plot_2.place(relx = PLOT_2_X_POSITION, y=0.52*HEIGHT, relwidth=PLOT_RELATIVE_WIDTH, relheight=PLOT_RELATIVE_HEIGHT, anchor='n')



'''___________PLOT_3 FRAME___________'''
frame_plot_3 = tk.Frame(root, bg=FRAME_COLOR, bd=5)
frame_plot_3.place(relx = PLOT_3_X_POSITION, y=0.52*HEIGHT, relwidth=PLOT_RELATIVE_WIDTH, relheight=PLOT_RELATIVE_HEIGHT, anchor='n')



root.mainloop()
    
    

    
    
