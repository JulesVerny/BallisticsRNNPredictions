#
# LSTM Learning Against Ballistics Missiles
# See Jason Brownlee clear explnation of Keras LSTM modelling 
#  https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
#
#  requires pygame, numpy, matplotlib, keras [and hence Tensorflow or Theono backend] 
# ==========================================================================================
import Ballistics # My Ballistics Simulaiton 
import numpy as np 
import random 
import matplotlib.pyplot as plt
#
# =======================================================================
#
# =====================================================================
# Main Experiment Method 
def CollectTrainingData():
    
    PlotHistory = []
	
	#Create our Ballistcs instance
    TheSimulation = Ballistics.BallisticGame()
 
    FiringAngle = 45.0
	
    NumberSamples = 400
    SampleCount = 0
    SampleLength = 15
	
    NumberTestSamples = 3
	
	# Create the TrainingSet
    TrainingSetX = np.zeros(shape=(NumberSamples,SampleLength,2))
    TrainingSetY = np.zeros(shape=(NumberSamples))
	# test Set
    TestSetX = np.zeros(shape=(NumberTestSamples,SampleLength,2))
    TestSetY = np.zeros(shape=(NumberTestSamples))
	
    # =================================================================
    KeepTraining=True

    print("  ============================================= ")
    print("  Collecting : " + str(NumberSamples) " + Samples ")
    print()	
	
    # Create a large randomsTraining Set	
    while (KeepTraining and (SampleCount< NumberSamples)):

      ThekeyPressed = TheSimulation.ReadGameEventsKey()	

      if(ThekeyPressed=='quit'):
         KeepTraining = False

      # Random Choice of Firing Angle
      RandomAngleInt = random.randint(200,750)
      FiringAngle = 0.1 * float(RandomAngleInt)
		 
      FAngle,MissileDistance,RunTrace = TheSimulation.SimulateFiring(FiringAngle) 

	  #  Now Log the raining Results 
      print(" Sample: " + str(SampleCount) +  "  Training Firing Angle: " + str(int(FAngle)) + "  Distance: " + str(int(MissileDistance))) 
	  	  
	  # Capture the Training Set TrainingSet[sample, timeset, feature]		  
      # copy first 15 x,y into numpy array
      for i in range (0,SampleLength):
         TrainingSetX[SampleCount,i,0] =  RunTrace[i][0]	        
         TrainingSetX[SampleCount,i,1] =  RunTrace[i][1]	 	  
  
      TrainingSetY[SampleCount] = MissileDistance
  
      PlotHistory.append((FAngle,MissileDistance,))
			
      SampleCount = SampleCount+1	  
	# ===============================================
	# End of Training Loop  so Scatter Plot the Firing Angle vs Missile Distance
    x_val = [x[0] for x in PlotHistory]
    y_val = [x[1] for x in PlotHistory]

    """
    plt.scatter(x_val,y_val)
    plt.xlabel("Firing Angle")
    plt.ylabel("Distance")
    plt.show()
	#
    """
	# Save the Training Set
    np.save("TrainingSetX.npy",TrainingSetX)
    np.save("TrainingSetY.npy",TrainingSetY)
	# 
	# =======================================================================
	# Create the Test Sets  At Firing Angles 25, 45, 65
    FiringAngle = 25.0 
    FAngle,MissileDistance,RunTrace = TheSimulation.SimulateFiring(FiringAngle) 
    print(" Test Firing Angle: " + str(int(FAngle)) + "  Distance: " + str(int(MissileDistance))) 
	# Capture the Test Case[sample, timeset, feature]		  
    # copy first 15 x,y into numpy array 
    for i in range (0,SampleLength):
       TestSetX[0,i,0] =  RunTrace[i][0]	        
       TestSetX[0,i,1] =  RunTrace[i][1]	 	  
    TestSetY[0] = MissileDistance
	
    FiringAngle = 45.0 
    FAngle,MissileDistance,RunTrace = TheSimulation.SimulateFiring(FiringAngle) 
    print(" Test Firing Angle: " + str(int(FAngle)) + "  Distance: " + str(int(MissileDistance))) 
	# Capture the Test Case[sample, timeset, feature]		  
    # copy first 15 x,y into numpy array 
    for i in range (0,SampleLength):
       TestSetX[1,i,0] =  RunTrace[i][0]	        
       TestSetX[1,i,1] =  RunTrace[i][1]	 	  
    TestSetY[1] = MissileDistance

    FiringAngle = 65.0 
    FAngle,MissileDistance,RunTrace = TheSimulation.SimulateFiring(FiringAngle) 
    print(" Test Firing Angle: " + str(int(FAngle)) + "  Distance: " + str(int(MissileDistance))) 
	# Capture the Test Case[sample, timeset, feature]		  
    # copy first 15 x,y into numpy array 
    for i in range (0,SampleLength):
       TestSetX[2,i,0] =  RunTrace[i][0]	        
       TestSetX[2,i,1] =  RunTrace[i][1]	 	  
    TestSetY[2] = MissileDistance
	# 
	# Save the Test Data
    #print("Test X Set Shape")
    # print(TestSetX.shape)
	# Save the Training Set
    np.save("TestSetX.npy",TestSetX)
    np.save("TestSetY.npy",TestSetY)
	
    print("  ============================================= ")  
    print("  Collection Complete Saved in TrainingSetX.npy and TrainingSetY.npy numpy Data files")
	print("  ============================================= ")
	# =================================
    TheSimulation.Closedown()   
	# =======================================================================
def main():
    #
	# Main Method Just Play our Experiment
	CollectTrainingData()
	
	# =======================================================================
if __name__ == "__main__":
    main()
