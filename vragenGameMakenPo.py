from appJar import gui
from pathlib import Path
import time
import threading

# Lijst met vragen en antwoorden (opbouw door ChatGPT, vragen van mijzelf)
vragen = [
    {"vraag": "Wat is de hoofdstad van Frankrijk?", "antwoorden": ["Parijs", "Londen", "Berlijn"], "correct": "Parijs"},
    {"vraag": "Welk land grenst aan Duitsland?", "antwoorden": ["Ierland", "Verenigd Koninkrijk", "Polen"], "correct": "Polen"},
    {"vraag": "Waar ligt Andorra?", "antwoorden": ["naast Spanje", "tussen Zwitserland en Oostenrijk", "Dat land bestaat niet"], "correct": "naast Spanje"},
    {"vraag": "Welke Alfabet gebruikt rusland?", "antwoorden": ["Russische alfabet", "Cyrillisch schrift", "Latijn alfabet"], "correct": "Cyrillisch schrift"},
    {"vraag": "Welk land heeft de meeste tijdzones", "antwoorden": ["Frankrijk", "Rusland", "Verenigd Koninkrijk"], "correct": "Frankrijk"},
    {"vraag": "Uit welk land komt Stalin", "antwoorden": ["Sovjet Unie", "Georgïe", "Rusland"], "correct": "Georgïe"},
    {"vraag": "Wat is de engelse vertaling van het woord: gezellig?", "antwoorden": ["cozy", "warm", "geen vertaling mogelijk"], "correct": "geen vertaling mogelijk"},
    {"vraag": "Indonesië verklaarde in ... onafhankelijkheid", "antwoorden": ["1945", "1949", "1972"], "correct": "1945"},
    {"vraag": "Wie werd op 4 November 1995 vermoordt?", "antwoorden": ["Premier Rabin van Israël", "President John F. Kennedy van de VS", "Stadhouder De Witt van de Republiek der zeven verenigde Nederlanden"], "correct": "Premier Rabin van Israël"},
    {"vraag": "Wat is het grootste bedrijf ooit?", "antwoorden": ["Apple", "Bad Boy records", "VOC"], "correct": "VOC"},
    {"vraag": "De staat israël werd in ... uitgeroepen", "antwoorden": ["1946", "1948", "1952"], "correct": "1948"},
    {"vraag": "Wat is de Joodse/Hebreeuwse benaming voor de holocaust?", "antwoorden": ["holocaust", "de ramp", "Shoah"], "correct": "Shoah"},
    {"vraag": "Hoe stierf keizer Basileios I van het Oost-Romeinse rijk?", "antwoorden": ["Gespiest door hert", "Op het slagveld", "Vergiftiging"], "correct": "Gespiest door hert"},
    {"vraag": "Hoe heet een wetenschapper die sterren bestudeert?", "antwoorden": ["Meteoroloog", "Astronoom", "Astroloog"], "correct": "Astronoom"},
    {"vraag": "Van welk van de volgende landen lijkt de vlag op die van Nederland?", "antwoorden": ["Liechtenstein", "Luxemburg", "DR Congo"], "correct": "Luxemburg"},
    {"vraag": "Welk orgaan zuivert je bloed?", "antwoorden": ["lever", "Kringspier", "nieren"], "correct": "nieren"},
    {"vraag": "Wat was Julius Caesar in de tijd van zijn dood?", "antwoorden": ["Romeinse generaal", "Romeinse dictator", "Romeinse keizer"], "correct": "Romeinse dictator"},
    {"vraag": "Wat is de dreamteam?", "antwoorden": ["Kieft & Klos", "LeBron & Bronny", "japan & Deutschland"], "correct": "Kieft & Klos"},
    {"vraag": "Op welke aardplaat ligt europa?", "antwoorden": ["europees-aziatische plaat", "europese plaat", "euraziatische plaat"], "correct": "euraziatische plaat"},
    {"vraag": "Op welke datum erkende Bhutan Nederland als echte staat?", "antwoorden": ["10 Juni 1985", "2 januari 1995", "nooit"], "correct": "10 Juni 1985"},
    {"vraag": "Wat is magma boven de grond?", "antwoorden": ["lava", "obsidiaan", "magma"], "correct": "lava"},
]

# Variabelen voor score en timer
score = 0
tijd_over = 15  # Start met 15 seconden per vraag
running = True  # Voor de timer-loop
huidige_vraag = 0  # Houdt bij welke vraag wordt getoond

# de code voor de eindschermen
def toon_eindscherm():
    app.removeAllWidgets()
    
    if score > 0:
        app.addLabel("eindeLabel", "∞ iq... je score: " + str(score), 0, 0)
        
    
    else:
        app.addLabel("eindeLabel", "you stupid... je score: " + str(score), 0, 0)
        
        
# Functie voor juiste en foute antwoorden
def controleer_antwoord(keuze):
    global score, tijd_over, huidige_vraag

    if keuze == vragen[huidige_vraag]["correct"]:
        app.queueFunction(app.setLabel, "feedbackLabel", "Goed antwoord! 🎉") #app.queueFunction met behulp van ChatGPT (de feedbacklabel kwam steeds niet in beeld)
        score += 1
                
    else:
        app.queueFunction(app.setLabel, "feedbackLabel", "Fout antwoord! ❌")
        score -= 1
                    
    app.setLabel("scoreLabel", f"Score: {score}")
           
    tijd_over = 16  # Reset de timer
    huidige_vraag += 1
    if huidige_vraag < len(vragen):
        app.after(1000, toon_vraag) #seconde vertraging met behulp van ChatGPT (de code ging eerst gelijk door naar de volgend evraag waardoor je de feedback niet kon zien)
    else:
        app.after(1000, toon_eindscherm) 

# Functie om vragen weer te geven
def toon_vraag():
    app.removeAllWidgets()
    app.addLabel("scoreLabel", f"Score: {score}", row=0, column=0)
    app.addLabel("timerLabel", f"Tijd: {tijd_over}s", row=0, column=1)
    app.addLabel("vraagLabel", vragen[huidige_vraag]["vraag"], row=1, column=0, colspan=2)
    app.setLabelFont("vraaglabel", size=15) # grootte van de vraag
    app.addLabel("feedbackLabel", "", row=2, column=0, colspan=2)  # Feedback label
    
    # antwoordknoppen
    for i, antwoord in enumerate(vragen[huidige_vraag]["antwoorden"]):
        app.addButton(antwoord, controleer_antwoord, row=3 + i, column=0, colspan=2)
        app.setButtonFont(size=13) # Grootte van de knoppen

# Timer-functie, met behulp van youtube video's en ChatGPT
def start_timer():
    global tijd_over, running
    while running:
        time.sleep(1)
        if tijd_over > 0:
            tijd_over -= 1
            app.queueFunction(app.setLabel, "timerLabel", f"Tijd: {tijd_over}s")
        else:
            app.queueFunction(app.setLabel, "feedbackLabel", "Te laat! ⏳")            
            time.sleep(1) #zorgt voor een seconde vertraging, met behulp van ChatGPT
            app.queueFunction(app.stop) #zorgt ervoor dat de app stopt met queuefunction (met behulp van ChatGPT want alleen app.stop deed niks)
            running = False # zorgt ervoor dat de timer thread stopt
            break #zorgt ervoor dat de lus stopt zodat de app goed kan sluiten, met behulpt van ChatGPT (eerst crashte het gehele programma als het zichzelf sloot)

def start_vragenGameMakenPo():
    global app
    # GUI formaat en kleur
    app = gui("WorldTrivia", "1000x500")
    app.setBg("white")

    # Dit start de vragen
    toon_vraag()

    # Timer starten in aparte thread met behulp van een Youtube video
    timer_thread = threading.Thread(target=start_timer)
    timer_thread.daemon = True
    timer_thread.start()

    

    

    # Start de GUI
    app.go()
    running = False  # Stopt de timer als de GUI wordt gesloten

if __name__ == "__main__": # zorgd ervoor dat deze gui niet gelijk start wanneer het opgeroepen wordt in de homescreen gui, met behulp van chat gpt.
    start_vragenGameMakenPo()
    
