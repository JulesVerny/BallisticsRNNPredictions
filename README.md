## Ballistics RNN Predictions  ##
Using Recurrent Nueral Networks to predict ballistics 

This set of Files simulates basic balistics fires and uses LSTM based neural networks to make predictions on the landing point, based upon the profile of the launch (first few seconds of launch).  

![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/BallisticsPic.PNG "Ballistics Picture")

This is achieved through Training the Keras based 2-layer LSTM network through a large number of ballistics firing samples (c.f. 400).  The X is a Time sequence of the first launch Porfile (first 25 [x,y] positions)  and the Y predicted valye is the Distance to Target. The Training Data is captured from a large (c.f. 400) set of Ballistics samples through simulation. The LSTM model is then trained against this sample set. 

### LSTM Model ###
I prefer to use keras, as it is simple way to understand and construct nueral networks. 
The core of the model is a two layer LSTM Model:

model = Sequential()
model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(NumberTimeSteps, NumberFeatures)))
model.add(LSTM(32, activation='relu',return_sequences=False))  
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

I suspect that leads to some overfitting.  The model is traiend over 100 epochs, and the loss profiles becoems rather erratic after the significant loss redcutions in th first 20 epochs. 

![picture alt](https://github.com/JulesVerny/BallisticsRNNPredictions/blob/master/TrainingLoss.PNG "Loss Profile")

However the results are genrally quite good, with Test predictions within 5.0 of the actuals

### Useage ###
* python CollectTrainingData.py   : This script captures a large set of Ballistics profiles Launch Data, and Destination data. Stores the Data in TrainingSetX/Y.npy numpy data files
* python TrainModel.py  : This script reads the TrainingData Sets and performs a keras LSTM model fit agaisnt the data. The Model is saved into BallisticsModel.h5 
* python TestModel.py   : This script loads the  BallisticsModel.h5 model, and makes a predictions from the initial Launch data. Press SPACE-BAR to Launch, To Continue and then to Exit. 

The Ballistics.py contains the ballistcsmodel, and annimimatiosn in Pygame. 


### Main Python Package Dependencies ###
pygame, keras [hence TensorFlow,Theano], numpy, matplotlib

### Acknowledgments: ###
* Setting up LSTM, and shaping the data to the required format is described amongst Jason Brownlee excellent explanation
 https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
 Jason is exceptional in making Machine Learning accessible to mere mortals.
