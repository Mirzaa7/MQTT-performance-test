import paho.mqtt.client as mqtt   #Uključena "paho.mqtt" biblioteka
import time     #Uključena "time" biblioteka


class KlasaPoruka: #Kreirana je klasa "KlasaPoruka", koja sadrži sve parametre poruke od interesa
    def __init__(self, Broj_poruka, Ukupna_velicina_poruka, Pocetno_vrijeme, Koncano_vrijeme):
        self.Broj_poruka = Broj_poruka
        self.Ukupna_velicina_poruka = Ukupna_velicina_poruka
        self.Pocetno_vrijeme = Pocetno_vrijeme
        self.Konacno_vrijeme = Koncano_vrijeme

    def PrimljenaPoruka(self, Klijent, KorisnickiPodaci, Poruka):

        if Poruka.payload.decode("utf-8") != "END":
            self.Broj_poruka+=1    #Brojanje primljenih poruka, osim poruke "END"

        if self.Broj_poruka == 1:   #Uzima se pocetno vrijeme, kada stigne prva poruka
           self.Pocetno_vrijeme = time.time()

        if Poruka.payload.decode("utf-8") == "END":
            self.Konacno_vrijeme = time.time()   #Uzima se konacno vrijeme, kada stigne poruka "END"

        print("Primljena poruka: " + " na temu AnalizaMQTT") #Ispise se sadržaj primljene poruke

        if Poruka.payload.decode("utf-8") != "END":     #Sabira se ukupna velicina poruka, osim poruke "END"
            self.Ukupna_velicina_poruka += len(Poruka.payload.decode("utf-8"))


NovaPoruka = KlasaPoruka(0,0,0,0)  #Kreira se nova instanca klase "KlasaPoruka"
Broker = "localhost"    #Potrebno je kreirati varijablu brokera
Klijent = mqtt.Client("Pretplatnik")  # Kao i varijablu klijenta
Klijent.connect(Broker)      #Klijent se poveže sa brokerom



Klijent.loop_start()

Klijent.subscribe("AnalizaMQTT") #Klijent se pretplati na odabranu temu
Klijent.on_message = NovaPoruka.PrimljenaPoruka #Klijent unutar petlje, konstantno prima poruke
time.sleep(12)

Klijent.loop_stop()

Vrijeme_slanja= NovaPoruka.Konacno_vrijeme - NovaPoruka.Pocetno_vrijeme #Kreira se vrijeme slanja poruka


print("\nVrijeme slanja podataka je: " + str(Vrijeme_slanja) + " s")     #Ispis vremena slanja, broja poruka u sekundi,
print("\nBroj poruka u sekundi: " + str(NovaPoruka.Broj_poruka/Vrijeme_slanja) + " msg/s")
print("\nKolicina podataka poslana u jedinici vremena je: "
      + str((NovaPoruka.Ukupna_velicina_poruka )/ (1000.0*Vrijeme_slanja))  #Ispis brzine prenosa podataka
      + " kB/s")