#          0-BIANCO  1- ROSSO       2- VERDE   3- BLU   4- GIALLO    5- VIOLA   6- ARANCIO   7- AZZURRO    8-FUCSIA   9-SPENTO
colors = [0x10FFFFFF, 0x10FF0000, 0x1000FF00, 0x100000FF, 0x10FFFF00, 0x107F00FF, 0x10FF7F00, 0x1000FFFF, 0x10FF00FF,0x10000000]


class ColorSelector:

    def __init__(self):
        self.color = ['FFFFFF', 'FF0000', '00FF00', '0000FF', 'FFFF00', '7F00FF', 'FF7F00', '00FFFF', 'FF00FF','000000']

    def choose_color(self, color):
        return self.color[color]
