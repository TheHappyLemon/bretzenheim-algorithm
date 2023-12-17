# Task made during course "Datorgrafikas un attēlu apstrādes pamati(1) (DAA300)" - 2021 Fall

Source code for course work in subject "Computer graphics and basics of image processing". This work was done entirely by myself during the last month of my first semester in Riga Technical University.

This application allows user to draw straight lines by giving coordinates with two clicks. After first click preview line will be drawn all the way from start point to the current position of pointer on the screen. This continues until second click is performed. "Preview" line is being drawn with tkinter built-in method of canvas c.create_line(). I chose built in, because putting multiple pixels whenever cursor moves impacts performance a lot. Final line after second click is drawn with my implementation of bresenham's algorithm. When line is drawn chosen figure starts moving on this line.

I made different setting available:
  1) Change colour of line
  2) Change colour of figure
  3) Change diameter of figure
  4) Draw custom figure
  5) Resize window. The reason I restricted to resize window by dragging its borders, is because I need to redraw coordinate system in the background.
