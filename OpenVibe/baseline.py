# we use numpy to compute the mean of an array of values
import numpy
import math

import numpy as np


import os


# let's define a new box class that inherits from OVBox
class MyOVBox(OVBox):
   out = []
   def __init__(self):
      OVBox.__init__(self)
   # we add a new member to save the signal header information we will receive
      self.signalHeader = None


   def initialize(self):
       self.signal = numpy.empty([1, 64*30])
       self.nb_chunk=0
       print("init...")



   # The process method will be called by openvibe on every clock tick
   def process(self):
      # we iterate over all the input chunks in the input buffer
      for chunkIndex in range( len(self.input[0]) ):
         # if it's a header we save it and send the output header (same as input, except it has only one channel named 'Mean'
         if(type(self.input[0][chunkIndex]) == OVSignalHeader):
            self.signalHeader = self.input[0].pop()
            outputHeader = OVSignalHeader(
            self.signalHeader.startTime,
            self.signalHeader.endTime,
            [1, self.signalHeader.dimensionSizes[1]],
            ['Mean']+self.signalHeader.dimensionSizes[1]*[''],
            self.signalHeader.samplingRate)
            self.output[0].append(outputHeader)
            print(self.signalHeader)


         # if it's a buffer we pop it and put it in a numpy array at the right dimensions
         # We compute the mean and add the buffer in the box output buffer
         elif(type(self.input[0][chunkIndex]) == OVSignalBuffer):
            chunk = self.input[0].pop()
            numpyBuffer = numpy.array(chunk).reshape(tuple(self.signalHeader.dimensionSizes))
            numpyBuffer = numpyBuffer.mean(axis=0)
            self.signal[0,self.nb_chunk]=(numpyBuffer)
            chunk = OVSignalBuffer(chunk.startTime, chunk.endTime, numpyBuffer.tolist())
            self.output[0].append(chunk)
            self.nb_chunk+=1
         # if it's a end-of-stream we just forward that information to the output
         elif(type(self.input[0][chunkIndex]) == OVSignalEnd):
            pass
            # print(self.signal)
            #self.output[0].append(self.input[0].pop())

   def uninitialize(self):
      self.signal = numpy.array(self.signal[0, 0:self.nb_chunk])
      # mask = numpy.isfinite(self.signal)
      # self.signal = self.signal[mask]
      # print(self.signal.shape)

      #  the 10% higher values

      high_percentile = numpy.percentile(self.signal, 90)
      self.signal  = self.signal [self.signal  < high_percentile]


      # Calculate mean and std
      mean = self.signal.mean()
      std = self.signal.std()

      print ("\nmean", mean)
      print("std", std)

      # For the moment does not work because path issues

      # # Overwrite the existing files with new values
      # with open("bin/baseline_mean.txt", "w") as mean_file:
      #    mean_file.write(str(mean))
      #
      # with open("bin/baseline_std.txt", "w") as std_file:
      #    std_file.write(str(std))



      # print("mean:",self.signal[0, 0:self.nb_chunk].mean(axis=0))
      # print("signal:",self.signal)
      # print("nb_chunk", self.nb_chunk)
      # mask = numpy.where(self.signal == 0)
      # print("mask", mask)





# Finally, we notify openvibe that the box instance 'box' is now an instance of MyOVBox.
# Don't forget that step !!
box = MyOVBox()
#%%
