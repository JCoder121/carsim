#Connect 4 Jeffrey Chen opened 2/6/19 closed 2/12/19
#6 vertical lines 5 horizontal lines
import tkinter as tk

class Connect4(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        #self.create_buttons()
        #self.create_board()

    #def create_buttons(self):
        #self.root = tk.Tk()
        #self.root.geometry("500x500")

#fix later
        frame = tk.Frame(self.root)
        frame.grid(row=0,column=0, sticky="n")

        self.button1 = tk.Button(self,width = 20, height = 2)
        self.button2 = tk.Button(self,width = 20, height = 2)
        self.button3 = tk.Button(self,width = 20, height = 2)
        self.button4 = tk.Button(self,width = 20, height = 2)
        self.button5 = tk.Button(self,width = 20, height = 2)
        self.button6 = tk.Button(self,width = 20, height = 2)
        self.button7 = tk.Button(self,width = 20, height = 2)

        self.button1.grid(row = 2, column =4)
        #self.button1.pack(side = 'left')
        #self.button2.pack(side = 'left')
        #self.button3.pack(side = 'left')
        #self.button4.pack(side = 'left')
        #self.button5.pack(side = 'left')
        #self.button6.pack(side = 'left')
        #self.button7.pack(side = 'left')

    def create_board(self):
        self.board = tk.Canvas(self, width = 500, height = 500)
        self.board.pack()
        #self.horizline1 = self.board.create_line(x1, y1, x2, y2)
    #    horizline1 = canvas.create_line(0,150,500,150)
    #    horizline2 = canvas.create_line(0,325,500,325)
    #    vertline1 = canvas.create_line(160,0,160, 500)
    #    vertline2 = canvas.create_line(335,0,335, 500)




print('start')

root = tk.Tk()
app = Connect4(master=root)
app.mainloop()

print('done')
