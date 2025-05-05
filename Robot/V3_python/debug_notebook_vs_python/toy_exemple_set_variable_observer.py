from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort

import time
import os

thymio_serial_ports = ThymioSerialPort.get_ports()
serial_port = thymio_serial_ports[0].device

use_tcp = False
host = None
tcp_port = None
speed = 100

def on_comm_error(error):

    # loss of connection: display error and exit
    print(error)
    os._exit(1) # forced exit despite coroutines


def prox(node_id):
    global left_ground_prox, right_ground_prox, speed
    thymio = th[node_id]

    # #onevent startup
    maxSteer = 20
    ground_prox = thymio["prox.ground.delta"]
    right_ground_prox = ground_prox[1]
    left_ground_prox = ground_prox[0]


    # Define speed correction to apply to motors
    tmp = maxSteer * left_ground_prox - maxSteer * right_ground_prox
    steerL = tmp // 50
    print(f'Left steer: {steerL}, speed : {speed}')

    # Set motor speed and correction
    thymio["motor.left.target"] = speed + steerL
    thymio["motor.right.target"] = speed - steerL






th = Thymio(use_tcp=use_tcp,
            serial_port=serial_port,
            host=host, tcp_port=tcp_port,
            refreshing_rate=0.1, #default 0.1
            refreshing_coverage={
                "prox.horizontal",
                "prox.ground.delta"
            },
            )
th.on_comm_error = on_comm_error
th.connect()
print("connecting")
# wait 2-3 sec until robots are known
time.sleep(2)


def play(th, node_id):
    # line_behavior(node_id)
    print("Playing ", node_id)
    th.set_variable_observer(node_id,prox)


if __name__ == "__main__":


    # Set global variables
    done = False
    line_moving = True
    speed = 300
    # prox_left = th[node_id]["prox.ground.delta"][0]
    # prox_right = th[node_id]["prox.ground.delta"][1]

    # th.set_variable_observer(node_id, play)


    # Once all nodes have been reached, request and apply rotation
    # for node_id in th.nodes():
    #     print("Playing ", node_id)
    node_id = th.first_node()
    play(th,node_id)


    # th.disconnect()

