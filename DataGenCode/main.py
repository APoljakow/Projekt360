import ThreadingCamera
import ThreadingControl
import time

# we use two threads to handle the situation

# First of all, the "camera" and "get-picture-control" model should wait for the calling of user all the time,
# that is the code must be in "while-true" loop. When we use threads to run model of "camera" and "get-picture-control", 
# it allows motor to call these function out of all "while-true" loop, and it's freely to write motor's controll code in 
# other python file. So the same as call CNN-Calculation

def get_image():
    controlThread.is_get_img = True

# instances of threads 
controlThread = ThreadingControl.controlThread("Control")
cameraThread = ThreadingCamera.cameraThread("Camera")

# let them run
cameraThread.start()
controlThread.start()

# for testing 
# To get one image every time calling
'''
time.sleep(3)
for i in range(5):
    get_image()
    time.sleep(1)
'''