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
        self.canvas.config(width=self.CANVAS_WIDTH+self.LABEL_WIDTH)
        self.canvas.pack(fill='both', expand=True)  # make canvas resizeable automatically
        self.root.bind('<Configure>', self.on_resize)
        self.canvas.pack()
        self.root.title('Object trajetory')
        self.draw_system()
        self.labels= [[],[]]


    def on_resize(self, event):
        deltax = self.canvas.winfo_width() - self.CANVAS_WIDTH
        deltay = self.canvas.winfo_height() - self.CANVAS_HEIGHT
        if deltax != 0:
            pass
            #pif deltax -
        if deltay != 0:
            pass


    def draw_system(self):
        for i in range(1,self.CANVAS_WIDTH // 100 + 1):
            tmp = tk.Label(self.canvas, text=i * 100)
            tmp.place(x=i * 100, y=0)
            tmp.config(bg='white')
            self.labels[0].append(tmp)
        for i in range(1, self.CANVAS_HEIGHT // 100 + 1):
            tmp = tk.Label(self.canvas, text=i * 100)
            tmp.place(x=0, y=i * 100)
            tmp.config(bg='white')
            self.labels[1].append(tmp)


if __name__ == '__main__':
    app = App()
    app.root.mainloop()
