!!! IMPORTANT !!! READ UNTIL THE END CAREFULLY !!!

You must find the I2C address of the LCD using the i2c_scanner example code.
After you find it, change the LCD address in the Tesla_Coil_Winder.ino file.

I2C pins for the LCD: SDA, SCL --> A4, A5 (This is only valid for Nano and Uno models but, you have to use Nano anyways because of the tight space of the controller box)

Rotator motor pins: A, B, C, D --> 2, 3, 4, 5
Slider motor pins:  A, B, C, D --> 6, 7, 8, 9
!!! NOTE: Connect Vcc pins of the motor driver modules to Vin on the arduino (or directly to power jack, it's essentially the same), NOT 5V.

SPI pin connections for MicroSD: http://lab.dejaworks.com/wp-content/uploads/2016/08/Arduino-Nano-SD-Card-Connection.png
!!! NOTE: Connect CS (chip select) pin to 10, NOT 4.

Set the power supply to 6 to 6.5 Volts and 3 Amps.
Notice that the machine doesn't have a menu or start button like controls, it doesn't even have a power switch. 
Make sure that you've set everything up correctly before powering it up. Here are the steps:

#1 Make sure that the ends of your pipe are leveled. Run the python code and check if your pipe's length exceeds the maximum of your machine.

#2 Loosen the bolts of the idle chuck mount, pull it from it's base, don't squeeze the aluminum extrusions while moving it.
   Place the pipe, tighten the bolts of the idle chuck mount, then tighten the chucks. DON'T over-tighten, just give them a "firm enough to not let the pipe slip" grip.

#3 Set the winding arm to it's starting position. DON'T force the arm! Gently pull the belt and turn the pulleys near the end for presicion.
   Make sure that the arm and the jaws of the chuck doesn't touch each other. Test every jaw by turning the chuck by hand.

#4 Mark the pipe at the winder arm's slick, turn the pipe and make a hole with a hot needle at the marked point.

#5 Place the spool holder on the extrusion at the back. Center it according to the pipe. DON'T put a heavy spool on the holder, it may cause the machine to jam.
   Around 200 grams should be good.

#6 Get the wire through the hole at the bottom of the winder arm, through the slick and the hole on the pipe. Tighten the wire by winding the spool.
   Then, wind a 1/4 turn on the pipe by turning the chuck. Fix the wire in the hole on the pipe with a little super glue.

#7 Double-check the previous steps.