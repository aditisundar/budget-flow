"""
Supervised ML on financial data.
"""

import h5py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split


def preprocess_data():
    # Load and basic cleaning.
    data = pd.read_csv('../../data/dummy_data.csv')
    data = data.drop(['Unnamed: 0'], axis = 1)
    data = pd.concat([data, pd.get_dummies(pd.Series(data['zipcodes']))], axis=1).drop(['zipcodes'], axis=1)

    # Get the 3 datasets.
    data_food = data.drop(['essentials', 'IEE'], axis=1)
    data_essentials = data.drop(['food', 'IEE'], axis=1)
    data_iee = data.drop(['food', 'essentials'], axis=1)

    return {'food': data_food, 'essentials': data_essentials, 'IEE': data_iee}

def build_model(input_shape):
    model = keras.Sequential()
    model.add(keras.layers.Dense(100, activation='relu',input_shape=(input_shape,)))
    model.add(keras.layers.Dense(100, activation='relu'))
    model.add(keras.layers.Dense(1))
    model.compile(loss='mse',
                    optimizer='rmsprop',
                    metrics=['mae'])
    return model

def split(dataset, variable):
    X_train, X_test, y_train, y_test =  train_test_split(dataset.drop([variable], axis=1), dataset[variable], test_size=0.1, random_state=13)
    mean = X_train['income'].mean(axis=0)
    std = X_train['income'].std(axis=0)
    X_train['income'] = (X_train['income'] - mean) / std
    X_test['income'] = (X_test['income'] - mean) / std
    return X_train, X_test, y_train, y_test

def train_model(train_data, train_labels, model):
    model.fit(train_data, train_labels, epochs=250,
                validation_split=0.2, verbose=0)
    return model

def predict(test_data, model):
    return model.predict(test_data).flatten()

def get_mean_std():
    all_data = preprocess_data()
    ms = dict()
    for key, value in all_data.items():
        X_train, X_test, y_train, y_test =  train_test_split(value.drop([key], axis=1), value[key], test_size=0.1, random_state=13)
        mean = X_train['income'].mean(axis=0)
        std = X_train['income'].std(axis=0)
        ms[key] = (mean, std)
    return ms


if __name__ == '__main__':
    all_data = preprocess_data()
    for key, value in all_data.items():
        X_train, X_test, y_train, y_test = split(value, key)
        model = build_model(X_train.shape[1])
        model = train_model(X_train, y_train, model)
        model.save(key + '.h5')

