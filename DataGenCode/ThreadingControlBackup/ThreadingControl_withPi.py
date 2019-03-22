import threading
import RunCamera
import client

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

            s = client.connect()
            print "Connected to PI\n"

            command = raw_input(u"Enter your command:")

            if command == "EXIT":
                s.send(str(command))
                s.close()

            elif command == "KILL":
                s.send(str(command))
                s.close()

            elif command == "MOTOR":

                go_on = 0
                while go_on == 0:
                    command1 = raw_input(u"Wie viele Fotos wollen sie machen?")
                    command2 = raw_input(u"Welcher Winkel sollen die Fotos aufgenommen werden?")
                    try:
                        intcommand1 = int(command1)
                        intcommand2 = int(command2)
                        go_on = 1
                    except:
                        print "Der Input muss eine Zahl sein"

                AnzSchritte = (intcommand2/0.9)//intcommand1
                command = "".join((command," ",str(round(AnzSchritte))))
                for i in range(0,intcommand1):
                    s.send(str(command))
                    replay = s.recv(2048)
                    if replay == "Fertig":


                        self.is_get_img = True
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

                    else:
                        print"Fehler bei der Kommunikation vom Server"

            else:
                s.send(str(command))
                replay = s.recv(2048)
                if replay == "Unbekannt":
                    print   "Das verwendete Befehl ist nicht bekannt!\n",\
                            "Versuchen Sie folgende:\n",\
                            "MOTOR: Gibt einen Drehbefehl\n",\
                            "EXIT: Die Verwendung wird vom Clienet verlassen, der Server (Pi) wartet auf neue Verbindung\n",\
                            "KILL: Der Server (Pi) wird ausgeschaltet"

                else:
                    print replay


            s.close()
