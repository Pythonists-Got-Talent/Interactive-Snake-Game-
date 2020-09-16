"""
This file is for the snake game using tkinter library
"""

# the libraries we need
import tkinter as tk
from random import randint
from PIL import Image, ImageTk
# from playsound import playsound
import pygame
from pygame import mixer
import time
from tkinter import ttk

# from directions import *
MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 3000 // MOVES_PER_SECOND
pygame.init()
# bk_song = pygame.mixer.music.load('./assets/Snake_music.mp3')

# time.sleep(10)
class Snake(tk.Canvas):
    """
    Class to represent the snake game contains all of the methods we need to play the game.
    """
    def __init__(self):
        super().__init__(
            width=600, height=620, background="lemon chiffon", highlightthickness=0
        )

        self.pack(pady=50)
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"
        self.score = 0
        self.load_assets()
        self.create_objects()
        self.bind_all("<Key>", self.on_key_press)
        # self.pack()
        self.after(GAME_SPEED, self.perform_actions)
        # self.end =tk.Button(self, text="End").pack()

    def load_assets(self):
        """
        Method to upload all the pictures and sounds we used in the game.
        """
        try:
            global bk_song
            global last_song
            # song_bk = bk_song
            # song_bk
            pygame.mixer.music.load(last_song)
            pygame.mixer.music.set_volume(0.02)
            pygame.mixer.music.play(-1)

            self.snake_head_image = Image.open("./assets/head2.png")
            self.snake_body_image = Image.open("./assets/body3.png")

            self.snake_head = ImageTk.PhotoImage(self.snake_head_image)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            self.food_image = Image.open("./assets/apple.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        """
        Method to creat the Snake in the game plase.
        """
        self.create_text(
            35, 12, text=f"Score: {self.score}", tag="score", fill="green", font=(10)
        )
        count = 0
        for x_position, y_position in self.snake_positions:
            if count == 0:
                self.create_image(
                    x_position, y_position, image=self.snake_head, tag="snake"
                )
            else:
                self.create_image(
                    x_position, y_position, image=self.snake_body, tag="snake"
                )
            count = 1
        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def check_collisions(self):
        """
        Method to ensure the head of the snake not crashed with the snake body. 
        """
        head_x_position, head_y_position = self.snake_positions[0]
        return (
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        """
        Method to add the food of the snake and ensure its not in the snake body positions.
        """
        if self.snake_positions[0] == self.food_position:
            # pygame.mixer.music.stop()
            eat = pygame.mixer.Sound('./assets/apple.wav')
            eat.play()
            # pygame.mixer.music.stop()
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")


    def play_again(self):
        """
        Method to run the game again.
        """
        self.destroy()
        # print(num)
        pygame.mixer.music.load(last_song)
        self.__init__()

    def end_game(self):
        """
        Method to end the game when the snake eat it self or when the snake crushed on the wall.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./assets/gameover.mp3')
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play()

        again = tk.Button(root, text='Play Again', command=self.play_again, font="Times 10 bold", bg="green")
        again.place(x=380, y=400)
        mybtn2 = tk.Button(root, text='Quit Game', command=clear, bg="red", font="Times 10 bold")
        mybtn2.place(x=380, y=500)
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            (self.winfo_height() / 2)-60,
            text=f"Game over!",
            fill="red",
            font=("", 20)
        )
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"You scored {self.score}!",
            fill="#000",
            font=("", 10)
        )

    def move_snake(self):
        """
        Method to move the snake.
        """
        head_x_position, head_y_position = self.snake_positions[0]
        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        """
        Method to avoid taking the opposite direction.
        """
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if (
                new_direction in all_directions
                and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def perform_actions(self):
        """
        Method to run the functionality of the game.
        """
        if self.check_collisions():
            self.end_game()
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
        """
        Method to put the food in a random location.
        """
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return food_position


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Snake")
    root.geometry("980x720")  # Width x Height

    bk_image = Image.open('./assets/bk3.jpg')
    bk_image = bk_image.resize((980, 720), Image.ANTIALIAS)
    resized1 = ImageTk.PhotoImage(bk_image)
    backgroundLabel = tk.Label(root, image=resized1)
    backgroundLabel.place(x=0, y=0)
    root.resizable(False, False)
    root.tk.call("tk", "scaling", 4.0)
    last_song='./assets/'


    def clear():
        """
        Method to close the game.
        """
        root.destroy()

    def level():
        """
        Method to choose the speed of the snake from the user
        """
        global easy
        global meduim
        global hard
        global GAME_SPEED
        global MOVES_PER_SECOND
        if easy.get():
            GAME_SPEED = 3000 // MOVES_PER_SECOND
        if meduim.get():
            GAME_SPEED = 2000 // MOVES_PER_SECOND

        if hard.get():
            GAME_SPEED = 1000 // MOVES_PER_SECOND
        if extreme.get():
            GAME_SPEED = 400 // MOVES_PER_SECOND





    def play():
        """
        Method to run the game.
        """
        level()
        ck_easy.destroy()
        ck_meduim.destroy()
        ck_hard.destroy()
        ck_extreme.destroy()
        global last_song

        global bk_song
        last_song += comboExample.get() +'.mp3'
        labelTop.destroy()
        comboExample.destroy()

        mybtn.place(x=0, y=0)
        mybtn.destroy()
        board = Snake()


    my_label = tk.Label(root, text="Snake Game", width=13, height=1, bg='#D2B48C', fg='green',font="Times 15 bold")
    my_label.place(x=285, y=175)
    mybtn = tk.Button(root, text='Start', command=play, bg='#D2B48C', font="Times 10 bold", fg='green', padx=50, pady=0)
    mybtn.place(x=400, y=400)


    # pygame.mixer.music.load('./assets/hakona_start.mp3')
    # pygame.mixer.music.set_volume(0.2)
    # pygame.mixer.music.play()

    pygame.mixer.Sound('./assets/hakona_start2.wav').play()

    # pygame.mixer.music.load('./assets/jungle.mp3')
    # pygame.mixer.music.set_volume(0.01)
    # pygame.mixer.music.play()

    # pygame.mixer.music.load('./assets/merged.mp3')
    # pygame.mixer.music.set_volume(0.01)
    # pygame.mixer.music.play()


    def callBackFunc(var):
        var.set(True)

    # Choose Level
    easy = tk.BooleanVar()
    easy.set(False)
    ck_easy = tk.Checkbutton(root, text="Easy", variable=easy,command=callBackFunc(easy))
    ck_easy.place(x=400,y=500)
    ck_easy.deselect()



    meduim = tk.BooleanVar()
    meduim.set(False)
    ck_meduim = tk.Checkbutton(root, text="Meduim", variable=meduim,command=callBackFunc(meduim))
    ck_meduim.place(x=500,y=500)
    ck_meduim.deselect()


    hard = tk.BooleanVar()
    hard.set(False)
    ck_hard = tk.Checkbutton(root, text="Hard", variable=hard,command=callBackFunc(hard))
    ck_hard.place(x=600,y=500)
    ck_hard.deselect()

    extreme = tk.BooleanVar()
    extreme.set(False)
    ck_extreme = tk.Checkbutton(root, text="Extreme, for people with strong hearts only!", variable=extreme,command=callBackFunc(extreme))
    ck_extreme.place(x=400,y=530)
    ck_extreme.deselect()

    # Choose Song
    fontExample = ("Courier", 5, "normal")

    labelTop = tk.Label(root,
                        text="Choose your song",
                        font = fontExample)
    labelTop.place(x=400,y=570)

    comboExample = ttk.Combobox(root,
                                values=[
                                    "Basic Snake Music",
                                    "Hakona Matata",
                                    "In the jungle",
                                    "Dance Monkey",
                                    "Havana",
                                    "Crazy Frog"],
                                font = fontExample)
    comboExample.current(0)
    root.option_add('*TCombobox*Listbox.font', fontExample)

    comboExample.place(x=400,y=600)

    root.mainloop()