import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from snake_game.play_snake_game import main as play_snake
from flappy_bird.play_flappy_bird_game import main as play_flappy


def play_game(game_name):
    if game_name == "Snake":
        play_snake()
    elif game_name == "Flappy Bird":
        play_flappy()
    else:
        print("Invalid")


def train_game(game_name):
    print(f"Training {game_name}...")


# Create the main window
root = tk.Tk()
root.title("Game Selection")
# root.geometry("400x300")  # Set window size

style = ttk.Style()
#style.theme_use('aqua')

vstack = ttk.Frame(root)
vstack.pack(ipadx=100, ipady=20)  # Add external padding

# WindowTitle
window_title = ttk.Label(vstack, text="AI Agent Game", font=("Arial", 24))
window_title.pack(pady=10)  # Add internal padding

# HStack for each game
games = [
    {"name": "Snake", "image_path": "snake.jpg"},
    {"name": "Flappy Bird", "image_path": "flappy.webp"},
    {"name": "Dino", "image_path": "snake.jpg"}
]

for game in games:
    hstack = ttk.Frame(vstack)
    hstack.pack(pady=10)  # Add spacing between games

    # Load and resize the image
    image = Image.open(game["image_path"])
    image = image.resize((100, 100))  # Resize the image to 100x100
    photo = ImageTk.PhotoImage(image)

    # Create a label with the image and text
    game_label = ttk.Label(hstack, text=game["name"], image=photo, compound=tk.TOP, font=("Arial", 18))
    game_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
    game_label.pack(padx=10, pady=10, ipadx=10, ipady=10)

    play_button = ttk.Button(hstack, text="Play", command=lambda game_name=game["name"]: play_game(game_name))
    play_button.pack(side=tk.LEFT, padx=5, pady=5)  # Add padding to the left and top

    train_button = ttk.Button(hstack, text="Train", command=lambda game_name=game["name"]: train_game(game_name))
    train_button.pack(side=tk.RIGHT, padx=5, pady=5)  # Add padding to the right and top

# Start the GUI event loop
if __name__ == "__main__":
    # Start the GUI event loop
    root.mainloop()
