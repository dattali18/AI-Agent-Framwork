class AIAgentGame:
    def __init__(self, input_size: int, output_size: int):
        self.input_size = input_size
        self.output_size = output_size

    def get_state(self):
        """
        implement this function in order to train an AI agent
        :return: state of the game at current time
        """
        pass

    def play_step(self, action):
        """
        implement this function  in order to train an AI agent
        :param action: the action the game takes (developer choice)
        :return: None
        """
        pass
