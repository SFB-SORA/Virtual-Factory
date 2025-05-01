import paho.mqtt.client as mqtt
import socket
import threading

# MQTT broker details
broker_address = "localhost"
broker_port = 1883
topics = [ ("SFB/Aktor/Q1", 0),("SFB/Aktor/Q2", 0),("SFB/Aktor/Q3", 0),("SFB/Aktor/Q4", 0),("SFB/Aktor/Q5", 0),("SFB/Aktor/Q6", 0),
          ("SFB/Aktor/Q7", 0),("SFB/Aktor/Q8", 0),("SFB/Aktor/Q9", 0),("SFB/Aktor/Q10", 0),("SFB/Aktor/Q11", 0),("SFB/Aktor/E1", 0),
          ("SFB/Aktor/E2", 0),("SFB/Aktor/E3", 0),("SFB/Aktor/M1", 0),("SFB/Aktor/M2", 0),("SFB/Aktor/P0", 0),("SFB/Aktor/P1", 0),
          ("SFB/Aktor/P2", 0),("SFB/Aktor/P3", 0),("SFB/Aktor/P4", 0),("SFB/Aktor/P5", 0),("SFB/Aktor/P6", 0),("SFB/Aktor/G1", 0),
          ]  

# UDP-Verbindung vorbereiten
UDP_IP = "127.0.0.1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP-Socket erstellen

# Port-Liste 
Topic_Port = {
"SFB/Aktor/Q1":1700,"SFB/Aktor/Q2":1701,"SFB/Aktor/Q3":1702,"SFB/Aktor/Q4":1703,"SFB/Aktor/Q5":1704,"SFB/Aktor/Q6":1705,
"SFB/Aktor/Q7":1706,"SFB/Aktor/Q8":1707,"SFB/Aktor/Q9":1708,"SFB/Aktor/Q10":1709,"SFB/Aktor/Q11":1710,"SFB/Aktor/E1":1711,
"SFB/Aktor/E2":1712,"SFB/Aktor/E3":1713,"SFB/Aktor/M1":1714,"SFB/Aktor/M2":1715,"SFB/Aktor/P0":1716,"SFB/Aktor/P1":1717,
"SFB/Aktor/P2":1718,"SFB/Aktor/P3":1719,"SFB/Aktor/P4":1720,"SFB/Aktor/P5":1721,"SFB/Aktor/P6":1722,"SFB/Aktor/G1":1723,
}



# Port-zu-Topic Mapping
Port_Topic = {
    1600: "SFB/Sensor/S0", 1601: "SFB/Sensor/S1", 1602: "SFB/Sensor/S2", 1603: "SFB/Sensor/S3",
    1604: "SFB/Sensor/S4", 1605: "SFB/Sensor/S5", 1606: "SFB/Sensor/S6", 1607: "SFB/Sensor/S7",
    1608: "SFB/Sensor/S8", 1609: "SFB/Sensor/S9", 1610: "SFB/Sensor/S10", 1611: "SFB/Sensor/S11",
    1612: "SFB/Sensor/S12", 1613: "SFB/Sensor/S13", 1614: "SFB/Sensor/S14", 1615: "SFB/Sensor/S15",
    1616: "SFB/Sensor/S16", 1617: "SFB/Sensor/S17", 1618: "SFB/Sensor/S18", 1619: "SFB/Sensor/S19",
    1620: "SFB/Sensor/S20", 1621: "SFB/Sensor/S21", 1622: "SFB/Sensor/S22", 1623: "SFB/Sensor/S23",
    1624: "SFB/Sensor/S24", 1625: "SFB/Sensor/S25", 1626: "SFB/Sensor/S27", 1627: "SFB/Sensor/S28",
    1630: "SFB/Endschalter/B1", 1631: "SFB/Endschalter/B2", 1632: "SFB/Endschalter/B3", 1633: "SFB/Endschalter/B4",
    1634: "SFB/Endschalter/B5", 1635: "SFB/Endschalter/B6", 1636: "SFB/Endschalter/B7", 1637: "SFB/Endschalter/B8",
    1638: "SFB/Endschalter/B9", 1639: "SFB/Endschalter/B10", 1640: "SFB/Endschalter/B11", 1641: "SFB/Endschalter/B12",
    1642: "SFB/Endschalter/B13", 1643: "SFB/Endschalter/B14", 1644: "SFB/Endschalter/B15", 1645: "SFB/Endschalter/B16",
    1646: "SFB/Endschalter/B17", 1647: "SFB/Endschalter/B18", 1648: "SFB/Endschalter/B19", 1649: "SFB/Endschalter/B20",
    1650: "SFB/Endschalter/B21", 1651: "SFB/Endschalter/B22",1652:"SFB/Sensor/F1",
}


# Callback-Funktion für empfangene MQTT-Nachrichten
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()  # Nachricht in String umwandeln

    # Überprüfen, ob das Topic in port_liste existiertx
    if topic in Topic_Port:
        port = Topic_Port[topic]
        print(f"Empfangene Nachricht von {topic} (Port {port}): {payload}")

        # Nachricht per UDP weiterleiten
        udp_message = str(payload).encode('utf-8')  # 🔹 Fix: Payload korrekt in String umwandeln
        sock.sendto(udp_message, (UDP_IP, port))
    else:
        print(f"Unbekanntes Topic: {topic}")


# Liste der Ports, die UDP-Nachrichten empfangen sollen
ports = list(Port_Topic.keys())


# Callback für MQTT-Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Erfolgreich mit MQTT-Broker verbunden!")
    else:
        print(f"⚠ Fehler bei der MQTT-Verbindung! Rückgabecode: {rc}")

    # Abonniere alle relevanten Topics
    for topic in set(Port_Topic.values()):
        client.subscribe(topic)
        print(f"📡 Abonniert: {topic}")


# Funktion für den Empfang von UDP-Nachrichten auf einem bestimmten Port
def Empfang_socket_Sendet_MQTT(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, port))
    print(f"🎧 UDP-Listener gestartet: Port {port} gebunden.")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()  # Entfernt Leerzeichen/Zeilenumbrüche
            print(f"🔹 Port {port} -> Nachricht empfangen: {msg} von {addr}")

            # MQTT-Nachricht senden
            topic = Port_Topic.get(port)
            if topic:
                client.publish(topic, msg)
                print(f"📤 MQTT gesendet: '{msg}' -> Thema: '{topic}'")
            else:
                print(f"⚠ Kein MQTT-Topic für Port {port} gefunden!")

        except Exception as e:
            print(f"❌ Fehler bei Port {port}: {e}")

# Starte Threads für UDP-Listener
def start_udp_threads():
    for port in ports:
        thread = threading.Thread(target=Empfang_socket_Sendet_MQTT, args=(port,))
        thread.daemon = True  # Beendet sich automatisch mit dem Hauptprogramm
        thread.start()



# MQTT-Client erstellen
client = mqtt.Client()
client.on_message = on_message  # Callback-Funktion registrieren
client.on_connect = on_connect
# Verbindung zum Broker herstellen
client.connect(broker_address, broker_port)

# Topics abonnieren
client.subscribe(topics)

  # Starte UDP-Listener in separaten Threads
start_udp_threads()

# MQTT-Loop starten
client.loop_forever()
