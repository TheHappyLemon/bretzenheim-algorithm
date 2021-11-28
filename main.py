import tkinter as tk


class App:
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 600
        self.canvas = tk.Canvas(self.root, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        tmp = tk.Label(master=self.canvas,text='0',width=4,bg='white') # WIDTH IS IN CHARACTERS!!!!!!!!!!!!!!!
        tmp.place(x=0,y=0)
        self.root.update()
        self.LABEL_WIDTH = tmp.winfo_width()
        self.LABEL_HEIGHT = tmp.winfo_reqheight()
        self.LABEL_DISTANCE = 100
        self.root.update()
        print(self.canvas.winfo_reqwidth())
        self.canvas.pack(fill='both', expand=True)  # make canvas resizeable automatically
        self.root.bind('<Configure>', self.on_resize)
        self.canvas.pack()
        self.root.title('Object trajetory')
        self.labels = [[],[]]
        self.draw_system()


    def add_coord_label(self, x, y, text):
        print('creating label at',x,y)
        label = tk.Label(self.canvas, text=text, bg='white')
        label.place(x=x,y=y)
        if y == 0:
            self.labels[0].append(label)
        else:
            self.labels[1].append(label)


    def on_resize(self, event):
        deltax = self.canvas.winfo_width() - self.CANVAS_WIDTH
        deltay = self.canvas.winfo_height() - self.CANVAS_HEIGHT
        if deltax >=self.LABEL_DISTANCE + self.LABEL_WIDTH:
            self.add_coord_label(self.labels[0][-1].winfo_x() + self.LABEL_DISTANCE,0,
                                int(self.labels[0][-1].cget('text')) + 100)
            self.CANVAS_WIDTH = self.canvas.winfo_width()
        if deltay >= self.LABEL_DISTANCE + self.LABEL_WIDTH:
            self.add_coord_label(0, self.labels[1][-1].winfo_y() + self.LABEL_DISTANCE,
                            int(self.labels[1][-1].cget('text')) + 100)
            self.CANVAS_HEIGHT = self.canvas.winfo_height()


    def draw_system(self):
        for i in range(1,self.CANVAS_WIDTH // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=i * 100,y=0,text=i * 100)
        for i in range(1, (self.CANVAS_HEIGHT - 200) // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=0,y=i * 100,text=i * 100)
        self.root.update()



if __name__ == '__main__':
    app = App()
    app.root.mainloop()
