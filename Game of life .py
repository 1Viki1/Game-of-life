import tkinter as tk
import numpy as np
from tkinter import filedialog as fd

win = tk.Tk()


WIDTH = 500
HEIGHT = 500
vs = 10
abs = vs
#cells = []
cells = np.zeros((WIDTH//vs, HEIGHT//vs), dtype = int) #dvojrozmerný zoznam
cells_new = np.zeros((WIDTH//vs, HEIGHT//vs), dtype = int)
print(cells)

def getne(x,y):
    total = 0
    if x > 0:
        total += cells[x-1, y]
    if x > 0 and y > 0:
        total += cells[x-1, y-1]
    if y > 0:
        total += cells[x, y-1]
    if x < (WIDTH//abs-1) and y < (HEIGHT//abs-1):
        total += cells[x+1, y+1]
    if x > 0 and y < (HEIGHT//abs-1):
        total += cells[x-1, y+1]
    if y < (HEIGHT//abs-1):
        total += cells[x, y+1]
    if x < (WIDTH//abs-1):
        total += cells[x+1, y]
    if y > 0 and x < (WIDTH//abs-1):
        total += cells[x+1, y-1]
    return total


def recalculate(): # počítame počet susedných buniek
    global cells, cells_new
    #prepočet - v dvoch cykloch chodím po bunkách a pýtam sa koľko majú susedov
    for y in range(HEIGHT//abs):
        for x in range(WIDTH//abs):
            temp = getne(x,y)
            if temp == 2 and cells[x,y] == 1:
                cells_new[x,y] = 1
            if temp == 3:
                cells_new[x,y] = 1
            if temp < 2 or temp > 3:
                cells_new[x,y] = 0
    cells = cells_new.copy()
    canvas.delete("all")
    create_stage()
    redraw_cells()

def slider_changed(e):
    global vs
    print(slider.get())
    canvas.delete("all") #vymaž canvas  - vymaže všetko čo je na canvase
    vs = slider.get()    #zoberie hodnotu slidera a dá ho do premennej vs
    create_stage()  #vykresli mriežku
    redraw_cells()


def create_cells(e):
    global cells
    tx = e.x//vs
    ty = e.y//vs
    x = (tx)*vs
    y = (ty)*vs
    #cells.append(canvas.create_oval(x+5,y+5,x+vs-5,y+vs-5,fill="yellow"))      #máme idečka v cells
    canvas.create_rectangle(x,y,x+vs,y+vs,fill="yellow")
    cells[tx,ty]=1
    print(getne(tx,ty))
    #print(cells)

def redraw_cells():
    # prechádzame cell a ak tam je 1 vykreslia bunku na prislušnom mieste a rozmeroch
    for x in range(WIDTH//vs):
        for y in range(HEIGHT//vs):
            if cells[x,y] == 1:
                canvas.create_rectangle(x*vs,y*vs,(x+1)*vs,(y+1)*vs, fill = "yellow")

def create_stage():
    for x in range(WIDTH//vs):
        canvas.create_line(x*vs,0,x*vs,HEIGHT)
    for y in range(HEIGHT//vs):
        canvas.create_line(0,y*vs,WIDTH,y*vs)

def open_file():
    #ak je tam jedna hod ju do cells a vykresli cells
    global cells, cells_new
    zoz = []
    poc = 0
    filename = fd.askopenfilename()
    f = open(filename,"r")
    for i in f:
        for j in i.split():
            zoz.append(j)
    for m in zoz:
        for n in m:
            poc += 1
    if poc < 2500:    # 50*50
        for o in range(len(zoz)):    #cyklus sa zopakuje toľkokrát, koľko je dlžka zoznamu
            for p in range(len(zoz[p])):
                print(zoz[o][p])
                if zoz[o][p] == "1":        #ak zoznam na tom mieste sa rovná 1 tak aj bunka sa budú rovnať 1 (vytvorí sa)
                    cells_new[o, p] = 1
                else:
                    cells_new[o, p] = 0
        cells = cells_new.copy()
        canvas.delete("all")
        create_stage()
        redraw_cell()
    else:
        print("Tvoj súbor je príliš veľký")

def opakovanie():
    if button2.config("text")[-1] == "STOP":  #ak je tlačidlo na tejto pozícii tak sa spustí recalculate
        recalculate()
        win.after(500, opakovanie)     # potom sa 500 milisekúnd obnocí canvas
    #print(button2.config("text")[-1])

def change():
    if button2.config("text")[-1] == "ŠTART":  #ak je tlačidlo na tejto pozícii tak po ďalšom kliknutí sa zmení
        button2.config(text = "STOP")
        opakovanie()        # a znovu sa spustí funkcia opakovanie
    else:
        button2.config(text = "ŠTART")

canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

slider = tk.Scale(win, from_=10, to=50, orient="horizontal", command = slider_changed, length = 500)  #https://python-course.eu/tkinter/sliders-in-tkinter.php
slider.pack()

button = tk.Button(win, text = "ĎALŠIA GENERÁCIA", command = recalculate)
button.pack(side = tk.RIGHT)

button1 = tk.Button(win, text = "OTVOR SÚBOR", command = open_file)
button1.pack(side=tk.LEFT)

button2 = tk.Button(win, text = "ŠTART", command = change)
button2.pack(side=tk.BOTTOM)

create_stage()
canvas.bind("<Button-1>",create_cells)

win.mainloop()
