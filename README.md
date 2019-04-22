## Ballistics RNN Predictions  ##
The use of Recurrent Nueral Networks to predict and defend against Ballistics 

This set of Files simulates basic 2-D ballistics fires using LSTM based neural networks to make predictions on the landing point and so aid air defence. The Predictions are based upon the profile of the initial few seconds of launch.  The LSTM is implemented using keras and the graphics use PyGame. 

![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/BallisticsPic.PNG "Ballistics Picture")

These examples are based upon Training a Keras based 2-layer LSTM network through a large number of ballistics firing samples (c.f. 400).  The X Input is the 2-D time sequence of the first 25 points during missile launch, and the Y dependent variable is the Distance to Landing point. The Training Data is captured through a large (c.f. 400) set of Ballistics simulations which are captured into  (TrainingSetX.npy and TrainingSetY.npy files. The LSTM model is then trained against this training set, over 100 epochs, and the model  saved in BallisticsModel.h5.  This model can then be used for Test predictions.   

Prediction of ballistics landing based upon the initial launch 15 values of (x,y) are used to feed the LSTM input sequence. The prediction in this 2-D representation therefore only two features, and one Y (Predicted Destination Distance) output:

![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/PredPic.PNG "Prediction Picture")

Although simple maths could perform these calculations. This example is to demonstrate how Recurrent Networks can be employed for time series predictions. More sophisticated missile dynamics, would obviously need access to lot more representative data samples to train the models upon.  

### Keras LSTM Model ###
I prefer to use keras, as it is simple way to understand and construct nueral networks. 
The core of the LSTM model is a two layers as follows:

  model = Sequential()
  model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(NumberTimeSteps, NumberFeatures)))
  model.add(LSTM(32, activation='relu',return_sequences=False))  
  model.add(Dense(1))
  model.compile(optimizer='adam', loss='mse')

NumberFearures = 2 and NumberTimeSteps = 15. I suspect that leads to some overfitting.  The model is trained over 100 epochs, and the loss profiles are a little erratic after the significant loss reductions within the first 20 epochs. 


![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/TrainingLoss.png "Loss Profile")

However the results are generally quite good, with Test predictions within 10.0m of the actuals

![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/SomePredictions.PNG "Loss Profile")

### Useage ###
* python CollectTrainingData.py   : This script captures a large set of Ballistics profiles Launch Data, and Destination data. Stores the Data in TrainingSetX/Y.npy numpy data files
* python TrainModel.py  : This script reads the TrainingData Sets and performs a keras LSTM model fit against the data. The Model is saved into BallisticsModel.h5 
* python TestModel.py   : This script loads the  BallisticsModel.h5 model, and makes a predictions from the initial Launch data. Press SPACE-BAR to Launch, To Continue and then to Exit. 

The Ballistics.py contains the ballistcs model, and animations displayed using Pygame. 

### Main Python Package Dependencies ###
pygame, keras [hence TensorFlow,Theano], numpy, matplotlib

### Acknowledgments: ###
* Jason Brownlee excellent explanation on setting up LSTM, and shaping the data to the required format is described here: 
 https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

Jason is exceptional in making Machine Learning accessible to mere mortals.
