import sys
from color import Color
from player import Player
from board import Board
from tile import Tile
from position import Position
import curses
import time
import re
from sty import fg, bg, ef, rs, Style, RgbBg
import keyboard

COLR_MODE = "COLR"
INIT_MODE = "INIT"
NAME_MODE = "NAME"
WINDOW = "WINDOW"
MODE = "MODE"
DIM_MODE = "DIM"
options = ["exit", "terminal", "window"]

class Game:
    """
    class that manages the game and the logic
    as it is played.

    also prompts the user for the game mode

    attributes
    ----------
    player: Player
        object of the player using game
    size: int
        size of the game board
    """
    def __init__(self, size: int, player: Player):
        self.board = Board(size)
        self._player = player

    def won(self) -> bool:
        """
        determines if games has finished and player won
        """
        color = self.board[0][0]

        for tile in self.board.__iter__():
            if tile.color != color:
                return False
        
        return True

class Terminal(Game):
    def __init__(self):
        self._mode = ""
        
    def finish_init(self, name: str, dim: int):
        super().__init__(dim, name)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode: str):
        self._mode = mode

    def clear(self):
        """
        clears the entire terminal and
        and goes back to the top
        """
        print("\033[2J")

    def del_n_lines(self, n: int = 0):
        """
        deletes n number of lines from the terminal
        :param: n, number of lines
        """
        string = ""
        # go up and back and delete n times
        for i in range(n):
            string = string + "\033[1A" + "\r" + "\033[K"
        print(string)
        # go back one more time to undo the '\n's
        print("\033[2A")

    def color_op(self, option = 0):
        colores = ""
        counter = 0
        for tone in Color:
            color = tone.value
            if counter == option:
                colores += (bg(color[0], color[1], color[2]) + " \u2573 " + bg.rs + "\t")
                counter += 1
            else:
                colores += (bg(color[0], color[1], color[2]) + "    " + bg.rs + "\t")
                counter += 1
        
        return colores

    def get_name(self):
        name_mssg = "enter your user name: "
        name = input(name_mssg)
        return name
    
    def get_dim(self):
        """
        interacts with user to get dimensions
        sets the dimensions for board
        """

        dim_mssg = "enter board dimensions (max 15): "
        while True:
            answer = input(dim_mssg)
            dim = -1
            try:
                dim = int(answer)

                if dim > 15:
                    raise ValueError

                return dim
            except ValueError:
                if dim > 15:
                    error = str(dim) + " is too big. Try a smaller number. . . . . "
                else:
                    error = str(answer) + " is not valid. Try again. . . . . "

                print(error)

                for i in range(5):
                    # sleep
                    time.sleep(1)
                    # remove a dot form error message
                    error = error[:-2]
                    # go up and to the start and reprint new error message
                    self.del_n_lines(1)
                    print(error)
                time.sleep(1)
                # at the end rewrite main prompt

                self.del_n_lines(2)
                continue

    def esc_mssg(self):
        print("press 'esc' to exit game any time.")

    def print_modes(self, selector):
        """
        prints the different game modes with an arrow on the current
        @param selector: indicated which option user is looking at
        """
        modes = ""
        sep = "\n"
        
        for i in range(len(options)):
            if i == len(options) - 1:
                sep = ""
            if i == selector:
                modes += "\u27A4  "
            
            else:
                modes += "   "
            modes += (options[i] + sep)
        print(modes)

    def mode_selector(self):
        """
        allows the user to select the game mode
        """
        selection = 0
        prev = 0
        tipo = "down"
        show = True
        self.print_modes(selection)
        while True:
            # read user event
            event = keyboard.read_event(suppress = True)
            key = event.name
            tipo = event.event_type
            # print(key, tipo)
            if tipo == "down" and key == "down":
                if selection >= 2:
                    # print(selection)
                    show = False
                else:
                    selection += 1
                    show = True

            elif tipo == "down" and key == "up":
                if selection <= 0:
                    # print(selection)
                    show = False
                else:
                    selection -= 1
                    show = True

            elif tipo == "down" and key == "enter":
                if selection == 0:
                    # exit the game
                    exit()
                elif selection == 1:
                    # enable name mode
                    self.mode = NAME_MODE
                elif selection == 2:
                    self.mode = WINDOW
                show = False
                return
            elif tipo == "down" and key == "esc":
                exit()
            
            if show:
                self.del_n_lines(len(options))
                self.print_modes(selection)

    def on_press(self, key):
        
        if self.mode == MODE:
            prev = self.selection
            if k == "down":
                self.selection = 1

            elif k == "up":
                self.selection = -1

            elif k == "enter":
                if self.selection == 0:
                    exit()
                elif self.selection == 1:
                    # this is the selection for te terminal mode
                    self.mode = NAME_MODE
                    print("terminal mode selected")
            
            # if there is a change, update the view to point to new option
            if prev != self.selection:
                    self.del_n_lines(len(options) + 1)
                    prompt_mode(self.selection)
        
        elif self.mode == NAME_MODE:
            pass
            # if key == "backspace":
            #     if self._temp_name != "":
            #         self._temp_name = self._temp_name[:-1]
            #         print("\033[K" + "\033[A")
            #     print(self._temp_name + "\033[A")
            # if key == "enter":
            #     # finalize the user name
            #     self.mode = DIM_MODE
            #     self.get_dim()
            # else:
            #     letter = k.split("\'")[1]
            #     if letter.isalnum():
            #         self._temp_name += letter
            #         print(self._temp_name + "\033[A")

        elif self.mode == DIM_MODE:
            pass
            # if key == keyboard.Key.backspace:
            #     if self._temp_name != "":
            #         self._temp_name = self._temp_name[:-1]
            #         print("\033[K" + "\033[A")
            #     print(self._temp_name + "\033[A")
            # if key == keyboard.Key.enter:
            #     number = k.split("\'")[1]
            #     if number.isnumeric():
            #         number = int(number)
            #         if number > 15:
            #             self.del_n_lines(2)
            #             print("That's too big! Try again.")
            #             # mode remains the same
            # else:
            #     number = k.split("\'")[1]
            #     if number.isnumeric():
            #         number = int(number)
            #         if number > 15:
            #             self.del_n_lines(2)
            #             print("That's too big! Try again.")
            #             # mode remains the same
            #         else:
            #             self._temp_dim = int(str(self._temp_dim) + str(number))
            #             print(str(self._temp_dim) + "\033[A")
                
    
def terminal_mode(terminal):
    """
    starts a game with the terminal settings
    @param terminal: the terminal game object
    """
    game = terminal
    
    # cleanup mode selection
    game.del_n_lines(len(options))

    # get the name of the user and cleanup (1 line max)
    name = game.get_name()
    game.del_n_lines(1)

    # get the dimensions and cleanup
    dim = game.get_dim()
    game.del_n_lines(1)

    # set size and name properties
    game.finish_init(name, dim)


def window_mode():
    """
    sets up the window version of the game

    attributes
    ----------
    # TODO
    """
    return

def main():
    terminal = Terminal()
    terminal.mode_selector()

    if terminal.mode == NAME_MODE:
        terminal_mode(terminal)

if __name__ == "__main__":
    main()