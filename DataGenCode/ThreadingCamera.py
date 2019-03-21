import threading
import RunCamera

# Threading of running camera
# final version of this class
# to understand threads in python
# https://docs.python.org/2.7/library/threading.html

class cameraThread(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self)
        self.threadName = threadName        

    def run(self):
        threadLock = threading.Lock()
        threadLock.acquire()
        try :
            runCamera = RunCamera.RunCamera()
            runCamera.run()
        finally:
            threadLock.release()

