"""
this file edits a file where the changes made in the game are reported 
and logged for debugging puposes
"""

import color
import queue

FILE = ""
COLOR = "{user} selected: {color}"
USER = "{user} playing"
OUT = "{user} decided to exit"
DIM = "creating a {num}x{num} board"
NAME = ""
WIN = "{user} has won!"
def create_log(name: str = 'log.txt'):
    """
    initializes the log file

    """
    global FILE 
    FILE = name
    open(name, "w")



def log(msg: str):

    try:
        file = open(FILE, "a")
        file.write(msg + "\n")
        file.close()
        return True

    except(FileNotFoundError):
        return False

def log_color(c: color.Color):
    log(COLOR.format(user = NAME, color = c.name))

def log_dim(dim: int):
    log(DIM.format(num = dim))

def log_user(name: str):
    global NAME
    NAME = name
    log(USER.format(user = NAME))

def log_exit():
    log(OUT.format(user = NAME))

def log_win():
    log(WIN.format(user = NAME))

def log_queue(q: queue.Queue):
    s = "state of the queue: "
    s += str(q.qsize())
    s += "\n"

    for t in q.queue:
        s += "\t" + str(t) + "\n"
    
    log(s)