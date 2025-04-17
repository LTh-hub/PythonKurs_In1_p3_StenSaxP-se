# PythonKurs_In1_p3_StenSaxP-se

 Detta är en inlämningsuppgift i kursen "Pythonprogrammering för AI-utveckling"

 Inlämningsuppift 1 / Projekt 3  -  Sten-Sax-Påse

 Skapa en version av spelet sten-sax-påse.

 · Datorn slumpar vilken av sten, sax eller påse den ska välja.
 
 · Spelaren väljer också sten, sax eller påse.
 
 · Datorn och spelaren visar sedan upp sina val samtidigt.
 
 · Reglerna är enligt följande: sten vinner över sax, sax vinner över påse, och påse vinner över sten. Om båda väljer samma alternativ blir det oavgjort.
 
 · Spelaren spelar tills hen vinner eller förlorar mot datorn.
#

# :>>>> py .\ssp.py 

Programmet startas från terminal:>>>> py .\ssp.py 

Programmet består huvudsakligen av två fönstersidor (Widget's) som spelaren styr programmet från. Första widgeten som kommer upp efter programstart ser ut enligt figur 1. Widgeten i figur 1 är uppdelad i två fält, ett övre där programmet startas och ett undre med uppgifter om spelregler och deltagare i spelprogrammets utveckling.

![alt text](image-1st-view.png)
# Figure 1

För att spela:

Skriv in namnet på spelaren, här är redan namnet "Klas"

Via dropdown menyn väljes det antal 'del-game' som skall spelas innan en match har avgjorts, se figur 2. I Sten-Sax-Påse är "Först till 5" default värde.

![alt text](image-2nd-view.png)
# Figure 2

Sten-Sax-Påse startas genom ett tryck på Button "Börja Spela".

