import tkinter as tk
from tkinter import colorchooser
from enum import Enum

class Window(Enum):
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
        self.main_btns = [self.start_btn, self.stg_btn, self.author_btn]
        tmp = tk.Button(master=self, text='Quit', width=10, font=self.FONT)
        tmp.configure(command=self.quit)
        tmp.pack()
        

    def action_33(self):
        self.withdraw()
        self.cur_window = Window.DRAWING
        self.drawing = tk.Toplevel(master=self)
        self.drawing.bind('<Escape>', self.open_main)
        self.drawing.protocol("WM_DELETE_WINDOW", self.quit)
        self.drawing.focus_force()
        self.CANVAS_WIDTH = 850
        self.CANVAS_HEIGHT = 650
        self.drawing.geometry(str(self.CANVAS_WIDTH)+'x'+str( self.CANVAS_HEIGHT))
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.drawing, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind('<Configure>', self.on_resize)
        self.start_point = ()
        self.is_drawing = False
        self.LINE_WIDTH = 0
        self.canvas.bind("<Button-1>", self.callback)
        self.drawing.title('Object trajetory')
        self.labels = [[],[]]
        self.pixels = []
        self.draw_system()

    def pick_color(self):
        self.pck_btn["state"] = tk.DISABLED
        colors = colorchooser.askcolor(title="Choose a fancy color!")
        self.pck_btn["state"] = tk.NORMAL
        print(colors[1])

    def open_settings(self):
        self.withdraw()
        self.cur_window = Window.SETTINGS
        self.settings = tk.Toplevel(master=self)
        self.settings.geometry('300x300')
        self.settings.resizable(False, False)
        self.settings.protocol("WM_DELETE_WINDOW", self.quit)
        self.pck_btn = tk.Button(master=self.settings, text="Pick line's colour", font=self.FONT)
        self.pck_btn.configure(command=self.pick_color)
        self.pck_btn.pack(pady=30)
        frame = tk.Frame(master=self.settings)
        frame.pack()
        tk.Label(master=frame, text="Line`s width in pixels", padx=5,
                 font=self.FONT).grid(row=0, column=0)
        self.spinbox = tk.Spinbox(master=frame,from_=0, to=50,font=self.FONT)
        self.spinbox.grid(row=0,column=1)
        tk.Label(master=self.settings, text="Resize window:", font=self.FONT).pack(pady=30)
        frame = tk.Frame(master=self.settings)
        frame.pack()
        tk.Label(master=frame, text="width  (0 - "+str(self.winfo_screenwidth())+")", padx=5,
                 font=self.FONT).grid(row=0,column=0)
        tk.Label(master=frame, text="height (0 - "+str(self.winfo_screenheight())+")", padx=5,
                 font=self.FONT).grid(row=1,column=0)
        self.entr_W = tk.Entry(master=frame, validate="key",
                               validatecommand=(self.settings.register(self.validate_width), "%P"), font=self.FONT)
        self.entr_W.grid(row=0,column=1)
        self.entr_H = tk.Entry(master=frame, validate='key',
                               validatecommand=(self.settings.register(self.validate_height), "%P"), font=self.FONT)
        self.entr_H.grid(row=1, column=1)


    def validate_width(self, value):
        # Checks if entered num is a num and less that screen width
        try:
            value = int(value)
            if value > 0 and value <= self.winfo_screenwidth():
                return True
            self.settings.bell()
            return False
        except ValueError:
            if value == '':
                return True
            self.settings.bell()
            return False

    def validate_height(self, value):
        # Checks if entered num is a num and less that screen height
        try:
            value = int(value)
            if value > 0 and value <= self.winfo_screenheight():
                return True
            self.settings.bell()
            return False
        except ValueError:
            if value == '':
                return True
            self.settings.bell()
            return False



    def open_author(self):
        print('3')
        pass

    def open_main(self, event):
        print(self.cur_window.value)
        self.main_btns[self.cur_window.value]["state"] = tk.DISABLED
        self.deiconify()

    def quit(self, event=None):
        self.destroy()
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

    def on_resize(self, event):
        # TODO make option to refresh if user resized too fast, because it breaks :)
        # DONT TOUCH THIS PART ANYMORE IT IS AWFUL, IT IS DISGUSTING
        for px in self.pixels:
            #that is just for test to see whether I can delete drawn lines
            self.canvas.delete(px)
            self.pixels.remove(px)
        print(len(self.pixels))
        labels_can_fit_x = (event.width - self.CANVAS_WIDTH) // self.LABEL_DISTANCE
        labels_can_fit_y = (event.height - self.CANVAS_HEIGHT) // self.LABEL_DISTANCE
        if event.width > self.CANVAS_WIDTH and labels_can_fit_x > 0:
            for i in range(labels_can_fit_x):
                self.add_coord_label(self.labels[0][-1].winfo_x() + self.LABEL_DISTANCE, 0, int(self.labels[0][-1].cget('text')) + 100)
                self.update()
            for i in range(labels_can_fit_x):
                delta = (i + len(self.labels[0]) - labels_can_fit_x) * 100
                print(self.canvas.create_line(delta, 0, delta, event.height, fill='light gray'))
            for i in range(0, len(self.labels[1])):
                self.canvas.create_line(self.CANVAS_WIDTH, (i + 1) * 100, event.width, (i + 1) * 100, fill='light gray')
            self.CANVAS_WIDTH = event.width
        if event.height > self.CANVAS_HEIGHT and labels_can_fit_y > 0:
            for i in range(labels_can_fit_y):
                self.add_coord_label(0, self.labels[1][-1].winfo_y() + self.LABEL_DISTANCE, int(self.labels[1][-1].cget('text')) + 100)
                self.update()
            for i in range(labels_can_fit_y):
                delta = (i + len(self.labels[1]) - labels_can_fit_y + 1) * 100
                self.canvas.create_line(0, delta, event.width, delta, fill='light gray')
            for i in range(0, len(self.labels[0])):
                self.canvas.create_line((i + 1) * 100, self.CANVAS_HEIGHT, (i + 1) * 100, event.height, fill='light gray')
            self.CANVAS_HEIGHT = event.height

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
                self.pixels.append(self.canvas.create_rectangle(x, y, x , y + self.LINE_WIDTH, outline='red'))
        else:
            p = 2 * dx - dy
            while y != y2:
                y = y + ys
                if p > 0:
                    p = p + 2 * dx - 2 * dy
                    x = x + xs
                else:
                    p = p + 2 * dx
                self.pixels.append(self.canvas.create_rectangle(x, y, x + self.LINE_WIDTH , y, outline='blue'))


if __name__ == '__main__':
    app = App()
    app.mainloop()
