# 
#  An LSTM Based analytics of the Balllitics Training Data Set 
#  From https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
#  
# ======================================================================================================================
import matplotlib.pyplot as plt 
import numpy as np
from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import load_model
# ======================================================================================================================
#  Load in the Training Data
print(" ****************************************************************")
print(" Ballsitics LSTM Fit ")
TrainingDataX = np.load("TrainingSetX.npy")
TrainingDataY = np.load("TrainingSetY.npy")
# Show Header of Samples
print("Training Set X Shape")
print(TrainingDataX.shape)
print("Training Set Y Shape")
print(TrainingDataY.shape)

NumberSamples = TrainingDataX.shape[0]
NumberTimeSteps = TrainingDataX.shape[1]
NumberFeatures = TrainingDataX.shape[2]
NumberOfEpochs = 100

print ("Samples: " + str(NumberSamples) + " TimeSteps: " + str(NumberTimeSteps) + " Number of Features: " + str(NumberFeatures)) 

"""
# Display the first few samples
for i in range (0,NumberSamples):
   print("Distance: " + str(TrainingDataY[i]))
   print("X values: ",end="")
   for j in range (0,NumberTimeSteps):
       print(str(TrainingDataX[i,j,0]) + ", ",end="")
   print()
   print("Y values: ",end="")
   for j in range (0,NumberTimeSteps):
       print(str(TrainingDataX[i,j,1])+", ",end="")
  		 
   print()
   print()   
"""
# =======================================================================================================
# Create an LSTM Recurrent Network
#
print("Please Wait for GPU Card to be Initialised with Model ") 	
print()
# keras Model	
model = Sequential()
model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(NumberTimeSteps, NumberFeatures)))
model.add(LSTM(32, activation='relu',return_sequences=False))  
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
print(model.summary())
# fit model
# Start Training the Network
print(" Starting To Train over " + str(NumberOfEpochs) + " Epochs")
history = model.fit(TrainingDataX, TrainingDataY, epochs= NumberOfEpochs, verbose=1)
#
# ================================================================================================
# Plot the Loss History  after 20 epochs
print(" Length of History file ")
print(len(history.history['loss']))
LossHistoryNP = np.array(history.history['loss'])
LossHistoryNP = LossHistoryNP[20:,]
print(LossHistoryNP.shape)
plt.plot(LossHistoryNP)
plt.title('model loss after 20 epochs')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()
#
print(" Saving Model  to BallisticsModel.h5 ")
model.save("BallisticsModel.h5")
# ============================================================================
print()
print(" =========================================================")
print(" Now Do Some Predictions" )
# Now Do Predictons on the Test Data
# Firing Angle Test[0] 65  Distance 899
# Firing Angle Test[1] 45  Distance 1116
# Firing Angle Test[2] 25  Distance 804 
TestDataX = np.load("TestSetX.npy")
TestDataY = np.load("TestSetY.npy")

# Predict First Angle
print()
x_test = TestDataX[0,:,:]
x_test = x_test.reshape((1, NumberTimeSteps, NumberFeatures))
PredDistance = model.predict(x_test, verbose=1)
print(" First Sample Test (65,899): " + str(TestDataY[0]) + "  vs Predicted Value: " + str(PredDistance[0])) 

# Predict Second Angle
print()
x_test = TestDataX[1,:,:]
x_test = x_test.reshape((1, NumberTimeSteps, NumberFeatures))
PredDistance = model.predict(x_test, verbose=1)
print(" First Sample Test (45,1116): " + str(TestDataY[1]) + "  vs Predicted Value: " + str(PredDistance[0])) 

# Predict Third Angle
print()
x_test = TestDataX[2,:,:]
x_test = x_test.reshape((1, NumberTimeSteps, NumberFeatures))
PredDistance = model.predict(x_test, verbose=1)
print(" First Sample Test (25,804): " + str(TestDataY[2]) + " vs  Predicted Value: " + str(PredDistance[0])) 

# =============================================================================
print()
print(" *******************************  END ***************************************")
print()
# ======================================================================================================================
#