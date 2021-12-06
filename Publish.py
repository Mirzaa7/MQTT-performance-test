import paho.mqtt.client as mqtt  #Uključena "paho.mqtt" biblioteka
import time     #Uključena "time" biblioteka

def KreirajPoruku(Duzina_poruke,Prazan):
        for i in range(Duzina_poruke):
                Prazan += "A"               #Funkcija za kreiranje
        return Prazan                       #payload-a željene veličine


Broker = "localhost"            #Potrebno je kreirati varijablu brokera
Klijent = mqtt.Client("Pošiljaoc") # Kao i varijablu klijenta
Klijent.connect(Broker)     #Klijent se poveže sa brokerom


for i in range(20):             #Kreirana poruka se šalje željeni broj puta
    Teret = KreirajPoruku(500000, "")
    Klijent.publish("AnalizaMQTT", Teret)   #Slanje tereta, na odabranu temu, se vrši u ovoj liniji koda
    print("Poslana poruka " + " na temu AnalizaMQTT")
    time.sleep(0.1)       #U ovoj liniji koda se varira brzina slanja poruka

Klijent.publish("AnalizaMQTT", "END")       #Za signalizaciju da je slanje poruka završeno
print("Poslana poruka " + "END" + " na temu AnalizaMQTT") #Šalje se poruka "END"
