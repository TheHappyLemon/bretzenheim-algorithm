from math import sqrt
import tkinter as tk
from webbrowser import  open_new
from tkinter import colorchooser
# For some reason tk.colorchooser raises error, so I have to import it separately.

class Trajectory:
    # Class for moving center of each figure
    def __init__(self, x0, y0, x1, y1, id):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.center_x = x0
        self.center_y = y0
        self.id = id
        self.sign = 1
        self.dir = self.get_normalized_dir()

    def move(self, deltx, delty):
        self.center_x += deltx
        self.center_y += delty

    def has_arrived(self, x, y):
        # Checks if vector's magnitude between center and destination is too small
        return sqrt((self.x1 - self.center_x) * (self.x1 - self.center_x) +
                         (self.y1 - self.center_y) * (self.y1 - self.center_y)) < 1

    def get_normalized_dir(self):
        # Returns direction from start point to end point
        # If these points are the same -> do not move
        L = sqrt((self.x1 - self.x0) * (self.x1 - self.x0) + (self.y1 - self.y0) * (self.y1 - self.y0))
        if L != 0:
            return ((self.x1 - self.x0) / L, (self.y1 - self.y0) / L)
        else:
            return (0, 0)

    def swap_points(self):
        self.x0, self.y0, self.x1, self.y1 = self.x1, self.y1, self.x0, self.y0


class App(tk.Tk):
    def __init__(self):
        # Initializes Main menu
        tk.Tk.__init__(self)
        pad = 30
        self.FONT = ('*font', 10)
        self.OUTLINE = 'black'
        self.geometry('250x300')
        self.title('Main menu')
        self.resizable(False, False)
        self.start_btn = tk.Button(master=self, text='Start', width=10, font=self.FONT,
                                   command=self.action_33).pack(pady=pad)
        self.stg_btn = tk.Button(master=self, text='Settings', width=10, font=self.FONT,
                                 command=self.open_settings).pack()
        self.author_btn = tk.Button(master=self, text='Author', width=10, font=self.FONT,
                                    command=self.open_author).pack(pady=pad)
        self.CANVAS_WIDTH = 850
        self.CANVAS_HEIGHT = 650
        self.MAX_WIDTH = self.CANVAS_WIDTH
        self.MAX_HEIGHT = self.CANVAS_HEIGHT
        self.drawing = None
        self.settings = None
        self.drawing_on = False
        self.diameter = 40
        self.labels = []
        self.figure_type = tk.IntVar(0)  # 0 - circle, 1 - square, 2 - custom
        self.figure_color = 'green'
        self.own_drawing_points = []
        self.question_mark = [(26, 38), (38, 19), (61, 17), (75, 30), (62, 48), (58, 70), (46, 70), (43, 48), (58, 34),
                              (47, 27), (36, 41)]
        tk.Button(master=self, text='Quit', width=10, font=self.FONT, command=self.quit).pack()

    def action_33(self):
        # Creates main window with coordinate system and ability to draw lines.
        self.withdraw()
        self.drawing = tk.Toplevel(master=self)
        self.drawing.focus_force()
        self.drawing.bind('<Motion>', self.on_mouse)
        self.drawing.bind('<Escape>', self.open_settings)
        self.drawing.protocol("WM_DELETE_WINDOW", lambda: self.my_quit(self.drawing))
        self.drawing.geometry(str(self.CANVAS_WIDTH) + 'x' + str(self.CANVAS_HEIGHT))
        self.drawing.resizable(False, False)
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.drawing, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        self.start_point = []
        self.canvas.bind("<Button-1>", self.callback)
        self.drawing.title("bresenham's algorithm")
        self.bg_line = None
        self.is_drawing = False
        self.figures = []  # will store only trajectory class
        self.my_grid = tk.PhotoImage(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.create_image((self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2), image=self.my_grid, state="normal")
        self.draw_system()
        self.move_figures()

    def figure_sel(self):
        # Creates window to draw custom figure which will be displayd after line is drawn.
        if self.figure_type.get() == 2:
            self.own_drawing = tk.Toplevel(master=self.settings)
            self.own_drawing.resizable(False, False)
            self.own_drawing.geometry = ('200x200')
            self.own_drawing_canvas = tk.Canvas(master=self.own_drawing, bg='white', width=200, height=200)
            self.own_drawing_canvas.pack()
            self.own_drawing_canvas.bind("<Button-1>", self.own_drawing_callback)
            self.own_drawing.bind("<Return>", self.own_drawing_key)
            self.own_drawing.bind("<Escape>", self.own_drawing_clear)
            frame = tk.Frame(master=self.own_drawing)
            frame.pack()
            tk.Button(master=frame, text='Draw <ENTER>', command=self.own_drawing_key, padx=5).grid(row=0, column=0)
            tk.Button(master=frame, text='Clear <ESC>', command=self.own_drawing_clear, padx=15).grid(row=0, column=1)
            self.my_grid_1 = tk.PhotoImage(width=200, height=200)
            self.own_drawing_canvas.create_image((100, 100), image=self.my_grid_1, state="normal")
            if self.own_drawing_points == self.question_mark:
                self.own_drawing_points.clear()
            self.tmp_circles = []
            self.was_drawn = False
            self.own_drawing_key(None)

    def own_drawing_callback(self, event):
        # Store a point for further figure. There can only be one active connection betwen points
        if self.was_drawn:
            self.own_drawing_clear()
            self.was_drawn = False
        self.own_drawing_points.append((event.x, event.y))
        self.tmp_circles.append(
            self.own_drawing_canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill=self.OUTLINE,
                                                outline=''))

    def own_drawing_key(self, event=None):
        # Connects all points with straight lines drawn by bresenham's algorithm
        if len(self.own_drawing_points) > 1 and not self.was_drawn:
            for i in range(len(self.own_drawing_points) - 1):
                self.draw_line(self.own_drawing_points[i][0], self.own_drawing_points[i][1],
                               self.own_drawing_points[i + 1][0], self.own_drawing_points[i + 1][1], self.OUTLINE,
                               alternative_grid=True)
            self.draw_line(self.own_drawing_points[len(self.own_drawing_points) - 1][0],
                           self.own_drawing_points[len(self.own_drawing_points) - 1][1],
                           self.own_drawing_points[0][0], self.own_drawing_points[0][1], self.OUTLINE,
                           alternative_grid=True)  # connects first and last points
            for circle in self.tmp_circles:
                self.own_drawing_canvas.delete(circle)
            self.was_drawn = True

    def own_drawing_clear(self):
        # Clears whole custom drawing
        for circle in self.tmp_circles:
            self.own_drawing_canvas.delete(circle)
        self.own_drawing_points.clear()
        self.my_grid_1 = tk.PhotoImage(width=200, height=200)
        self.own_drawing_canvas.create_image((100, 100), image=self.my_grid_1, state="normal")



    def set_diameter(self, value):
        self.diameter = int(value)

    def open_settings(self, event=None):
        # Creates settings if it was not created, else focuses on existing ones.
        if self.settings is None:
            self.withdraw()
            self.settings = tk.Toplevel(master=self)
            self.settings.focus_force()
            self.settings.geometry('300x320')
            self.settings.resizable(False, False)
            self.settings.protocol("WM_DELETE_WINDOW", lambda: self.my_quit(self.settings))
            frame = tk.Frame(master=self.settings)
            frame.pack(pady=30)
            self.pck_line = tk.Button(master=frame, text="Pick line's colour", font=self.FONT,
                                      command=lambda: self.pick_color(0))
            self.pck_line.grid(row=0, column=0, padx=10)
            self.pck_fig = tk.Button(master=frame, text="Pick figure's colour", font=self.FONT,
                                     command=lambda: self.pick_color(1))
            self.pck_fig.grid(row=0, column=1, padx=10)
            frame = tk.Frame(master=self.settings)
            frame.pack()
            tk.Radiobutton(master=frame, text='Circle', variable=self.figure_type, value=0,
                           command=self.figure_sel).grid(
                row=0, column=0, padx=10)
            tk.Radiobutton(master=frame, text='Square', variable=self.figure_type, value=1,
                           command=self.figure_sel).grid(
                row=0, column=1, padx=10)
            tk.Radiobutton(master=frame, text='Custom', variable=self.figure_type, value=2,
                           command=self.figure_sel).grid(
                row=0, column=2, padx=10)
            self.scale = tk.Scale(frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                  command=lambda x: self.set_diameter(x),length=150)
            self.scale.set(self.diameter)
            self.scale.grid(row=1, column=1, columnspan=3)
            tk.Label(master=frame, text="Diameter:", font=self.FONT).grid(row=1, column=0)
            tk.Label(master=self.settings, text="Resize window:", font=self.FONT).pack(pady=15)
            frame = tk.Frame(master=self.settings)
            frame.pack()
            tk.Label(master=frame, text="width  (250 - " + str(self.winfo_screenwidth()) + ")", padx=5,
                     font=self.FONT).grid(row=0, column=0)
            tk.Label(master=frame, text="height (250 - " + str(self.winfo_screenheight()) + ")", padx=5,
                     font=self.FONT).grid(row=1, column=0)
            self.entr_W = tk.Entry(master=frame, validate="key",
                                   validatecommand=(self.settings.register(self.validate),
                                   "%P", 1, self.winfo_screenwidth(), 1),font=self.FONT)
            self.entr_W.insert('0', self.CANVAS_WIDTH)
            self.entr_W.grid(row=0, column=1)
            self.entr_H = tk.Entry(master=frame, validate='key',
                                   validatecommand=(self.settings.register(self.validate),
                                   "%P", 1, self.winfo_screenheight(), 2), font=self.FONT)
            self.entr_H.insert('0', self.CANVAS_HEIGHT)
            self.entr_H.grid(row=1, column=1)
            # This button does nothing. I think it just makes user feel comnfortable
            tk.Button(master=self.settings, text='Save', font=self.FONT).pack(pady=15)
        else:
            self.settings.focus_force()

    def open_author(self):
        self.withdraw()
        self.author = tk.Toplevel(master=self)
        self.author.focus_force()
        self.author.geometry('200x200')
        self.author.resizable(False, False)
        self.author.protocol("WM_DELETE_WINDOW", lambda: self.my_quit(self.author))
        link = tk.Label(self.author, text="https://github.com/TheHappyLemon/bretzenheim-algorithm/", fg="blue",
                        cursor="hand2", wraplength=150)
        link.bind("<Button-1>", lambda x: open_new("https://github.com/TheHappyLemon/bretzenheim-algorithm"))
        link.pack(pady=30)
        tk.Label(self.author, text="Link to this project's GitHub repository :)", wraplength=150,
                 justify="center").pack(padx=10)

    def pick_color(self, id) -> str:
        #  Returns choosen color from colorpicker menu
        if id == 0:
            self.pck_line["state"] = tk.DISABLED
            colors = tk.colorchooser.askcolor(title="Choose a fancy color!")
            self.pck_line["state"] = tk.NORMAL
        else:
            self.pck_fig["state"] = tk.DISABLED
            colors = tk.colorchooser.askcolor(title="Choose a fancy color!")
            self.pck_fig["state"] = tk.NORMAL
        if colors[1] != None:
            if id == 0:
                self.OUTLINE = colors[1]
            else:
                self.figure_color = colors[1]

    def my_quit(self, window):
        # Closes given window
        if window == self.settings and self.drawing is not None and self.drawing.winfo_exists():
            # If settings were closed while drawing was on -> apply changes (if they present)
            self.apply_changes()
            self.settings = None
        else:
            # This is needed for future checks
            if window == self.drawing:
                self.drawing = None
                self.labels.clear()
            elif window == self.settings:
                self.settings = None
            self.deiconify()
        window.destroy()

    def validate(self, value, min_value, max_value, widget_num):
        # Checks if entered num is a num and less than given value
        # Used only for screen's width and height entries. However, it is still possible to enter little values
        # Additional checks are located in apply_settings()
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

    def move_figures(self):
        # Moves each drawn figure by its trajectory once 10ms
        if not self.is_drawing and not (self.settings is not None):
            for figure in self.figures:
                self.canvas.move(figure.id, figure.dir[0] * 0.5 * figure.sign, figure.dir[1] * 0.5 * figure.sign)
                figure.move(figure.dir[0] * 0.5 * figure.sign, figure.dir[1] * 0.5 * figure.sign)
                if figure.has_arrived(self.canvas.coords(figure.id)[0], self.canvas.coords(figure.id)[1]):
                    figure.sign = -figure.sign
                    figure.swap_points()
        self.canvas.after(10, self.move_figures)

    def delete_bg_line(self):
        if self.bg_line is not None:
            self.canvas.delete(self.bg_line)

    def on_mouse(self, event):
        # draw line (built-in) from start point to pointer position
        if self.is_drawing and not self.settings is not None:
            self.delete_bg_line()
            self.bg_line = self.canvas.create_line(self.start_point[0], self.start_point[1], event.x, event.y,
                                                   fill=self.OUTLINE)
        else:
            self.is_drawing = False
            self.start_point.clear()
            self.delete_bg_line()

    def callback(self, event):
        # Draw final line with bresenham's algorithm and create choosen figure with center in start point
        if not self.settings is not None:
            if not self.is_drawing:
                self.start_point = [event.x, event.y]
                self.is_drawing = True
            else:
                self.is_drawing = False
                self.end_point = [event.x, event.y]
                self.delete_bg_line()
                self.draw_line(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1],
                               color=self.OUTLINE)
                if self.figure_type.get() == 0:
                    fig = self.canvas.create_oval(self.start_point[0] - self.diameter // 2,
                                                  self.start_point[1] - self.diameter // 2,
                                                  self.start_point[0] + self.diameter // 2,
                                                  self.start_point[1] + self.diameter // 2,
                                                  fill=self.figure_color, outline='')
                    self.figures.append(
                        Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig))
                elif self.figure_type.get() == 1:
                    fig = self.canvas.create_rectangle(self.start_point[0] - self.diameter // 2,
                                                       self.start_point[1] - self.diameter // 2,
                                                       self.start_point[0] + self.diameter // 2,
                                                       self.start_point[1] + self.diameter // 2,
                                                       fill=self.figure_color, outline='')
                    self.figures.append(
                        Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig))
                elif self.figure_type.get() == 2:
                    # max_x and max_y are used to move figure closer to starting points if it was drawn to small
                    if len(self.own_drawing_points) < 2:
                        self.own_drawing_points = self.question_mark.copy()
                    min_x = min([elem[0] for elem in self.own_drawing_points])
                    min_y = min([elem[1] for elem in self.own_drawing_points])
                    max_x = max([elem[0] for elem in self.own_drawing_points])
                    max_y = max([elem[1] for elem in self.own_drawing_points])
                    real_points = [(elem[0] - (max_x + min_x) // 2 + self.start_point[0],
                                    elem[1] - (max_y + min_y) // 2 + self.start_point[1])
                                   for elem in self.own_drawing_points]
                    fig = self.canvas.create_polygon(real_points, outline=self.OUTLINE, fill=self.figure_color)
                    self.figures.append(
                        Trajectory(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], fig))

    def apply_changes(self):
        # Clear whole canvas, resize and draw everything again
        if self.CANVAS_WIDTH != self.drawing.winfo_width() or self.CANVAS_HEIGHT != self.drawing.winfo_height():
            if self.CANVAS_WIDTH < 250:
                self.CANVAS_WIDTH = 250
            if self.CANVAS_HEIGHT < 250:
                self.CANVAS_HEIGHT = 250
            self.my_grid = tk.PhotoImage(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
            self.canvas.create_image((self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2), image=self.my_grid,
                                     state="normal")
            for fig in self.figures:
                self.draw_line(fig.x0, fig.y0, fig.x1, fig.y1, self.OUTLINE)
                self.canvas.lift(fig.id)
            self.drawing.geometry(str(self.CANVAS_WIDTH) + 'x' + str(self.CANVAS_HEIGHT))
            self.draw_system()

    def add_coord_label(self, x, y, text):
        # Adds label to display coordinates in x,y axes
        label = tk.Label(self.canvas, text=text, bg='white', anchor='w')
        if (x, y) not in self.labels:
            label.place(x=x, y=y)
            self.labels.append((x, y))

    def draw_system(self):
        # Draws horizontal and vertical lines with distance of 100 pixels
        self.add_coord_label(0, 0, '0')
        for i in range(1, self.CANVAS_WIDTH // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=i * 100 - 10, y=0, text=i * 100)
            self.draw_line(i * 100, 0, i * 100, self.CANVAS_HEIGHT, color='gray')
        for i in range(1, self.CANVAS_HEIGHT // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=0, y=i * 100 - 10, text=i * 100)
            self.draw_line(0, i * 100, self.CANVAS_WIDTH, i * 100, color='gray')

    def draw_line(self, x1, y1, x2, y2, color, alternative_grid=False):
        # Draws line from (x1, y1) to (x2, y2) with bresenham's algorithm.
        # Alternative grid is a grid for custom drawing.
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
