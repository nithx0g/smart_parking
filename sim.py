from tkinter import *
import server
import camera
import sensor
import time
import random

slots = {}
occupied = []
free = []
sensors = {}
random_var=1
for i in range(1,21):
    slots[i] = "" #4-digit car number if parked there
    if(i%8 == random_var):
        slots[i] = str(random.randint(1111,9999))
        random_var=(2*random_var+3)%4 + 1
        occupied.append(i)
    else:
        free.append(i)
    sensors[i] = sensor.Sensor(i)
serv = server.Server(slots)
camera = camera.Camera()
time.sleep(2)
list_slot = list(serv.slots.values())
# main window 
par = Tk()
# title of parking slot
par.title("Smart Parking Simulation")
code_entry=Entry(par,width=20,borderwidth=5)
code_entry.grid(row=1,column=1)
#entryclick used to get the entry of car
def entryclick():
    if(len(free) == 0):
        Label(par ,width=20,height=3,text="Parking space is full").grid(row  = 6,column =0)
        return
    Label(par ,width=20,height=3,text="").grid(row  = 6,column =0)
    i = int(code_entry.get())
    if not i in free:
        Label(par ,width=20,height=3,text="Slot " + str(i) + " is occupied").grid(row  = 3,column =0)
        return
    Label(par ,width=20,height=3,text="").grid(row  = 3,column =0)
    free_slot = i#free[i]
    free.remove(free_slot)
    occupied.append(free_slot)
    print("Parked at " + str(free_slot))
    sensors[free_slot].entry()
#use this fun to get car to exit from the parking lot  
code_exit=Entry(par,width=20,borderwidth=5)
code_exit.grid(row=4,column=1)
def exitclick():
    if(len(occupied) == 0):
        Label(par ,width=20,height=3,text="Parking Space empty").grid(row  = 6,column =0)
        return
    Label(par ,width=20,height=3,text="").grid(row  = 6,column =0)
    i = int(code_exit.get())
    if i not in occupied:
        Label(par ,width=20,height=3,text="Slot " + str(i) + " is empty").grid(row  = 5,column =0)
        return
    Label(par ,width=20,height=3,text="").grid(row  = 5,column =0)
    exiting_slot = i
    print("exiting " + str(i))
    occupied.remove(exiting_slot)
    free.append(i)
    sensors[exiting_slot].exit()

Label(par ,width=15,height=3,text="Entry Car:").grid(row  = 1,column =0)
Button(par ,text="Entry",activebackground="Black",command=entryclick).grid(row=1,column=2)
Label(par ,width=15,height=3,text="").grid(row  = 2,column =0)
Label(par ,width=15,height=3,text="Exit Car:").grid(row  = 4,column =0)
Button(par ,text="Exit",activebackground="Black",command=exitclick).grid(row=4,column=2)

# sub window for user 
user = Tk()
user.title("USER UI")
car_location = []
# search car location from car number
Label(user ,width=20,height=3,text="Search Car Location").grid(row=1)
code=Entry(user,width=20,borderwidth=5)
code.grid(row=2,column=0)
# slot fun use for searching car location
def slot():
    list_slot = list(serv.slots.values())
    val = code.get()
    if(val == ""):
        Label(user ,width=15,height=3,text="No input given").grid(row=4,column=0,padx=10,pady=10)
        return
    slot_pos=0
    for i in range(len(car_location)):
        Label(user ,width=15,height=3,text="").grid(row=4,column=i,padx=10,pady=10)
    car_location.clear()
    while True:
        try:
            slot_pos = list_slot.index(val, slot_pos)
            car_location.append(slot_pos+1)
            slot_pos += 1
        except ValueError as e:
            break
    for i in range(len(car_location)):
        Label(user ,width=15,height=3,text="Car Location:{}".format(car_location[i]),bg="#CDC0B0").grid(row=4,column=i,padx=10,pady=10)
    if(len(car_location) == 0):
        Label(user ,width=15,height=3,text="Car not found").grid(row=4,column=0,padx=10,pady=10)

# car serach button calls slot function 
Button(user ,width=5,text="Car Search",activebackground="Black",font="Raleway",bg="#20bebe",command=slot).grid(row=2,column=1)
Label(user ,width=15,height=3,text="Slots").grid(row=5) 
 
# here we dispaly all parking slot info
count=0
row_inc=0
for i in list_slot: 
    if(i==""):
        Label(user ,width=15,height=3,text="free",bg="blue").grid(row=6+row_inc,column=count,padx=10,pady=10)
        count=count+1
        if(count==4):
            row_inc=row_inc+1
            count=0
    else:
        Label(user ,width=15,height=3,text=i,bg="red").grid(row=6+row_inc,column=count,padx=10,pady=10)
        count=count+1
        if(count==4):
            row_inc=row_inc+1
            count=0
frees=[]
Label(user ,width=15,height=3,text="find free slot").grid(row=14,column=0)
# Update fun update ui page
def update():
    count=0
    row_in=0
    list_slot = list(serv.slots.values())
    for i in list_slot: 
        if(i==""):
            Label(user ,width=15,height=3,text="free",bg="blue").grid(row=6+row_in,column=count,padx=10,pady=10)
            count=count+1
            if(count==4):
                row_in=row_in+1
                count=0
        else:
            Label(user ,width=15,height=3,text=i,bg="red").grid(row=6+row_in,column=count,padx=10,pady=10)
            count=count+1
            if(count==4):
                row_in=row_in+1
                count=0
# freeslot find free slot available in a parking slot                
row_val=0
def freeslot():
    row_val=0
    count = 0
    list_slot = list(serv.slots.values())
    val = ""
    slot_pos=0
    for i in range(len(frees)):
        Label(user ,width=10,height=3,text="").grid(row=16+row_val,column=count,padx=10,pady=10)
        count = count + 1
        if(count==4):
            row_val = row_val+1
            count=0
    frees.clear()
    while True:
        try:
            slot_pos = list_slot.index(val, slot_pos)
            frees.append(slot_pos+1)
            slot_pos += 1
        except ValueError as e:
            break
    row_val=0
    count = 0
    for i in range(len(frees)):
        Label(user ,width=10,height=3,text="{}".format(frees[i]),bg="#CDC0B0").grid(row=16+row_val,column=count,padx=10,pady=10)
        count = count + 1
        if(count==4):
            row_val = row_val+1
            count=0
    
#FreeSlot button calls the freeslot fun
Button(user ,width=5,text="FreeSlot",activebackground="Black",font="Raleway",bg="#20bebe",command=freeslot).grid(row=14,column=1)
#UpdateUI button calls the Update fun 
Button(user ,width=5,text="UpdateUI",activebackground="Black",font="Raleway",bg="#20bebe",command=update).grid(row=15,column=1)       
# user window end
user.mainloop()
# main window end
par.mainloop()
