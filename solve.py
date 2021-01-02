import pygame
import sys

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Grid:

    def __init__(self, screen, rows, cols, width, height):
        self.cur_row = None
        self.cur_col = None
        self.rows = rows
        self.columns = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.val = 'x'
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.winner = None

        self.screen.fill(WHITE)

        # Loading the images
        x_img = pygame.image.load('x.png')
        y_img = pygame.image.load('o.png')

        # Transforming the images
        self.x_img = pygame.transform.scale(x_img, (self.width // 3, self.height // 3))
        self.y_img = pygame.transform.scale(y_img, (self.width // 3, self.height // 3))

        # Drawing the grid
        pygame.draw.line(self.screen, BLACK, (self.width // 3, 0), (self.width // 3, self.height), 4)
        pygame.draw.line(self.screen, BLACK, (self.width // 3 * 2, 0), (self.width // 3 * 2, self.height), 4)
        pygame.draw.line(self.screen, BLACK, (0, self.height // 3), (self.width, self.height // 3), 4)
        pygame.draw.line(self.screen, BLACK, (0, self.height // 3 * 2), (self.width, self.height // 3 * 2), 4)

    def user_click(self):
        # Getting the current mouse position
        x, y = pygame.mouse.get_pos()

        # Finding the column clicked
        for i in range(self.columns):
            if x < self.width // 3 * (i + 1):
                self.cur_col = i
                break

        # Finding the row clicked
        for j in range(self.rows):
            if y < self.height // 3 * (j + 1):
                self.cur_row = j
                break

        # Pasting the 'X' or 'O' image on the screen
        if self.board[self.cur_row][self.cur_col] is None:
            self.board[self.cur_row][self.cur_col] = self.val
            self.draw_xo()
            print(self.board)

    def draw_xo(self):
        x_pos = self.width // 3 * self.cur_col
        y_pos = self.height // 3 * self.cur_row

        # Pasting the images over the screen
        if self.val == 'x':
            self.screen.blit(self.x_img, (x_pos, y_pos))
            self.val = 'o'
        else:
            self.screen.blit(self.y_img, (x_pos, y_pos))
            self.val = 'x'

    def check_win(self):

        # Checking the rows
        for i in range(self.rows):
            if self.board[i][0] == self.board[i][2] == self.board[i][1] and self.board[i][0]:
                pygame.draw.line(self.screen, RED, (0, self.height // 3 * i + self.height // 6),
                                 (self.width, self.height // 3 * i + self.height // 6), 6)
                self.winner = self.board[i][0]
                break

        # Checking the columns
        for j in range(self.columns):
            if self.board[0][j] == self.board[2][j] == self.board[1][j] and self.board[0][j]:
                pygame.draw.line(self.screen, RED, (self.width // 3 * j + self.width // 6, 0),
                                 (self.width // 3 * j + self.width // 6, self.height), 6)
                self.winner = self.board[0][j]
                break

        # Checking the diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0]:
            pygame.draw.line(self.screen, RED, (0, 0), (self.width, self.height), 6)
            self.winner = self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2]:
            pygame.draw.line(self.screen, RED, (self.width, 0), (0, self.height), 6)
            self.winner = self.board[0][2]

        if not any(None in l for l in self.board):
            self.winner = 'draw'

        return self.winner

    def print_result(self):
        # Delay of 2 secs
        pygame.display.flip()
        pygame.time.delay(1000)

        # Initialising the font
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Setting the message that is to be displayed
        if self.winner == 'draw':
            msg = "It is a DRAW."
        else:
            msg = self.winner.upper() + " is the winner."

        # Displaying the message on screen
        text = font.render(msg, True, WHITE)
        self.screen.fill(BLACK)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)


def main():
    # Initialising pygame
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tic Tac Toe')
    board = Grid(win, 3, 3, 500, 500)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.user_click()
                winner = board.check_win()
                if winner:
                    board.print_result()
                    board = Grid(win, 3, 3, 500, 500)

        pygame.display.update()
    pygame.quit()
    sys.exit()


main()
