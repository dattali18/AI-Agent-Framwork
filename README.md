## How to Use AI-Agent-Framework

### Overview
The AI-Agent-Framework provides a flexible framework for training and playing games using AI agents. It follows a simple architecture where the game, agent, and model components interact with each other to train and play games.

### Prerequisites
Before using the AI-Agent-Framework, ensure you have Python 3.6 or higher installed. You'll also need to install the required packages listed in the `requirements.txt` file using `pip install -r requirements.txt`.

### Implementing the AIAgentGame Interface
1. **Import the `AIAgentGame` class**: Start by importing the `AIAgentGame` class from `ai_agent.game`.

2. **Create a Game Class**: Create a subclass of `AIAgentGame` for your game. This class will implement the game logic and interactions with the AI agent.

3. **Implement Required Methods**:
   - `get_state()`: Return the current state of the game as a list or numpy array.
   - `play_step(action)`: Take an action (input) and return a tuple `(reward, game_over, score)`.
   - `reset()`: Reset the game to its initial state.

Example implementation for any game:

```python
from ai_agent.game import AIAgentGame

class MyGame(AIAgentGame):
    def __init__(self):
        super().__init__(input_size=YOUR_STATE_SIZE, output_size=YOUR_ACTION_SIZE)
        # Your game initialization code here

    def get_state(self):
        # Your get_state implementation here

    def play_step(self, action):
        # Your play_step implementation here

    def reset(self):
        # Your reset implementation here
```

### Training the AI Agent
1. **Import the `Agent` class**: Import the `Agent` class from `ai_agent`.

2. **Create an Agent Instance**: Create an instance of the `Agent` class, passing your game instance to its constructor.

3. **Train the Agent**: Call the `train` method of the `Agent` instance to start training the AI agent.

Example training code:

```python
from ai_agent import Agent

def main():
    game = MyGame()
    agent = Agent(game)
    agent.train(model_path="model.pth")

if __name__ == "__main__":
    main()
```

### Playing the Game with the AI Agent
1. **Create an Agent Instance**: Create an instance of the `Agent` class, passing your game instance to its constructor.

2. **Play the Game**: Call the `play` method of the `Agent` instance to play the game with the trained AI agent.

Example playing code:

```python
from ai_agent import Agent

def main():
    game = MyGame()
    agent = Agent(game)
    agent.play(model_path="model.pth")

if __name__ == "__main__":
    main()
```

Follow these steps to integrate the AI-Agent-Framework into your game and train/play with your AI agent. Remember, the specific game implementation details don't matter as long as you implement the required functions correctly. The `input_size` and `output_size` in the `super().__init__` should match the size of the state returned by `get_state` and the actions received by `play_step`, respectively.

## GUI for the AI Agent with 3 examples

### Images

Main GUI Window

<img width="400" src="/AI-Agent-Framwork/images/main_window.png">

Snake Game Window

<img width="400" src="/AI-Agent-Framwork/images/snake_window.png">

Flappy Game Window

<img width="400" src="/AI-Agent-Framwork/images/flappy_window.png">