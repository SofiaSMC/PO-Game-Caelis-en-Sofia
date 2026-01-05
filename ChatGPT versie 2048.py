from appJar import gui
import random

SIZE = 4 #maakt het speelveld 4x4
board = [[0]*SIZE for _ in range(SIZE)] #maakt het spelbord met allemaal nullen

def add_tile(): #functie om een nieuwe 2 op een lege plekj te zetten
    empty = [(r,c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0] #zoekt de lege vakjes
    if empty: #alleen doorgaan als er nog lege plekken zijn
        r, c = random.choice(empty) #zoekt een willekeurige lege plek
        board[r][c] = 2 #plaats een 2 op het lege plek

def draw(): #functie om het bord te tekenen in gui
    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c] #haalt waarde van het vakje op
            app.setLabel(f"{r}{c}", str(val) if val else "") #alle vakjes hebben/krijgen een waarde, als waarde > 0 dan toont het getal, als waarde = 0 dan blijft het leeg

def compress(row): #code voor het schuiven (naar links)
    row = [n for n in row if n]
    return row + [0]*(SIZE-len(row)) #vult de (nieuwe) lege plekken aan met nullen

def merge(row): #code om de getallen samen te voegen
    for i in range(SIZE-1): #loopt door de rij (behalve laatst)
        if row[i] and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
            #alleen mergen als het getal niet nul en beiden hetzelfde
    return row

def move_left():
    moved = False #houdt bij of er iets veranderd is
    for r in range(SIZE):
        new = compress(merge(compress(board[r]))) #schuift (compress) -> samenvoegen (merge) -> gaten opruimen (compress)
        if new != board[r]:
            moved = True #checkt of de rij echt is veranderd
        board[r] = new #updated het board
    return moved

def rotate(): #hiermee word het bord 90 graden rechtsom gedraaid
    global board
    board = [list(r) for r in zip(*board[::-1])]
    #hiermee kan het bord zo draaien dat elke richting naar links is

def move(turns): #turns = hoeveel keer draaien
    for _ in range(turns):
        rotate() #draait het bord zodat de gewenste richting links is
    moved = move_left() #doet de beweging
    for _ in range((4-turns)%4): 
        rotate() #draait het bord terug
    return moved

def key(key):
    keys = {"a":0, "w":1, "d":2, "s":3} #koppelt de toetsen aan richtingen
    if key in keys and move(keys[key]):
        add_tile() #nieuwe 2
        draw() #tekend het bord opnieuw

app = gui("2048 (appJar)", "300x300")
app.setFont(18) #maakt gui en vegroot de tekst

for r in range(SIZE):
    for c in range(SIZE):
        app.addLabel(f"{r}{c}", "", r, c) #elk vakje is één laben in een grid
        app.setLabelBg(f"{r}{c}", "lightgrey")
        app.setLabelWidth(f"{r}{c}", 5)

#koppelt toetsen aan de key() functie
app.bindKey("w", key)
app.bindKey("a", key)
app.bindKey("s", key)
app.bindKey("d", key)

#startspel, 2 tegels en tekent bord
add_tile()
add_tile()
draw()

app.go()