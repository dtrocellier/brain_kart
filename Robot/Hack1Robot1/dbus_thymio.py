#!/usr/bin/python

import threading
import dbus
import dbus.mainloop.glib
import sys
import os

from pylsl import StreamInlet, resolve_stream
import numpy as np




class ThymioController(object):
    def __init__(self, initial_speed = False, useEEGStream = False):
        # initialize asebamedulla in background and wait 0.3s to let
        # asebamedulla startup (!!bad habit to wait...)
        os.system("(asebamedulla ser:name=Thymio-II &) && sleep .3")
        
        # init the dbus main loop
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        # get stub of the aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')

        # prepare interface
        self.asebaNetwork = dbus.Interface(
            asebaNetworkObject,
            dbus_interface='ch.epfl.mobots.AsebaNetwork'
        )

        print(self.asebaNetwork.GetNodesList())

        print('loading file...')

        # load the file which is run on the thymio
        self.asebaNetwork.LoadScripts(
            "./thympi.aesl",
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

        print('file loaded')
        print(self.asebaNetwork.GetNodeId('thymio-II'))

        if useEEGStream:
            self.connectStream()

        self.streamInput = useEEGStream

        # initialize some variables which can be used in the main loop
        # to set thymio states
        # self.ledState = [1, 2, 4, 8, 16, 24, 32, 2]
        self.counter = 0
        self.colors = [[32, 0, 0], [0, 32, 0], [0, 0, 32]]

        self.asebaNetwork.SendEventName(
            'sound.system',
            [0],
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

        if initial_speed:
            self.set_speed(int(initial_speed))

        self.speed = 0

    def connectStream(self):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')


        # create a new inlet to read from the stream
        self.inlet = StreamInlet(streams[0])

        print('connection found')


    def get_speed_input(self):
        speed = raw_input("Enter speed:")
        self.set_speed(int(speed))
        self.get_speed_input()

    def run(self):
        threading.Timer(0.02, self.main_loop).start()
        if not self.streamInput:
            threading.Thread(target=self.get_speed_input).start()
        # self.mainLoop()

    def stopAsebamedulla(self):
        # stop the asebamedulla process
        # !!dbus connection will fail after this call
        os.system("pkill -n asebamedulla")


    def dbusReply(self):
        # dbus replys can be handled here.
        # Currently ignoring
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        # Currently only the error is logged. Maybe interrupt the mainloop here
        print('dbus error: %s' % str(e))

    def set_speed(self, speed):
        # acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')

        self.asebaNetwork.SendEventName(
            'setSpeed',
            [speed],
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )    

    def main_loop(self):

        # self.asebaNetwork.SendEventName(
        #     'leds.top',
        #     self.colors[self.counter],
        #     reply_handler=self.dbusReply,
        #     error_handler=self.dbusError
        # )

        # self.counter = (self.counter + 1) % 3

        # ambiant = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.ambiant')
        # reflected = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected')
        delta = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.delta')

        # print(ambiant)
        # print(reflected)
        print(delta)
        print("-----")


        # rightSpeed = self.asebaNetwork.GetVariable('thymio-II', 'motor.right.speed')
        # leftSpeed = self.asebaNetwork.GetVariable('thymio-II', 'motor.left.speed')
        
        # print(rightSpeed[0])
        # print(leftSpeed[0])
        # print("-----")


        if self.streamInput:
            speed = 0
            chunk, timestamps = self.inlet.pull_chunk()
            if timestamps:
                # print(timestamps, chunk)
                alpha = np.array(chunk).mean(axis=0)[0]
                print(alpha)
                if alpha < 0:
                    speed = min(- alpha * 50, 400)
                print(speed)
                if abs(self.speed - speed) > 2:
                    self.set_speed(speed)
                    self.speed = speed


        # self.asebaNetwork.SendEventName(
        #     'motor.target',
        #     [0, 0],
        #     reply_handler=self.dbusReply,
        #     error_handler=self.dbusError
        # )

        # read and display acc sensors
        # acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')

        # read and display temperature
        # temperature = self.asebaNetwork.GetVariable('thymio-II', 'temperature')
        # print(temperature[0])

        # prox_horizontal = self.asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
    #     ground_ambiant = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.ambiant')
    #     ground_reflected = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected')
    #     ground_delta = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.delta')
    #     mic_intensity = self.asebaNetwork.GetVariable('thymio-II', 'mic.intensity')

    #     # print the readed sensor values
    #     print(
    #         "Acc: {0:+3d}, {1:+3d}, {2:+3d} "
    #         "Temp: {3:3d} "
    #         "Button: f{4:1d}, r{5:1d}, b{6:1d}, l:{7:1d}, c:{8:1d} "
    #         "Horizontal: {9:4d}, {10:4d}, {11:4d}, {12:4d}, {13:4d}, {14:4d}, {15:4d}, "
    #         "Ground: [{16:3d}, {17:3d}, {18:3d}] | [{19:3d}, {20:3d}, {21:3d}], "
    #         "Mic: {22:3d}"
    #         "".format(
    #             *acc,
    #             *temperature,
    #             *button_fd,
    #             *button_r,
    #             *button_bw,
    #             *button_l,
    #             *button_c,
    #             *prox_horizontal,
    #             ground_ambiant[0],
    #             ground_reflected[0],
    #             ground_delta[0],
    #             ground_ambiant[1],
    #             ground_reflected[1],
    #             ground_delta[1],
    #             mic_intensity[0]
    #         )
    #     )

    #     # set programmatically some states on the thymio
    #     # optional you can specify reply- and error handler
        # self.asebaNetwork.SendEventName(
        #     'motor.target',
        #     [0*acc[0], 16*acc[1]],
        #     reply_handler=self.dbusReply,
        #     error_handler=self.dbusError
        # )
    #     self.asebaNetwork.SendEventName(
    #         'leds.bottom.right',
    #         [0, self.ledState[0], 0]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.bottom.left',
    #         [0, 0, self.ledState[0]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.temperature',
    #         [self.ledState[0], self.ledState[1]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.circle',
    #         self.ledState
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.prox.h',
    #         self.ledState
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.prox.v',
    #         [self.ledState[0], self.ledState[2]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.buttons',
    #         [self.ledState[0], self.ledState[1], self.ledState[2], self.ledState[3]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.top',
    #         [self.ledState[0], self.ledState[1], self.ledState[2]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.sound',
    #         [self.ledState[0]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.rc',
    #         [self.ledState[4]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'mic.threshold',
    #         [200]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'sound.system',
    #         [self.counter % 8]
    #     )
    #     # self.asebaNetwork.SendEventName(
    #     #     'sound.play',
    #     #     [self.counter  % 8]
    #     # )
    #     # self.asebaNetwork.SendEventName(
    #     #     'sound.freq',
    #     #     [(self.counter * 10) % 3200, 1/60.0]
    #     # )

    #     # shift the ledState array
    #     # [1, 2, 4, 8, 16, 24, 32, 2] becomes [2, 1, 2, 4, 8, 16, 24, 32]
    #     self.ledState.append(self.ledState.pop(0))
    #     # increase the counter
    #     self.counter += 1

        # reschedule mainLoop
        if self.asebaNetwork.GetVariable('thymio-II', 'button.center')[0] == 1:
            # self.stopAsebamedulla()
            print("done")
        else:
            self.run()


if __name__ == '__main__':

    if len(sys.argv) == 2:
        thymio = ThymioController(sys.argv[1])
    elif len(sys.argv) == 3:
        thymio = ThymioController(sys.argv[1],sys.argv[2])
    else:
        thymio = ThymioController()
    
    print('Starting process')

    thymio.run()
