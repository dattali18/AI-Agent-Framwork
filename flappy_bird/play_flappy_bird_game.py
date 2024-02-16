from flappy_bird.flappy_bird import FlappyBirdGame
from ai_agent import Agent


def main():
    game = FlappyBirdGame()
    agent = Agent(game)
    agent.play(model_path="model.pth")


if __name__ == "__main__":
    main()
