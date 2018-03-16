#!/usr/bin/python3
#
# GUI for Member
#

import sys
import tkinter as tk
from Member import *
from random import randint

mem = None

root = tk.Tk()
root.title("Block Chain Member")

frm1 = tk.Frame(root)

txt_port = tk.Text(frm1, width=10, height=2); txt_port.pack(side=tk.LEFT)
txt_port.delete(1.0, tk.END)
txt_port.insert(tk.END, "1112")

txt_data = tk.Text(frm1, width=10, height=2); txt_data.pack(side=tk.LEFT)
txt_data.delete(1.0, tk.END)

def click_run():
    p = txt_port.get(1.0, tk.END)
    global mem
    if mem == None:
        mem = Member(int(p))
        mem.startListening()
    mem.runLoops()

btn_run = tk.Button(frm1, text="Run", command=click_run); btn_run.pack(side=tk.LEFT)

def click_stop():
    mem.stopLoops()

btn_run = tk.Button(frm1, text="Stop Loops", command=click_stop); btn_run.pack(side=tk.LEFT)


def click_create():
    blk = mem.blockChain.createBlock(txt_data.get(1.0, tk.END))
    if blk!=-1:
        mem.broadcastBlock(blk.id)

btn_create = tk.Button(frm1, text="Create Block", command=click_create); btn_create.pack(side=tk.LEFT)

def click_print():
    print(mem.blockChain)

btn_print = tk.Button(frm1, text="Print Chain", command=click_print); btn_print.pack(side=tk.LEFT)


frm1.pack(side=tk.TOP)

txt_log = tk.Text(root, width=60, height=30); txt_log.pack()

class stdoutRedirector:
    def __init__(self, tkwidget):
        self.tkwidget = tkwidget
    
    def write(self, string):
        self.tkwidget.insert('end', string)
        self.tkwidget.see('end')

sys.stdout = stdoutRedirector(txt_log)

root.mainloop()



