# -*- coding: utf-8 -*-

# Copyright © 2020 Ismael Belisario

# This file is part of Open Translation.

# Open Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Open Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Open Translation. If not, see <https://www.gnu.org/licenses/>.

"""
Script Name: canvasbox.py

"""

from tkinter import Tk, Canvas, Frame
from tkinter.ttk import Frame, Scrollbar
from ..utils import __forwardmethods


class BoxCanvas(Frame):
    """Modeled after the scrolled canvas class from Grayons's Tkinter book.

    Used as the default canvas, which pops up automatically when
    using turtle graphics functions or the Turtle class.
    """
    def __init__(self, master, width=500, height=350,
                 canvwidth=600, canvheight=500):
        super().__init__(master, width=width, height=height)
        
        self._rootwindow = self.winfo_toplevel()
        self.width, self.height = width, height
        self.canvwidth, self.canvheight = canvwidth, canvheight

        self.bg = "white"
        
        self.canvas = Canvas(master, width=width, height=height,
                                 bg=self.bg, relief='flat', borderwidth=2)
        
        self.hscroll = Scrollbar(master, command=self.canvas.xview,
                                    orient='horizontal')
        self.vscroll = Scrollbar(master, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=self.hscroll.set,
                               yscrollcommand=self.vscroll.set)
        
        self.rowconfigure(0, weight=1, minsize=0)
        self.columnconfigure(0, weight=1, minsize=0)
        
        self.canvas.grid(padx=1, in_ = self, pady=1, row=0,
                column=0, rowspan=1, columnspan=1, sticky='news')
        self.vscroll.grid(padx=1, in_ = self, pady=1, row=0,
                column=1, rowspan=1, columnspan=1, sticky='news')
        self.hscroll.grid(padx=1, in_ = self, pady=1, row=1,
                column=0, rowspan=1, columnspan=1, sticky='news')
        from tkinter import Frame as tkfr
        self.frame = tkfr(self.canvas, bg='blue', width=100, height=50)
        self.canvas.create_window(0, 0, window=self.frame, tag='frame')

        self.reset()
        self._rootwindow.bind('<Configure>', self.adjustScrolls())

    def reset(self, canvwidth=None, canvheight=None, bg=None):
        """Adjust canvas and scrollbars according to given canvas size."""
        if canvwidth:
            self.canvwidth = canvwidth
        if canvheight:
            self.canvheight = canvheight
        if bg:
            self.bg = bg
        self.canvas.config(bg=bg,
                        scrollregion=(-self.canvwidth//2, -self.canvheight//2,
                                       self.canvwidth//2, self.canvheight//2))
        self.canvas.xview_moveto(0.5*(self.canvwidth - self.width + 30) /
                                                               self.canvwidth)
        self.canvas.yview_moveto(0.5*(self.canvheight- self.height + 30) /
                                                              self.canvheight)
        self.adjustScrolls()


    def adjustScrolls(self):
        """ Adjust scrollbars according to window- and canvas-size.
        """
        cwidth = self.canvas.winfo_width()
        cheight = self.canvas.winfo_height()
        
        self.canvas.xview_moveto(0.5*(self.canvwidth-cwidth)/self.canvwidth)
        self.canvas.yview_moveto(0.5*(self.canvheight-cheight)/self.canvheight)
        
        if cwidth < self.canvwidth or cheight < self.canvheight:
            self.hscroll.grid(padx=1, in_ = self, pady=1, row=1,
                              column=0, rowspan=1, columnspan=1, sticky='news')
            self.vscroll.grid(padx=1, in_ = self, pady=1, row=0,
                              column=1, rowspan=1, columnspan=1, sticky='news')
        else:
            self.hscroll.grid_forget()
            self.vscroll.grid_forget()
        
        self.canvas.move('frame', 0.5*(self.canvwidth-cwidth)/self.canvwidth, 0.5*(self.canvheight-cheight)/self.canvheight)

       
        #self.frame['width'] = self.canvas.winfo_width()
        #self.frame['height'] = self.canvas.winfo_height()
        #self.canvas.tag_bind('frame', '<Enter>', lambda x: print("Hola"))
        
        


class OTBoxCanvas(BoxCanvas):

    def create_title(self, text, x=10, y=100):
        self.canvas.create_text(x, y, text=text)

    def create_window(self, title, description, logo=None, x=10, y=100):
        fr = Frame(self.canvas)
        pass

__forwardmethods(OTBoxCanvas, Canvas, '_canvas')     
        
    
   
"""
addtag, bbox, bind, canvasx, canvasy, cget, configure, coords, create, dchars,
delete, dtag, find, focus, gettags, icursor, imove, index, insert, itemcget,
itemconfigure, lower, move, moveto, postscript, raise, rchars, scale, scan,
select, type, xview, or yview
"""