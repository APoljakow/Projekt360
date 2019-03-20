import ThreadingCamera
import ThreadingControl
import time

# Now we use two threads to handle the situation

# First of all, the "camera" and "get-picture-control" model should wait for the calling of user all the time,
# that is the code must be in "while-true" loop. When we use threads to run model of "camera" and "get-picture-control", 
# it allows motor to call these function out of all "while-true" loop, and it's freely to write motor's controll code in 
# other python file. So the same as call CNN-Calculation


def get_image():
    controlThread.is_get_img = True

def motor_step():
    pass

def call_CNN():
    pass


controlThread = ThreadingControl.controlThread("Control")
cameraThread = ThreadingCamera.cameraThread("Camera")
# using another threading to control motor
# using another threading to calculate with CNN


cameraThread.start()
controlThread.start()
# motorThread.start()
# CNNThread.start()



# To get one image every time calling
time.sleep(3)
for i in range(5):
    get_image()
    time.sleep(1)




#abfrage_1 = input("Wie viele Fotos sollen aufgenommen werden?")
#abfrage_2 = input("Bei welchem Drehwinkel?")

#stepnum = int(abfrage_2/0.9)
#teilschritt = int(stepnum//abfrage_1)







print "\nAll Tasks have been done :)"



