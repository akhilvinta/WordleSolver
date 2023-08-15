from tkinter import *

root = Tk()
myLabel = Label(root, text="Wordle Solver")
myLabel.pack()


firstLetter = Entry(root, width=10, borderwidth=5)
firstLetter.grid(row=0, column=0, padx=10, pady=10)
firstLetter.insert(0,"fl")








root.mainloop()


