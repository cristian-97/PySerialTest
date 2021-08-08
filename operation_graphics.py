import os

import pygame
import rfid_class
import time
class Graphics:

    def __init__(self):

        # initialize the pygame module and audio module

        pygame.init()
        pygame.mixer.init()
        self.clock=pygame.time.Clock()

        # load and set the logo
        logo = pygame.image.load("images/logo50x50.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Tiro a segno")
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        #self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # init image e background
        self.background = pygame.image.load("images/background1024x768.jpg")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.back_rect = self.background.get_rect()
        self.screen.blit(self.background, (0, 0))
        self.start_button = pygame.image.load("images/press-start.png")
        self.stop_button = pygame.image.load("images/press-stop.png")
        self.new_game_button = pygame.image.load("images/new_game.png")
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = self.back_rect.center
        self.stop_button_rect = self.stop_button.get_rect()
        self.stop_button_rect.center = self.back_rect.center
        self.new_game_button_rect= self.new_game_button.get_rect()
        self.new_game_button_rect.bottomright=self.back_rect.bottomright
        self.img_choose_player = pygame.image.load("images/choose_player.png")
        self.img_choose_player_rect = self.img_choose_player.get_rect()
        self.img_choose_player_rect.center = self.back_rect.center
        self.number_1 = pygame.image.load("images/number-1.png")
        self.number_1R = self.number_1.get_rect()
        self.number_1R.topleft = self.back_rect.topleft
        self.number_2 = pygame.image.load("images/number-2.png")
        self.number_2R = self.number_2.get_rect()
        self.number_2R.topright = self.back_rect.topright
        self.number_3 = pygame.image.load("images/number-3.png")
        self.number_3R = self.number_3.get_rect()
        self.number_3R.bottomleft = self.back_rect.bottomleft
        self.number_4 = pygame.image.load("images/number-4.png")
        self.number_4R = self.number_4.get_rect()
        self.number_4R.bottomright = self.back_rect.bottomright
        self.skip = pygame.image.load("images/skip.png")
        self.skipR = self.skip.get_rect()
        self.skipR.bottomright = self.back_rect.bottomright
        self.no_avatar=pygame.image.load('images/no_avatar.png')
        self.no_avatarR=self.no_avatar.get_rect()
        self.score_players_pos=[]



        # init sound
        self.sound_stop = pygame.mixer.Sound("Effects/stop.wav")
        self.sound_start = pygame.mixer.Sound("Effects/start.flac")
        self.sound_shot = pygame.mixer.Sound("Effects/shot.wav")
        self.ends_1sec = pygame.mixer.Sound("Effects/ends_1sec.wav")
        self.ends_2sec = pygame.mixer.Sound("Effects/ends_2sec.wav")
        self.ends_3sec = pygame.mixer.Sound("Effects/ends_3sec.wav")
        self.ends_4sec = pygame.mixer.Sound("Effects/ends_4sec.wav")
        self.ends_5sec = pygame.mixer.Sound("Effects/ends_5sec.wav")
        self.end_game = pygame.mixer.Sound("Effects/explosion.wav")
        background_music = "Effects/background.wav"
        pygame.mixer.music.load(background_music)

        # basic colors
        self.player_color=[(255, 255, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255,127,0),(255,0,255),(0,255,255),(0, 0, 0)]
        ##                    bianco           rosso       verde        blu        giallo      arancione    fucsia      azzurro     nero
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        # init font
        self.font_score = pygame.font.SysFont('bell', 70)
        self.txt_score = self.font_score.render('Score:', True, self.white)
        self.txt_scoreR = self.txt_score.get_rect()
        self.rect_txt_score = self.txt_score.get_rect()
        self.rect_txt_score.topleft = (10, 10)
        self.font_clock = pygame.font.SysFont("Trebuchet MS", 35)
        minute_font = self.font_clock.render("{0:02}".format(0), 1, self.black)  # zero-pad minutes to 2 digits
        second_font = self.font_clock.render(":{0:02}".format(0), 1, self.black)  # zero-pad hours to 2 digits
        self.minute_fontR = minute_font.get_rect()
        self.second_fontR = second_font.get_rect()
        self.second_fontR.topleft = self.back_rect.midtop
        self.minute_fontR.topright = self.second_fontR.topleft
        self.title_ranking_font = pygame.font.SysFont('bell', 80)
        self.title_ranking = self.title_ranking_font.render("Ranking:", True, self.white)
        self.title_ranking_rect = self.title_ranking.get_rect()
        self.ranking_score_font= pygame.font.SysFont('bell', 50)
        self.rfid_player_font=self.title_ranking_font
        self.menu_font = pygame.font.SysFont('comicsansms', 50)
        self.txt_choose_player = self.menu_font.render("SCEGLIERE NUMERO GIOCATORI",True, self.red)
        self.txt_choose_playerR=self.txt_choose_player.get_rect()
        self.txt_choose_playerR.center = self.back_rect.center
        self.players_txt = self.ranking_score_font.render("player n", True, self.white)
        self.players_txtR = self.players_txt.get_rect()
        self.players_txtR.topleft=self.back_rect.topleft
        self.txt_insert_rfid= self.menu_font.render("INSERIRE TESSERA GIOCATORE COLORE",True, self.white)
        self.txt_insert_rfidR=self.txt_insert_rfid.get_rect()
        self.txt_insert_rfidR.center=self.back_rect.center

        #create RFID varaible
        self.rfid_number=''
        self.rfid=None
        # update the screen to make the changes visible
        pygame.display.flip()

    def __show_rfid(self,rfid):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.skip, self.skipR)
        avatar = pygame.image.load(rfid.get_avatar())
        avatar_rect=avatar.get_rect()
        rfid_player = self.rfid_player_font.render(rfid.character.nickname, True, self.white)
        rfid_playerR=rfid_player.get_rect()
        rfid_playerR.midtop= tuple(map(sum, zip(self.back_rect.midtop, (0, 150))))
        avatar_rect.midright=tuple(map(sum, zip(rfid_playerR.midleft, (-20, 0))))
        self.screen.blit(rfid_player, rfid_playerR)
        self.screen.blit(avatar, avatar_rect)
        pygame.display.flip()

    def __set_dim_avatar(self,w,h):
        if w > self.no_avatarR.size[0]:
            w = self.no_avatarR.size[0]
        if h > self.no_avatarR.size[1]:
            h = self.no_avatarR.size[1]
        return w, h

    def choose_players(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.txt_choose_player,self.txt_choose_playerR)
        self.screen.blit(self.number_1, self.number_1R)
        self.screen.blit(self.number_2, self.number_2R)
        '''self.screen.blit(self.number_3, self.number_3R)
        self.screen.blit(self.number_4, self.number_4R)'''
        pygame.display.flip()
        self.score_players_pos=[None]
        while True:
            for event in pygame.event.get():
                # only do something if the event if of type QUIT
                if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                    raise (KeyboardInterrupt)
                # check for keypress and check if it was Esc
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise (KeyboardInterrupt)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.pos
                    if self.number_1R.collidepoint(click):
                        return 1
                    elif self.number_2R.collidepoint(click):
                        return 2
                    '''elif self.number_3R.collidepoint(click):
                        return 3
                    elif self.number_4R.collidepoint(click):
                        return 4'''
            self.clock.tick(30)

    def insert_rfid(self,player):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.skip,self.skipR)
        waiting_read=True
        if player==0:
            self.players_txtR.topleft=self.back_rect.topleft
            self.txt_insert_rfid=self.menu_font.render("INSERIRE TESSERA GIOCATORE ROSSO",True, self.red)
            self.screen.blit(self.txt_insert_rfid,self.txt_insert_rfidR)
            self.players_txt = self.ranking_score_font.render("player1", True, self.red)
            self.screen.blit(self.players_txt, self.players_txtR)

        if player==1:
            self.txt_insert_rfid = self.menu_font.render("INSERIRE TESSERA GIOCATORE VERDE", True, self.green)
            self.screen.blit(self.txt_insert_rfid, self.txt_insert_rfidR)
            self.players_txt = self.ranking_score_font.render("player2", True, self.green)
            self.screen.blit(self.players_txt, self.players_txtR)

        '''if player == 2:
            self.txt_insert_rfid = self.menu_font.render("INSERIRE TESSERA GIOCATORE BLU", True, self.blue)
            self.screen.blit(self.txt_insert_rfid, self.txt_insert_rfidR)
            self.players_txt = self.ranking_score_font.render("player3", True, self.blue)
            self.screen.blit(self.players_txt, self.players_txtR)

        if player == 3:
            self.txt_insert_rfid = self.menu_font.render("INSERIRE TESSERA GIOCATORE GIALLO", True, self.yellow)
            self.screen.blit(self.txt_insert_rfid, self.txt_insert_rfidR)
            self.players_txt = self.ranking_score_font.render("player4", True, self.yellow)
            self.screen.blit(self.players_txt, self.players_txtR)'''
        pygame.display.flip()
        rfid_read_control=True
        read_rfid_time = 0
        self.rfid=None
        while waiting_read:
            for event in pygame.event.get():
                # only do something if the event if of type QUIT
                if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                    raise (KeyboardInterrupt)
                # check for keypress and check if it was Esc
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise (KeyboardInterrupt)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.pos
                    if self.skipR.collidepoint(click):
                        waiting_read=False

                if event.type == pygame.KEYDOWN and event.key in range(48, 58):
                    if rfid_read_control:
                        read_rfid_time = time.time()
                        rfid_read_control = False
                    self.rfid_number += str(chr(event.key))
                    if len(self.rfid_number) == 10:
                        print(self.rfid_number)
                        self.rfid = rfid_class.RfID(self.rfid_number)
                        self.rfid.get_character()
                        if self.rfid.character is not None:
                            self.__show_rfid(self.rfid)
                        self.rfid_number = ''
                        rfid_read_control = True
                    elif not rfid_read_control and time.time() - read_rfid_time > 2:
                        self.rfid_number = ''
                        rfid_read_control = True
            self.clock.tick(30)

    def show_players(self,players_list):
        self.screen.blit(self.background, (0, 0))
        pos=self.back_rect.topleft
        for player in players_list:
            if player is not None:
                self.no_avatarR.topleft=pos
                if player.get_name() is None:
                    self.players_txt = self.ranking_score_font.render(player.username, True, player.color)
                    self.players_txtR.midleft = self.no_avatarR.midright
                    self.screen.blit(self.players_txt, self.players_txtR)
                    self.screen.blit(self.no_avatar, self.no_avatarR)
                else:
                    if os.path.isfile(player.get_avatar_path()):
                        img_player=pygame.image.load(player.get_avatar_path())
                    else:
                        img_player = pygame.image.load(player.get_avatar())
                    img_playerR = img_player.get_rect()
                    img_width, img_height = img_playerR.size
                    try:
                        img_player = pygame.transform.smoothscale(img_player,(self.__set_dim_avatar(img_width, img_height)))
                    except:
                        img_player = pygame.transform.scale(img_player,(self.__set_dim_avatar(img_width, img_height)))
                    img_playerR = self.no_avatarR
                    self.screen.blit(img_player, img_playerR)

                    player_txt = self.ranking_score_font.render(player.get_name(), True, player.color)
                    player_txtR = player_txt.get_rect()
                    player_txtR.midleft = img_playerR.midright
                    self.screen.blit(player_txt, player_txtR)
                txt_score = self.font_score.render('score:', True, player.color)
                self.txt_scoreR.topleft = self.no_avatarR.bottomleft
                score = self.font_score.render(str(player.score), True, player.color)
                scoreR = score.get_rect()
                scoreR.topleft = self.txt_scoreR.topright
                self.score_players_pos.append(scoreR.topleft)
                self.screen.blit(txt_score, self.txt_scoreR)
                self.screen.blit(score, scoreR)
                pos=self.txt_scoreR.bottomleft
        pygame.display.flip()

    def show_start(self):
        self.start_button_rect.center = self.back_rect.center
        self.screen.blit(self.start_button,self.start_button_rect)
        pygame.display.update(self.start_button_rect)

    def control_start(self):
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                raise (KeyboardInterrupt)
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise (KeyboardInterrupt)


            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if self.start_button_rect.collidepoint(click):
                    self.screen.blit(self.background, (0, 0))
                    self.screen.blit(self.stop_button, self.stop_button_rect)
                    pygame.display.update([self.start_button_rect,self.stop_button_rect])
                    print("lets go!")
                    self.sound_start.play()
                    return False
        return True

    def control_stop(self):
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                raise (KeyboardInterrupt)
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise (KeyboardInterrupt)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if self.stop_button_rect.collidepoint(click):
                    print("stop!")
                    self.sound_stop.play()
                    return False
        return True

    def play_shot(self):
        self.sound_shot.play()

    def show_score(self, player):
        if player is not None:
            self.screen.blit(self.background, (0, 0))
            score = self.font_score.render(str(player.score), True, player.color)
            rect_score = score.get_rect()
            rect_score.topleft=self.score_players_pos[player.id]
            self.screen.blit(score, rect_score)
            pygame.display.update(rect_score)

    def show_duration(self, duration):
        minute= duration // 60
        second=duration % 60
        self.screen.blit(self.background, (0, 0))
        second_font = self.font_clock.render(":{0:02}".format(second), 1, self.white)
        minute_font = self.font_clock.render("{0:02}".format(minute), 1, self.white)
        self.screen.blit(minute_font, self.minute_fontR)
        self.screen.blit(second_font, self.second_fontR)
        pygame.display.update([self.minute_fontR, self.second_fontR])

    def play_countdown(self, second):
        if second == 5:
            self.ends_5sec.play()
        elif second == 4:
            self.ends_4sec.play()
        elif second == 3:
            self.ends_3sec.play()
        elif second == 2:
            self.ends_2sec.play()
        elif second == 1:
            self.ends_1sec.play()
        elif second == 0:
            self.end_game.play()

    def start_menu(self, ranking):

        self.screen.blit(self.new_game_button,self.new_game_button_rect)
        self.title_ranking_rect.topright = tuple(map(sum, zip(self.back_rect.midtop, (50, 10))))
        self.screen.blit(self.title_ranking, self.title_ranking_rect)
        point_cell = tuple(map(sum, zip(self.title_ranking_rect.midbottom, (0, 10))))
        pos = 1
        col_pos=1
        for position in ranking:
            if col_pos==8:
                col_pos=1
            txt_position = self.ranking_score_font.render(str(pos) + '-', True, self.player_color[col_pos])
            txt_positionR = txt_position.get_rect()
            txt_positionR.topright = point_cell
            player_font = self.ranking_score_font.render(position[2], True, self.player_color[col_pos])
            player_fontR = player_font.get_rect()
            score_player_font = self.ranking_score_font.render(position[1], True, self.player_color[col_pos])
            score_player_fontR = score_player_font.get_rect()
            player_fontR.topleft = tuple(map(sum, zip(txt_positionR.topright, (5, 0))))
            score_player_fontR.topleft = tuple(map(sum, zip(player_fontR.topright, (10, 0))))
            point_cell = tuple(map(sum, zip(txt_positionR.bottomright, (0, 5))))
            self.screen.blit(txt_position, txt_positionR)
            self.screen.blit(score_player_font, score_player_fontR)
            self.screen.blit(player_font, player_fontR)
            pos+=1
            col_pos+=1

        pygame.display.flip()

    def control_new_game(self):
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                raise (KeyboardInterrupt)
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise (KeyboardInterrupt)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if self.new_game_button_rect.collidepoint(click):
                    self.sound_start.play()
                    return False
        return True


    def start_music_background(self):
        pygame.mixer.music.play()

    def stop_music_background(self):
        pygame.mixer.music.stop()