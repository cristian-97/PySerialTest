import operation_csv
import serial_target
import serial_phaser
import operation_graphics
import my_mqtt
import time
import json
import modality_function
import player_class
import traceback
import usb_path_finder


class MyModality:
    def __init__(self):
        self.operation_csv = operation_csv.OpCVS()
        target_port=usb_path_finder.find_dev_by_path(1.3)
        phaser1_port=usb_path_finder.find_dev_by_path(1.1)
        try:
            phaser2_port=usb_path_finder.find_dev_by_path(1.2)
        except Exception as e:
            print(e)
        self.serial_target = serial_target.OpSerial(target_port)
        self.serial_target.reset_all()
        self.phasers= {}
        try:
            self.phasers[1]=serial_phaser.OpSerial(phaser1_port,1)
            self.phasers[2]=serial_phaser.OpSerial(phaser2_port, 2)
        except Exception as e:
            print(e)
        self.ranking = self.operation_csv.ranking
        self.dev_reg = {}
        self.n_player = 0
        self.mqtt_msg = {}
        client_id = "Xraid-poligono"
        broker = "192.168.1.109"
        self.client = my_mqtt.myClient(client_id, broker)
        self.client.loop_start()
        self.dev_reg = self.serial_target.dev_init()
        self.n_dev = len(self.dev_reg)
        print("sono presenti", self.n_dev, "dispositivi")
        print(self.dev_reg)
        self.serial_target.reset_msg_list()
        self.serial_target.remove_target(list(self.dev_reg.values()))
        self.serial_target.send_msg()
        time.sleep(1)
        self.graphics = operation_graphics.Graphics()
        self.players_list = []

    '''def __config_player_list(self):
        i = 0
        while i < len(self.players_list):
            if self.players_list[i] is None:
                self.players_list.remove(self.players_list[i])
            else:
                i += 1'''

    def choose_modality(self):
        self.serial_target.set_register(list(self.dev_reg.values()), -1, 50 + 128, 0, 0)
        self.serial_target.send_msg()
        self.players_list = []
        self.mqtt_msg = {}
        self.n_player = self.graphics.choose_players()
        print(self.n_player, "giocatori scelti")
        for i in range(0, self.n_player):
            self.mqtt_msg['player%s' % (i + 1)] = {'username': 'player%s' % (i + 1),
                                                   'thumbnail': 'images/RFID_images/no_avatar.png', 'score': '0'}
            self.graphics.insert_rfid(i)
            self.players_list.append(player_class.Player(self.graphics.rfid))
            self.players_list[i].init_player(i + 1)
            if self.players_list[i].get_name() is not None:
                self.mqtt_msg['player%s' % self.players_list[i].id]["username"] = (self.players_list[i].get_name())
                self.mqtt_msg['player%s' % self.players_list[i].id]["thumbnail"] = (self.players_list[i].rfid.character.avatarlinks['thumbnail'])
                self.mqtt_msg['player%s' % self.players_list[i].id]["score"] = (str(self.players_list[i].score))
            else:
                self.players_list[i].username = 'player%s' % (i + 1)

        # self.__config_player_list()
        self.graphics.show_players(self.players_list)

        return self.n_player

    def waiting_start(self):
        in_waiting = True
        self.graphics.show_start()
        while in_waiting:
            in_waiting = self.graphics.control_start()
            self.graphics.clock.tick(30)

        self.serial_target.remove_target(list(self.dev_reg.values()))
        self.serial_target.send_msg()
        for i in range(1,self.n_player+1):
            self.phasers[i].enable_phaser(i, 0, 1, self.players_list[i-1].username)
            time.sleep(0.1)
            while not self.phasers[i].check_init_parameter():
                self.phasers[i].enable_phaser(i, 0, 1, self.players_list[i-1].username)
                time.sleep(0.5)

        self.graphics.start_music_background()

    def mod_player(self):
        running = True
        print(json.dumps(self.mqtt_msg))
        self.client.publish("Xraid-poligono/Players", json.dumps(self.mqtt_msg), qos=1, retain=True)
        target = []
        time_match = 200
        duration = time_match
        elapsed = time_match - duration
        mod_fun = modality_function.ModFunction(time_match, self.n_dev, self.n_player)
        for player in self.players_list:
            self.graphics.show_score(player)
        self.graphics.show_duration(duration)
        time_choose_target = mod_fun.time_target(elapsed)
        time_buffer_target = time.time()
        n_target = mod_fun.number_of_target(elapsed)
        time_clock = time.time()
        target_to_choose = []
        powerful_target = []
        time_send=time.time()
        time_music_background= time.time()
        self.client.publish("Xraid-poligono/match_status", "START", qos=1, retain=True)
        while running:
            running = self.graphics.control_stop()
            if time.time() - time_music_background > 180:
                self.graphics.stop_music_background()
                time.sleep(0.01)
                self.graphics.start_music_background()
                time_music_background=time.time()
            if time.time() - time_clock >= 1:
                duration -= 1
                elapsed = time_match - duration
                # time_choose_target = mod_fun.time_target(elapsed)
                time_choose_target = 1
                n_target = mod_fun.number_of_target(elapsed)
                if duration < 6:
                    self.graphics.play_countdown(duration)
                    if duration == 0:
                        running = False

                self.client.publish("Xraid-poligono/clock", duration)
                self.graphics.show_duration(duration)
                time_clock = time.time()

            if time.time() - time_buffer_target > time_choose_target:
                target_to_choose[:] = list(self.dev_reg.values())
                self.serial_target.reset_msg_list()
                self.serial_target.remove_target(target)
                target = []
                powerful_target = []
                for player in self.players_list:
                    target_tmp = mod_fun.choose_target(n_target, target_to_choose)
                    self.serial_target.set_register(target_tmp, player.id, 0, player.id, 0)
                    target += target_tmp
                    print("player %s: " % player.id, target_tmp)
                try:
                    powerful_target = mod_fun.choose_target(1, target_to_choose)
                    self.serial_target.set_register(powerful_target, 5, 0, 5, 0)
                    target += powerful_target
                    print("player 5: ", powerful_target)
                except ValueError:
                    pass
                time_buffer_target = time.time()
            id_shot, phaser = self.serial_target.read_shot()
            if id_shot in self.dev_reg:
                self.graphics.play_shot()
                for player in self.players_list:
                    if player.id == phaser:
                        if self.dev_reg[id_shot] in powerful_target:
                            player.score += 300
                        else:
                            player.score += 100
                        self.mqtt_msg["player%s" % player.id]["score"] = str(player.score)
                        self.graphics.show_score(player)
                        self.phasers[player.id].set_score(player.score)
                        print("punteggio giocatore %s : %s" % (player.id, player.score))
                self.client.publish("Xraid-poligono/Players", json.dumps(self.mqtt_msg), qos=1, retain=True)
                self.serial_target.set_register([self.dev_reg[id_shot]], 0, 100, 0, 0)
                print("target", id_shot, "colpito")
            if time.time() - time_send > 0.2:
                self.serial_target.send_msg()
                self.serial_target.reset_msg_list()
                time_send = time.time()
            self.graphics.clock.tick(30)
        self.graphics.stop_music_background()
        # self.serial_target.set_register(self.dev_reg.values(), -1, 50 + 128, 0, 0)
        self.serial_target.set_register(list(self.dev_reg.values()), -1, 50 + 128, 0, 0)
        self.serial_target.send_msg()
        for phaser in self.phasers.values():
            phaser.disable_phaser()
        self.client.publish("Xraid-poligono/match_status", "END", qos=1, retain=True)
        self.client.publish("Xraid-poligono/Players", json.dumps(self.mqtt_msg), qos=1, retain=True)

        self.graphics.show_players(self.players_list)
        try:
            for player in self.players_list:
                if player.get_name() is not None:
                    self.operation_csv.put_new_score(player.get_rfid_number(), player.score)
                    self.ranking.append([player.get_rfid_number(), str(player.score), player.get_name(), player.avatar_path])
            self.ranking.sort(key=lambda v: int(v[1]), reverse=True)
            self.ranking[:] = self.ranking[:10]
            dict_ranking = {}
            i = 1
            for rank in self.ranking:
                dict_ranking['rank%s' % i] = {
                    'username': rank[-2],
                    'thumbnail': rank[-1],
                    'score': rank[-3]
                }
                i += 1
            self.client.publish("Xraid-poligono/ranking", json.dumps(dict_ranking), qos=1, retain=True)
            self.graphics.start_menu(self.ranking)
        except:
            print(traceback.format_exc())
        in_waiting = True
        while in_waiting:
            in_waiting = self.graphics.control_new_game()
            self.graphics.clock.tick(30)
