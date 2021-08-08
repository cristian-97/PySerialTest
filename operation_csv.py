import csv
import rfid_class
import player_class
import os

class OpCVS:

    def __init__(self):
        self.ranking = []
        try:
            with open('ranking.csv', mode='r') as csv_file:
                self.ranking=[]
                csv_reader = csv.reader(csv_file)
                list_ranking = [l for l in csv_reader if len(l) == 2]
                list_ranking.sort(key=lambda v: int(v[1]), reverse=True)
                list_ranking[:]=list_ranking[:10]
                for rank in list_ranking:
                    rfid=rfid_class.RfID(rank[0])
                    rfid.get_character()
                    player=player_class.Player(rfid)
                    if os.path.isfile(player.get_avatar_path()):
                        avatar_path=player.get_avatar_path()
                    else:
                        avatar_path = player.get_avatar()
                    rank.append(player.get_name())
                    rank.append(avatar_path)
                    self.ranking.append(rank)
        except Exception as e:
            print(e)

    def get_ranking(self):
        with open('ranking.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            list_ranking = [l for l in csv_reader if len(l) == 2]
            list_ranking.sort(key=lambda v: int(v[1]), reverse=True)
            return list_ranking[:10]

    def put_new_score(self, player_rfid, score):
        with open('ranking.csv', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([player_rfid, str(score)])


if __name__=='__main__':
    operation_csv=OpCVS()
    operation_csv.put_new_score('0006467265',200)
    operation_csv.put_new_score('0006467265', 5000)
    operation_csv.put_new_score('0006467265', 800)
    operation_csv.put_new_score('0006467265', 600)