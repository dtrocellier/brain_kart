from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort
import time
import os

# Detect serial port
thymio_serial_ports = ThymioSerialPort.get_ports()
serial_port = thymio_serial_ports[0].device

use_tcp = False
host = None
tcp_port = None

# Initialize Thymio connection
th = Thymio(
    use_tcp=use_tcp,
    serial_port=serial_port,
    host=host,
    tcp_port=tcp_port,
    refreshing_coverage={"prox.horizontal", "button.center", "prox.ground.delta"}
)

# Handle communication errors
def on_comm_error(error):
    print("Communication Error:", error)
    os._exit(1)  # Force exit

th.on_comm_error = on_comm_error

# Connect to Thymio
th.connect()
print("Connecting...")
time.sleep(2)  # Allow time for connection

node_id = th.first_node()

# Print connected nodes
for node in th.nodes():
    print("Node:", node)

# Function to be triggered when proximity values change
def prox(th, node_id, variables):
    """Observer function that reacts to ground proximity changes."""
    thymio = th[node_id]

    # Check if "prox.ground.delta" is in updated variables
    if "prox.ground.delta" in variables:
        maxSteer = 20
        speed = 300  # Set default speed (adjust if needed)

        ground_prox = variables["prox.ground.delta"]  # Get new proximity values
        left_ground_prox = ground_prox[0]
        right_ground_prox = ground_prox[1]

        # Compute steering adjustment
        tmp = maxSteer * left_ground_prox - maxSteer * right_ground_prox
        steerL = tmp // 50

        print(f'Left steer: {steerL}, Speed: {speed}')

        # Adjust motor speeds
        thymio["motor.left.target"] = speed + steerL
        thymio["motor.right.target"] = speed - steerL

# Register observer for proximity sensors
th.set_variable_observer(node_id, prox)

print("Observer set. Robot should now respond to proximity changes.")

# Run the robot for 10 seconds (adjust as needed)
time.sleep(10)

# Stop motors
th[node_id]["motor.left.target"] = 0
th[node_id]["motor.right.target"] = 0

# Disconnect Thymio
th.disconnect()
print("Disconnected.")
