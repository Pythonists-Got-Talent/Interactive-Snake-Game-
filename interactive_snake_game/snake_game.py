import tkinter as tk
from random import randint
from PIL import Image, ImageTk
# from playsound import playsound
import pygame
from pygame import mixer
import time

# from directions import *
MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 3000 // MOVES_PER_SECOND
pygame.init()


# time.sleep(10)
class Snake(tk.Canvas):
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
        try:
            pygame.mixer.music.load('./assets/Snake_music.mp3')
            pygame.mixer.music.set_volume(0.03)
            pygame.mixer.music.play(-1)
            self.snake_head_image = Image.open("./assets/head2.png")
            self.snake_body_image = Image.open("./assets/body3.png")
            # self.snake_body_image = Image.open("./assets/head.png")
            # self.snake_head_image = Image.open("./assets/head.png")
            self.snake_head = ImageTk.PhotoImage(self.snake_head_image)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            self.food_image = Image.open("./assets/apple.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
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
        head_x_position, head_y_position = self.snake_positions[0]
        return (
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
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
            # pygame.mixer.music.queue('./assets/Snake_music.mp3')
            # pygame.mixer.music.load('./assets/Snake_music.mp3')
            # pygame.mixer.music.play(-1)

    def play_again(self):
        self.destroy()
        self.__init__()

    def end_game(self):
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
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if (
                new_direction in all_directions
                and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
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


    def clear():
        root.destroy()


    def play():
        mybtn.place(x=0, y=0)
        mybtn.destroy()
        board = Snake()


    my_label = tk.Label(root, text="Snake Game", width=13, height=1, bg='#D2B48C', fg='green',font="Times 15 bold")
    my_label.place(x=285, y=175)
    mybtn = tk.Button(root, text='Start', command=play, bg='#D2B48C', font="Times 10 bold", fg='green', padx=50, pady=0)
    mybtn.place(x=400, y=400)

    # bg_image = ImageTk.PhotoImage(file=r"./assets/edit_snake.png")
    # tk.Label(root, image=bg_image).place(relwidth=1, relheight=1)
    # my_label = tk.Label(root, text='Interactive snake game', width=20, height=1, bg='#E1F6FF',
    #                     font="Times 20 bold")

    # my_label.place(x=175, y=25)
    # button_start = tk.Button(root, text="start new game", command=play, bg='green', padx=40, pady=10,
    #                          font="Times 16 bold", borderwidth=2)
    # button_start.place(x=200, y=150)
    root.mainloop()