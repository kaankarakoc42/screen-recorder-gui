from tkinter import *
import pyautogui,os
from PIL import Image,ImageTk
from tkinter import filedialog
import dotenv

from main import screenRecorder

dotenv_path = ".env"
config = dotenv.dotenv_values(".env")

recorder = screenRecorder()
recorder.setOutput(config["output_folder"])


window = Tk()
window.geometry("500x400")
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "pink")
window.config(bg='pink')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

img= Image.open('./images/pause.png').resize((25,20))
photo = ImageTk.PhotoImage(img)
img= Image.open('./images/resume.png').resize((25,25))
photo2 = ImageTk.PhotoImage(img)
buttonImage = photo

img= Image.open('./images/settings.png').resize((20,20))
settingsico = ImageTk.PhotoImage(img)

img= Image.open('./images/close.png').resize((20,20))
closeico = ImageTk.PhotoImage(img)

img= Image.open('./images/github.png').resize((23,25))
githubico = ImageTk.PhotoImage(img)

playButtonState = True
settingsMenuState = False

rect = None
startingPoint = ()
rectDrawingState = False
realesedButtons=0
coords = ()

def move(widget:Canvas):
    def e(e):
      x,y=pyautogui.position()
      w=widget.winfo_width()
      h=widget.winfo_height()
      widget.place(x=x-w,y=y-h)
    widget.bind('<B1-Motion>',e)

def moveParent(widget,parent):
    def e(e):
      x,y=pyautogui.position()
      w=widget.winfo_width()
      h=widget.winfo_height()
      parent.place(x=x-w,y=y-h)
    widget.bind('<B1-Motion>',e)
    
def create(widget,x,y):
    widget.place(x=x,y=y)
    return widget

def setStarting(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    startingPoint = pyautogui.position()
    rectDrawingState = True
    if not rect:
       rect = canvas.create_rectangle(startingPoint[0], startingPoint[1],1,1, outline='red')

def setEnding(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    if not rectDrawingState: return
    x,y=pyautogui.position()
    canvas.coords(rect,startingPoint[0], startingPoint[1], x,y)
    coords = (str(startingPoint[0]), str(startingPoint[1]), str(x),str(y))
    
def drawingDone(canvas):
    global rectDrawingState,rect,coords;
    rectDrawingState = False
    canvas.delete(rect)
    rect = None

def on_double_click_release(func):
    global realesedButtons;
    if realesedButtons == 2:
       func()
       realesedButtons = 0
    realesedButtons+=1
    
def grabScreen():
    canvas = create(Canvas(window,width = screen_width,height=screen_height),0,0)
    window.config(cursor="tcross")
    window.attributes('-alpha', 0.5)
    canvas.bind("<Double-Button-1>",lambda x:setStarting(canvas))
    canvas.bind("<B1-Motion>",lambda x:setEnding(canvas))
    canvas.bind("<ButtonRelease-1>",lambda x:on_double_click_release(lambda :(drawingDone(canvas),canvas.destroy(),window.attributes('-alpha', 1),window.config(cursor="arrow"),recorder.setGrab(coords),dotenv.set_key(dotenv_path,"grab_screen",",".join(coords)))))
    
def defaultButtonFunctions(widget,buttonFunction):
    widget.bind("<Enter>",lambda x:widget.configure(bg="#5CC6F7"))
    widget.bind("<Leave>",lambda x:widget.configure(bg="#00AFE7"))
    widget.bind("<Button-1>",lambda x:(widget.configure(bg="#9BD7F2"),buttonFunction(x)))

def defaultMenuButtonFunctions(widget,buttonFunction):
    widget.bind("<Enter>",lambda x:widget.configure(bg="#E3E3E3"))
    widget.bind("<Leave>",lambda x:widget.configure(bg="lightgray"))
    widget.bind("<Button-1>",lambda x:(widget.configure(bg="#EEEEEE"),buttonFunction(x)))

def changePlayButtonState():
    global playButtonState,buttonImage
    playButtonState = not playButtonState
    buttonImage = photo if playButtonState else photo2
    if not playButtonState:
       window.iconify()

def changeSettingsMenuState():
    global settingsMenuState;
    settingsMenuState = not settingsMenuState
    
def playerComponent():
    canvas = create(Canvas(width=100,height=35,bg="#00AFE7",highlightthickness=2, highlightbackground="#59797E"),((screen_width-100)/2),0)
    playButton = create(Label(canvas,height = 25,width = 25,image = photo,bg="#00AFE7",fg="white"),10,4)
    settingsButton = create(Label(canvas,height = 25,width = 25,image = settingsico,bg="#00AFE7",fg="white"),65,4)
    defaultButtonFunctions(playButton,lambda x:(changePlayButtonState(),playButton.configure(image=buttonImage),recorder.handleCapture()))
    defaultButtonFunctions(settingsButton,lambda x:(settingsMenu()))
    move(canvas)

def selectTempDir():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=window, initialdir=currdir, title='Please select a directory')
    dotenv.set_key(dotenv_path,"output_folder",tempdir)
    recorder.setOutput(tempdir)

def settingsMenu():
    global settingsMenuState;
    if settingsMenuState: return
    changeSettingsMenuState()
    canvas = create(Canvas(width=300,height=200,bg="#00AFE7",highlightthickness=2, highlightbackground="#59797E"),(screen_width-300)/2,(screen_height-200)/2)
    canvasMenu = create(Canvas(canvas,width=300,height=30,bg="lightgray",highlightthickness=2, highlightbackground="#59797E"),0,0)
    githubButton = create(Label(canvas,height = 25,width = 25,image = githubico,bg="lightgray",fg="white"),10,2)
    closeButton = create(Label(canvas,height = 25,width = 25,image = closeico,bg="lightgray",fg="white"),265,2)
    pathButton = create(Label(canvas,bg="#00AFE7",text="Select Folder",width=25, anchor='w',justify='left',font=("Helvetica",13),highlightthickness=2, highlightbackground="#59797E"),10,50)
    selectScreenPartButton = create(Label(canvas,bg="#00AFE7",width=25,text="Select Screen Part",anchor='w',justify='left',font=("Helvetica",13),highlightthickness=2, highlightbackground="#59797E"),10,90)
    exitButton = create(Label(canvas,bg="#00AFE7",text="Exit (saves also records)",width=25, anchor='w',justify='left',font=("Helvetica",13),highlightthickness=2, highlightbackground="#59797E"),10,130)
    defaultButtonFunctions(pathButton,lambda x:(selectTempDir()))
    defaultButtonFunctions(selectScreenPartButton,lambda x:(grabScreen()))
    defaultButtonFunctions(exitButton,lambda x:(recorder.stopRecord(),window.destroy()))
    defaultMenuButtonFunctions(closeButton,lambda x:(canvas.destroy(),changeSettingsMenuState()))
    defaultMenuButtonFunctions(githubButton,lambda x:(os.startfile("https://github.com/kaankarakoc42/screen-recorder-gui")))
    move(canvas)
    moveParent(canvasMenu,canvas)


playerComponent()
mainloop()
