from Tkinter import *

class App:
    def __init__(self,root):
        frame = Frame(root)
        frame.pack()
        root.title('Simple')
        self.quitbutton=Button(frame,text="Quit",command=frame.quit)
        self.quitbutton.pack(side=LEFT)
        self.hibutton=Button(frame,text="press me", command=self.hi)
        self.hibutton.pack(side=RIGHT)
    def hi(self):
        print 'hello!'


if __name__ == '__main__':
    root = Tk()

    App(root)

    root.mainloop()
