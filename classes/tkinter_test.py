from tkinter import *

master = Tk()

w = Canvas(master, width=200, height=100)
w.pack()

w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

i = w.create_rectangle(50, 25, 150, 75, fill="blue")

#w.delete(i) # remove

#w.delete(ALL) # remove all items

mainloop()