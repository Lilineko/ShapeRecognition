from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw


class Paint(object):

    CLASS = 'triangle'
    DEFAULT_COLOR = 'white'
    BACKGROUND_COLOR = 'black'
    PATH = './images/01_init/' + CLASS + '/'
    RESOLUTION = 128
    IMAGE_INDEX = 101
    IMAGE = Image.new('L', (RESOLUTION, RESOLUTION), BACKGROUND_COLOR)

    def __init__(self):
        self.root = Tk()  

        self.color_button = Button(self.root, text='capture', command=self.capture_image)
        self.color_button.grid(row=0, column=0)

        self.eraser_button = Button(self.root, text='clear', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg=self.BACKGROUND_COLOR, width=self.RESOLUTION, height=self.RESOLUTION)
        self.c.grid(row=1, columnspan=4)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def capture_image(self):
        fileName = self.PATH + self.CLASS + str(self.IMAGE_INDEX).rjust(4, '0')
        # save postscipt image 
        # self.c.postscript(file = fileName + '.eps') 
        # use PIL to convert to PNG 
        self.IMAGE.save(fileName + '.png', 'png')
        self.c.delete('all')
        self.IMAGE_INDEX += 1
        self.IMAGE = Image.new('L', (self.RESOLUTION, self.RESOLUTION), self.BACKGROUND_COLOR)

    def use_eraser(self):
        self.c.delete('all')
        self.IMAGE = Image.new('L', (self.RESOLUTION, self.RESOLUTION), self.BACKGROUND_COLOR)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def reset(self, event):
        self.old_x, self.old_y = None, None    

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = self.BACKGROUND_COLOR if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            draw = ImageDraw.Draw(self.IMAGE)
            draw.line(((self.old_x, self.old_y), (event.x,event.y)), paint_color, width=self.line_width)
        self.old_x = event.x
        self.old_y = event.y


if __name__ == '__main__':
    Paint()