import tkinter as tk


class App:
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.create_constants()
        self.canvas = tk.Canvas(self.root, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack(fill='both', expand=True)  # make canvas resizeable automatically
        self.root.bind('<Configure>', self.on_resize)
        self.canvas.pack()
        self.root.title('Object trajetory')
        self.draw_system()

    def create_constants(self):
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 600
        self.COORD_WIDTH = 500
        self.COORD_HEIGHT = 500
        self.COORD_PADDING = {'padx': 100, 'pady': 100}

    def draw_system(self):
        for i in range(self.COORD_WIDTH // 100):
            tmp = tk.Label(self.canvas, text=(i + 1) * 100)
            tmp.place(x=(i + 1) * 100, y=0)
            tmp.config(bg='white')
        for i in range((self.COORD_HEIGHT + 100) // 100):  # +100 to put coordinate (0;0)
            tmp = tk.Label(self.canvas, text=i * 100)
            tmp.place(x=0, y=i * 100)
            tmp.config(bg='white')


if __name__ == '__main__':
    app = App()
    app.root.mainloop()
