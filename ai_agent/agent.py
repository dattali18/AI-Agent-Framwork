import torch
import random
import numpy as np
from collections import deque
from . import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self, game):
        self.game = game
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(self.game.input_size, 256, self.game.output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self):
        return np.array(self.game.get_state(), dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, training=True):
        # random moves: tradeoff exploration / exploitation
        size = self.game.output_size
        final_move = [0] * size
        if training:
            self.epsilon = 80 - self.n_games

            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, size)
                final_move[move] = 1
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

    def train(self, model_path=None, training=True):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0

        if model_path is not None:
            self.model.load(model_path)

        while True:
            # get old state
            state_old = self.get_state()

            # get move
            final_move = self.get_action(state_old, training=training)

            # perform move and get new state
            reward, done, score = self.game.play_step(final_move)
            state_new = self.get_state()

            # train short memory
            self.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            self.remember(state_old, final_move, reward, state_new, done)

            if done:
                # train long memory, plot result
                self.game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    if model_path:
                        self.model.save(model_path)
                    else:
                        self.model.save()

                # Print to console
                print('Game:', self.n_games, 'Score:', score, 'Record:', record)

                # mean_score = total_score / self.n_games

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)