import logging
import socket
import time
import paho.mqtt.client as mqtt




class myClient(mqtt.Client):

    @staticmethod
    def __on_connect(client, userdata, flags, rc):
        print(mqtt.connack_string(rc) + " Flags: " + str(flags))
        print("__on_connect")
        client.publish("Xraid-poligono/instances/" + client.client_id, True, qos=1, retain=True)

    @staticmethod
    def __on_disconnect(client, userdata, rc):
        print("__on_disconnect")
        print(rc)

    def __init__(self, client_id, host, port=1883):
        super(myClient, self).__init__(client_id, clean_session=True)
        self.control_status=0
        self.on_connect = myClient.__on_connect
        self.on_disconnect = myClient.__on_disconnect
        self.client_id = client_id

        self.__reconnect_time = time.time()

        self.will_set("Xraid-poligono/instances/" + self.client_id, False, qos=1, retain=True)
        try:
            self.connect(host, port=port, keepalive=60)
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.publish("Xraid-poligono/instances/" + self.client_id, False, qos=1, retain=True)
        print("disconnesso")
        return super(myClient, self).disconnect()



"""
Descrizone Topics MQTT:

xraid.server/instances/         istanze del server connesse
xraid.server/mqtt_targets/      lista di target connessi

xraid.server/server_load        Carico del server
xraid.server/shot_info          Informazione colpi in tempo reale
xraid.server/match_status       
xraid.server/match_info

xraid.server/media_player/playlist
xraid.server/media_player/theme
"""
