import json
import os
import re
import requests
from collections import namedtuple


class RfID:
    __template = {'username': '',
                  'nickname': '',
                  'rfid': '',
                  'user_email': '',
                  'user_registered': '',
                  'avatarlinks': {'thumbnail': '',
                                  'medium': '',
                                  'large': '',
                                  'full': ''
                                  },
                  'globalranklevel': ''}

    Character = namedtuple('Character', __template.keys())

    error_codes = ['get_user_by_rfid', 'No-Authorised-Rfid', 'No-User-by-Rfid']

    rfid_pattern = r'^\d{10}$'

    def __init__(self, code: str = ''):
        self.code = code
        self.character = None
        self.error = ''

    def get_character(self):
        try:
            print('Try to get player %s character...' % self.__str__())

            api_url = 'https://www.x-raid.net/wp-json/xraid-rest-api/v1'
            r = requests.get(api_url + '/user/%s' % self.__str__())
            print('GET %s - %s' % (str(r.url), str(r.status_code)))

            if r.status_code == 200:
                data = json.loads(r.text)

                if data['code'] == self.error_codes[0]:

                    user = data['data']['user']
                    try:
                        self.character = RfID.Character(**user)
                    except TypeError as e:
                        print('Required Character data:' + str(self.__template))
                        print('User data:' + str(data))
                        raise e

                    print('Character %s username: %s' % (self.__str__(), self.character.username))
                    print(self.character)

                else:
                    self.character = None
                    self.error = data['code']
            #else:
            #    logger.error(r.status_code)

        except requests.RequestException as e:
            print(e)
            self.error = str(e)

        except Exception as e:
            print(e)

    def __eq__(self, c):
        return self.code == c.code

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        if re.match(self.rfid_pattern, self.code):
            return self.code
        else:
            return ''

    def get_avatar(self):

        image_url = self.character.avatarlinks['thumbnail']
        #ora vado a prendere il percorso in cui memorizzerò il file
        image_path = 'images/RFID_images/%s' % os.path.basename(image_url)

        # controllo estensione del file
        imge_filename, image_extension = os.path.splitext(image_path)
        if image_extension.upper() not in ['.PNG', '.GIF', '.JPG', '.JPEG']:
            return "images/avatar_not_supported.jpg"

        if image_url != "" and image_path != "":
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
        return image_path

#rfid = RfID('0002554370')
#rfid.get_character()


