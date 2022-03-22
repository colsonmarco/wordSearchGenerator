import sys
import getopt
import numpy as np
from english_words import english_words_lower_alpha_set
import random
from tkinter import *

def generate_words(num_words, max_word_length, custom_words):
    """
    Generates a list of random words governed by a max word length.

    Args:
        num_words: Int specifying how many words should be randomly selected.
        max_word_length: An int governing the max length a word should be.
    
    Returns: A list containing the random words.
    """
    words = []
    if custom_words != []:
        print(custom_words)
        while len(words) < num_words and custom_words != []:
            words.append(random.choice(custom_words))
            custom_words.remove(words[-1])
    while len(words) < num_words:
        word = random.choice(tuple(english_words_lower_alpha_set))
        if len(word) <= max_word_length:
            word = word.lower()
            words.append(word)
    return words

def generate_board(grid_width, grid_height, word_list = []):
    global grid
    grid = np.empty([grid_width, grid_height], dtype = str)
    for i in range(grid_width):
        for j in range(grid_height):
            grid[i, j] = str('0')


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

def get_horizontal_options(word):
    global grid
    safe_zones = []
    for i in range(np.shape(grid)[0]):
        safe_zone_start = (i, 0)
        for j in range(np.shape(grid)[1]):
            if j == np.shape(grid)[1] - 1:
                safe_zones.append((safe_zone_start, (i, j)))
            if grid[i,j] != '0':
                safe_zones.append((safe_zone_start, (i, j - 1)))
                safe_zone_start = (i, j + 1)
    safe_zones = [zone for zone in safe_zones if zone[1][1] - zone[0][1] >= len(word)]
    return safe_zones


def get_vertical_options(word):
    global grid
    safe_zones = []
    for j in range(np.shape(grid)[1]):
        safe_zone_start = (0, j)
        for i in range(np.shape(grid)[0]):
            if i == np.shape(grid)[0] - 1:
                safe_zones.append((safe_zone_start, (i, j)))
            if grid[i,j] != '0':
                safe_zones.append((safe_zone_start, (i - 1, j)))
                safe_zone_start = (i + 1, j)
    safe_zones = [zone for zone in safe_zones if zone[1][0] - zone[0][0] >= len(word)]
    return safe_zones


def diagonal(word):
    global grid
    shape = np.shape(grid)
    grid_width = shape[0]
    grid_height = shape[1]
    max_row = grid_height - len(word)
    max_column = grid_width - len(word)
    try:
        col_index = random.randrange(max_column)
        row_index = random.randrange(max_row)
    except:
        row_index = 0
        col_index = 0
    for char in word:
        grid[row_index, col_index] = char
        row_index += 1
        col_index += 1


def horizontal(word):
    global grid
    safe_zones = get_horizontal_options(word)
    zones_equalized = []
    for zone in safe_zones:
        for i in range(zone[1][1] - zone[0][1] - len(word) + 2):
            zones_equalized.append([[zone[0][0], zone[0][1] + i], [zone[0][0], zone[0][1] + len(word) - 1 + i]])
    chosen_zone = random.choice(zones_equalized)
    for char in word:
        grid[chosen_zone[0][0], chosen_zone[0][1]] = char
        chosen_zone[0][1] += 1


def vertical(word):
    global grid
    safe_zones = get_vertical_options(word)
    zones_equalized = []
    for zone in safe_zones:
        for i in range(zone[1][0] - zone[0][0] - len(word) + 2):
            zones_equalized.append([[zone[0][0] + i, zone[0][1]], [zone[0][0] + len(word) - 1 + i, zone[0][1]]])
    chosen_zone = random.choice(zones_equalized)
    for char in word:
        grid[chosen_zone[0][0], chosen_zone[0][1]] = char
        chosen_zone[0][0] += 1


def add_in_words(word_list):
    global grid
    orientations = [vertical, horizontal]
    i = 1
    for word in word_list:
        try:
            random.choice(orientations)(word)
            print(f"{i}:\t{word}")
            i += 1
        except:
            continue

def fill_in_board():
    global chars
    global grid
    for i in range(np.shape(grid)[0]):
        for j in range(np.shape(grid)[1]):
            if grid[i, j] == '0':
                grid[i, j] = random.choice(chars)




def parse_sys_args(argv):
    global num_words, grid_width, grid_height, max_word_length, hard_mode, custom_words
    num_words = 10
    grid_width = 20
    grid_height = 20
    hard_mode = False
    custom_words = []

    arg_help = "{0} <help> -n <num_words> -w <grid_width> -h <grid_height> -m <max_word_length> -d <difficult_mode> -c <custom_words>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "n:w:h:m:d:c", ["help",
        "num_words=", "grid_width=", "grid_height=", "max_word_length=",
        "difficult_mode=", "custom_words="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        print(f"opt: {opt} | arg: {arg}")
        if opt in ("--help",):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-n", "--num_words"):
            num_words = int(arg)
        elif opt in ("-w", "--grid_width"):
            grid_height = int(arg)
        elif opt in ("-h", "--grid_height"):
            grid_width = int(arg)
        max_word_length = min(grid_height, grid_width)
        if opt in ("-m", "--max_word_length"):
            max_word_length = int(arg)
        elif opt in ("-d", "--difficult_mode"):
            hard_mode = bool(arg)
        elif opt in ("-c", "--custom_words"):
            custom_words = arg


def start_game(num_words, grid_width, grid_height, max_word_length, hard_mode, custom_words):
    global words
    words = generate_words(num_words, max_word_length, custom_words)
    generate_board(grid_width, grid_height)
    global grid
    add_in_words(words)
    global chars
    chars = 'abcdefghijklmnopqrstuvwxyz'
    if hard_mode == True:
        chars = ''
        for row in grid:
            for char in row:
                if char != '0':
                    chars += char
    fill_in_board()
    display_grid(grid)

parse_sys_args(sys.argv)
print(num_words, grid_width, grid_height, max_word_length, hard_mode, custom_words)
start_game(num_words, grid_width, grid_height, max_word_length, hard_mode, custom_words)

disp_words = ''
disp_grid = ''

for i in range(1, len(words) + 1):
    disp_words += f"{i}: {words[i - 1]} | "

for row in grid:
    for char in row:
        disp_grid += char + ' '
    disp_grid = disp_grid[:-1]
    disp_grid += '\n'
disp_grid = disp_grid[:-1]

win= Tk()
win.attributes('-fullscreen', True)
win.configure(bg="black")
can = Canvas(win, width=1920, height=1080, bg='black')
can.pack()
word_label = Label(win, text=disp_words, bg='black', fg = "white", wraplength=1880, justify=CENTER)
word_label.configure(font=("Monaco", 13))
word_label.place(relx=.5, rely=.94, anchor="center")
grid_label = Label(win, text=disp_grid, bg='black', fg = "white")
grid_label.configure(font=("Monaco", 10))
grid_label.place(relx=.5, rely=.5, anchor="center")

win.mainloop()
