import time
class DisplayOff(object):
    def __init__(self, coordinates, client, options):
        self.fps = options.fps

    def run_once(self):
        time.sleep(1 / self.fps)
