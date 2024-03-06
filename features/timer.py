import tkinter as tk
import threading

seconds = 60
DEFAULT_FOCUS = 25 * seconds
DEFAULT_BREAK = 5 * seconds

class Timer():
    def __init__(self):
        self.time = DEFAULT_FOCUS
        self.times = {"reset": self.time,
                      "focus": DEFAULT_FOCUS,
                      "break": DEFAULT_BREAK}
        self.run = False # is the timer running
        self.thread = None
        self.control = "focus" # current mode
        self.time = self.times[self.control]
        self.session_count = 0 # num of sessions done

    # start the timer
    def start(self, func):
        if not self.run:
            self.run = True
            self.timer_with_call(func)

    # threading
    def timer_with_call(self, func):
        if self.run and self.time > 0:
            # decrease by one second
            self.time -= 1
            func()
            self.thread = threading.Timer(1, self.timer_with_call, [func])
            self.thread.start()
          
    # stop the timer
    def stop(self):
        if self.run:
            self.run = False
            self.thread.cancel()

    # reset the timer to current mode's default duration
    def reset(self):
        self.control = "reset"

    @property
    def control(self):
        return self.__control

    @control.setter
    def control(self, control):
        self.stop()
        self.__control = control
        self.time = self.times[control]

class Pomodoro:
    def __init__(self):
        self.master = tk.Tk()
        self.frame = tk.Frame(self.master)
        self.timer = Timer()

        # colors
        self.background_color = "white"

        self.buttons = []
        self.buttons.append(tk.Button(self.frame, text='Start', command=lambda: self.start_with_focus()))
        self.buttons.append(tk.Button(self.frame, text='Reset', command=lambda: self.change_control("reset")))
        self.buttons.append(tk.Button(self.frame, text='Stop', command=self.stop))
        self.buttons.append(tk.Button(self.frame, text='Continue',  command=self.start))

        # timer
        self.time_string = tk.StringVar()
        self.time_label = tk.Label(self.frame, textvariable=self.time_string, font=(None, 37,), width=0)

        # session
        self.session_string = tk.StringVar()
        self.session_label = tk.Label(self.frame, textvariable=self.session_string, font=(None, 10,), width=0)
        #self.session_label.grid(row=3, column=1)
      
        self.display_on_window()
        self.update_time()
        self.window_config()
        self.button_config()
        self.master.mainloop()
      
    def display_on_window(self):
        self.time_label.grid(row=1, column=1, pady=17)
        self.time_label.config(foreground="red")

        self.session_label.grid(row=3, column=1, pady=17)
        self.session_label.config(foreground="black") #padx=20)
      
        self.buttons[0].grid(row=0, column=0)  # start
        self.buttons[1].grid(row=0, column=2)  # reset
        self.buttons[2].grid(row=2, column=0)  # stop
        self.buttons[3].grid(row=2, column=2)  # continue
        self.frame.pack(pady=4, padx=0)

    def window_config(self):
        self.master.title("Pomodoro Timer")
        self.master.geometry("429x200")
        self.master.config(background=self.background_color)
        self.frame.config(background=self.background_color)
        self.time_label.config(background=self.background_color)
        self.session_label.config(background=self.background_color)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.eval('tk::PlaceWindow . center')
        
    def button_config(self):
        for button in self.buttons:
            button["width"] = 14
            button["bg"] = "#dedede"
            button["border"] = 0

    def change_control(self, control):
        #print(self.timer.control)
        self.timer.control = control
        self.update_time()

    def on_closing(self):
        self.timer.stop()
        self.master.destroy()

    def start(self):
        self.timer.start(self.update_time)

    def stop(self):
        self.timer.stop()

    def update_time(self):
        time = self.timer.time
        min, sec = divmod(time, seconds)
        self.time_string.set(f"{min:>02}:{sec:>02}")
        self.session_string.set(f"Sessions: {self.timer.session_count}")
      
        # change mode
        if time == 0:
            if self.timer.control == "focus":
                self.start_with_break()
            elif self.timer.control == "break":
                self.start_with_focus()
                self.timer.session_count += 1
                # self.session_count_string.set(f"Sessions: {self.timer.session_count}")
                
    def start_with_focus(self):
        self.change_control("focus")
        self.start()
        
    def start_with_break(self):
        self.change_control("break")
        self.start()

def main():
    app = Pomodoro()
  
if __name__ == '__main__':
    main()