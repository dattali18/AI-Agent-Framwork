from flappy_bird import FlappyBirdGame
from ai_agent import Agent


def main():
    game = FlappyBirdGame()
    agent = Agent(game)
    agent.train(model_path="model_1.pth", training=True)
    # agent.play(model_path="model.pth")


if __name__ == "__main__":
    main()
