import threading
import RunCamera

# Threading of Control the flag of Saving-Image in Class RunCamera
class controlThread(threading.Thread):

    def __init__(self, threadName):
        threading.Thread.__init__(self)
        self.threadName = threadName     
        self.is_get_img = False

    def run(self):
        threadLock = threading.Lock()
        threadLock.acquire()
        try:
            self.main_control()
        finally:
            threadLock.release()

    def main_control(self):

        while True:

            # --- control camera to save a new image
            if RunCamera.RunCamera._img_save == False and RunCamera.RunCamera._img_done == True:
                if self.is_get_img == True:
                    self.is_get_img = False
                    RunCamera.RunCamera._img_save = True
                    RunCamera.RunCamera._img_done = False
                    print "\nUnlock save-image-processing...\n"
                    str_processing = "Processing:"
                    print str_processing 
                #else:
                #    print("Waiting next Order...\n")
            elif RunCamera.RunCamera._img_save == True and RunCamera.RunCamera._img_done == False :
                str_processing += "."
                print str_processing 
            else :
               pass 

           # --- control motor here, e.g. turn around for a winkel/step
           #
           #
           #

           # --- call CNN here
           #
           #
           #
