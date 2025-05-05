import tdmclient
import time

# Initialize Thymio connection
client = tdmclient.Client()
node = None

print("Waiting for Thymio connection...")
try:
    with client:
        nodes = client.nodes
        if nodes:
            node = nodes[0]
            print("Connection established!")
        else:
            raise Exception("No Thymio node found")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Global variables
maxSteer = 20
speed = 0
steerL = 0

# Function to handle received speed event
def receivedSpeed(s):
    global speed
    speed = s

# Function to handle proximity sensor event
def prox():
    global speed, maxSteer, steerL

    if node is not None:
        with node.lock():
            left = node.v.prox_ground_delta[0]
            right = node.v.prox_ground_delta[1]

            tmp = maxSteer * left - maxSteer * right
            steerL = tmp // 50

            node.v.motor_left_target = speed + steerL
            node.v.motor_right_target = speed - steerL

# Main loop
speed = 300
while True:
    prox()  # Poll proximity sensors
    print(f"Current Speed: {speed}")
    time.sleep(0.1)
