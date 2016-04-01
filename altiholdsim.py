from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse 

_land = False

def arm_and_takeoff(aTargetAltitude):
    global _land
    print kp
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    '''while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)'''

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("STABILIZE")
    vehicle.armed=True 
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    
   # vehicle.mode = VehicleMode("STABILIZE")
    #vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:

        try:
            if _land==False:          
                setz = 10
                currentz = vehicle.location.global_relative_frame.alt
                PID = 0
                sum_error = 0
                prev_error = 0
                errorz = (setz - currentz)*10
                
                print " Altitude: ", currentz , "errorz:", errorz
                print()
                vehicle.armed=True 
                #Break and return from function just below target altitude.        
                if abs(errorz)>=setz*0.0001: 
                   PID = kp*errorz + ki*sum_error + kd*(errorz - prev_error)
                   print "check:", PID
                   PID = PID + 1380
                   if PID<1380 :
                     PID = 1350
                   if PID>2000 :
                     PID = 2000
                   print "PID:", PID 
                   vehicle.channels.overrides['3']  = PID
                   sum_error = sum_error + errorz
                   prev_error = errorz
                   """ print "Reached target altitude"
                    break"""
                time.sleep(1)
            else:
                vehicle.channels.overrides['3']=1000
                exit()
             
        except KeyboardInterrupt:
            vehicle.channels.overrides['3']=1000
           # vehicle.mode = VehicleMode("LAND")            
           # if _land:
            #    vehicle.channels.overrides['3']=1000
            #    exit()
            _land = True

#Set up option parsing to get connection string
 
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

#Start SITL if no connection string specified
if not args.connect:
    print "Starting copter simulator (SITL)"
    from dronekit_sitl import SITL
    sitl = SITL()
    sitl.download('copter', '3.3', verbose=True)
    sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
    sitl.launch(sitl_args, await_ready=True, restart=True)
    #connection_string = 'tcp:127.0.0.1:5760'   #for tcp
    connection_string = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00' #for serial


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
#vehicle = connect(connection_string, wait_ready=True)   #for tcp
vehicle = connect(connection_string, baud=115200, wait_ready=True)   #for serial

print "Give Kp Ki Kd" 
kp = float(input())
ki = float(input())
kd = float(input())

print _land

arm_and_takeoff(1)


"""
print "Set default/target airspeed to 3"
vehicle.airspeed = 3

print "Going towards first point for 30 seconds ..."
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")
"""
#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()