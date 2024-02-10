# we use csv to the save the perfomance

import time
import csv
import subprocess

import sys

def install(package):
      subprocess.check_call([sys.executable, "-m", "pip", "install", package])
      print("package installed")
install('pandas')
import pandas as pd



# let's define a new box class that inherits from OVBox
class MyOVBox(OVBox):
   out = []
   def __init__(self):
      OVBox.__init__(self)
   # we add a new member to save the signal header information we will receive
      self.signalHeader = None


   def initialize(self):
       print(self.setting)
       self.prenom = self.setting['pseudo']
       self.event =  self.setting['event']

   
   def process(self):
      pass


   
   def uninitialize(self):


      score = self.getCurrentTime() 
      fichier_gdf = f"{self.prenom}_{self.event}_{score}.gdf"
      nouvelle_ligne = [self.prenom, self.event, score, fichier_gdf ]

      nom_fichier = "bin/performances.csv"

      df = pd.read_csv(nom_fichier)

      df.append(nouvelle_ligne, ignore_index=True)

      df.to_csv(nom_fichier, index=False)

      #Ouvrir le fichier CSV en mode écriture
 #     with open(nom_fichier, mode='a', newline='') as file:
         # Créer un objet writer
  #       writer = csv.writer(file)

      #Ajouter la nouvelle ligne au fichier CSV
 #        writer.writerow(nouvelle_ligne)




     

# Finally, we notify openvibe that the box instance 'box' is now an instance of MyOVBox.
# Don't forget that step !!
box = MyOVBox()
#%%
