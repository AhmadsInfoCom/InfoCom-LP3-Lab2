from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests
import os


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


#Give a unique ID for the drone
#===================================================================
myID = "drone1"    #stod bara typ "MY_DRONE" från början
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
current_longitude = 13.21008 #rätt? stod 0 från början. hämtade från lp2 lab1 build.py, det var våra initial OSM coordinates då, de hette longitude och latitude.
current_latitude = 55.71106 #samma som ovan.
size = os.path.getsize("dronedestination.txt")
if size > 0:
    dronedest = open("dronedestination.txt", "w+")    #.txt? 
    linelist = dronedest.readlines()
    current_longitude = float(linelist[0])
    current_latitude = float(linelist[1])
else:
    dronedest = open("dronedestination.txt", "w+")    #.txt? 
    dronedest.writelines([str(current_longitude), str(current_latitude)])   #sparar värdena första gången
#===================================================================

drone_info = {'id': myID,
                'longitude': current_longitude,
                'latitude': current_latitude,
                'status': 'idle'
            }

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
SERVER= "http://100.100.100.24:5001/drone"
print(SERVER)
#bytte IP till den vi sätter på serverdrönaren (satte till 23, så drönarna kan vara 24 och 25), och porten till den som database ska köra på enligt README-filen.    #Stod från början: "http://SERVER_IP:PORT/drone"
with requests.Session() as session:
    resp = session.post(SERVER, json=drone_info)
#===================================================================

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    # Get current longitude and latitude of the drone 
    #===================================================================
    dronedest = open('dronedestination.txt', 'r')
    linelist = dronedest.readlines()
    current_longitude = float(linelist[0]) #?? hämta från textfilen som ni gjorde i simulator. Från instruktionerna till simulator.py:
    current_latitude = float(linelist[1]) #?? "The simulator moves the drone and stops when the drone arrives at to_location. You can save the final coordinates of the drone to a text file, so that the drone knows where it is and can start from this location as current_location for the next delivery.
    #===================================================================
    from_coord = coords['from']
    to_coord = coords['to']
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
