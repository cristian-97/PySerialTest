import random

class ModFunction:
    def __init__(self, duration, n_target,n_player):
        self.time_match = duration
        self.time_change = (self.time_match // n_target) + 10
        self.n_target = 1
        self.n_max_target=n_target//n_player

    def time_target(self, elapsed):
    #divido il tempo di gioco in 6 step al superamento di ogni step i bersagli cambieranno più in fretta
        time_step= self.time_match//6
        if elapsed < time_step:
            return 3
        elif elapsed < time_step*2:
            return 2.5
        elif elapsed < time_step*3:
            return 2
        else:
            return 1

    def number_of_target(self, elapsed):
        if elapsed > self.n_target * self.time_change and self.n_target<self.n_max_target:
            self.n_target += 1
        return self.n_target

    def choose_target(self,n_target,target_buff):
        target=random.sample(target_buff,n_target)
        target.sort()
        for dev in target:
            target_buff.remove(dev)
        return target




