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
k=1
for i in range(1,21):
    slots[i] = "" #4-digit car number if parked there
    if(i%8 == k):
        slots[i] = str(random.randint(1111,9999))
        k=(2*k+3)%4 + 1
        occupied.append(i)
    else:
        free.append(i)
    sensors[i] = sensor.Sensor(i)
serv = server.Server(slots)
camera = camera.Camera()
time.sleep(2)

list_slot = list(serv.slots.values())

par = Tk()

par.title("Smart Parking Simulation")
code_entry=Entry(par,width=20,borderwidth=5)
code_entry.grid(row=1,column=1)
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



user = Tk()

user.title("USER UI")
yy = []
Label(user ,width=20,height=3,text="Search Car Location").grid(row=1)
code=Entry(user,width=20,borderwidth=5)
code.grid(row=2,column=0)
def slot():
    list_slot = list(serv.slots.values())
    val = code.get()
    if(val == ""):
        Label(user ,width=15,height=3,text="No input given").grid(row=4,column=0,padx=10,pady=10)
        return
    slot_pos=0
    for i in range(len(yy)):
        Label(user ,width=15,height=3,text="").grid(row=4,column=i,padx=10,pady=10)
    yy.clear()
    while True:
        try:
            slot_pos = list_slot.index(val, slot_pos)
            yy.append(slot_pos+1)
            slot_pos += 1
        except ValueError as e:
            break
    for i in range(len(yy)):
        Label(user ,width=15,height=3,text="Car Location:{}".format(yy[i]),bg="#CDC0B0").grid(row=4,column=i,padx=10,pady=10)
    if(len(yy) == 0):
        Label(user ,width=15,height=3,text="Car not found").grid(row=4,column=0,padx=10,pady=10)


Button(user ,width=5,text="Search",activebackground="Black",font="Raleway",bg="#20bebe",command=slot).grid(row=2,column=1)
Label(user ,width=15,height=3,text="Slots").grid(row=5) 
 

count=0
k=0
for i in list_slot: 
    if(i==""):
        Label(user ,width=15,height=3,text="free",bg="blue").grid(row=6+k,column=count,padx=10,pady=10)
        count=count+1
        if(count==4):
            k=k+1
            count=0
    else:
        Label(user ,width=15,height=3,text=i,bg="red").grid(row=6+k,column=count,padx=10,pady=10)
        count=count+1
        if(count==4):
            k=k+1
            count=0
frees=[]
Label(user ,width=15,height=3,text="find free slot").grid(row=14,column=0)

def update():
    count=0
    k=0
    list_slot = list(serv.slots.values())
    for i in list_slot: 
        if(i==""):
            Label(user ,width=15,height=3,text="free",bg="blue").grid(row=6+k,column=count,padx=10,pady=10)
            count=count+1
            if(count==4):
                k=k+1
                count=0
        else:
            Label(user ,width=15,height=3,text=i,bg="red").grid(row=6+k,column=count,padx=10,pady=10)
            count=count+1
            if(count==4):
                k=k+1
                count=0
    # frees=[]
# Label(user ,width=15,height=3,text="find free slot").grid(row=14,column=0)
j=0
def freeslot():
    j=0
    count = 0
    list_slot = list(serv.slots.values())
    val = ""
    slot_pos=0
    for i in range(len(frees)):
        # Label(user ,width=10,height=3,text="").grid(row=4,column=i,padx=5,pady=5)
        Label(user ,width=10,height=3,text="").grid(row=16+j,column=count,padx=10,pady=10)
        count = count + 1
        if(count==4):
            j = j+1
            count=0
    frees.clear()
    while True:
        try:
            slot_pos = list_slot.index(val, slot_pos)
            frees.append(slot_pos+1)
            slot_pos += 1
        except ValueError as e:
            break
    j=0
    count = 0
    for i in range(len(frees)):
        # if(count == 4):
        Label(user ,width=10,height=3,text="{}".format(frees[i]),bg="#CDC0B0").grid(row=16+j,column=count,padx=10,pady=10)
        count = count + 1
        if(count==4):
            j = j+1
            count=0
    


Button(user ,width=5,text="Search",activebackground="Black",font="Raleway",bg="#20bebe",command=freeslot).grid(row=14,column=1)
Button(user ,width=5,text="Update",activebackground="Black",font="Raleway",bg="#20bebe",command=update).grid(row=15,column=1)       
user.mainloop()

par.mainloop()

# root = Tk()
# root.title("USer")
# Label(root ,width=50,height=3,text="USer").grid(row=0)
# root.mainloop()
