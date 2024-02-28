import torch
import random
import numpy as np
from collections import deque
from . import Linear_QNet, QTrainer
from .game import AIAgentGame

from typing import List, Union

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self, game: AIAgentGame):
        self.game = game
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(self.game.input_size, 256, self.game.output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self) -> np.ndarray:
        return np.array(self.game.get_state(), dtype=float)

    def remember(self, state: np.ndarray, action: List[int], reward: int, next_state: np.ndarray, done: bool) -> None:
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self) -> None:
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state: np.ndarray, action: List[int], reward: int, next_state: np.ndarray, done: bool):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state: np.ndarray, training: bool = True) -> List[int]:
        # random moves: tradeoff exploration / exploitation
        size = self.game.output_size
        final_move: List[int] = [0] * size

        if training:

            self.epsilon = 250 - self.n_games
            # if random.randint(0, 10) == (self.n_games % 10):

            # if random.randint(0, 350) < self.epsilon or random.randint(0, 10) == (self.n_games % 10):
            if random.randint(0, 10) == (self.n_games % 10):
                move = random.randint(0, size - 1)
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

    def play(self, model_path: str):
        if not model_path:
            return

        self.model.load(model_path)

        record = 0

        while True:
            state = self.get_state()
            final_move = self.get_action(state, training=False)

            # perform move and get new state
            reward, done, score = self.game.play_step(final_move)

            if done:
                self.game.reset()
                self.n_games += 1

                if record < score:
                    record = score

                print('Game:', self.n_games, 'Score:', score, 'Record:', record)

    def train(self, model_path: Union[str, None] = None, training: bool = True) -> None:
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
