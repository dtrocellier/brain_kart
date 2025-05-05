from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort

import time
import os



thymio_serial_ports = ThymioSerialPort.get_ports()
serial_port = thymio_serial_ports[0].device

use_tcp = False
host = None
tcp_port = None



def prox(th, node_id, speed):
    global left_ground_prox, right_ground_prox
    thymio = th[node_id]
    # #onevent startup
    maxSteer = 20

    # global speed, motor_left_target, motor_right_target, maxSteer, steerL, tmp
    # thymio["motor.left.target"] = speed
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
            refreshing_coverage={
                "prox.horizontal",
                "button.center",
                "prox.ground.delta"
            },
            )


def on_comm_error(error):

    # loss of connection: display error and exit
    print(error)
    os._exit(1) # forced exit despite coroutines

th.on_comm_error = on_comm_error

th.connect()
print("connecting")
# wait 2-3 sec until robots are known
time.sleep(2)

node_id = th.first_node()
for node in th.nodes():
    print(node)


def play(th, node_id):
    # line_behavior(node_id)
    #th.set_variable_observer(node_id, line_behavior) # lance une fonction de façon asynchrone
    print("Playing ", node_id)
    thymio = th[node_id]

    ground_left = thymio["prox.ground.delta"][0]
    ground_right = thymio["prox.ground.delta"][1]
    # th[node_id]["leds.top"] = [32,0,32]



    while True :

        # collect speed with eeg
        speed =300

        # th.set_variable_observer(node_id,prox)
        prox(th, node_id, speed)
        # time.sleep(0.1)



from multiprocessing import Pool


if __name__ == "__main__":


    # Set global variables
    done = False
    line_moving = True
    prox_left = th[node_id]["prox.ground.delta"][0]
    prox_right = th[node_id]["prox.ground.delta"][1]

    # th.set_variable_observer(node_id, play)


    # Once all nodes have been reached, request and apply rotation
    for node_id in th.nodes():
        print("Playing ", node_id)
        play(th,node_id)

        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0
        time.sleep(2)
        # print("Rotating ", node_id)
        # rotation_order = request_llm(node_id)
        # rotate(node_id, rotation_order)
        # th[node_id]["motor.left.target"] = 0
        # th[node_id]["motor.right.target"] = 0

    th.disconnect()

