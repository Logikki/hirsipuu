import resources
import json
from os import system,name,remove  
from pathlib import Path  #Tama on tiedoston olemassaolon tarkistusta varten

def cls(): #tama funktio pyyhkii komentokehotteen riippuen kayttojarjestelmasta
    system('cls' if name=='nt' else 'clear') # Jos windows niin cls ja jos unix pohjainen niin clear
arvatutKirjaimet = [] # Luodaan tyhjä lista johon tulee arvatut kirjaimet
#tämä moduuli joko tallentaa tai lataaa muistista kayttajan syöttamat sanat ja eri pelaajat
def Tallenna(tallenna, lataa):
    if tallenna == 1:
        with open('kayttajansanat.json', 'w') as a:
            json.dump(resources.KayttajanSanat, a)  
        with open('pelaajat.json', 'w') as b:
            json.dump(resources.Pelaaja, b)   
    if lataa == 1:
        a = open('kayttajansanat.json', 'r')
        b = open('pelaajat.json', 'r')
        resources.KayttajanSanat = json.load(a)
        resources.Pelaaja = json.load(b)
        a.close()
        b.close()
#Tässä moduulissa selvitetään kuka pelaaja on
#pelaaja muuttuja sitten palautetaan paavalikko() moduuliin
def pelaajaValikko():
    print(resources.Hirsipuu[0])       
    pelaajaInput = input("Oletko uusi vai vanha pelaaja?" + "\n" + "1. Jos vanha" + "\n" + "2. jos uusi" +"\n")
    while pelaajaInput != "1" and pelaajaInput != "2": # Jos käyttäjä syöttää jotain muuta kuin 1 tai 2 niin palautetaan funktio
        return pelaajaValikko()
    if pelaajaInput == "1": # Suoritetetaan jos pelaajalla on jo vanha käyttäjä
        print("Tallennetut kayttajat ovat: ")
        for pelaajat in resources.Pelaaja:
            print(pelaajat, "pisteita: ", resources.Pelaaja[pelaajat]["pisteet"])
        pelaaja = input("Kirjoita pelaajanimesi: ")
        while pelaaja not in resources.Pelaaja:
            pelaaja = input("Kirjoita pelaajanimesi: ")
    if pelaajaInput == "2": # Suoriteteaan jos pelaaja on uusi käyttäjä
        pelaaja = input("Kirjoita pelaajanimesi: ")
        while pelaaja in resources.Pelaaja:
            print("Tuo nimi on jo kaytössa! Valitse toinen nimi.")
            pelaaja = input("Kirjoita pelaajanimesi: ")
        resources.Pelaaja[pelaaja] = {"nimi": pelaaja, "pisteet":0} # Lisätään käyttäjä hajautustauluun. Pisteet ovat alussa 0
    Tallenna(1,1) # Tallennetaan uusi käyttäjä Json tiedostoon 
    cls()
    return pelaaja # Palautetaan päävalikko metodille pelaaja

#Tässä moduulissa kysytään pelaajalta mitä pelitilaa tämä haluaa pelata
#Pelitilan mukaan päätetään sanalista resources.py tiedostosta
#Moduulissa vois myös lisätä tai poistaa sanoja listasta, jossa on pelaajan omia sanoja.
def paavalikko(pelaaja): 
    print("Tervetuloa pelaamaan Hirsipuupelia ", pelaaja, "!")
    PeliTila = input("Haluatko pelata yksinpelia vai yhteispelia?" + " \n" + "pelataksesi yksinpelia kirjoita 1" + "\n" + \
     "pelatakesi yhteispelia kirjoita '2'" +"\n" +"lisaaksesi sanoja yhteispelitilaan kirjoita '3'" + "\n"+ \
         "Poistaaksesi sanoja yhteispelitilasta kirjoita '4'" + "\n")
    cls()
    if PeliTila == "1": #jos pelitila on yksinpeli niin tama suoritetaan
        Sanat = input("Mita sanoja haluat arvata?" + "\n" + "1. Teknologia yhtiöitä" + "\n" "2. Nimia" + "\n")
        if Sanat == "1":
            Sanat = resources.Teknologia
        elif Sanat == "2":
            Sanat = resources.Nimet
    elif PeliTila == "2": # jos pelitila on yhteispeli niin tama suoritetaan 
        if resources.KayttajanSanat == []: # Jos käyttäjä ei ole syöttänyt vielä sanoja yhteispelitilaan ja lista on tyhjä, niin palautetaan päävalikko moduuli
            print("Sinun pitaa ensin lisata sanoja tahan pelitilaan!")
            poistu = input("Kirjoita '0' poistuaksesi")
            while poistu != "0": # kysytään nollaa niin kauan kuin pelaaja syöttää sen
                poistu = input("Kirjoita '0' poistuaksesi")
            cls()
            paavalikko(pelaaja)
        else: # Jos listassa on sanoja asetetaan sanalistaksi käyttäjänsanat
            Sanat = resources.KayttajanSanat  
    elif PeliTila == "3": #jos pelaaja haluaa syöttaa omia sanoja yhteispelitilaan niin tama suoritetaan
        #Kysytään sanaa. Jos kirjoitetaan '0' niin poistutaan takaisin päävalikkoon
        OmaSana = str(input("Kirjoita sana jonka haluat lisata. Jos haluat poistua tasta niin kirjoita luku 0" + "\n"))
        while OmaSana != '0':
            resources.KayttajanSanat.append(OmaSana)
            OmaSana = input("Kirjoita sana jonka haluat lisata. Jos haluat poistua tasta niin kirjoita luku 0" + "\n") 
            cls()
        Tallenna(1,1) #tallennetaan ja ladataan muisti
        cls()
        return paavalikko(pelaaja) 
    else: #Jos pelaaja haluaa poistaa sanoja yhteispelitilasta niin tama suoritetaan
        print("Kaikki kayttajan syöttamat sanat ovat:")
        poistettavaSana = str # määritetään poistettavaSana jotta voidaan tehdä while looppi
        while poistettavaSana != "poistu": # Suoritetaan tätä niin kauan kun käyttäjä syöttää 'poistu' 
            #numeroidaan sanat, jotta käyttäjä voi syöttää sanan numeron jonka haluaa poistaa.
            for numero, sana in enumerate(resources.KayttajanSanat): 
                print("'",numero,"'", sana)
            poistettavaSana = input("Jos haluat poistua paavalikkoon kirjoita 'poistu'" + "\n" + "Kirjoita sanan numero minka haluat poistaa: ")
            if poistettavaSana != "poistu":
                resources.KayttajanSanat.pop(int(poistettavaSana)) #Poistetetaan käyttäjän haluama sana listasta
            cls()
            Tallenna(1,1)
        paavalikko(pelaaja)
    cls()
    return luodaanPeli(Sanat,pelaaja) #Palautetaan luodaanPeli metodi jossa on sanalista sekä pelaaja

#Moduuli joka arpoo arvattavan sanan sille annetusta sanalistauksesta
#Myös asetetaan pisteet täysiin, sekä generoidaan pelilauta
def luodaanPeli(Sanat, pelaaja): 
    from random import randrange
    pisteita = 10 # Pisteitä on alussa 10 ja niitä poistuu aina kun arvataan väärin
    ArvattavaSana = Sanat[int(randrange(len(Sanat)))].lower() #Arvotaan sana
    pelilauta = ["-" for x in range(len(ArvattavaSana))] #pelilauta on lista 
    return arvataanSana(ArvattavaSana, pelilauta, pelaaja, pisteita)

#Tässä moduulissa kysytään mitä sanaa tai kirjainta pelaaja haluaa arvata
#Arvattu sana tai kirjain viedään onkoKirjainSanassa() moduulille, joka tarkistaa onko kirjain tai sana oikein
def arvataanSana(ArvattavaSana, pelilauta, pelaaja, pisteita): 
    #Sitten kun tämä if lause ei toteudu niin peli loppuu
    if onkoPeliLoppu(pelilauta, ArvattavaSana,pelaaja) == False and pisteita != 0:
        print('Jos haluat poistua tallentamalla kirjoita "poistu"','|','Sana on', len(ArvattavaSana), 'merkkia pitka', 'ja sinulla on arvauksia jaljella', str(pisteita), resources.Hirsipuu[pisteita], "".join(arvatutKirjaimet), "\n", "".join(pelilauta)) 
        peliVuoro = str(input('Arvaa sana tai kirjain :  ')) # Kysytään kirjainta tai sanaa
        # Jos pelaaja haluaa poistua tallentamalla pelin niin tallennetaan pelin tila hajautustauluun ja tallennetaan tiedostoon
        if peliVuoro == "poistu": 
            Save = {"0":ArvattavaSana, "1":pelilauta, "2":pelaaja, "3":pisteita}
            with open('pelitallennus.json', 'w') as f:
                json.dump(Save,f)
            quit()
        cls()
        if peliVuoro in arvatutKirjaimet: # Jos kirjainta on jo arvattu niin palautetaan moduuli
            print("OLET JO ARVANNUT TUOTA KIRJAINTA")
            return arvataanSana(ArvattavaSana, pelilauta,pelaaja,pisteita)
        arvatutKirjaimet.append(peliVuoro+",") #lisätään arvaus arvattujen listaan
        onkoKirjainSanassa(ArvattavaSana, peliVuoro, pelilauta,pelaaja, pisteita)    
    print("Oikea sana oli", ArvattavaSana)
    peliloppu(pelaaja, pisteita)

#Tässä selvitetaan onko arvattava sana tai kirjain oikein
#Miinuspiste asetetaan ykköseksi. Jos arvaus kuitenkin menee oikein, niin miinuspiste asetetaan nollaksi eikä pisteitä miinusteta.
#Piste vähennetään moduulin lopussa
def onkoKirjainSanassa(ArvattavaSana, peliVuoro, pelilauta,pelaaja, pisteita):  
    miinuspiste = 1
    if len(peliVuoro) > 1: #Jos kayttaja arvaa koko sanaa niin tama suoritetaan
        if peliVuoro == ArvattavaSana: #tarkistetaan onko sana oikea
            pelilauta = ArvattavaSana #paljastetaan kaikki sanan kirjaimet
            miinuspiste = 0
    else: # Jos kayttaja arvaa normaalisti pelkkaa kirjainta niin tama suoritetetaan.
        for numero, kirjain in enumerate(ArvattavaSana):
            if peliVuoro  ==  kirjain:
                pelilauta[numero] = kirjain 
                miinuspiste = 0
    pisteita -= miinuspiste #Jos arvaus menee vaarin niin miinustetaan yksi piste
    return arvataanSana(ArvattavaSana,pelilauta,pelaaja, pisteita)

def onkoPeliLoppu(pelilauta, ArvattavaSana,pelaaja): # Tarkistetaan onko "-" merkkejä enää pelilaudalla. Jos on niin peli ei ole vielä loppunut
    if "-" not in pelilauta:
        return True
    else: 
        return False

# Kun peli on loppu niin tämä suoritetaan
#Näytetään saadut pisteet ja tallennetaan ne muistiin
def peliloppu(pelaaja, pisteita): 
    global arvatutKirjaimet
    resources.Pelaaja[pelaaja]["pisteet"] += pisteita
    Tallenna(1,0)
    if pisteita == 0:
        print("Aina ei voi voittaa. Et saanut yhtakaan pistetta.", "Sinulla on pisteita yhteensa:", resources.Pelaaja[pelaaja]["pisteet"])
    else:
        print("Onneksi olkoon kerasit pisteita: " + str(pisteita) + "!", "Sinulla on pisteita nyt yhteensa:", resources.Pelaaja[pelaaja]["pisteet"])
    jatko = int(input(("Kirjoita '0' niin paaset takaisin paavalikkoon")))
    if jatko == 0: # Kun pelaaja haluaa palata takaisin päävalikkoon
        arvatutKirjaimet = [] #nollataan arvatut kirjaimet
        cls()
        return paavalikko(pelaaja)

tallennus = Path("kayttajansanat.json")  #Tassa tarkastetaan onko tallennustiedostoa olemassa ( Jos kaynnistetaan ekaa kertaa niin ei ole)
if tallennus.is_file():   
    Tallenna(0,1)
#tämä tiedosto on luotu jos peli jäi kesken
#Jos tiedosto löytyy niin ladataan se ja poistetaan
pelitallennus = Path("pelitallennus.json")
if pelitallennus.is_file(): # Jos pelitallennus on olemassa, niin ladataan hajautustaulusta pelin tila ja palautetaan se "arvataanSana" metodille
    f = open("pelitallennus.json", "r")
    Save = json.load(f)
    remove("pelitallennus.json") # Poistetaan tallennus
    arvataanSana(Save["0"],Save["1"],Save["2"],Save["3"])
#aloitetaan peli
paavalikko(pelaajaValikko()) 
