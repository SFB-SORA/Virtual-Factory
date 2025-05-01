import paho.mqtt.client as mqtt
import time
import threading

    # MQTT Broker-Daten
broker_address = "localhost"    
port = 1883 


topics = [
    ("SFB/Endschalter/B1", 0), ("SFB/Endschalter/B2", 0), ("SFB/Endschalter/B3", 0),
    ("SFB/Endschalter/B4", 0), ("SFB/Endschalter/B5", 0), ("SFB/Endschalter/B6", 0),
    ("SFB/Endschalter/B7", 0), ("SFB/Endschalter/B8", 0), ("SFB/Endschalter/B9", 0),
    ("SFB/Endschalter/B10", 0), ("SFB/Endschalter/B11", 0), ("SFB/Endschalter/B12", 0),
    ("SFB/Endschalter/B13", 0), ("SFB/Endschalter/B14", 0), ("SFB/Endschalter/B15", 0),
    ("SFB/Endschalter/B16", 0), ("SFB/Endschalter/B17", 0), ("SFB/Endschalter/B18", 0),
    ("SFB/Endschalter/B19", 0), ("SFB/Endschalter/B20", 0), ("SFB/Endschalter/B21", 0),
    ("SFB/Endschalter/B22", 0), ("SFB/Sensor/F1", 0),
    ("SFB/Aktor/Q1", 0), ("SFB/Aktor/Q2", 0), ("SFB/Aktor/Q3", 0), ("SFB/Aktor/Q4", 0),
    ("SFB/Aktor/Q5", 0), ("SFB/Aktor/Q6", 0), ("SFB/Aktor/Q7", 0), ("SFB/Aktor/Q8", 0),
    ("SFB/Aktor/Q9", 0), ("SFB/Aktor/Q10", 0), ("SFB/Aktor/Q11", 0), ("SFB/Aktor/E1", 0),
    ("SFB/Aktor/E2", 0), ("SFB/Aktor/E3", 0), ("SFB/Aktor/M1", 0), ("SFB/Aktor/M2", 0),("SFB/Aktor/M2/Ein",0),("SFB/Solltemperatur",0),
    ("SFB/Aktor/P0", 0), ("SFB/Aktor/P1", 0), ("SFB/Aktor/P2", 0), ("SFB/Aktor/P3", 0),("SFB/Aktor/Q90", 0),
    ("SFB/Aktor/P4", 0), ("SFB/Aktor/P5", 0), ("SFB/Aktor/P6", 0), ("SFB/Aktor/G1", 0),("SFB/Aktor/Q100", 0),
    ("Anlage/Start",0),("Anlage/Stop",0),("Anlage/Quittieren",0),("SFB/Sensor/S10",0),("SFB/Sensor/S9",0),
    ("Step_Strart1", 0),("Step_Strart",0),("Step_0",0),("Step_1",0),("Step_2",0),("Step_3",0),("Step_4",0),("Step_5",0),("Automatik_Ein_Aus", 0),
    ("Step_6",0),("Step_7",0),("Step_8",0),("Step_9",0),("Step_10",0),("Step_11",0),("Step_12",0),("Step_13",0),("Step_14",0),("Step_15",0),("Step_16",0),
    ("Bewegungsmelder_Aktiv", 0)
]


umwandlung_Tempartur_in_Zahl = { 240:50,250:62.5,260:75,270:87.5,280:100,290:112.5,300:125,31:137.5,32:150,33:162.5,34:175,
35:187.5,36:200,37:212.5,38:225,39:237.5,40:250,41:262.5,42:275,43:287.5,44:300,45:312.5,46:325,47:337.5,48:350,49:362.5,50:375,
51:387.5,52:400,53:412.5,54:425,55:437.5,56:450,57:462.5,58:475,59:487.5,60:500,61:512.5,62:525,63:537.5,64:550,65:562.5,66:575,
67:587.5,68:600,69:612.5,70:625,71:637.5,72:650,73:662.5,74:675,75:687.5,76:700,77:712.5,78:725,79:737.5,80:750,81:762.5,82:775,
83:787.5,84:800,85:812.5,86:825,87:837.5,88:850,89:862.5,90:875,91:887.5,92:900,93:912.5,94:925,95:937.5,96:950,97:962.5,98:975,
99:987.5,100:1000,}

umwandlung_Sol_in_Ist = { 
    0:200,12.5:210,25:220, 37.5:230, 50:240, 62.5:250, 75:260, 87.5:270, 100:280, 112.5:290, 125:300, 137.5:310, 150:320,
    162.5:330, 175:340, 187.5:350, 200:360, 212.5:370, 225:380, 237.5:390, 250:400, 262.5:410, 275:420, 287.5:430, 300:440, 
    312.5:450, 325:460, 337.5:470, 350:480, 362.5:490, 375:500, 387.5:510, 400:520, 412.5:530, 425:540, 437.5:550, 450:560, 
    462.5:570, 475:580, 487.5:590, 500:600, 512.5:610, 525:620, 537.5:630, 550:640, 562.5:650, 575:660, 587.5:670, 
    600:680, 612.5:690, 625:700, 637.5:710, 650:720, 662.5:730, 675:740, 687.5:750, 700:760, 712.5:770, 725:780, 
    737.5:790, 750:800, 762.5:810, 775:820, 787.5:830, 800:840, 812.5:850, 825:860, 837.5:870, 850:880, 862.5:890, 
    875:900, 887.5:910, 900:920, 912.5:930, 925:940, 937.5:950, 950:960, 962.5:970, 975:980, 987.5:990, 1000:1000 
}




status_B18 = False
status_B19 = False


# Globale Variablen für die Temperaturregelung
solltemperatur = 0
isttemperatur = 20 
integral = 0
letzter_fehler = 0
Bewegungsmelder_Aktiv_Status = False
solwert=20



# Variable zum Speichern der letzten Nachricht jedes Topics
    
sensor_data = {}


def on_message(client, userdata, message):

    topic = message.topic
    payload = message.payload.decode()
    global status_B18, status_B19,solltemperatur, isttemperatur, Bewegungsmelder_Aktiv_Status,solwert

    
    # Speichern der Nachricht in einem Dictionary
    sensor_data[topic] = payload

   
    
    print(f"Received message on topic {topic}: {payload}")


# Hebebühne Steuerung ----------------------------------------------------------------------------------------------------


    if topic == "SFB/Aktor/Q1" and payload == "1":
        client.publish("SFB/Aktor/Q2", "0")

    if topic == "SFB/Aktor/Q2" and payload == "1":
        client.publish("SFB/Aktor/Q1", "0")

    if topic == "SFB/Endschalter/B1":
        client.publish("SFB/Aktor/Q1", "0")

    if topic == "SFB/Endschalter/B2":
        client.publish("SFB/Aktor/Q2", "0")

    if topic == "SFB/Sensor/F1":
        client.publish("SFB/Aktor/Q1", "0")
        client.publish("SFB/Aktor/Q2", "1")


# Garagen-Tor Steuerung ----------------------------------------------------------------------------------------------------

    if topic == "SFB/Aktor/Q3" and payload == "1":
        client.publish("SFB/Aktor/Q4", "0")

    if topic == "SFB/Aktor/Q4" and payload == "1":
            client.publish("SFB/Aktor/Q3", "0")

    if topic == "SFB/Endschalter/B3":
        client.publish("SFB/Aktor/Q3", "0")

    if topic == "SFB/Endschalter/B4":
        client.publish("SFB/Aktor/Q4", "0")


    if topic == "SFB/Endschalter/B5":
        client.publish("SFB/Aktor/Q3", "1")
        client.publish("SFB/Aktor/Q4", "0")

    
# Lift (Flache) Steuerung ----------------------------------------------------------------------------------------------------

#Lift fährt nach unten
    if topic == "SFB/Aktor/Q100" and payload == "1":
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "1")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "1")
        client.publish("Step_1", "1")
      
    if sensor_data.get("SFB/Endschalter/B6") == "1" and sensor_data.get("SFB/Endschalter/B10") == "1" and sensor_data.get("Step_1") == "1":
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "1")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "0")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "0")
        client.publish("SFB/Aktor/P1","0")
        client.publish("SFB/Aktor/P2","1")
        client.publish("Step_1", "0")
        client.publish("Step_2", "1")
        
    if topic == "SFB/Endschalter/B9" and payload == "1" and sensor_data.get("Step_2") == "1":
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "1")
        client.publish("SFB/Aktor/Q8", "0")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "0")
        client.publish("SFB/Aktor/P1","0")
        client.publish("SFB/Aktor/P2","0")
        client.publish("Step_2", "0")

    if topic == "SFB/Endschalter/B12" and payload == "0":
        client.publish("SFB/Aktor/Q9", "1")
        client.publish("SFB/Aktor/Q10", "0")


#Lift  fährt nahr Oben
    if topic == "SFB/Aktor/Q90" and payload == "1":
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "1")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "1")
        client.publish("Step_4", "1")
       
    if sensor_data.get("SFB/Endschalter/B6") == "1" and sensor_data.get("SFB/Endschalter/B10") == "1" and sensor_data.get("Step_4") == "1":
        client.publish("SFB/Aktor/Q5", "1")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "0")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "0")
        client.publish("SFB/Aktor/P1","1")
        client.publish("SFB/Aktor/P2","0")
        client.publish("Step_4", "0")
        client.publish("Step_5", "1")

    if topic == "SFB/Endschalter/B13" and payload == "1" and sensor_data.get("Step_5") == "1":
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "0")
        client.publish("SFB/Aktor/Q9", "1")
        client.publish("SFB/Aktor/Q10", "0")
        client.publish("SFB/Aktor/P1","0")
        client.publish("SFB/Aktor/P2","0")
        client.publish("Step_5", "0")
    
    if topic == "SFB/Endschalter/B8" and payload == "0":
        client.publish("SFB/Aktor/Q7", "1")
        client.publish("SFB/Aktor/Q8", "0")



# Ausserbeleuchtung Steuerung ----------------------------------------------------------------------------------------------------

    if topic==("Bewegungsmelder_Aktiv") and payload == "1":
        Bewegungsmelder_Aktiv_Status = True  


    if topic == "Bewegungsmelder_Aktiv" and payload == "1" and int(sensor_data.get("SFB/Endschalter/B21", "1000")) < 750:
        client.publish("SFB/Aktor/E3", "1")  # Aktor einschalten
        print("Bewegungsmelder aktiviert")

        # Starte einen separaten Thread für den Timer
        threading.Thread(target=bewegungsmelder_timer, daemon=True).start()
        
# Tauchpresse Steuerung ----------------------------------------------------------------------------------------------------


    if topic == "SFB/Solltemperatur":
        solltemperatur = float(payload)
        print(f"Solltemperatur empfangen: {solltemperatur}")
        berechne_stellwert()  # Sobald eine neue Isttemperatur kommt, berechnen wir den Stellwert

    if topic == "SFB/Endschalter/B20":
        isttemperatur = float(payload)
        print(f"Isttemperatur empfangen: {isttemperatur}")
        berechne_stellwert()  # Sobald eine neue Isttemperatur kommt, berechnen wir den Stellwert

        
    if topic =="SFB/Aktor/M2/Ein" and payload == "1"and int(sensor_data.get("SFB/Endschalter/B20", "0")) == solwert:
        client.publish("SFB/Aktor/M2", "1")
    
    if topic =="SFB/Endschalter/B15" and payload == "1"and int(sensor_data.get("SFB/Endschalter/B20", "0")) == solwert:
        client.publish("SFB/Aktor/M2", "1")
        
    if topic == "SFB/Endschalter/B17" and payload == "1":
        client.publish("SFB/Aktor/M2", "0")

 
# Lastwagen Ausfahrt Steuerung ----------------------------------------------------------------------------------------------------


    if topic == "SFB/Endschalter/B18" and payload == "0":
        status_B18 = True  # B18 wurde betätigt

    if topic == "SFB/Endschalter/B19" and payload == "0":
        if status_B18:  # Prüfen, ob B18 bereits aktiviert wurde
            status_B19 = True  # B19 wurde betätigt, nachdem B18 aktiv war
            time.sleep(1)
            client.publish("SFB/Aktor/P4", "0")  # Aktion auslösen
            client.publish("SFB/Aktor/P3", "1")  # Aktion auslösen
            client.publish("SFB/Aktor/P6", "0")  # Aktion auslösen
            
            
    if topic == "SFB/Endschalter/B19" and payload == "0":
        status_B19 = True  # B18 wurde betätigt

    if topic == "SFB/Endschalter/B18" and payload == "0":
        if status_B19:  # Prüfen, ob B18 bereits aktiviert wurde
            status_B18 = True  # B19 wurde betätigt, nachdem B18 aktiv war
            time.sleep(1)
            client.publish("SFB/Aktor/P3", "0")  # Aktion auslösen
            client.publish("SFB/Aktor/P4", "1")  # Aktion auslösen
            client.publish("SFB/Aktor/P6", "1")  # Aktion auslösen
        


# Automation Steuerung ----------------------------------------------------------------------------------------------------
   
   
# Tor geht auf
    if topic == "SFB/Aktor/P3" and payload == "1" and sensor_data.get("Automatik_Ein_Aus") == "1":
        client.publish("SFB/Aktor/Q3", "1")
        client.publish("SFB/Aktor/E2", "1")  
        client.publish("Step_7", "1")

# Flasche lift geht nahr oben
    if topic==("SFB/Endschalter/B3") and payload== "1"and sensor_data.get("Step_7") == "1":
        client.publish("SFB/Aktor/Q90", "1")
        client.publish("Step_7", "0")
        client.publish("Step_8", "1")

#Presse wird gestartet    
    if topic==("SFB/Endschalter/B11") and payload== "1"and sensor_data.get("Step_8") == "1":
        client.publish("SFB/Aktor/Q11", "1")
        client.publish("Step_8", "0")
        client.publish("Step_9", "1")
    
# Tauchpresse wird gestarte 
    if topic==("Step_9") and payload== "1":
        time.sleep(3)
        client.publish("SFB/Aktor/Q11", "0")
        client.publish("SFB/Aktor/M1", "1")
        client.publish("Step_9", "0")
        client.publish("Step_10", "1")

# Tauchpresse wird getaucht
    if topic==("SFB/Endschalter/B15") and payload== "1"and sensor_data.get("Step_10") == "1":
        client.publish("SFB/Aktor/M2/Ein")
        client.publish("Step_10", "0")
        client.publish("Step_11", "1")

# Tauchpresse wird eingezogen
    if topic==("SFB/Endschalter/B16") and payload== "1"and sensor_data.get("Step_11") == "1":
        time.sleep(2)
        client.publish("SFB/Aktor/M1", "0")
        client.publish("Step_11", "0")
        client.publish("Step_12", "1")


# flasche lift geht nahr unten 
    if topic==("SFB/Endschalter/B14") and payload== "1"and sensor_data.get("Step_12") == "1":
        client.publish("SFB/Aktor/Q100", "1")
        client.publish("Step_12", "0")
        client.publish("Step_13", "1")

# Hebebühne geht nahr Oben
    if topic==("SFB/Endschalter/B7") and payload== "1"and sensor_data.get("Step_13") == "1":
        client.publish("SFB/Aktor/Q1", "1")
        client.publish("SFB/Aktor/Q2", "0")
        client.publish("Step_13", "0")
        client.publish("Step_14", "1")
# Hebebühne geht nahr Unten
    if topic==("SFB/Endschalter/B1") and payload== "0"and sensor_data.get("Step_14") == "1":
        client.publish("SFB/Aktor/Q2", "1")
        client.publish("SFB/Aktor/Q1", "0")
        client.publish("Step_14", "0")
        client.publish("Step_15", "1")

# Tor geht nahr unten
    if topic==("SFB/Endschalter/B2") and payload== "0"and sensor_data.get("Step_15") == "1":
        client.publish("SFB/Aktor/Q4", "1")
        client.publish("SFB/Aktor/E2", "0")
        client.publish("Step_15", "0")
        client.publish("Automatik_Ein_Aus", "0")




# Funktionen ----------------------------------------------------------------------------------------------------
   



def bewegungsmelder_timer():
    global Bewegungsmelder_Aktiv_Status
    time.sleep(10)  # 10 Sekunden warten
    client.publish("SFB/Aktor/E3", "0")  # Bewegungsmelder ausschalten
    client.publish("Bewegungsmelder_Aktiv", "0")  # Falls dieses Topic korrekt ist
    Bewegungsmelder_Aktiv_Status = False  # Status zurücksetzen
    print("Bewegungsmelder deaktiviert")
  

def berechne_stellwert():
    global solltemperatur, isttemperatur,solwert
        # Berechnung des Sollwertes basierend auf der Umwandlungstabelle
    solwert = umwandlung_Sol_in_Ist[solltemperatur]

    if solltemperatur is None or isttemperatur is None:
        return  # Keine Berechnung möglich, wenn ein Wert fehlt

    # Stellwert-Entscheidung basierend auf der Differenz
    if solwert > int(isttemperatur) + 150:
        stellwert = 1000
        print("heizen")
    elif int(isttemperatur) > solwert + 150:
        stellwert = 0
        print("kühlen")
    else:
        stellwert = int(solltemperatur)  

    print(f"Neuer Stellwert: {stellwert}")
    client.publish("SFB/Aktor/E1", str(stellwert)) 


# MQTT-Client erstellen und verbinden
client = mqtt.Client()
client.connect(broker_address, port)

# Callback-Funktion für die Nachrichtenverarbeitung festlegen
client.on_message = on_message

# Alle Topics abonnieren
for topic in topics:
    client.subscribe(topic)

# Starte die MQTT-Schleife zur Verarbeitung empfangener Nachrichten
client.loop_forever()
