import keras
import numpy as np
from keras.src.models import Sequential
from keras.src.layers import Dense
from game import Game

class AI:
    def __init__(self, game):
        self.game = game
        self.model = self.create_model(4, 3)
        self.game_states = []
        self.actions = []

    def create_model(self, input_dim, output_dim):
        model = Sequential()
        model.add(Dense(128, input_dim=input_dim, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(output_dim, activation='linear'))
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        return model

    def preprocess_data(self):
        X = np.array(self.game_states)
        y = np.array(self.actions)
        return X, y

    def train_model(self, X, y, epochs=100, batch_size=32):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    def evaluate_model(self, X_test, y_test):
        scores = self.model.evaluate(X_test, y_test, verbose=0)
        return scores

    def make_prediction(self):
        return self.model.predict(np.array([self.game_state]))[0]

    def play_game(self):
        self.game_state = self.game.game_state()
        prediction = AI.make_prediction(self.model, self.game_state)
        action = np.argmax(prediction)
        self.game.play(action)
