from interactive_snake_game.snake_game import *
import pytest


def test_food_collision(prepare_snake):
    snake = prepare_snake
    snake_length = len(snake.snake_positions)
    snake.snake_positions[0] = snake.food_position
    snake.check_food_collision()
    assert snake.snake_positions[0] != snake.food_position[0]
    assert len(snake.snake_positions) == snake_length + 1

def test_score(prepare_snake):
    snake = prepare_snake
    snake.snake_positions[0] = snake.food_position
    snake.check_food_collision()
    assert snake.score == 1


def test_moving_snake_to_the_left(prepare_snake):
    snake = prepare_snake
    x_position, y_postion = snake.snake_positions[0]
    snake.direction = 'Left'
    snake.move_snake()
    x_position -= 20
    assert snake.snake_positions[0][0] == x_position

def test_moving_snake_Up(prepare_snake):
    snake = prepare_snake
    x_position, y_postion = snake.snake_positions[0]
    snake.direction = 'Up'
    snake.move_snake()
    y_postion -= 20
    assert snake.snake_positions[0][1] == y_postion

def test_collision_with_screen(prepare_snake):
    snake = prepare_snake
    snake.snake_positions = [(600,50)] + snake.snake_positions[:-1]
    assert snake.check_collisions() == True

@pytest.fixture
def prepare_snake():
    snake = Snake()
    return snake