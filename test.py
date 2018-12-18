
from Tkinter import *
from mt_support import put, evaluate, set_master
from time import sleep
import threading


class MultiThreadingEnvironment:
    def __init__(self):
        self.root = Tk()
        set_master(self.root)
        self.text = Text(self.root)
        self.text.pack()

    def update_text(self):
        for i in range(100):
            put(self.text.insert, END, str(i)+"\n")
            # self.text.insert(END, str(i)+"\n")
            put(self.text.yview, END)
            sleep(0.5)

    def start(self):
        threading.Thread(target=self.update_text).start()
        self.root.mainloop()


mte = MultiThreadingEnvironment()
mte.start()