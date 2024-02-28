from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple


class AIAgentGame(ABC):
    def __init__(self, input_size: int, output_size: int, main_window=None):
        self.input_size = input_size
        self.output_size = output_size
        self.main_window = main_window

    @abstractmethod
    def get_state(self) -> np.ndarray:
        """
        implement this function in order to train an AI agent
        :return: state of the game at current time
        """
        pass

    @abstractmethod
    def play_step(self, action: List[int]) -> Tuple[int, bool, int]:
        """
        implement this function  in order to train an AI agent
        :param action: the action the game takes (developer choice)
        :return: None
        """
        pass

    @abstractmethod
    def reset(self):
        """
        implement this function  in order to train an AI agent
        this function reset the game inorder to continually train the model
        """
        pass
