
class Menu:
    def __init__(self,img_start,img_options,loader):
        self.img_start = img_start
        self.img_options = img_options
        self.loader = loader

        self.img_current = self.img_start

        self.enabled = False

    def swap(self):
        self.enabled = not self.enabled

        # Initialize
        if not self.enabled:
            self.goToStart()

    def draw(self):
        if self.enabled:
            self.img_current.draw()

    def goToOptions(self):
        self.img_current = self.img_options

    def goToStart(self):
        self.img_current = self.img_options
