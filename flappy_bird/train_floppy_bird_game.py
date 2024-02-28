from flappy_bird import FlappyBirdGame
from ai_agent import Agent


def main():
    game = FlappyBirdGame()
    agent = Agent(game)
    agent.train(model_path="model_v1.0.pth", training=False)
    # agent.play(model_path="model_v1.0.pth")


if __name__ == "__main__":
    main()
