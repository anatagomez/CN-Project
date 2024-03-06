import socket
import select
import pickle
import wave
from threading import Thread
import time

#for storing client sockets
client = dict()
#list containing which client is in which station (the file descriptor)
station_client = [[], [], []]
#audio property
frames_per_buffer = 2048
#for storing client station
client_station = dict()
#for select
read_check = []

#for broadcasting the audio
def run_music_station(music_name, counter):
    #open the song file
    wf = wave.open(music_name, 'rb')

    # send the song to client   
    while True:
        #get the audio frames
        while len(data := wf.readframes(512)):
            #get the fd
            for i in station_client[counter]:
                #send to client
                try:
                    client[i].sendall(data)
                except BrokenPipeError:
                    if i in client_station:
                        client_station.pop(i)
                    if i in station_client[counter]:
                        station_client[counter].remove(i)
                        
                    if i in read_check:
                        read_check.remove(i)
                        
                    if i in client:
                        client[i].close()
                        client.pop(i)
                    print("Client with file descriptor", i, "successfully disconnected")
                    
        #song finished, loop again
        wf.rewind()  

def main():
    print("hi")
    #doing the socket stuff
    #SOCK_STREAM is tcp
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port, n_clients = 12345, 10
    host = socket.gethostname()
    s.bind(("", port))
    s.listen(n_clients)

    #get file descriptor of socket
    s_fd = s.fileno()

    read_check.append(s_fd)
    read_check.append(0)

    #music file name
    music_station = ["station1.wav", "station2.wav", "station3.wav"]

    counter = 0
    for i in music_station:
        #create threads to achieve parallelism
        #each thread is equal to one music station
        t = Thread(target=run_music_station, args=(i, counter,))
        t.start()
        counter += 1

    #for storing audio property
    audio_info = []
    for i in music_station:
        #get audio property
        wf = wave.open(i, 'rb')

        sample_width = wf.getsampwidth()
        channels = wf.getnchannels()
        frame_rate = wf.getframerate()

        audio_info.append((i, sample_width, channels, frame_rate))

    print("Waiting for connections...")

    while True:
        try:
            read_fd, _ , _ = select.select(read_check, [], [])
            
            for i in read_fd:
                #got a new connection
                if i is s_fd:
                    #accept connection
                    c_socket, _ = s.accept()
                    c_fd = c_socket.fileno()

                    print("Client with file descriptor", c_fd, "successfully connected")

                    #store the socket
                    client[c_fd] = c_socket

                    #add the client file descriptor to read_check for select function
                    read_check.append(c_fd)

                    #sending our music station information
                    data_send = pickle.dumps(audio_info)
                    c_socket.sendall(data_send)

                else:
                    try:
                        data_recv = pickle.loads(client[i].recv(1024))
                        if data_recv < 0:
                            data_recv *= -1
                            station_client[data_recv-1].remove(i)

                        else:
                            station_client[data_recv-1].append(i)
                            client_station[c_fd] = data_recv-1

                    except (ConnectionResetError, EOFError) as e:

                        #to cut connection with client
                        if c_fd in client_station:
                            if c_fd in station_client[client_station[c_fd]]:
                                station_client[client_station[c_fd]].remove(c_fd)
                            client_station.pop(c_fd)
                        
                        if c_fd in read_check:
                            read_check.remove(c_fd)
                        
                        if i in client:
                            client[i].close()
                            client.pop(i)
                        print("Client with file descriptor", c_fd, "successfully disconnected")
        except:
            pass

if __name__ == '__main__':
    main()