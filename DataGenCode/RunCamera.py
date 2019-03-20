from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import pygame
import sys
import ctypes

class RunCamera(object):

    # check if it needs to make a picture and save the picture
    _img_save = False
    _img_num = 0
    _img_done = True

    def __init__(self):

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
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        
    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
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
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- When the flage of Saving image is unlocked, so do it 
            if RunCamera._img_save == True:

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

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # --- Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


if __name__ == "__main__":
    runTest1 =  RunCamera()
    runTest1.run()

