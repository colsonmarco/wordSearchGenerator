import numpy as np
from english_words import english_words_lower_alpha_set
import random

def generate_words(num_words, max_word_length, custom_words = []):
    """
    Generates a list of random words governed by a max word length.

    Args:
        num_words: Int specifying how many words should be randomly selected.
        max_word_length: An int governing the max length a word should be.
    
    Returns: A list containing the random words.
    """
    words = []
    if custom_words != []:
        while len(words) < num_words and custom_words != words:
            words.append(random.choice(custom_words))
    while len(words) < num_words:
        word = (random.choice(english_words_lower_alpha_set))
        if len(word) <= max_word_length:
            words.append(word)
    return words

def generate_board(grid_width, grid_height, word_list = []):
    global grid
    chars = 'abcdefghijklmnopqrstuvwxyz'
    if word_list != []:
        chars = ''
        for word in word_list:
            for char in word:
                if char not in chars:
                    chars += char

    grid = np.chararray((grid_width, grid_height)).astype(str)
    for i in range(grid_width):
        for j in range(grid_height):
            grid[i, j] = random.choice(chars)


def display_grid(grid):
    """
    Displays a grid of chars for the word search.

    Args:
        grid: A 2D np array of one character strings representing the word
        search board.
    """
    for row in grid:
        for char in row:
            print(f" {char}", end = '')
        print()

def diagonal(word):
    global grid
    grid_width, grid_height = grid.shape()
    max_row = grid_height - len(word)
    max_column = grid_width - len(word)
    row_index = random.randrange(max_row)
    col_index = random.randrange(max_column)
    for char in word:
        grid[row_index, col_index] = char
        row_index += 1
        col_index += 1


def horizontal(word):
    global grid
    grid_width, grid_height = grid.shape()
    max_row = grid_height - 1
    max_column = grid_width - len(word)
    row_index = random.randrange(max_row)
    col_index = random.randrange(max_column)
    for char in word:
        grid[row_index, col_index] = char
        col_index += 1


def vertical(word):
    global grid
    grid_width, grid_height = grid.shape()
    max_row = grid_height - len(word)
    max_column = grid_width - 1
    row_index = random.randrange(max_row)
    col_index = random.randrange(max_column)
    for char in word:
        grid[row_index, col_index] = char
        row_index += 1


def add_in_words(word_list):
    global grid
    orientations = [diagonal, vertical, horizontal]
    for word in word_list:
        random.choice(orientations)(word)

def start_game(num_words, grid_width, grid_height, max_word_length = None, hard_mode = 0, custom_words = []):
    if max_word_length == None:
        max_word_length = min(grid_height, grid_width)
    words = generate_words(num_words, max_word_length, custom_words)
    generate_board(grid_width, grid_height, words)
    global grid
    print("test")
    display_grid(grid)

start_game(10, 10, 10)