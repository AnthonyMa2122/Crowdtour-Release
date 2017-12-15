# Croudtour
## Contributers: <br>
Aung Phyo <br/>
John Lazzarini <br/>
Anthony Ma <br/>

### This is a project for SFSU CSC 690 Fall Semester
### URL: [https://anthonyma2122.github.io/CSC-690-Final-Project/](https://anthonyma2122.github.io/CSC-690-Final-Project/)


### Introduction
This application will work as a crowdsourced tour guide for the city. Users can upload sound files for their current area (up to 10 seconds). Other users within range of the area can listen to what others have to say about locations and businesses in the area whether it be personal experiences or popular suggestions.


### Instructions <br>
Python Version 3.6.2 <br>
<br>
1.Install these modules (use pip for best results):<br>
tkinter <br>
Pil <br>
PyQT5 <br>
gooMPy (v. 11.27) <br>
geolocation <br>
pymysql <br>
pyaudio <br>
wave <br>
pygame <br>

2.Create a local SQL server under these settings: <br>
Standard (TCP/IP) <br>
Hostname: localhost <br>
Port: 3306 <br>
Username: root <br>
password: test <br>


3.In the CSC-690-Final-Project directory, compile and run 'python simpleapp.py' <br>

### Croudtour in action

Crowdtour main UI:<br>
<img src="https://github.com/AnthonyMa2122/CSC-690-Final-Project/blob/master/images/SearchedHybridView.png" alt="hi" class="inline"/><br />

How the database should look after recording: <br>
<img src="https://github.com/AnthonyMa2122/CSC-690-Final-Project/blob/master/images/WorkbenchSQL.png" alt="hi" class="inline"/><br />

<br><br>
### Milestone 1:
Create a working SQL database and be able to read through an attribute from the SQL database. Use python as interface.

### Milestone 2:
user enters lat/long, display map <br>
display a few places on map <br>
decide how to select one of several places <br>
play audio clip from server

### Milestone 3:
all of milestone 2 <br>
select a place from list, play audio <br>
zoom/pan map <br>
