import math
import tkinter as tk
from tkinter import colorchooser
from enum import Enum
import webbrowser
import threading
from multiprocessing import Process

class Window(Enum):
    MAIN = -1
    DRAWING = 0
    SETTINGS = 1
    AUTHOR = 2


class Trajectory:
    # This trajectory should do the same trick both for circles, squares and maybe images
    # x0, y0 - start point, x1, y1 - end point
    def __init__(self, x0, y0, x1, y1, id, diameter):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.id = id
        self.sign = 1
        self.diameter = diameter
        self.dir = self.get_normalized_dir()

    def has_arrived(self, x, y):
        return math.sqrt((self.x1 - (x + self.diameter // 2)) * (self.x1 - (x + self.diameter // 2)) +
                              (self.y1 - (y + self.diameter // 2)) * (self.y1 - (y + self.diameter // 2))) < 1

    def get_normalized_dir(self):
        L = math.sqrt((self.x1 - self.x0) * (self.x1 - self.x0) + (self.y1 - self.y0) * (self.y1 - self.y0))
        return ((self.x1 - self.x0) / L, (self.y1 - self.y0) / L)

    def swap_points(self):
        self.x0, self.y0, self.x1, self.y1 = self.x1, self.y1, self.x0, self.y0

    def __str__(self):
        return f'x0 {self.x0} y0 {self.y0} x1 {self.x1} y1 {self.y1} id {self.id} sign {self.sign}'

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        pad = 30
        self.FONT = ('*font', 10)
        self.OUTLINE = 'black'
        self.geometry('250x300')
        self.title('Main menu')
        self.resizable(False,False)
        self.start_btn = tk.Button(master=self, text='Start', width=10, font=self.FONT)
        self.start_btn.configure(command=self.action_33)
        self.start_btn.pack(pady=pad)
        self.stg_btn = tk.Button(master=self, text='Settings', width=10, font=self.FONT)
        self.stg_btn.configure(command=self.open_settings)
        self.stg_btn.pack()
        self.author_btn = tk.Button(master=self, text='Author', width=10, font=self.FONT)
        self.author_btn.configure(command=self.open_author)
        self.author_btn.pack(pady=pad)
        self.windows = [None, None, None] # list to store all the windows in order to close them with ESC button
        self.CANVAS_WIDTH = 850
        self.CANVAS_HEIGHT = 650
        self.MAX_WIDTH = self.CANVAS_WIDTH
        self.MAX_HEIGHT = self.CANVAS_HEIGHT
        self.drawing_on = False
        self.LINE_WIDTH = 1
        self.cur_window = -1
        self.own_drawing_points = []
        self.figure_type = tk.IntVar(0) # 0 - circle, 1 - square, 2 - custom
        self.figure_color = 'green'
        tmp = tk.Button(master=self, text='Quit', width=10, font=self.FONT)
        tmp.configure(command=self.quit)
        tmp.pack()
        

    def action_33(self):
        # action_33 was intented as an Easter egg to smth (at least I think so). However,
        # I forgot what it meant :(
        self.withdraw()
        self.cur_window = Window.DRAWING
        self.drawing = tk.Toplevel(master=self)
        self.drawing.focus_force()
        self.windows[0] = self.drawing
        self.drawing.bind('<Escape>', self.open_main)
        self.drawing.bind('<Motion>', self.on_mouse)
        self.drawing.protocol("WM_DELETE_WINDOW", self.quit)
        self.drawing.focus_force()
        self.drawing.geometry(str(self.CANVAS_WIDTH)+'x'+str( self.CANVAS_HEIGHT))
        self.drawing.resizable(False, False)
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.drawing, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        self.start_point = []
        self.is_drawing = False
        self.canvas.bind("<Button-1>", self.callback)
        self.drawing.title('Object trajetory')
        self.labels = [[],[]]
        self.bg_line = None
        self.figures = [] # will store only trajectory class
        self.my_grid = tk.PhotoImage(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.create_image((self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2), image=self.my_grid, state="normal")
        self.diameter = 40
        self.draw_system()
        self.move_figures()


    def own_drawing_callback(self, event):
        if self.was_drawn:
            self.own_drawing_clear()
            self.was_drawn = False
        self.own_drawing_points.append((event.x, event.y))
        self.tmp_circles.append(self.own_drawing_canvas.create_oval(event.x-3,event.y-3,event.x+3,event.y+3, fill = self.OUTLINE, outline=''))


    def own_drawing_key(self, event = None):
        if len(self.own_drawing_points) > 1 and not self.was_drawn:
            for i in range(len(self.own_drawing_points) - 1):
                self.draw_line(self.own_drawing_points[i][0], self.own_drawing_points[i][1],
                              self.own_drawing_points[i + 1][0], self.own_drawing_points[i + 1][1], self.OUTLINE, alternative_grid=True)
            self.draw_line(self.own_drawing_points[len(self.own_drawing_points) - 1][0],
                           self.own_drawing_points[len(self.own_drawing_points) - 1][1],
                           self.own_drawing_points[0][0], self.own_drawing_points[0][1], self.OUTLINE, alternative_grid=True) #connects first and last points
            for circle in self.tmp_circles:
                self.own_drawing_canvas.delete(circle)
            self.was_drawn = True

    def own_drawing_clear(self):
        for circle in self.tmp_circles:
            self.own_drawing_canvas.delete(circle)
        self.own_drawing_points.clear()
        self.my_grid_1 = tk.PhotoImage(width=200, height=200)
        self.own_drawing_canvas.create_image((100, 100), image=self.my_grid_1, state="normal")

    def figure_sel(self):
        if self.figure_type.get() == 2:
            self.own_drawing = tk.Toplevel(master = self.settings)
            self.own_drawing.resizable(False,False)
            self.own_drawing.geometry=('200x200')
            self.own_drawing_canvas = tk.Canvas(master = self.own_drawing,bg='white',width = 200, height=200)
            self.own_drawing_canvas.pack()
            self.own_drawing_canvas.bind("<Button-1>", self.own_drawing_callback)
            self.own_drawing.bind("<Return>", self.own_drawing_key)
            self.own_drawing.bind("<Escape>", self.own_drawing_clear)
            frame = tk.Frame(master=self.own_drawing)
            frame.pack()
            tk.Button(master=frame, text='Draw <ENTER>', command=self.own_drawing_key, padx=5).grid(row = 0, column=0)
            tk.Button(master=frame, text='Clear <ESC>', command=self.own_drawing_clear , padx=15).grid(row = 0, column=1)
            self.my_grid_1 = tk.PhotoImage(width=200, height=200)
            self.own_drawing_canvas.create_image((100, 100), image=self.my_grid_1, state="normal")
            self.tmp_circles = []
            self.was_drawn = False
            self.own_drawing_key(None)



    def open_settings(self):
        self.withdraw()
        self.cur_window = Window.SETTINGS
        self.settings = tk.Toplevel(master=self)
        self.settings.focus_force()
        self.windows[1] = self.settings
        self.settings.bind('<Escape>', self.open_main)
        self.settings.geometry('300x320')
        self.settings.resizable(False, False)
        self.settings.protocol("WM_DELETE_WINDOW", self.quit_stg)
        frame = tk.Frame(master=self.settings)
        frame.pack(pady=30)
        self.pck_line = tk.Button(master=frame, text="Pick line's colour", font=self.FONT, command= lambda : self.pick_color(0))
        self.pck_line.grid(row=0, column=0, padx=10)
        self.pck_fig = tk.Button(master=frame, text="Pick figure's colour", font=self.FONT, command= lambda : self.pick_color(1))
        self.pck_fig.grid(row=0, column=1, padx=10)
        frame = tk.Frame(master=self.settings)
        frame.pack()
        tk.Radiobutton(master=frame, text='Circle',variable=self.figure_type, value=0, command = self.figure_sel).grid(row = 0, column = 0,padx = 10)
        tk.Radiobutton(master=frame, text='Square',variable=self.figure_type, value=1, command = self.figure_sel).grid(row = 0, column = 1,padx = 10)
        tk.Radiobutton(master=frame, text='Custom',variable=self.figure_type, value=2, command = self.figure_sel).grid(row = 0, column = 2,padx = 10)
        tk.Label(master=self.settings, text="Resize window:", font=self.FONT).pack(pady=30)
        frame = tk.Frame(master=self.settings)
        frame.pack()
        tk.Label(master=frame, text="width  (250 - "+str(self.winfo_screenwidth())+")", padx=5,
                 font=self.FONT).grid(row=0,column=0)
        tk.Label(master=frame, text="height (250 - "+str(self.winfo_screenheight())+")", padx=5,
                 font=self.FONT).grid(row=1,column=0)
        self.entr_W = tk.Entry(master=frame, validate="key", validatecommand=(self.settings.register(self.validate),
                                                                "%P", 1, self.winfo_screenwidth(),1), font=self.FONT)
        self.entr_W.insert('0',self.CANVAS_WIDTH)
        self.entr_W.grid(row=0,column=1)
        self.entr_H = tk.Entry(master=frame, validate='key', validatecommand=(self.settings.register(self.validate),
                                                                "%P", 1, self.winfo_screenheight(),2), font=self.FONT)
        self.entr_H.insert('0',self.CANVAS_HEIGHT)
        self.entr_H.grid(row=1, column=1)
        # This button is actually useless. I think it just makes user feel comnfortable
        tk.Button(master=self.settings, text='Save',font = self.FONT).pack(pady=30)

    def open_author(self):
        self.withdraw()
        self.author = tk.Toplevel(master=self)
        self.author.focus_force()
        self.windows[2] = self.author
        self.cur_window = Window.AUTHOR
        self.author.bind('<Escape>', self.open_main)
        self.author.geometry('200x200')
        self.author.resizable(False, False)
        self.author.protocol("WM_DELETE_WINDOW", self.quit)
        link = tk.Label(self.author, text="https://github.com/", fg="blue", cursor="hand2")
        link.bind("<Button-1>", self.open_github)
        link.pack(pady=30)
        tk.Label(self.author, text="Link to this project's GitHub repository :)",wraplength=150, justify="center").pack(padx = 10)


    def open_github(self, event):
        webbrowser.open_new("https://github.com/")


    def pick_color(self, id) -> str:
        #  Returns none if window was closed using X
        if id == 0:
            self.pck_line["state"] = tk.DISABLED
            colors = colorchooser.askcolor(title="Choose a fancy color!")
            self.pck_line["state"] = tk.NORMAL
        else:
            self.pck_fig["state"] = tk.DISABLED
            colors = colorchooser.askcolor(title="Choose a fancy color!")
            self.pck_fig["state"] = tk.NORMAL
        if colors[1] != None:
            if id == 0:
                self.OUTLINE = colors[1]
            else:
                self.figure_color = colors[1]
        else:
            self.OUTLINE = 'black'

    def quit_stg(self):
        if self.drawing_on:
            self.drawing_on = False
            self.cur_window = Window.DRAWING
            self.resize_drawing()
            self.settings.destroy()
            print(self.LINE_WIDTH)
        else:
            self.quit()

    def validate(self, value, min_value, max_value, widget_num):
        # Checks if entered num is a num and less than given value
        try:
            value = int(value)
            if value >= int(min_value) and value <= int(max_value):
                if widget_num == '1':
                    self.CANVAS_WIDTH = value
                elif widget_num == '2':
                    self.CANVAS_HEIGHT = value
                return True
            self.settings.bell()
            return False
        except ValueError:
            if value == '':
                return True
            self.settings.bell()
            return False


    def open_main(self, event):
        if self.cur_window == Window.SETTINGS and self.drawing_on:
            self.windows[self.cur_window.value].destroy()
            self.cur_window = Window.DRAWING
            self.resize_drawing()
        elif self.cur_window == Window.DRAWING:
            self.drawing_on = True
            self.open_settings()
        else:
            self.windows[self.cur_window.value].destroy()
            self.deiconify()
            self.cur_window = -1


    def quit(self, event=None):
        if self.cur_window == -1:
            self.destroy()
        else:
            self.windows[self.cur_window.value].destroy()
            self.deiconify()
        pass

    def move_figures(self):
        if not self.is_drawing:
            for figure in self.figures:
                self.canvas.move(figure.id, figure.dir[0] * 0.5 * figure.sign, figure.dir[1] * 0.5 * figure.sign)
                if figure.has_arrived(self.canvas.coords(figure.id)[0], self.canvas.coords(figure.id)[1]):
                    figure.sign = -figure.sign
                    figure.swap_points()
        self.canvas.after(10, self.move_figures)

    def delete_bg_line(self):
        if self.bg_line is not None:
            self.canvas.delete(self.bg_line)

    def on_mouse(self, event):
        if self.is_drawing:
            self.delete_bg_line()
            self.bg_line = self.canvas.create_line(self.start_point[0],self.start_point[1], event.x, event.y,fill=self.OUTLINE)

    def callback(self, event):
        if not self.is_drawing:
            self.start_point = [event.x, event.y]
            self.is_drawing = True
        else:
            self.is_drawing = False
            self.end_point = [event.x, event.y]
            self.delete_bg_line()
            self.draw_line(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], color=self.OUTLINE)
            if self.figure_type.get() == 0:
                fig =  self.canvas.create_oval(self.start_point[0] - self.diameter // 2,
                                            self.start_point[1] - self.diameter // 2,
                                            self.start_point[0] + self.diameter // 2,
                                            self.start_point[1] + self.diameter // 2,
                                            fill=self.figure_color, outline='')
                self.figures.append(Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig, self.diameter))
            elif self.figure_type.get() == 1:
                fig = self.canvas.create_rectangle(self.start_point[0] - self.diameter // 2,
                                              self.start_point[1] - self.diameter // 2,
                                              self.start_point[0] + self.diameter // 2,
                                              self.start_point[1] + self.diameter // 2,
                                              fill=self.figure_color, outline='')
                self.figures.append(Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig, self.diameter))
            elif self.figure_type.get() == 2:
                # max_x and max_y are used to move figure closer to starting points if it was drawn to small
                max_x = max([elem[0] for elem in self.own_drawing_points])
                max_y = max([elem[1] for elem in self.own_drawing_points])
                real_points = [(elem[0] - max_x // 2 + self.start_point[0], elem[1] - max_y // 2 + self.start_point[1]) for elem in self.own_drawing_points]
                fig = self.canvas.create_polygon(real_points, outline=self.OUTLINE,fill=self.figure_color)
                self.figures.append(Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig, max(max_x,max_y)))



    def delete_widgets(self, system_only = False):
        if system_only:
            for line in self.lines:
                self.canvas.delete(line)
        else:
            self.canvas.delete('all')

    def resize_drawing(self):
        if self.CANVAS_WIDTH != self.drawing.winfo_width() or self.CANVAS_HEIGHT != self.drawing.winfo_height():
            if self.CANVAS_WIDTH < 250:
                self.CANVAS_WIDTH = 250
            if self.CANVAS_HEIGHT < 250:
                self.CANVAS_HEIGHT = 250
            self.delete_widgets(system_only=True)
            self.draw_system()
            for px in self.pixels:
                self.draw_line(px[0],px[1],px[2],px[3],self.OUTLINE)
            self.drawing.geometry(str(self.CANVAS_WIDTH)+'x'+str(self.CANVAS_HEIGHT))

    def add_coord_label(self, x, y, text):
        label = tk.Label(self.canvas, text=text, bg='white',anchor='w')
        label.place(x=x,y=y)
        if y == 0:
            self.labels[0].append(label)
        else:
            self.labels[1].append(label)

    def draw_system(self):
        self.add_coord_label(0,0,'0')
        for i in range(1,self.CANVAS_WIDTH // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=i * 100 - 10,y=0,text=i * 100)
            self.draw_line(i * 100,0,i * 100,self.CANVAS_HEIGHT,color='gray')
        for i in range(1,self.CANVAS_HEIGHT // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=0,y=i * 100 - 10,text=i * 100)
            self.draw_line(0,i * 100,self.CANVAS_WIDTH,i * 100,color='gray')


    def draw_line(self, x1, y1, x2, y2,  color, alternative_grid = False):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        if x2 > x1:
            xs = 1
        else:
            xs = -1
        if y2 > y1:
            ys = 1
        else:
            ys = -1
        x = x1
        y = y1
        if dx > dy:
            p = 2 * dy - dx
            while x != x2:
                x = x + xs
                if p > 0:
                    p = p + 2 * dy - 2 * dx
                    y = y + ys
                else:
                    p = p + 2 * dy
                if not alternative_grid:
                    self.my_grid.put(color, (x, y))
                else:
                    self.my_grid_1.put(color, (x, y))
        else:
            p = 2 * dx - dy
            while y != y2:
                y = y + ys
                if p > 0:
                    p = p + 2 * dx - 2 * dy
                    x = x + xs
                else:
                    p = p + 2 * dx
                if not alternative_grid:
                    self.my_grid.put(color, (x, y))
                else:
                    self.my_grid_1.put(color, (x, y))


if __name__ == '__main__':
    app = App()
    app.mainloop()
