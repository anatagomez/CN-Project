import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk


class Readme(tk.Toplevel):

  def __init__(self):
    super().__init__()
    self.title("Readme")
    self.geometry('728x350')

    readme_text = """
        Online Pomodoro Timer

        TomatoTimers is a customizable and easy to use looping pomodoro timer to boost your efficiency.

        About Pomodoro Technique

        Pomodoro™ Technique is a time management method developed by Francesco Cirillo in the late 1980s. 
        This technique use timer to break down works into a set of intervals separated by breaks. 
        Pomodoro technique increases productivity by taking short scheduled breaks regularly.

        How to use Pomodoro/ Tomato timers

        Decide task to be done set timers to 25 minutes for one "Pomodoro"
        Work on task until timer is complete
        After timer completion, put a checkmark on to-do list
        Take a 5 minutes short break
        After four "Pomodoro" take a long break
        Repeat to step 1
        USE THE LOOP BUTTON TO DO STEP 1 UNTIL STEP 5 IN A ROW
        """

    readme_label = tk.Label(self,
                            text=readme_text,
                            font=("Helvetica", 12),
                            padx=10,
                            pady=10)
    readme_label.pack()


def button_click(button_text):
  messagebox.showinfo("Button clicked",
                      f"You clicked the {button_text} button")


root = tk.Tk()
root.title("The Canned Room")
root.geometry('728x410')

# Load the JPG photo
background_image = Image.open("CNL/background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas with the background photo
canvas = tk.Canvas(root, width=728, height=410)
canvas.pack()
canvas.create_image(0, 0, anchor='nw', image=background_photo)

# Set the background color and font styles
font_style = ("Helvetica", 15)
welcome_font_style = ("Helvetica", 30)

welcome_text = canvas.create_text(364,
                                  100,
                                  text="Welcome to the Canned Room",
                                  font=welcome_font_style,
                                  fill='white')


def start_pomodoro():
  subprocess.Popen(["python", "CNL/timer.py"])

def start_music():
  subprocess.Popen(["python", "CNL/client.py"])

def start_blocker():
  subprocess.Popen(["python", "CNL/blocker.py"])



def open_readme():
  Readme()


pomodoro_button = tk.Button(canvas,
                            text="Start Pomodoro",
                            width=30,
                            font=font_style,
                            command=start_pomodoro,
                            highlightbackground='purple')
pomodoro_button.place(relx=.5,  anchor="center", y=170)

music_button = tk.Button(canvas,
                         text="Music Channel",
                         width=30,
                         font=font_style,
                         command=start_music,
                         highlightbackground='purple')
music_button.place(relx=.5,  anchor="center", y=220)

website_blocker_button = tk.Button(
  canvas,
  text="Website Blocker",
  width=30,
  font=font_style,
  command=start_blocker,
  highlightbackground='purple')
website_blocker_button.place(relx=.5,  anchor="center", y=270)

readme = tk.Button(canvas,
                   text="What is Pomodoro Timer?",
                   width=30,
                   font=font_style,
                   command=open_readme,
                   highlightbackground='purple',
                   fg='red')
readme.place(relx=.5,  anchor="center", y=350)

root.mainloop()
