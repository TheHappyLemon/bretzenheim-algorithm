import tkinter as tk
from tkinter import colorchooser
from enum import Enum
import webbrowser

class Window(Enum):
    MAIN = -1
    DRAWING = 0
    SETTINGS = 1
    AUTHOR = 2

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        pad = 30
        self.FONT = ('*font', 10)
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
        self.cur_window = -1
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
        self.drawing.protocol("WM_DELETE_WINDOW", self.quit)
        self.drawing.focus_force()
        self.drawing.geometry(str(self.CANVAS_WIDTH)+'x'+str( self.CANVAS_HEIGHT))
        self.drawing.resizable(False, False)
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.drawing, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        self.start_point = ()
        self.is_drawing = False
        self.LINE_WIDTH = 0
        self.OUTLINE = 'black'
        self.canvas.bind("<Button-1>", self.callback)
        self.drawing.title('Object trajetory')
        self.labels = [[],[]]
        self.pixels = []
        self.draw_system()
        self.bind_tree(self.drawing, '<Escape>', self.open_main)


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
        self.pck_btn = tk.Button(master=self.settings, text="Pick line's colour", font=self.FONT)
        self.pck_btn.configure(command=self.pick_color)
        self.pck_btn.pack(pady=30)
        frame = tk.Frame(master=self.settings)
        frame.pack()
        tk.Label(master=frame, text="Line`s width in pixels", padx=5,
                 font=self.FONT).grid(row=0, column=0)
        self.spinbox = tk.Spinbox(master=frame,from_=1,to=50,validate="key",
                                  validatecommand=(self.settings.register(self.validate), "%P", 0, 50,0), font=self.FONT)
        self.spinbox.grid(row=0,column=1)
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
        # self.bind_tree(self.settings, '<Escape>', self.open_main) -
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

    def pick_color(self) -> str:
        #  Returns none if window was closed using X
        self.pck_btn["state"] = tk.DISABLED
        colors = colorchooser.askcolor(title="Choose a fancy color!")
        self.pck_btn["state"] = tk.NORMAL
        if colors[1] != None:
            self.OUTLINE = colors[1]
        else:
            self.OUTLINE = 'black'

    def quit_stg(self):
        if self.drawing_on:
            self.drawing_on = False
            self.cur_window = Window.DRAWING
            self.resize_drawing(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
            self.settings.destroy()
        else:
            self.quit()

    def bind_tree(self, widget, event, call):
        # Function to recursively bind ESC event (to open main window)
        # to every single widget in a widget
        #I think it is useleess hmmm
        for child in widget.children.values():
            if len(child.winfo_children()):
                self.bind_tree(child, event, call)
            child.bind('<Escape>', self.open_main)

    def validate(self, value, min_value, max_value, widget_num):
        # Checks if entered num is a num and less than given value
        try:
            value = int(value)
            if value >= int(min_value) and value <= int(max_value):
                print(widget_num)
                if widget_num == '0':
                    self.LINE_WIDTH = value
                elif widget_num == '1':
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
        print('ESC pressed')
        print(self.cur_window)
        if self.cur_window == Window.SETTINGS and self.drawing_on:
            self.windows[self.cur_window.value].destroy()
            self.cur_window = Window.DRAWING
            self.resize_drawing(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
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


    def on_click(self, event):
        print(event)

    def callback(self, event):
        self.canvas.delete()
        if self.is_drawing:
            self.draw_line(self.start_point[0],self.start_point[1], event.x, event.y, '#ffffff')
            self.is_drawing = False
        else:
            self.start_point = (event.x, event.y)
            self.is_drawing = True

    def resize_drawing(self,width, height):
        if width > self.MAX_WIDTH:
            self.MAX_WIDTH = width
            labels_can_fit_x = (width - self.drawing.winfo_width()) // self.LABEL_DISTANCE
            for i in range(labels_can_fit_x):
                self.add_coord_label(self.labels[0][-1].winfo_x() + self.LABEL_DISTANCE, 0, int(self.labels[0][-1].cget('text')) + 100)
                self.update()
            for i in range(labels_can_fit_x):
                delta = (i + len(self.labels[0]) - labels_can_fit_x) * 100
                print(self.canvas.create_line(delta, 0, delta, height, fill='light gray'))
                pass
            for i in range(0, len(self.labels[1])):
                self.canvas.create_line(self.drawing.winfo_width(), (i + 1) * 100, width, (i + 1) * 100, fill='light gray')
        if height > self.MAX_HEIGHT:
            self.MAX_HEIGHT = height
            labels_can_fit_y = (height - self.drawing.winfo_height()) // self.LABEL_DISTANCE
            for i in range(labels_can_fit_y):
                self.add_coord_label(0, self.labels[1][-1].winfo_y() + self.LABEL_DISTANCE, int(self.labels[1][-1].cget('text')) + 100)
                self.update()
            for i in range(labels_can_fit_y):
                delta = (i + len(self.labels[1]) - labels_can_fit_y + 1) * 100
                self.canvas.create_line(0, delta, width, delta, fill='light gray')
            for i in range(0, len(self.labels[0])):
                self.canvas.create_line((i + 1) * 100, self.drawing.winfo_height(), (i + 1) * 100, height, fill='light gray')
        self.drawing.geometry(str(self.CANVAS_WIDTH)+'x'+str(self.CANVAS_HEIGHT))

    def add_coord_label(self, x, y, text):
        label = tk.Label(self.canvas, text=text, bg='white',anchor='w')
        label.place(x=x,y=y)
        label.bind('<Button-1>,', self.on_click)
        if y == 0:
            self.labels[0].append(label)
        else:
            self.labels[1].append(label)

    def draw_system(self):
        self.add_coord_label(0,0,'0')
        for i in range(1,self.CANVAS_WIDTH // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=i * 100 - 10,y=0,text=i * 100)
            self.canvas.create_line(i * 100,0,i * 100,self.CANVAS_HEIGHT,fill='light gray')
        for i in range(1,self.CANVAS_HEIGHT // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=0,y=i * 100 - 10,text=i * 100)
            print(0,i * 100,self.CANVAS_WIDTH,i * 100)
            self.canvas.create_line(0,i * 100,self.CANVAS_WIDTH,i * 100,fill='light gray')

    def draw_line(self, x1, y1, x2, y2, color):
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
                self.pixels.append(self.canvas.create_rectangle(x, y, x , y + self.LINE_WIDTH, outline=self.OUTLINE))
        else:
            p = 2 * dx - dy
            while y != y2:
                y = y + ys
                if p > 0:
                    p = p + 2 * dx - 2 * dy
                    x = x + xs
                else:
                    p = p + 2 * dx
                self.pixels.append(self.canvas.create_rectangle(x, y, x + self.LINE_WIDTH , y, outline=self.OUTLINE))


if __name__ == '__main__':
    app = App()
    app.mainloop()
