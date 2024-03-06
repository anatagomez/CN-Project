## Computer Networks Lab Final Project
# The Canned Room Study App

**Group 10**
B09902082 李秀
B09902085 郭雅美
B09902077 黃麗企
B09902086 楊心如
B09902080 王彬
B09902083 郭俐欣

## Motivation 

Most students struggle with leaving assignments/tasks up until the last minute leading to increased stress. We wanted to offer a comprehensive solution for students to overcome their procrastination.

So, we decided to make an interface that provides you with several studying tools all in a single place. Including a “radio” with different stations of study music, a studying timer, and a website blocker.

The name “canned room” comes from the japanese term 缶詰部屋 which means a room where usually an author stays a day/week in before deadline to catch up with their work.

The concept inspired by anti-procrastination Japanese coffee shop ([Video1](https://www.instagram.com/reel/CdWQYtHAnPj/?igshid=ZWIzMWE5ZmU3Zg%3D%3D), [Video2](https://www.youtube.com/watch?v=_ZPw7gRc-VU))


## Features

1. Focus Music Channels

Audio streaming and multicast features into the GUI so that the user can select and listen to the audio content of their preference.
 
 
2. Pomodoro Timer 

A timer inspired by the Pomodoro Technique which is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. With the timer, the users can focus better and spread out their productivity levels throughout the day. 


3. Website Blocker 

Restrict access to distracting websites throughout the duration of your focused work periods. So, the users can focus on their works. 


## Implementation 


<u> 1. Focus Music Channel Implementation </u>
- Implemented using socket programming 
- Server will bind a TCP socket using port 12345.
- Before allowing any clients to connect, it will create three threads (one thread for one music station) in order to send audio later on.
- Note: This music station is like a radio broadcasting. Hence, if a client stopped playing the music, and started to play it again few seconds afterward, it won't start at the point where it is stopped.
- Once a client connects to the server, the server will send various information about the stations including the frame rate and channels of the audio.
- The client can then pick the station it wants to connect to. 
- On the client side, it will create a thread specifically to receive and listen to the audio.
- The server will continuously get the audio frames of the song and send them to the client.
- The client uses PyAudio stream in order to play the song.
- Once the client closes the window, the socket will be closed and the audio stream is terminated.

<u> 2. Pomodoro Implementation </u>
Implemented using threading. A new thread will be created every time the timer is started, with the timer_with_call() function. A new thread will be created to update the timer during the countdown. When the timer is stopped or has stopped, it will remove the current running thread.

<u> 3. Website Blocker Implementation </u>
Implemented using firewall and NAT concept from lab 1. The iptables commands are executed with python using os.system(). It provides a simple and effective way to block and unblock specific websites for the users. By utilizing the power of iptables and the subprocess module in Python, users can easily manage website access control.

<u> 4. Interface </u> 
The application's user interface is designed using Tkinter's widgets and layout managers. The main window consists of a Music Channel, a Website Blocker, and a Pomodoro Timer buttons, so when a button is clicked, it will direct the users to each features. On the button of the main window, it contains an extra buttons for the instructions.


## Demonstration 
<img src=[Imgur](https://i.imgur.com/HOXMYf6.png) width=50% height=50%>
<img src="https://hackmd.io/_uploads/ry737qTLn.png" width=50% height=50%>
<img src="https://hackmd.io/_uploads/BkX3XcTUh.png" width=50% height=50%>
<img src="https://hackmd.io/_uploads/S1mhX5pI3.png" width=50% height=50%>
<img src="https://hackmd.io/_uploads/r1mn7cpIn.png" width=50% height=50%>
<img src="https://hackmd.io/_uploads/ByXhX9aUh.png" width=50% height=50%>


## Difficulties
* Technical Challenges
    * Integrating and managing different components of the application, such as the website blocker, music channels, and pomodoro timer, posed technical challenges. Coordinating their functionalities, ensuring transitions between features, and maintaining code modularity required careful planning and implementation.
    * The music channels require a careful buffer management. Without it, the client can hear the previous song if they are trying to switch between music station.
    * Another difficulty is handling multiple clients and making sure everything is working fine when the client closes the window in the middle of the song.
    
* User Interface Design and Usability
    * Designing an intuitive and visually appealing user interface that accommodated all features while maintaining simplicity and usability was a significant challenge. Balancing functionality with an attractive and user-friendly design required iterative testing and incorporating user feedback to ensure an optimal user experience.
    

## Limitations
* Security Issues
    * There can be security issues which we have not managed yet. Moreover, the iptables command might not work in the future when the client has an upgraded version of iptables.
    * Iptables is designed for Linux, and hence, won't work for other operating system.
    
* User Validation and Status Management
    * There is no user authentication or login system, and as a result, there is no user management, and the server can't exactly track user activity.
    * No login system means lack of user customization. (Perhaps user customization can be implemented in the future so that user can tweak the application to their need. For example: automatically joining a specific music station as soon as they opened the application.)
    * Since there is no user authentication, people can open the application many times and make the server slower.

## Further work
* Develop an all-in-one interface for all the features. As for now, users need to open multiple windows to use several features silmutaneously. 
* Adds user authentication to allow only authorized users can access the app. Moreover, this will also allow user to save their records and see them the next time they log in to the system.
* We can also allow users to interact with other users with "Add Friend" feature. Multiple users can start a study session together.
* A new function to allow file sharing between users. In this case, we are expecting mostly for sharing study materials. 
* Expanding the music channel content by allowing users to choose their own preferred songs.
* Let user to adjust the timer duration according to their preferences.

## Environment
python 3.10.9
pyaudio 0.12.3
tkinter 8.6

## How To Run
- Run server<span/>.py in one terminal.
- Then run main<span/>.py in another terminal.

## Work Distribution (1-5)
B09902082 李秀 (5) : Interfaces
B09902085 郭雅美 (5) : Music channel
B09902077 黃麗企 (5) : Pomodoro, Blocker
B09902086 楊心如 (5) : Interfaces
B09902080 王彬 (5) : Blocker
B09902083 郭俐欣 (5) : Interfaces

## Source Code 
https://drive.google.com/drive/folders/1v5HW1s69l70HdqqvmdTdHGoYj8odtVup?usp=sharing 
