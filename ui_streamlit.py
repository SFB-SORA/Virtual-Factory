import paho.mqtt.client as mqtt
import streamlit as st
import time
import threading



# MQTT broker details
broker_address = "localhost"
port = 1883
topics = [("SFB/Endschalter/B1", 0), ("SFB/Endschalter/B2", 0), ("SFB/Endschalter/B3", 0),("SFB/Endschalter/B4", 0), ("SFB/Endschalter/B5", 0), 
          ("SFB/Endschalter/B6", 0), ("SFB/Endschalter/B7", 0), ("SFB/Endschalter/B8", 0),("SFB/Endschalter/B9", 0), ("SFB/Endschalter/B10", 0), 
          ("SFB/Endschalter/B11", 0), ("SFB/Endschalter/B12", 0), ("SFB/Endschalter/B13", 0),("SFB/Endschalter/B14", 0), ("SFB/Endschalter/B15", 0), 
          ("SFB/Endschalter/B16", 0), ("SFB/Endschalter/B17", 0), ("SFB/Endschalter/B18", 0),("SFB/Endschalter/B19", 0), ("SFB/Endschalter/B20", 0), 
          ("SFB/Endschalter/B21", 0), ("SFB/Endschalter/B22", 0), ("SFB/Sensor/F1", 0), ("Step_Strart1", 0),("Step_Strart",0),("Step_0",0),("Step_1",0),("Step_2",0),("Step_3",0),("Step_4",0),("Step_5",0),
        ("SFB/Aktor/P0", 0), ("SFB/Aktor/P1", 0), ("SFB/Aktor/P2", 0), ("SFB/Aktor/P3", 0),("SFB/Aktor/P4", 0), ("SFB/Aktor/P5", 0), ("SFB/Aktor/P6", 0),
        ("SFB/Aktor/Q3",0), ("SFB/Aktor/Q4",0), ("SFB/Aktor/E1",0), ("SFB/Aktor/G1",0)                                                                                                                                                                                         
    
]  # Liste der Topics


umwandlung_Zahl_in_Tempartur = { 0:200, 50:240,100:280,150:320,200:360,250:400,300:440,350:480,400:520,450:560,500:600,550:640,
                                   600:680,650:720,700:760,750:800,800:840,850:880,900:920,950:960,1000:1000,}

umwandlung_Tempartur_in_Zahl = { 
20:0,21:12.5,22:25,23:37.5,24:50,25:62.5,26:75,27:87.5,28:100,29:112.5,30:125,31:137.5,32:150,33:162.5,34:175,
35:187.5,36:200,37:212.5,38:225,39:237.5,40:250,41:262.5,42:275,43:287.5,44:300,45:312.5,46:325,47:337.5,48:350,49:362.5,50:375,
51:387.5,52:400,53:412.5,54:425,55:437.5,56:450,57:462.5,58:475,59:487.5,60:500,61:512.5,62:525,63:537.5,64:550,65:562.5,66:575,
67:587.5,68:600,69:612.5,70:625,71:637.5,72:650,73:662.5,74:675,75:687.5,76:700,77:712.5,78:725,79:737.5,80:750,81:762.5,82:775,
83:787.5,84:800,85:812.5,86:825,87:837.5,88:850,89:862.5,90:875,91:887.5,92:900,93:912.5,94:925,95:937.5,96:950,97:962.5,98:975,
99:987.5,100:1000,}


# Variable zum Speichern der letzten Nachricht für jedes Topic
sensor_data = {}


# Callback function for when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    
    # Speichern der Nachricht in einem Dictionary
    sensor_data[topic] = payload
    print(f"Received message on topic {topic}: {payload}")
    
    if topic == "SFB/Endschalter/B1" or topic == "SFB/Endschalter/B2":
        Endschalter_B1_B2(client, userdata, message)

    elif topic == "SFB/Endschalter/B3" or topic == "SFB/Endschalter/B4":
        Endschalter_B3_B4(client, userdata, message)

    elif topic == "SFB/Endschalter/B5":
        Endschalter_B5(client, userdata, message)

    elif topic == "SFB/Endschalter/B6"or topic == "SFB/Endschalter/B7":
        Endschalter_B6_B7(client, userdata, message)  

    elif topic == "SFB/Endschalter/B9" or topic == "SFB/Endschalter/B13":
        Endschalter_B9_B13(client, userdata, message)

    elif topic == "SFB/Endschalter/B10"or topic == "SFB/Endschalter/B11":
        Endschalter_B10_B11(client, userdata, message)
        
    elif topic == "SFB/Endschalter/B14"or topic == "SFB/Endschalter/B17":
        Endschalter_B14_B17(client, userdata, message)
    
    elif topic == "SFB/Endschalter/B20":
        Endschalter_B20(client, userdata, message)

    elif topic == "SFB/Endschalter/B21":    
        Endschalter_B21(client, userdata, message)

    elif topic == "SFB/Endschalter/B22":
        Endschalter_B22(client, userdata, message)

    elif topic == "SFB/Aktor/P3"or "SFB/Aktor/P4":
        Aktor_P3_P4(client, userdata, message)



# Platzhalter für die sich aktualisierende Nachricht
Aktualisierung_B1_B2= st.empty()
Aktualisierung_B3_B4= st.empty() 
Aktualisierung_B6_B7= st.empty()
Aktualisierung_B10_B11= st.empty()
Aktualisierung_B9_B13= st.empty() 
Aktualisierung_B4= st.empty()
Aktualisierung_B5= st.empty()
Aktualisierung_B14_B17= st.empty()
Aktualisierung_B20= st.empty()
Aktualisierung_B21= st.empty()
Aktualisierung_B22= st.empty()
Aktualisierung_P3_P4= st.empty()
anzeige_status = st.empty()

        
def Aktor_P3_P4(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()

    if topic == "SFB/Aktor/P3" and payload == "1":
        Aktualisierung_P3_P4.write("Lastwagen Einfahrt") 

    elif topic == "SFB/Aktor/P4" and payload == "1":
        Aktualisierung_P3_P4.write("Lastwagen Ausfahrt") 

def Endschalter_B1_B2(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if topic == "SFB/Endschalter/B1" and payload == "0":
        Aktualisierung_B1_B2.write("Status Hebebühne Oben")  
    elif topic == "SFB/Endschalter/B2" and payload == "0":
        Aktualisierung_B1_B2.write("Status Hebebühne Unten")  
    else:
        Aktualisierung_B1_B2.write("Status Hebebühne Fährt") 

def Endschalter_B3_B4(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if topic == "SFB/Endschalter/B3" and payload == "1":
        Aktualisierung_B3_B4.write("Status Tor Oben")  
    elif topic == "SFB/Endschalter/B4" and payload == "1":
        Aktualisierung_B3_B4.write("Status Tor Unten")  
    else:
        Aktualisierung_B3_B4.write("Status Tor Fährt") 
        
def Endschalter_B4(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if int(payload) == 1:
        Aktualisierung_B4.write("Tor Unten")
    else:Aktualisierung_B4.write("Tor -")

def Endschalter_B5(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if int(payload) == 1:
        Aktualisierung_B5.write("Lichtschranke Ein")
    else:Aktualisierung_B5.write("Lichtschranke Aus")

def Endschalter_B6_B7(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
 
    if topic == "SFB/Endschalter/B6" and payload == "1":
        Aktualisierung_B6_B7.write("EG Tür Geschlossen")  
    elif topic == "SFB/Endschalter/B7" and payload == "1":
        Aktualisierung_B6_B7.write("EG Tür Offen") 
    else:
        Aktualisierung_B6_B7.write("EG Tür Fährt") 
    
def Endschalter_B9_B13(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if topic == "SFB/Endschalter/B9" and payload == "1":
        Aktualisierung_B9_B13.write("Lift ist Unten")  
    elif topic == "SFB/Endschalter/B13" and payload == "1":
        Aktualisierung_B9_B13.write("Lift ist Oben") 
    else:
        Aktualisierung_B9_B13.write("Lift Fährt") 
  
def Endschalter_B10_B11(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if topic == "SFB/Endschalter/B10" and payload == "1":
        Aktualisierung_B10_B11.write("1.OG Tür Geschlossen")  
    elif topic == "SFB/Endschalter/B11" and payload == "1":
        Aktualisierung_B10_B11.write("1.OG Tür Offen") 
    else:
        Aktualisierung_B10_B11.write("1.OG Tür Fährt")
  
def Endschalter_B14_B17(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
   
    if topic == "SFB/Endschalter/B14" and payload == "1":
        Aktualisierung_B14_B17.write("Tauchpresse Bereit")  
    elif topic == "SFB/Endschalter/B17" and payload == "1":
        Aktualisierung_B14_B17.write("Tauchpresse ist im Wasser") 

    else:Aktualisierung_B14_B17.write("Tauchpresse fährt")

def Endschalter_B20(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    wert = int(float(payload))  # Falls `payload` eine Dezimalzahl ist, wird sie umgewandelt
    Umwanlung = round(wert / 10)    
    Aktualisierung_B20.write(f"Ist Temperatur {Umwanlung}C")
 
def Endschalter_B21(client, userdata, message):
    topic, payload = message.topic, message.payload.decode().strip()  # Entferne unnötige Leerzeichen
    wert = int(float(payload))  # Falls `payload` eine Dezimalzahl ist, wird sie umgewandelt
    Umwanlung = round(wert / 10)    
    Aktualisierung_B21.write(f"Helligkeit {Umwanlung}%")
   
def Endschalter_B22(client, userdata, message):
    topic, payload = message.topic, message.payload.decode()
    if int(payload) == 1:
        Aktualisierung_B22.write("Bewegungsmelder Ein")
    else:Aktualisierung_B22.write("Bewegungsmelder Aus")




# MQTT-Client erstellen und verbinden
client = mqtt.Client()
client.connect(broker_address, port)



# Sidebar für Raumauswahl
with st.sidebar:
    st.title("Raumsteuerung")
    st.subheader("Wählen Sie einen Standort aus:")
    section = st.radio('', ('SGK+Anzeige', 'Garagen-Tor', 'Hebebühne', 'Flaschenlift', 'Presse', 'Tauchpresse','Beleuchtung Innen/Aussen','Ventilation','Lastwagen','Automation',))
 
# SGK+Anzeige Steuerung ----------------------------------------------------------------------------------------------------
# Initialisiere den Zustand beim ersten Start

    if "anlage_aktiv" not in st.session_state:
        st.session_state.update({
            "anlage_aktiv": False,
            "not_aus": False,
            "quittiert": False,
            "sperrung": True,
            "Aktor_E2": False,
            "soll_temperatur":50
        })

if section == 'SGK+Anzeige':
    st.header("SGK+Anzeige")

    # Start-Button (immer bedienbar)
    if st.button("Start (S0)"):
        st.session_state.anlage_aktiv = not st.session_state.anlage_aktiv  # zu 1 oder 0 senden
        st.session_state.sperrung = not st.session_state.anlage_aktiv  # Lampe wird gesperrt, wenn die Anlage ausgeschaltet wird
        client.publish("SFB/Solltemperatur", str(375))
        client.publish("SFB/Aktor/G1", "400")

    
    # Status für Start-Anlage
    status_Start = "Anlage Eingeschaltet" if st.session_state.anlage_aktiv else "Anlage Ausgeschaltet"
    st.write(status_Start)
        
    # Not-Aus-Button (immer bedienbar)
    if st.button("Not-Aus (S13)"):
        st.session_state.update({"not_aus": True, "quittiert": False, "sperrung": True})
        client.publish("SFB/Aktor/Q1", "0")
        client.publish("SFB/Aktor/Q2", "0")
        client.publish("SFB/Aktor/Q3", "0")
        client.publish("SFB/Aktor/Q4", "0")
        client.publish("SFB/Aktor/Q5", "0")
        client.publish("SFB/Aktor/Q6", "0")
        client.publish("SFB/Aktor/Q7", "0")
        client.publish("SFB/Aktor/Q8", "0")
        client.publish("SFB/Aktor/Q9", "0")
        client.publish("SFB/Aktor/Q10", "0")
        client.publish("SFB/Aktor/Q11", "0")
        client.publish("SFB/Solltemperatur", "0")
        client.publish("SFB/Aktor/E2", "1")
        client.publish("SFB/Aktor/E3", "0")
        client.publish("SFB/Aktor/P0", "1")
        client.publish("SFB/Aktor/P1", "0")
        client.publish("SFB/Aktor/P2", "0")
        client.publish("SFB/Aktor/P3", "0")
        client.publish("SFB/Aktor/P4", "0")
        client.publish("SFB/Aktor/P5", "0")
        client.publish("SFB/Aktor/P6", "0")
        client.publish("SFB/Aktor/G1", "0")
        client.publish("SFB/Aktor/M1", "0")
        client.publish("SFB/Aktor/M2", "0")
       

    # Quittieren-Button (immer bedienbar)
    if st.button("Quittieren (S23)") and st.session_state.anlage_aktiv:
        st.session_state.update({"not_aus": False, "quittiert": True, "sperrung": False})
        client.publish("SFB/Aktor/P0", "0")
    # Status Not-Aus (Aktiv/Inaktiv)
    status_Not_Aus = "Not-Aus Aktiv" if st.session_state.not_aus else"" or "Not-Aus Deaktiviert" if st.session_state.quittiert else ""
    st.write(status_Not_Aus)

    # Lampe-Schalter
    def click_E2():
        st.session_state.Aktor_E2 = not st.session_state.Aktor_E2  # Zustand der Lampe umkehren
        client.publish("Anlage/Aktor/E2", "1" if st.session_state.Aktor_E2 else "0")  # MQTT-Befehl

    # Lampe Ein/Aus Button
    if st.button("Lampe Ein/Aus", on_click=click_E2, disabled=st.session_state.sperrung):

        # Aktualisiere den Status der Lampe in einem separaten Publish-Befehl
        client.publish("SFB/Aktor/E2", "1" if st.session_state.Aktor_E2 else "0")
    # Anzeige des aktuellen Status der Lampe

    status_lampe = "EIN" if st.session_state.Aktor_E2 else "AUS"
        # Anzeige des Lampe-Status
    st.write(f"Lampe ist **{status_lampe}**")
    st.write("_________________________________________________________________________")


    # Hebebühne-Tor Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Hebebühne':
    st.header("Lichtschalter Hebebühne")
    
    Aktualisierung_B1_B2= st.empty()

    if st.button("Hebebühne Auf(S1)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q1", "1") 
        
    if st.button("Hebebühne Stop(S21)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q1", "0")  
        client.publish("SFB/Aktor/Q2", "0")  
        
    if st.button("Hebebühne Ab(S2)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q2", "1")  

    st.write("_________________________________________________________________________")


# Garagen-Tor Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Garagen-Tor':
    st.header("Garagen-Tor")
    
    # Status Tor
    
    Aktualisierung_B3_B4 = st.empty()

    # Schlüsselschalter
    st.subheader("Schlüsselschalter(S3)")
    if st.button("Schlüsselschalter Tor Auf", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q3", "1") 
        
    if st.button("Schlüsselschalter Tor Stop", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q3", "0")  
        client.publish("SFB/Aktor/Q4", "0")  
        
    if st.button("Schlüsselschalter Tor Ab", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q4", "1")  

    # Funksender   
    st.subheader("Funksender(S22)") 
    if st.button("Funksender Tor Auf", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q3", "1") 
        
    if st.button("Funksender Tor Stop", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q3", "0")  
        client.publish("SFB/Aktor/Q4", "0")  
        
    if st.button("Funksender Tor Ab", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q4", "1")  

    st.write("_________________________________________________________________________")


# Lift (Flache) Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Flaschenlift':
    st.header("Flaschenlift")

    Aktualisierung_B9_B13= st.empty()  
    Aktualisierung_B10_B11= st.empty()
    Aktualisierung_B6_B7= st.empty()

    st.subheader("1.OG")

    if st.button("1.OG Lift Fahrbefehl Auf(S6)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q90", "1")
        client.publish("SFB/Aktor/Q100", "0")

    if st.button("1.OG Lift Fahrbefehl Ab(S7)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q100", "1")
        client.publish("SFB/Aktor/Q90", "0")
    
    st.subheader("EG")
   
    if st.button("EG Lift Fahrbefehl Auf(S4)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q90", "1")
        client.publish("SFB/Aktor/Q100", "0")

    if st.button("EG Lift Fahrbefehl Ab(S5)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/Q100", "1")
        client.publish("SFB/Aktor/Q90", "0")
    st.write("_________________________________________________________________________")


# Presse-Tor Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Presse':
    st.header("Presse")

    # Schalter für Presse
    schalter1 = st.checkbox("Schalter 1 (S14)",disabled=st.session_state.sperrung)
    schalter2 = st.checkbox("Schalter 2 (S15)",disabled=st.session_state.sperrung)

    if schalter1 and schalter2:
        st.write("Presse aktiviert!")
        client.publish("SFB/Aktor/Q11","1")
    elif not schalter1 or not schalter2:
        st.write("Ein Schalter wurde losgelassen – Presse fährt hoch!")
        client.publish("SFB/Aktor/Q11","0")
    st.write("_________________________________________________________________________")


# Tauchpresse Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Tauchpresse':
    st.header("Tauchpresse")

    if st.button("Tauchbad Ein (S16)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/M1", "1")

    if st.button("Tauchbad Tauchen", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/M2/Ein", "1")
        
    if st.button("Tauchbad Aus (S17)", disabled=st.session_state.sperrung):
        client.publish("SFB/Aktor/M1", "0")
    
    Aktualisierung_B14_B17= st.empty()

    
    st.subheader ("Temperatursteuerung des Tauchbecken")
    soll_temperatur = st.slider("Solltemperatur (in C von 0-100)", 20, 100, 50, 1)

    if st.button("Solltemperatur setzen (S20)", disabled=st.session_state.sperrung):
        Temparatur_wert = umwandlung_Tempartur_in_Zahl[soll_temperatur]
        print(Temparatur_wert)
        client.publish("SFB/Solltemperatur", str(Temparatur_wert))
    
        st.write(f"Solltemperatur auf {soll_temperatur}C gesetzt!")

    Aktualisierung_B20= st.empty()
    
    st.write("_________________________________________________________________________")


# Beleuchtung Innen/Aussen----------------------------------------------------------------------------------------------------
if section == 'Beleuchtung Innen/Aussen':
    st.header("Lichtschalter Beleuchtung Innen")
   
    # Lampe-Schalter
    def click_E2():
        st.session_state.Aktor_E2 = not st.session_state.Aktor_E2  # Zustand der Lampe umkehren
        client.publish("Anlage/Aktor/E2", "1" if st.session_state.Aktor_E2 else "0")  # MQTT-Befehl

    # Lampe Ein/Aus Button
    if st.button("Lampe Ein/Aus(S11)", on_click=click_E2, disabled=st.session_state.sperrung):

        # Aktualisiere den Status der Lampe in einem separaten Publish-Befehl
        client.publish("SFB/Aktor/E2", "1" if st.session_state.Aktor_E2 else "0")
    # Anzeige des aktuellen Status der Lampe

    status_lampe = "EIN" if st.session_state.Aktor_E2 else "AUS"
        # Anzeige des Lampe-Status
    st.write(f"Lampe ist **{status_lampe}**")

    st.header("Lichtschalter Beleuchtung Aussen")

    if st.button("Bewegungsmelder Einschalten (B21)", disabled=st.session_state.sperrung):
        client.publish ("Bewegungsmelder_Aktiv", "1")

    st.write("_________________________________________________________________________")


# Ventilation Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Ventilation':
    st.header("Ventilation")

    # Lüftersteuerung
    st.subheader("Lüfter Steuerung")
    luefter_speed = st.slider("Lüftergeschwindigkeit", 0, 100, 80, 5)

    if st.button("Setze Lüftergeschwindigkeit (G1)", disabled=st.session_state.sperrung):
        Veni_wert = luefter_speed * 10 
        client.publish("SFB/Aktor/G1", str(Veni_wert))
        st.write(f" Neue Drehzahl gesendet: {luefter_speed}/100")

    st.write("_________________________________________________________________________")
     
  
# Lastwagen Ausfahrt Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Lastwagen':
    st.header("Lastwagen")

    Aktualisierung_P3_P4= st.empty()

    Aktualisierung_P6= st.empty()

    st.write("_________________________________________________________________________")

       
# Automation Steuerung ----------------------------------------------------------------------------------------------------
if section == 'Automation':
    st.header("Automation")

    if st.button("Automation Ein", disabled=st.session_state.sperrung):
        client.publish("Automatik_Ein_Aus", "1")
        client.publish("SFB/Aktor/Q4", "1")
        client.publish("SFB/Aktor/Q100", "1")
        client.publish("SFB/Aktor/Q11", "0")   
        client.publish("SFB/Aktor/M1", "0") 
        client.publish("SFB/Solltemperatur", str(375))
        
    if st.button("Automation Aus", disabled=st.session_state.sperrung):
        client.publish("Automatik_Ein_Aus", "0")


# Set the callback function for message handling
client.on_message = on_message

# Alle Topics abonnieren
for topic in topics:
    client.subscribe(topic)

# Start the loop to process received messages
client.loop_forever()
