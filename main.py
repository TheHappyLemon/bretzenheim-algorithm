import tkinter as tk


class App:
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.CANVAS_WIDTH = 850
        self.CANVAS_HEIGHT = 650
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.root, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind('<Configure>', self.on_resize)
        self.start_point = ()
        self.drawing = False
        self.LINE_WIDTH = 0
        self.canvas.bind("<Button-1>", self.callback)
        self.root.title('Object trajetory')
        self.labels = [[],[]]
        #self.draw_system()
        self.create_main_window()

    def create_main_window(self):
        pad = 30
        font = ('*font',10)
        self.main_window = tk.Toplevel(self.root)
        self.main_window.geometry('250x300')
        self.main_window.title('Main menu')
        tmp_hold = tk.Button(master=self.main_window,text='Start',width = 10,font=font)
        tmp_hold.bind("<Button-1>",self.start)
        tmp_hold.pack(pady=pad)
        tmp_hold = tk.Button(master=self.main_window, text='Settings', width=10,font=font)
        tmp_hold.bind("<Button-1>", self.open_settings)
        tmp_hold.pack()
        tmp_hold = tk.Button(master=self.main_window, text='Author', width=10,font=font)
        tmp_hold.bind("<Button-1>", self.open_author)
        tmp_hold.pack(pady=pad)
        tmp_hold = tk.Button(master=self.main_window, text='Quit', width=10, font=font)
        tmp_hold.bind("<Button-1>", self.quit)
        tmp_hold.pack()

    def start(self, event):
        print('1')
        pass

    def open_settings(self,event):
        print('2')
        pass

    def open_author(self,event):
        print('3')
        pass

    def quit(self,event):
        print('4')
        pass

    def on_click(self, event):
        print(event)

    def callback(self, event):
        if self.drawing:
            self.draw_line(self.start_point[0],self.start_point[1], event.x, event.y, '#ffffff')
            self.drawing = False
        else:
            self.start_point = (event.x, event.y)
            self.drawing = True

    def on_resize(self, event):
        # TODO make option to refresh if user resized too fast, because it breaks :)
        # DONT TOUCH THIS PART ANYMORE IT IS AWFUL, IT IS DISGUSTING
        labels_can_fit_x = (event.width - self.CANVAS_WIDTH) // self.LABEL_DISTANCE
        labels_can_fit_y = (event.height - self.CANVAS_HEIGHT) // self.LABEL_DISTANCE
        if event.width > self.CANVAS_WIDTH and labels_can_fit_x > 0:
            for i in range(labels_can_fit_x):
                self.add_coord_label(self.labels[0][-1].winfo_x() + self.LABEL_DISTANCE, 0, int(self.labels[0][-1].cget('text')) + 100)
                self.root.update()
            for i in range(labels_can_fit_x):
                delta = (i + len(self.labels[0]) - labels_can_fit_x) * 100
                self.canvas.create_line(delta, 0, delta, event.height, fill='light gray')
            for i in range(0, len(self.labels[1])):
                self.canvas.create_line(self.CANVAS_WIDTH, (i + 1) * 100, event.width, (i + 1) * 100, fill='light gray')
            self.CANVAS_WIDTH = event.width
        if event.height > self.CANVAS_HEIGHT and labels_can_fit_y > 0:
            for i in range(labels_can_fit_y):
                self.add_coord_label(0, self.labels[1][-1].winfo_y() + self.LABEL_DISTANCE, int(self.labels[1][-1].cget('text')) + 100)
                self.root.update()
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
                self.canvas.create_rectangle(x, y, x , y + self.LINE_WIDTH, outline='red')
        else:
            p = 2 * dx - dy
            while y != y2:
                y = y + ys
                if p > 0:
                    p = p + 2 * dx - 2 * dy
                    x = x + xs
                else:
                    p = p + 2 * dx
                self.canvas.create_rectangle(x, y, x + self.LINE_WIDTH , y, outline='blue')


if __name__ == '__main__':
    app = App()
    app.root.mainloop()
