# brain_kart
Races of thimio robots controled by OpenBCI

To use it (with an OpenBCI devices) : 

**Step 1 : connect the Open BCI to Openvibe** 

- Plug the dongle on the PC
- Check in the peripheric manager : find the COM corresponding to it : got to parameters : advanced : latency : modify to 1s
- Open the Acquisition Server (OpenVibe)
- Select Open BCI : verify in the device manager that the COM is recognized
- Conect and Play 

**Step 2 connect the Thymio**

- Plug the dongle of a specific Thymio (if the thymio is not paired : see the specific procedure)
- Open the Thymio Suit : check that the Thymio is recognized 

**Step 3 :**
- Open the Pyhton Notebook
- Install the packages with pip if you do not have them

**Step 4 :** 
- Open the Open Vibe Designer with the scenarios 
- Check if the signal is alright with visualisation-alpha : show to the participants what is he is not supposed to do (moove, blink etc...)
- Record the baseline and check what is its value (in the log) 
- Open the scenario send-speed : change in the Scenario Configuration the right value of the baseline depending of the subject
- Play the scenario send-speed
- Run the cells of the notebook until the while loop

  
- It should be working !!
