
import modality

my_modality=None
try:
    my_modality=modality.MyModality()
    while True:
        n_player=my_modality.choose_modality()
        my_modality.waiting_start()
        print(n_player)
        my_modality.mod_player()

except KeyboardInterrupt:
    print("Ciao!")
my_modality.client.loop_stop()
my_modality.serial_target.stop()
