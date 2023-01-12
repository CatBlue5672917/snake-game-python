from tkinter import *
import random

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
GAME = True
BG = "white"

root = Tk()
root.title("Змейка")
can = Canvas(root, width=WIDTH, height=HEIGHT, background=BG)
can.pack(anchor=CENTER, expand=1)
can.focus_set()

game_over_text = can.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER",
                                 font='Arial 28', fill='red',
                                 state='hidden')

restart_text = can.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3, font="Arial 38", fill="white",
                               text="Click here to restart", state="hidden")


class Segment(object):
    def __init__(self, x, y):
        self.instance = can.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="#000000")


def create_block():
    global BLOCK
    posx = (SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    posy = (SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))
    BLOCK = can.create_oval(posx, posy, posx + SEG_SIZE, posy + SEG_SIZE, fill="#ff6f00")


def main():
    global GAME
    if GAME:
        s.move()
        head_coords = can.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            GAME = False
        elif head_coords == can.coords(BLOCK):
            s.add_segment()
            can.delete(BLOCK)
            create_block()
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == can.coords(s.segments[index].instance):
                    GAME = False
        root.after(100, main)
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


def clicked(event):
    global GAME
    GAME = True
    can.delete(BLOCK)
    can.itemconfigure(restart_text, )
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    can.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.mapping["Right"]

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            can.delete(segment.instance)

    def add_segment(self):
        last_seg = can.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = can.coords(self.segments[index + 1].instance)
            can.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = can.coords(self.segments[-2].instance)
        can.coords(self.segments[-1].instance,
                   x1 + self.vector[0] * SEG_SIZE,
                   y1 + self.vector[1] * SEG_SIZE,
                   x2 + self.vector[0] * SEG_SIZE,
                   y2 + self.vector[1] * SEG_SIZE)


def set_state(item, state):
    can.itemconfigure(item, state=state)


can.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()
