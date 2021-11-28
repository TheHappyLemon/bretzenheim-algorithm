import tkinter as tk


class App:
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.CANVAS_WIDTH = 850
        self.CANVAS_HEIGHT = 600
        self.COORD_WIDTH = self.CANVAS_WIDTH
        self.COORD_HEIGHT = self.CANVAS_HEIGHT - 200
        self.LABEL_DISTANCE = 100
        self.canvas = tk.Canvas(self.root, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()
        self.my_grid = tk.PhotoImage(width=self.CANVAS_WIDTH,height=self.CANVAS_HEIGHT)
        self.canvas.create_image((self.CANVAS_WIDTH/2, self.CANVAS_HEIGHT/2), image=self.my_grid, state="normal")
        self.root.title('Object trajetory')
        self.labels = [[],[]]
        self.draw_system()

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
                self.my_grid.put(color,(x,y))
        else:
            p = 2 * dx - dy
            while y != y2:
                y = y + ys
                if p > 0:
                    p = p + 2 * dx - 2 * dy
                    x = x + xs
                else:
                    p = p + 2 * dx
                self.my_grid.put(color,(x,y))

    def add_coord_label(self, x, y, text):
        #print('creating label at',x,y)
        label = tk.Label(self.canvas, text=text, bg='white',anchor='w')
        label.place(x=x,y=y)
        if y == 0:
            self.labels[0].append(label)
        else:
            self.labels[1].append(label)

    def draw_system(self):
        self.add_coord_label(0,0,'0')
        for i in range(1,self.COORD_WIDTH // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=i * 100 - 10,y=0,text=i * 100)
            print(i * 100,0,i * 100,self.COORD_HEIGHT)
            self.draw_line(i * 100,0,i * 100,self.COORD_HEIGHT,'#a0a3a1')
        for i in range(1,(self.COORD_HEIGHT) // self.LABEL_DISTANCE + 1):
            self.add_coord_label(x=0,y=i * 100 - 10,text=i * 100)
            self.draw_line(0,i * 100,self.COORD_WIDTH,i * 100,'#a0a3a1')
        self.root.update()



if __name__ == '__main__':
    app = App()
    app.root.mainloop()
