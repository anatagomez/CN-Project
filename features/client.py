import socket
import pickle
import pyaudio
from threading import Thread, Event
import tkinter as tk
import time


n_stations = 3
station_names = ("Station1", "Station2", "Station3")
root = tk.Tk()
root.title("Music Channel")    
frames = []

play = 0
stop_flag = Event()



def show(cur, i):
    cur.grid_remove()
    frames[i].grid()

def send_server(cur, i, c):

    #send to server telling which station it want to join. 
    data_send = pickle.dumps(i)
    c.sendall(data_send)

    show(cur, i)



class station_select(tk.Frame):
    def __init__(self, c):
        cur_i = 0
        tk.Frame.__init__(self, root)

        label = tk.Label(self, text ="Select music station:", font =("Arial", 20))
        label.grid(column=0, row=0, columnspan=3)
        
        store_button = [[None] for _ in range(n_stations)]
        for i in range(n_stations):
            store_button[i] = tk.Button(self, text=station_names[i],
                                        width = 10, height = 5,
                                        command=lambda i=i: send_server(self, i+1, c))
            store_button[i].grid(column=i, row=1)
    


class stations(tk.Frame):
    def __init__(self, c, data_recv, cur_i):

        tk.Frame.__init__(self, root)

        text = "Currently in station " + str(cur_i)
        label = tk.Label(self, text = text, font =("Arial", 20))
        label.grid(column=0, row=0, columnspan=3)

        store_button = [[None] for _ in range(n_stations)]
        store_button[0] = tk.Button(self, text="Back",
                                    width = 10, height = 5,
                                    command=lambda:  back_and_stop(c, cur_i, "back", self))
        store_button[0].grid(column=0, row=1)

        store_button[1] = tk.Button(self, text="Play",
                                    width = 10, height = 5,
                                    command=lambda: thread_handle_audio(c, data_recv, cur_i-1))
        store_button[1].grid(column=1, row=1)

        store_button[2] = tk.Button(self, text="Stop",
                                    width = 10, height = 5,
                                    command=lambda: back_and_stop(c, cur_i, "stop", self))
        store_button[2].grid(column=2, row=1)


def thread_handle_audio(c, data_recv, station):
    global play
    global t

    if play == 0:
        play = 1
        stop_flag.clear()
        t = Thread(target=listen_audio, args=(c, data_recv, station, ))
        t.start()


def listen_audio(c, data_recv, station):
    frames_per_buffer = 2048

    c.setblocking(0)
    try:
        data= c.recv(frames_per_buffer)
        while data:
            data= c.recv(frames_per_buffer)
    except BlockingIOError:
        pass

    c.setblocking(1)

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(data_recv[station][1]),
                    channels=data_recv[station][2],
                    rate=data_recv[station][3],
                    output=True,
                    frames_per_buffer=512)
    

    while not stop_flag.is_set():
        data= c.recv(frames_per_buffer)
        if not data:
            
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()



def back_and_stop(c, cur_i, s, cur):
    global play
    if play == 1:
        play = 0
        #stop the audio thread
        stop_flag.set()
        t.join()

    #if back button is pressed, go back to previous page
    if s=="back":
        temp = cur_i * -1
        data_send = pickle.dumps(temp)
        c.sendall(data_send)

        show(cur, 0)


def on_closing(c):

    if play == 1:
        stop_flag.set()
        t.join()

    root.destroy()

def main():

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #yap initializing server ip and port
    server_ip, port = '127.0.0.1', 12345

    c.connect((server_ip, port))

    print("Connected to server")

    #get the audio properties
    data_recv = pickle.loads(c.recv(1024))

    global frames

    #setting up frames for gui
    frames = [station_select(c), stations(c, data_recv, 1), stations(c, data_recv, 2), stations(c, data_recv, 3)]
    frames[0].grid()

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(c))
    #to run the window gui
    root.mainloop()



if __name__ == '__main__':
    main()
