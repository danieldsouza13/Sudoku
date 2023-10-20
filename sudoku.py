import pygame
from constants import *
from sudoku_generator import *


class Cell:  # cell class

    def __init__(self, value, row, col, screen):  # constructor function
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):  # setter for the cell's value
        self.value = value

    def set_sketched_value(self, value):  # setter for the sketched cell's value
        self.value = value

    def draw(self):  # draws the cell, displays the value within the cell, and highlights the selected cell
        num_font = pygame.font.Font(None, 75)  # sets up the font  of the user's number
        num_surf = num_font.render(str(self.value), 0, (0, 0, 0))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect(self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 12)
            self.selected = False

        if self.value == 1 or self.value == 2 or self.value == 3 or self.value == 4 or self.value == 5 or self.value == 6 or self.value == 7 or self.value == 8 or self.value == 9:  # valid numbers for user to input
            num_x_rect = num_surf.get_rect(
                center=(SQUARE_SIZE * self.col + SQUARE_SIZE // 2,
                        SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
            screen.blit(num_surf, num_x_rect)


class Board:  # board class

    def __init__(self, width, height, screen, difficulty):
        # constructor function
        self.width = 9
        self.height = 9
        self.screen = screen
        self.difficulty = difficulty
        self.board = self.initialize_board()
        self.cells = [
            [Cell(self.board[i][j], i, j, SQUARE_SIZE) for j in range(self.width)]
            for i in range(self.height)
        ]

    def initialize_board(self):  # initializes 2-D Board
        # 1st approach
        # start of board
        return [["-" for i in range(9)] for j in range(9)]

    def select(self, row, col):
        # Marks the cell at (row,col) in the board as the current selected cell.
        # Once a cell has been selected, the user can edit its value or sketched value.
        for i in range(row):
            for j in range(col):
                self.cells[i][j].selected = False
        self.cells[row][col].selected = True

        if self.cells[row][col].selected:
            pygame.draw.rect(self.screen, RED, (col * 67, row * 67, 67, 67), 2)
            pygame.display.update()

    def click(self, x, y):
        # If a tuple of (x,y) coordinates is within the displayed board, this function returns a tuple of the (row,
        # col) of the cell which was clicked. Otherwise, this function returns None.

        if x >= 0 and x <= 600 and y >= 0 and y <= 600:
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            return row, col

        else:
            return None

    def clear(self):
        # Clears the value cell. Note that the user can only remove the cell values that are filled by themselves.
        pass

    def sketch(self, value):
        # Sets the sketched value of the current selected cell equal to user entered value.
        # Called when the user presses the Enter key.
        self.value = value

    def place_number(self, value):
        # Sets the value of the current selected cell equal to user entered value.
        # Called when the user presses the Enter key.
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or pygame.K_2 or pygame.K_3 or pygame.K_4 or pygame.K_5 or pygame.K_6 or pygame.K_7 or pygame.K_8 or pygame.K_9:
                    value == event.key

                    if event.key == pygame.K_RETURN:
                        return value

    def reset_to_original(self):
        # Resets all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        self.board = self.initialize_board()
        self.update_board()

    def is_full(self):
        # Returns a Boolean value indicating whether the board is full or not.
        for self.height in self.board:
            for self.value in self.height:
                if self.value == "-":
                    return False

    def update_board(self):
        # Updates the underlying 2D board with the values in all cells.
        self.cells = [
            [Cell(self.board[i][j], i, j, SQUARE_SIZE) for j in range(self.width)]
            for i in range(self.height)
        ]

    def find_empty(self):
        # Finds an empty cell and returns its row and col as a tuple (x,y).
        pass

    def check_board(self):
        # Check whether the Sudoku board is solved correctly.
        if self.is_full():
            row_count = 0

            for r in range(len(self.board)):
                for c in range(len(self.board)):
                    row_count += self.board[r][c]
                    if self.board[r][c] == self.board[r][-1]:
                        if row_count != 45:
                            return False
                        else:
                            row_count = 0
            col_count = 0

            for c in range(len(self.board)):
                for r in range(len(self.board)):
                    col_count += self.board[r][c]
                    if self.board[r][c] == self.board[-1][c]:
                        if col_count != 45:
                            return False
                        else:
                            col_count = 0
            box_indices = [
                (0, 0), (3, 0), (6, 0),
                (0, 3), (3, 3), (6, 3),
                (0, 6), (3, 6), (6, 6)
            ]
            box_count = 0

            for row_index, col_index in box_indices:
                for r in range(3):
                    for c in range(3):
                        box_count += self.board[r + row_index][c + col_index]

                        if r == 2 and c == 2:
                            if box_count != 45:
                                return False
                            else:
                                box_count = 0
            return True


pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def easy_mode():  # mode for easy
    screen.fill(BG_COLOR)
    draw_grid()
    board = generate_sudoku(9, 30)  # removes 30 cells

    for row, col in enumerate(board):

        for col in range(9):
            num = Cell(int(board[row][col]), row, col, screen)
            num.draw()

    pygame.display.update()
    return board


def medium_mode():  # mode for medium
    screen.fill(BG_COLOR)
    draw_grid()
    board = generate_sudoku(9, 40)  # remove 40 cells

    for row, col in enumerate(board):

        for col in range(9):
            num = Cell(int(board[row][col]), row, col, screen)
            num.draw()

    pygame.display.update()
    return board


def hard_mode():  # mode for hard
    screen.fill(BG_COLOR)
    draw_grid()
    board = generate_sudoku(9, 50)  # remove 50 cells

    for row, col in enumerate(board):

        for col in range(9):
            num = Cell(int(board[row][col]), row, col, screen)
            num.draw()

    pygame.display.update()
    return board


def game_start():
    # initialize title font
    start_title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 45)

    # color background
    screen.fill(BG_COLOR)

    # initialize and draw title
    title_surface = start_title_font.render("Welcome to Sudoku", 0, LINE_COLOR)
    title_rectangle = title_surface.get_rect(center=(WIDTH // 2,
                                                     HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rectangle)

    # initialize buttons
    # initialize text
    start_text = button_font.render("Start", 0, (255, 255, 255))
    quit_text = button_font.render("Quit", 0, (255, 255, 255))
    easy_text = button_font.render("Easy", 0, (255, 255, 255))
    medium_text = button_font.render("Medium", 0, (255, 255, 255))
    hard_text = button_font.render("Hard", 0, (255, 255, 255))

    # initialize button background color and text
    start_surface = pygame.Surface(
        (start_text.get_size()[0] + 20, start_text.get_size()[1] + 20))
    start_surface.fill(LINE_COLOR)
    start_surface.blit(start_text, (10, 10))
    quit_surface = pygame.Surface(
        (quit_text.get_size()[0] + 20, quit_text.get_size()[1] + 20))
    quit_surface.fill(LINE_COLOR)
    quit_surface.blit(quit_text, (10, 10))

    # initialize game mode background color and text
    easy_surface = pygame.Surface(
        (easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit(easy_text, (10, 10))
    medium_surface = pygame.Surface(
        (medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surface.fill(LINE_COLOR)
    medium_surface.blit(medium_text, (10, 10))
    hard_surface = pygame.Surface(
        (hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill(LINE_COLOR)
    hard_surface.blit(hard_text, (10, 10))

    # initialize button rectangle
    start_rectangle = start_surface.get_rect(center=(WIDTH // 2,
                                                     HEIGHT // 2 + 0))
    quit_rectangle = quit_surface.get_rect(center=(WIDTH // 2,
                                                   HEIGHT // 2 + 65))

    # initialize game mode buttons
    easy_rectangle = start_surface.get_rect(center=(WIDTH // 2,
                                                    HEIGHT // 2 + 165))
    medium_rectangle = start_surface.get_rect(center=(WIDTH // 2,
                                                      HEIGHT // 2 + 215))
    hard_rectangle = start_surface.get_rect(center=(WIDTH // 2,
                                                    HEIGHT // 2 + 265))

    # Draw buttons
    screen.blit(start_surface, start_rectangle)
    screen.blit(quit_surface, quit_rectangle)

    # mode buttons

    while True:
        # event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_rectangle.collidepoint(event.pos):
                    # checks if mouse is on start button
                    screen.blit(easy_surface, easy_rectangle)
                    screen.blit(medium_surface, medium_rectangle)
                    screen.blit(hard_surface, hard_rectangle)

                elif easy_rectangle.collidepoint(event.pos):
                    game_in_progress("easy")  # calls game_in_progress with mode passed in
                    x, y = event.pos[0], event.pos[1]
                    print(x, y)
                    click = Board.click(x, y)
                    Board.select(click)

                elif medium_rectangle.collidepoint(event.pos):
                    game_in_progress("medium")  # calls game_in_progress with mode passed in

                elif hard_rectangle.collidepoint(event.pos):
                    game_in_progress("hard")  # calls game_in_progress with mode passed in

                elif quit_rectangle.collidepoint(event.pos):
                    # exits program if mouse presses quit
                    pygame.quit()

        pygame.display.update()


def game_in_progress(mode):

    if mode == "easy":
        easy_mode()

    elif mode == "medium":
        medium_mode()

    elif mode == "hard":
        hard_mode()

    board = Board(WIDTH, HEIGHT, screen, mode)
    # draws grid once a mode is passed by user from game_start funtion
    # initializes the size of the button
    button_font = pygame.font.Font(None, 40)

    # initializes the text for the buttons
    reset_text = button_font.render("RESET", 0, (255, 255, 255))
    restart_text = button_font.render("RESTART", 0, (255, 255, 255))
    exit_text = button_font.render("EXIT", 0, (255, 255, 255))

    # initializes the background of the buttons
    reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
    reset_surface.fill(LINE_COLOR)
    reset_surface.blit(reset_text, (10, 10))

    restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surface.fill(LINE_COLOR)
    restart_surface.blit(restart_text, (10, 10))

    exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surface.fill(LINE_COLOR)
    exit_surface.blit(exit_text, (10, 10))

    # initializes the location of the buttons
    reset_rectangle = reset_surface.get_rect(
        center=(WIDTH // 2 - 200, HEIGHT // 8 + 550))
    restart_rectangle = reset_surface.get_rect(
        center=(WIDTH // 2 - 10, HEIGHT // 8 + 550))
    exit_rectangle = exit_surface.get_rect(
        center=(WIDTH // 2 + 200, HEIGHT // 8 + 550))

    # draws the buttons
    screen.blit(reset_surface, reset_rectangle)
    screen.blit(restart_surface, restart_rectangle)
    screen.blit(exit_surface, exit_rectangle)
    pygame.display.update()

    while True:
        var_board = Board(9, 9, screen, mode)

        # event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                click = var_board.click(x, y)

                if click:
                    if var_board.select(click[0], click[1]):
                        Cell.draw()

                if reset_rectangle.collidepoint(event.pos):
                    # resets the board to as it was initially
                    board.reset_to_original()

                elif restart_rectangle.collidepoint(event.pos):
                    # sends user back to main menu when restart
                    game_start()
                    game_in_progress()

                elif exit_rectangle.collidepoint(event.pos):
                    # exits game
                    pygame.quit()


def game_over():
    # if statement to check whether check_board function returned true or false
    if check_board() is True:
        # if true is returned game is won -> Game Won

        # initialize title font
        start_title_font = pygame.font.Font(None, 80)
        button_font = pygame.font.Font(None, 55)

        # color background
        screen.fill(BG_COLOR)

        # initialize and draw game over screen
        title_surface = start_title_font.render("Game Won!!", 0, LINE_COLOR)
        title_rectangle = title_surface.get_rect(center=(WIDTH // 2,
                                                         HEIGHT // 2 - 150))
        screen.blit(title_surface, title_rectangle)

        # initialize text for button
        exit_text = button_font.render("EXIT", 0, (255, 255, 255))

        # initialize background of restart button
        exit_surface = pygame.Surface(
            (exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surface.fill(LINE_COLOR)
        exit_surface.blit(exit_text, (10, 10))

        # initialize button
        exit_rectangle = exit_surface.get_rect(center=(WIDTH // 2,
                                                       HEIGHT // 2 + 0))

        # draw button
        screen.blit(exit_surface, exit_rectangle)
        pygame.display.update()

        while True:
            # event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rectangle.collidepoint(event.pos):
                        pygame.quit()  # quits if user clicks exit

    #######################################
    else:
        # if false is returned game is lost -> Game over

        # initialize title font
        start_title_font = pygame.font.Font(None, 80)
        button_font = pygame.font.Font(None, 55)

        # color background
        screen.fill(BG_COLOR)

        # initialize and draw game over screen
        title_surface = start_title_font.render("Game Over :(", 0, LINE_COLOR)
        title_rectangle = title_surface.get_rect(center=(WIDTH // 2,
                                                         HEIGHT // 2 - 150))
        screen.blit(title_surface, title_rectangle)

        # initialize text for button
        restart_text = button_font.render("RESTART", 0, (255, 255, 255))

        # initialize background of restart button
        restart_surface = pygame.Surface(
            (restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surface.fill(LINE_COLOR)
        restart_surface.blit(restart_text, (10, 10))

        # initialize button
        restart_rectangle = restart_surface.get_rect(center=(WIDTH // 2,
                                                             HEIGHT // 2 + 0))

        # draw button
        screen.blit(restart_surface, restart_rectangle)
        pygame.display.update()
        while True:
            # event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rectangle.collidepoint(event.pos):
                        game_start()  # sends user to main menu


def draw_grid():
    # horizontal lines
    screen.fill(BG_COLOR)

    for i in range(1, BOARD_ROWS + 1):

        # for every 3rd row
        if i == 3 or i == 6 or i == 9:
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE),
                             (WIDTH, i * SQUARE_SIZE), WIN_LINE_WIDTH)
        # for every other row
        else:
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE),
                             (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # vertical lines

    for j in range(1, BOARD_COLS):

        # for every 3rd column
        if j == 3 or j == 6 or j == 9:
            pygame.draw.line(screen, LINE_COLOR, (j * SQUARE_SIZE, 0),
                             (j * SQUARE_SIZE, HEIGHT), WIN_LINE_WIDTH)
        # for every other column
        else:
            pygame.draw.line(screen, LINE_COLOR, (j * SQUARE_SIZE, 0),
                             (j * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

    pygame.display.update()


def main():
    game_start()
    game = True
    while game:
        game_in_progress()


if __name__ == "__main__":
    main()
y