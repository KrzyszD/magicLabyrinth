# Taken from
# https://stackoverflow.com/a/71011331

import tkinter as tk
from config import gridCellSize

class CanvasButton:
    """ Create leftmost mouse button clickable canvas image object.

    The x, y coordinates are relative to the top-left corner of the canvas.
    """
    flash_delay = 100  # Milliseconds.

    def __init__(self, canvas, x, y, color, image, state=tk.NORMAL):
        self.canvas = canvas
        # self.btn_image = tk.PhotoImage(file=image_path)
        self.color = color
        offset = gridCellSize // 2
        x1 = gridCellSize * x
        y1 = gridCellSize * y
        x2 = gridCellSize + x1
        y2 = gridCellSize +y1  
        self.rect = canvas.create_rectangle((x1, y1, x2, y2), fill=self.color)   
        self.coin = canvas.create_image((x1 + offset, y1 + offset), image=image) 
        self.canvas.itemconfigure(self.coin, state=tk.HIDDEN)            

    def setCmd(self, cmd):                               
        self.canvas.tag_bind(self.rect, "<ButtonRelease-1>",
                        lambda event: (self.flash(), cmd()))
        self.canvas.tag_bind(self.coin, "<ButtonRelease-1>",
                        lambda event: (self.flash(), cmd()))

    def flash(self):
        self.set_state(tk.HIDDEN)
        self.canvas.after(self.flash_delay, self.set_state, tk.NORMAL)

    def changeColor(self, color):
        # self.canvas.itemconfig(self.canvas_btn_img_obj, background=color)
        self.canvas.itemconfig(self.rect, fill=color)
    
    def configure(self, coin=False):
        if coin:
            self.canvas.itemconfigure(self.coin, state=tk.NORMAL)  
            self.canvas.itemconfigure(self.rect, state=tk.HIDDEN)   
        else:
            self.canvas.itemconfigure(self.coin, state=tk.HIDDEN)  
            self.canvas.itemconfigure(self.rect, state=tk.NORMAL)         

        pass

    def set_state(self, state):
        """ Change canvas button image's state.

        Normally, image objects are created in state tk.NORMAL. Use value
        tk.DISABLED to make it unresponsive to the mouse, or use tk.HIDDEN to
        make it invisible.
        """
        self.canvas.itemconfigure(self.rect, state=state)
