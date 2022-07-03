import cv2
import numpy as np
import pyautogui,os
from threading import Thread
from keyboard import add_hotkey,wait
from uuid import uuid4


class screenRecorder:
      def __init__(self) -> None:     
          self.__capture = False
          self.__captureState = False
          self.videoName = str(uuid4()).split("-")[0]+".mp4"
          self.__output = self.videoName 
          self.__grab = False
          self.__record = False

      def setGrab(self,data):
          self.__grab = data

      def setOutput(self,data):
          if data == '' or not os.path.exists(data):
             self.__output = "./" + self.videoName
          else:
             self.__output = data +"/"+ self.videoName

      def Capture(self):
          if not self.__grab:
             img = pyautogui.screenshot()
          else:
             img = pyautogui.screenshot(region=self.__grab)
          if not self.__record:
             img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
             height, width, channels = img.shape
             fourcc = cv2.VideoWriter_fourcc(*'mp4v')
             self.out = cv2.VideoWriter(self.__output, fourcc, 10.0, (width, height))
          self.__record = True
          print("starting")
          while self.__capture:
            if not self.__grab:
               img = pyautogui.screenshot()
            else:
               img = pyautogui.screenshot(region=self.__grab)
            image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.out.write(image)
            StopIteration(0.1)
          print("stoped")


      def startCapture(self):
          self.__capture = True
          Thread(target=self.Capture).start()

      def stopCapture(self):
          self.__capture = False

      def handleCapture(self):
          if not self.__capture:
             self.startCapture()
          else:
             self.stopCapture()
        
      def stopRecord(self):
          if self.__record:
             self.out.release()
             cv2.destroyAllWindows()
             self.__record = False
             print("record stopped")

if "__main__"==__name__:
   recorder = screenRecorder()
   add_hotkey("a",recorder.handleCapture)
   add_hotkey("c",recorder.stopRecord)
   wait("esc")

