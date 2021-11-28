import tkinter as tk


class App:
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()
        self.root.title('Object trajetory')
        self.a = 'a'
        self.COORD_WIDTH = 500
        self.COORD_HEIGHT = 500
        self.COORD_PADDING = {'padx': 100, 'pady': 100}
        self.draw_system()

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
