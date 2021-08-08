import os
import requests


class Player:

    def __init__(self, rfid_object=None):
        self.rfid = rfid_object
        self.score = 0
        self.username = ''
        self.avatar_path = ''
        self.color = None
        self.id = None

    def get_name(self):
        if self.rfid is not None:
            if self.rfid.character is not None:
                self.username = self.rfid.character.username
                return self.username
        return None

    def get_rfid_number(self):
        if self.rfid is not None:
            if self.rfid.character is not None:
                return self.rfid.character.rfid
        return None

    def init_player(self, id):
        color = [None, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.color = color[id]
        self.id = id

    def get_avatar_path(self):
        image_url = self.rfid.character.avatarlinks['thumbnail']
        # ora vado a prendere il percorso in cui memorizzerò il file
        image_path = 'images/RFID_images/%s' % os.path.basename(image_url)

        # controllo estensione del file
        imge_filename, image_extension = os.path.splitext(image_path)
        if image_extension.upper() not in ['.PNG', '.GIF', '.JPG', '.JPEG']:
            self.avatar_path = "images/RFID_images/avatar_not_supported.jpg"
            return "images/RFID_images/avatar_not_supported.jpg"
        self.avatar_path = image_path
        return image_path

    def get_avatar(self):
        image_url = self.rfid.character.avatarlinks['thumbnail']
        # ora vado a prendere il percorso in cui memorizzerò il file
        image_path = 'images/RFID_images/%s' % os.path.basename(image_url)

        # controllo estensione del file
        imge_filename, image_extension = os.path.splitext(image_path)
        if image_extension.upper() not in ['.PNG', '.GIF', '.JPG', '.JPEG']:
            self.avatar_path = "images/avatar_not_supported.jpg"
            return "images/avatar_not_supported.jpg"

        if image_url != "" and image_path != "":
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
        self.avatar_path = image_path
        return image_path
