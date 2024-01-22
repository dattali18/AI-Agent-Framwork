from snake_game import SnakeGameAI
from ai_agent import Agent


def main():
    game = SnakeGameAI()
    agent = Agent(game)
    agent.train(model_path="model.pth", training=False)


if __name__ == "__main__":
    main()
