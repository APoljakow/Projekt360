import numpy as np
import os
import pygame
import sys
import ctypes

from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
from pylibfreenect2 import Freenect2, SyncMultiFrameListener

if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
PyObject_AsWriteBuffer.restype = ctypes.c_int
PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def get_address_from_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

class RunCamera(object):

    # check if it needs to make a picture and save the picture
    _img_save = False
    _img_num = 0
    _img_done = True

    def __init__(self):
        
        try:
            from pylibfreenect2 import OpenGLPacketPipeline
            self._pipeline = OpenGLPacketPipeline()
        except:
            try:
                from pylibfreenect2 import OpenCLPacketPipeline
                self._pipeline = OpenCLPacketPipeline()
            except:
                from pylibfreenect2 import CpuPacketPipeline
                self._pipeline = CpuPacketPipeline()
        print("Packet pipeline:", type(self._pipeline).__name__)

        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._screen_width = 500
        self._screen_heigth = 300
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_heigth), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        # Set the titel of the screen- window
        pygame.display.set_caption("Kamera")

        # Loop until the user clicks the close button.
        self._done = False

        # Kinect runtime object, we want only color and body frames 
        #self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

        # Create and set logger
        logger = createConsoleLogger(LoggerLevel.Debug)
        setGlobalLogger(logger)

        self._fn = Freenect2()
        self._num_devices = self._fn.enumerateDevices()
        if self._num_devices == 0:
            print("No device connected!")
            sys.exit(1)

        self._serial = self._fn.getDeviceSerialNumber(0)
        self._device = self._fn.openDevice(self._serial, pipeline=self._pipeline)

        self._listener = SyncMultiFrameListener(
            FrameType.Color | FrameType.Ir | FrameType.Depth)

        # Register listeners
        self._device.setColorFrameListener(self._listener)
        self._device.setIrAndDepthFrameListener(self._listener)

        self._device.start()

        # NOTE: must be called after device.start()
        self._registration = Registration(self._device.getIrCameraParams(),
                                    self._device.getColorCameraParams())

        self._undistorted = Frame(512, 424, 4)
        self._registered = Frame(512, 424, 4)

        # Optinal parameters for registration
        # set True if you need
        self._need_bigdepth = False
        self._need_color_depth_map = False

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        #self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        self._bigdepth = Frame(1920, 1082, 4) if self._need_bigdepth else None
        self._color_depth_map = np.zeros((424, 512),  np.int32).ravel() if self._need_color_depth_map else None
        self._frame_surface = pygame.Surface((self._registered.width, self._registered.height), 0, 32)


    def draw_color_frame(self, np_frame, target_surface):
        target_surface.lock()
        #address = self._kinect.surface_as_array(target_surface.get_buffer())
        #ctypes.memmove(address, frame.ctypes.data, frame.size)
        address = get_address_from_array(target_surface.get_buffer())
        ctypes.memmove(address, np_frame.ctypes.data, np_frame.size)
        del address
        target_surface.unlock()

    def run(self):
        

        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
            
                    

            # --- Getting frames and drawing  
            #if self._kinect.has_new_color_frame():
            #    frame = self._kinect.get_last_color_frame()
            #    self.draw_color_frame(frame, self._frame_surface)
            #    frame = None

            frames = self._listener.waitForNewFrame()
            color_frame = frames["color"]
            ir = frames["ir"]
            depth = frames["depth"]
            self._registration.apply(color_frame, depth, self._undistorted, self._registered, bigdepth=self._bigdepth, color_depth_map=self._color_depth_map)
            color_arr_view = color_frame.asarray()[:,:,0:3]

            test_surf = pygame.surfarray.make_surface(color_arr_view)
            #self.draw_color_frame(color_frame.asarray(), self._frame_surface)

            self._frame_surface = test_surf

            # --- When the flag of Saving image is unlocked, so do it 
            if RunCamera._img_save == True:
                print("entered if statement for image saving")
                # First to lock it, or it will save too many picture
                RunCamera._img_save = False

                # Folder and names of pictures 
                # or we can just use other names of th picture..
                name = "pic\\test-" + str(RunCamera._img_num) + ".jpg"

                # Save the image
                pygame.image.save(self._frame_surface, name)

                print "\n \nWe just saved the " + name + "!\n\nLock save-image-processing...\n\n===============================================\n"

                RunCamera._img_num = RunCamera._img_num + 1

                # Tell wether all be done
                RunCamera._img_done = True
                


            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()

            # --- Screen's width and height
            target_width = self._screen.get_width()
            target_height = int(h_to_w * target_width )

            surface_to_draw = pygame.transform.scale(self._frame_surface, (target_width, target_height))
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 30 frames per second, try 60 if 30 runs smoothly
            self._clock.tick(30)
            self._listener.release(frames)

        # Close our Kinect sensor, close the window and quit.
        #self._kinect.close()
        #self._device.stop()
        self._device.close()
        pygame.quit()


