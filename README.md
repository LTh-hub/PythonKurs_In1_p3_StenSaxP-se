<h2>PythonKurs Inlämningsuppgift 1 - projekt 3</h2>
<h1>Sten-Sax-Påse</h1>
<h3>PythonKurs_In1_p3_StenSaxP-se</h3>
<br>
<p>
    <h4>Uppgift</h4>
    <br>Skapa en version av spelet sten-sax-påse.
    <br>· Datorn slumpar vilken av sten, sax eller påse den ska välja.
    <br>· Spelaren väljer också sten, sax eller påse.
    <br>· Datorn och spelaren visar sedan upp sina val samtidigt.
    <br>· Reglerna är enligt följande: sten vinner över sax, sax vinner över påse, och påse vinner över sten. Om båda väljer samma alternativ blir det oavgjort.
    <br>· Spelaren spelar tills hen vinner eller förlorar mot datorn.
</p>


<h2>>> py .\ssp.py  </h2>
Programmet startas från terminal<bold>:>> py .\ssp.py </bold>

Programmet består huvudsakligen av två fönstersidor (Widget's) som spelaren styr programmet från. Första widgeten som kommer upp efter programstart ser ut enligt figur 1. Widgeten i figur 1 är uppdelad i två fält separerade av en horisontell linje, ett övre där programmet startas och ett undre med uppgifter om spelregler och deltagare i spelprogrammets utveckling.

![alt text](image-1st-view.png)
<h3> Figure 1 </h3>

<h2> För att spela: </h2>
Skriv in namnet på spelaren, högst upp i figur 1's inmatningsfält har redan namnet "Klas" skrivits in. Via dropdown menyn väljes det antal 'del-game' som skall spelas innan en match är avgjord, se figur 2. I Sten-Sax-Påse gäller att "Först till 5" är ett default värde.

![alt text](image-2nd-view.png)
<h3> Figure 2 </h3>
Sten-Sax-Påse startas genom ett tryck på Button "Börja Spela", som är strax under dropdown menyn.

