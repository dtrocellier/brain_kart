
import time

rainbow = [
    32, 0, 0,      # Rouge
    32, 16, 0,     # Orange
    32, 32, 0,     # Jaune
    16, 32, 0,     # Vert clair
    0, 32, 0,      # Vert
    0, 32, 16,     # Turquoise
    0, 32, 32,     # Cyan
    0, 16, 32,     # Bleu clair
    0, 0, 32       # Bleu
]
# def change_color(thymio):
#     for i in range(0, len(rainbow), 3):
#         thymio["leds.top"] = rainbow[i:i+3]
#         time.sleep(1)


#

#
# rainbow = [
#     32, 0, 0,      # Rouge
#     32, 16, 0,     # Orange
#     32, 32, 0,     # Jaune
#     16, 32, 0,     # Vert clair
#     0, 32, 0,      # Vert
#     0, 32, 16,     # Turquoise
#     0, 32, 32,     # Cyan
#     0, 16, 32,     # Bleu clair
#     0, 0, 32       # Bleu
# ]
# colorIndex = 0
# currentSound = -1


# def timer0():
#     # Cycles color using rainbow color array (1 dimension)
#     nf_leds_top(rainbow[colorIndex], rainbow[colorIndex + 1], rainbow[colorIndex + 2])
#     colorIndex = (colorIndex + 3) % len(rainbow)
#
# def updateColor(s):
#     global timer_period, currentSound
#     # Depends on current speed of the robot
#     if s == 0:
#         #Pas de couleur
#         nf_sound_play(-1)
#         currentSound = -1
#         nf_leds_top(0,0,0)
#         timer_period[0] = 0
#     elif s < 100:
#         #Couleur Blue
#         nf_sound_play(-1)
#         currentSound = -1
#         timer_period[0] = 0
#         nf_leds_top(0,0,32)
#     elif s >= 100 and s < 200:
#         # Couleur Vert
#         nf_sound_play(-1)
#         currentSound = -1
#         timer_period[0] = 0
#         nf_leds_top(0,32,0)
#     elif s >= 200 and s < 300:
#         # Couleur Orange
#         nf_sound_play(-1)
#         currentSound = -1
#         timer_period[0] = 0
#         nf_leds_top(32,8,0)
#     elif s >= 300 and s < 350:
#         # Couleur Rouge
#         #nf_sound_play(-1)
#         currentSound = -1
#         timer_period[0] = 0
#         nf_leds_top(32,0,0)
#     elif s >= 350 :
#         # Couleur Arc en Ciel
#         timer_period[0] = 100
#         #if currentSound != 7:
#         #nf_sound_play(7)
#         #currentSound = 7
#         nf_leds_top(32,32,32)
#
# # Event raised when a playing sound ends
# @onevent
# def sound_finished():
#     global currentSound
#     nf_sound_play(currentSound)
#
# Raised when a new speed is read from the EEG stream
def receivedSpeed(s):
    global speed
    # updateColor(s)
    speed = s

# # Raised when the proximity sensors are read
# # Frequency : 100Hz
# @onevent
def prox(speed=100):
    global left_ground_prox, right_ground_prox, th
    thymio = th[node_id]
    # #onevent startup
    maxSteer = 20

    # global speed, motor_left_target, motor_right_target, maxSteer, steerL, tmp
    left_motor_speed = thymio["motor.left.target"]
    thymio["motor.right.target"] = thymio["motor.right.target"]
    # thymio["motor.left.target"] = speed
    horiz_prox = thymio["prox.horizontal"]
    ground_prox = thymio["prox.ground.delta"]
    right_ground_prox = ground_prox[1]
    left_ground_prox = ground_prox[0]

    print(f"left : {left_ground_prox} , right {right_ground_prox}")



    # If an obstacle is detected, stop the robot
    if any([prox > 500 for prox in horiz_prox[:4]]): #need to exclude last censor?
        speed = 0
        print("see wall")
        thymio["motor.left.target"] = speed
        thymio["motor.right.target"] = speed

        return
    # if all([prox < 700 for prox in ground_prox]): # If both sensors are on black, stop the robot
    #     speed = 0
    #     thymio["motor.left.target"] = speed
    #     thymio["motor.right.target"] = speed
    #     print("see black lines that indicates stop")
    #
    #     return


    # Define speed correction to apply to motors
    tmp = maxSteer * left_ground_prox - maxSteer * right_ground_prox
    steerL = tmp // 50
    print(f'Left steer: {steerL}')
    # thymio["motor.left.target"] = 0
    # thymio["motor.right.target"] = 0


    # Set motor speed and correction
    thymio["motor.left.target"] = speed + steerL
    thymio["motor.right.target"] = speed - steerL