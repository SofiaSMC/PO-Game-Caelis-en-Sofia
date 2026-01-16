from appJar import gui
import vragenGameMakenPo

# Functie voor de knoppen
def on_button_press(button):
    if button == "stop":
        app.stop()
    
    elif button == "start":
        app.stop() #homescreen sluit
        vragenGameMakenPo.start_vragenGameMakenPo()
        
    # info box met uitleg, ik heb voor de info box en de edit box ChatGpt geraadpleegd.
    elif button == "instructies":
        app.infoBox("instructies", "Klik op start om te beginnen, de vragen zullen meteen beginnen met een 15 secode timer (als die op is sluit de GUI). Er zijn twee eindschermen; een voor een negatieve score en een voor een positieve score (mischien moet je de GUI bewegen om de eindschermen te zien)")
    
    # Edit box waar je in kan typen
    elif button == "login":
        # Tekstveld voor gebruikersnaam
        username = app.textBox("Login", "Voer je gebruikersnaam in:")
        
        # Ingevoerde data weergeven
        app.infoBox("Gegevens", f"Gebruikersnaam: {username}")
    

# GUI-app
app = gui("Homescreen", "1000x500")


# achtergrond-GIF
app.setBgImage("biggif.gif")

# formaat en kleur titel
app.addLabel("title", "Quiz", row=0, column=1)
app.setLabelFont("title", size=20)
app.setLabelBg("title", "white")  
app.setLabelFg("title", "black")

# Knoppen en hun posities
app.addButton("start", on_button_press, row=1, column=1)
app.setButtonFont(size=13)
app.addButton("instructies", on_button_press, row=2, column=2)
app.addButton("stop", on_button_press, row=2, column=0)
app.addButton("login", on_button_press, row=2, column=1)

# Kleuren van de knoppen
app.setButtonBg("start", "white")
app.setButtonBg("stop", "white")
app.setButtonBg("instructies", "white")
app.setButtonBg("login", "white")

app.setButtonFg("start", "black")
app.setButtonFg("stop", "black")
app.setButtonFg("instructies", "black")
app.setButtonFg("login", "black")

# Dit start de app
app.go()