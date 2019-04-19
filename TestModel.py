#  Testing Phase 
# LSTM Learning Against Ballistics Missiles
# 
# See Jason Brownlee clear explnation of Keras LSTM modelling 
#  https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
#
# Load the LSTM Model. and run Ballsitcis simulaitons against the LSTM Predictoon
#  requires pygame, numpy, matplotlib, keras [and hence Tensorflow or Theono backend] 
# ==========================================================================================
import Ballistics # My Ballistics Simulaiton 
import numpy as np 
import random 
#
# ======================================================================================================================
import matplotlib.pyplot as plt 
from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import load_model
# ======================================================================================================================
READY, LAUNCHING, LAUNCHCOMPLETE, FLYING, LANDED = range(5)
#
# =====================================================================
# Main Testing Loop Method 
def PerformTesting():
    
	#Create our Ballistcs instance
    TheSimulation = Ballistics.BallisticGame()
    # Test Set Shape  [#samples, #Time Steps, # Features] 
    SampleLength = 15
    NumberOfFeatures = 2
    TestSetX = np.zeros(shape=(1,SampleLength,NumberOfFeatures))
 
    FiringAngle = 45.0
    TestCount = 0
    SampleLength = 15	
    TheTestState = READY
    # =================================================================
    print(" ================ Start Of Testing ==================== ") 	
    print(" Creating a Load the Keras LSTM Model - Please Wait for GPU Card to be Initialised with Model ") 	
    print()	
	# Create an LSTM Recurrent Network
    model = Sequential()
    model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(SampleLength, NumberOfFeatures)))
    model.add(LSTM(32, activation='relu',return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
	
	# Now Load the Trained Model Weights From File 
    model = load_model("BallisticsModel.h5")
    # =================================================================	
    print()
    print()
    print(" *** Ready to Launch: Press Space Bar to Launch ") 
    ThekeyPressed = 'null'
    # Now Wait Upon Space Bar KeyPress to Launch  
    while(ThekeyPressed == 'null'):
       # Do Nothing Much
       ThekeyPressed = TheSimulation.ReadGameEventsKey()
	 
    TheTestState = LAUNCHING
    RandomAngleInt = random.randint(200,750)
    FiringAngle = 0.1 * float(RandomAngleInt)
    TheTestState, LaunchData = TheSimulation.SimulateLaunchPhase(FiringAngle)
			
    # Now Check the Luanch Complete - It Should Be perfom the predicton 
    if(TheTestState == LAUNCHCOMPLETE):
 
       # Compile the Launch Data into Correct Test Set Shape [#Samples, #Time Steps, # Features] 
       for i in range (0,SampleLength):
         TestSetX[0,i,0] =  LaunchData[i][0]	        
         TestSetX[0,i,1] =  LaunchData[i][1]	
			
       # Just be sure in correct Shape  - only One Sample
       TestSetX = TestSetX.reshape((1, SampleLength, NumberOfFeatures))
	   
	   # Now Perform the Prediction - Will return  List
       ModelPred = model.predict(TestSetX, verbose=1)

       print()
       print("Returned Prediction: " + str(ModelPred[[0]])) 	   
	
       # Now Set Up the Precitor Display	
       PredictedDistance = ModelPred[[0]]			
       TheSimulation.PlacePred(PredictedDistance)			
			
 	# ===================================
    print()
    print(" *** Prediction Completed : Press Space Bar to Continue Flight ") 
    # Now Wait Upon Sapace Bar To Continue  the Simulation
    ThekeyPressed = 'null'
    while(ThekeyPressed == 'null'):
       # Do Nothing Much
       ThekeyPressed = TheSimulation.ReadGameEventsKey() 
  
    # Complete the Missile Flight		
    TheTestState = FLYING
    TheTestState = TheSimulation.SimulateApproachPhase()      
 	# ===================================
    # Simulaton should have completed - Wait on Space Bar to Exit
    print()
    print(" *** Simulation Complete Completed : Press Space Bar to Exit ") 
    ThekeyPressed = 'null'
    while(ThekeyPressed == 'null'):
       # Do Nothing Much
       ThekeyPressed = TheSimulation.ReadGameEventsKey() 

	# ===================================
    print(" ================ The End of Testing ==================== ") 	
	# =================================
    TheSimulation.Closedown()   
	# =======================================================================
def main():
    #
	# Main Method Just Play our Experiment
	PerformTesting()
	
	# =======================================================================
if __name__ == "__main__":
    main()
