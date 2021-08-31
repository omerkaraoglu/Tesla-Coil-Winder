from math import pi

def AWG_to_mm(awg):
    mm = 0.127 * 92**((36-awg)/39)
    return mm

def size_error(type):
    if type == "pipe":
        print("Pipe is too long, max pipe length for your machine is " + str(pipe.max_length))
    elif type == "coil":
        print("Pipe is too short, there is no room for the wire to be wound on")
    elif type == "wire":
        print("Wire is too thick")

wire_diameter = AWG_to_mm(int(input("Wire gauge (AWG): ")))
pivot_length = int(input("Pivot length (mm): "))

class pipe:
    max_length = pivot_length - 106.03
    length = int(input("Pipe length (mm): "))
    diameter = int(input("Pipe outer diameter (mm): "))

class coil:
    max_length = pipe.max_length - 20
    length = pipe.length - 31
    diameter = pipe.diameter + wire_diameter / 2
    turns = length / wire_diameter
    inductance = ((diameter/2/25.4)**2 * (turns/2/25.4)**2) / 9*diameter/2/25.4 + 10*length/25.4 #uH

loop = True

if pipe.length > pipe.max_length: #possible errors
    size_error("pipe")
    loop = False

if coil.length <= 0:
    size_error("coil")
    loop = False

if wire_diameter > 1:
    size_error("wire")
    loop = False

if loop:
    print("\nCoil Properties:\n")
    print("Length: " + str(round(coil.length, 2)) + " mm")
    print("Diameter: " + str(round(coil.diameter, 2)) + " mm")
    print(str(int(coil.turns)) + " Turns")
    print("Inductance: " + str(round(coil.inductance, 2)) + " uH\n")

file = open("coil.dola", "w") #create/open the file and erase the data
file.seek(0)
file.truncate()
file.close()

while loop:
    x_per_turn = wire_diameter  #how much does the slider mechanism needs to move for one turn
    turns_per_revolution = 12.73*pi / x_per_turn   #how many slider revolutions needed to move the slider mechanism the needed amount for one turn
    steps_per_turn = 512 / turns_per_revolution #how many steps needed to rotate the slider motor the needed amount for one turn
    temp_SPT = str(round(steps_per_turn, 1)) #converting the needed step count for onne tur into a string
    SPT = temp_SPT.split(".", 1) #splitting the number from the decimal point (this returns a list with two elements: required full steps and required microsteps
    microstep_count = int(SPT[0]) * 8 + int(round(int(SPT[1]) * 4/5, 0)) #how many microsteps does the slider motor needs for winding one turn (since the second element of the list is decimal but we use 8 microsteps, we need to multipy it by 8/10 and then round it to the closest whole number)
    slider_microstep_interval = int(round(512 * 8 / microstep_count, 0)) #how many rotator microsteps needed between two slider microsteps to equally disperse the slider microsteps among the rotator microsteps

    a1 = "1000"  # these are the microsteps for one full step in order
    a2 = "1100"
    b1 = "0100"
    b2 = "0110"
    c1 = "0010"
    c2 = "0011"
    d1 = "0001"
    d2 = "1001"

    step_map = [a1, a2, b1, b2, c1, c2, d1, d2]  #one step with 8 microsteps

    slider_last_microstep = 0   #set counters
    rotator_last_microstep = 0

    print("Writing to file...")

    file = open("coil.dola", "a") #open the file which will contain required steps for one turn of the coil
    file.write(str(int(coil.turns)) + "E")

    for i in range(int(round(4096 / slider_microstep_interval * coil.turns))):
        for j in range(slider_microstep_interval):
            file.write("0") #0 indicates rotator motor
            file.write(step_map[(j + rotator_last_microstep) % 8])

        if i == int(round(4096 / slider_microstep_interval)):
            slider_last_microstep = i % 8

        file.write("1") #1 indicates slider motor
        file.write(step_map[(i + slider_last_microstep) % 8])
        rotator_last_microstep = (j + rotator_last_microstep + 1) % 8

    file.close()
    print("File ready\n")
    break