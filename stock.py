from utils import *
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

def buildModel(train_subset, val_subset, test_subset,hParams):
    # print(np.array(test_data)[:, np.newaxis])
    # Build the model
    train_x, train_y, train_scaler = train_subset
    val_x, val_y, val_scaler = val_subset
    test_x, test_y, test_scaler = test_subset


    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(128, return_sequences=True, input_shape= (train_x.shape[1], 1)),
        tf.keras.layers.LSTM(32,activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error', metrics = ['mae'])
    # Train the model
    history = model.fit(train_x,train_y, epochs=hParams['epochs'], validation_data = (val_x,val_y))
    # Evaluate the model on the test data
    test_loss = model.evaluate(test_x, test_y)
    # print(test_loss)
    # Make predictions on new data
    predictions = model.predict(test_x)
    predictions = test_scaler.inverse_transform(predictions)
    model.save('stock.h5')
    return predictions

def main():
    df = get_stock('AAPL',"2020-12-31","2022-12-31")
    hParams = {
        'test_prop': 0.1,
        'valid_prop':0.2,
        'look_back': 10,
        'epochs': 50,
        'LSTM': [128, 32],
        'Dense': [32,32]
    }

    train_data,val_data, test_data = preprocessing(df,hParams)
    train_subset = generate_data(train_data, hParams['look_back'])
    val_subset =  generate_data(val_data, hParams['look_back'])
    test_subset =  generate_data(test_data, hParams['look_back'])
    predictions = buildModel(train_subset,val_subset,test_subset,hParams)
    plotPredictions(df,predictions,hParams)

# main()


