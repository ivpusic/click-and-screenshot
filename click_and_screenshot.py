import wx
from pymouse import PyMouse
from threading import Thread, Event


class ScreenShot(Thread):

    # CONFIGURATION
    SCALE_RATIO_X = 1.4
    SCALE_RATIO_Y = 2
    MAX_SCREENSHOT_COUNT = 5
    # DELAY IN SECONDS
    DELAY_BETWEEN_SCREENSHOTS = 2.0

    slide_counter = 0

    def __init__(self, event):
        Thread.__init__(self)

        # set wx for screenshot
        self.screen = wx.ScreenDC()
        self.size = self.screen.GetSize()
        self.bmp = wx.EmptyBitmap(self.size[0], self.size[1])

        # set mouse click settings
        self.stopped = event
        self.mouse = PyMouse()
        self.width, self.height = self.mouse.screen_size()
        self.set_coordinates()

    def set_coordinates(self):
        self.x = self.width / self.SCALE_RATIO_X
        self.y = self.height / self.SCALE_RATIO_Y

    def perform_click(self):
        self.mouse.click(self.x, self.y)

    def take_screenshot(self):
        mem = wx.MemoryDC(self.bmp)
        mem.Blit(0, 0, self.size[0], self.size[1], self.screen, 0, 0)
        del mem
        self.bmp.SaveFile('screenshot{0}.png'.format(self.slide_counter), wx.BITMAP_TYPE_PNG)

    def run(self):
        while not self.stopped.wait(self.DELAY_BETWEEN_SCREENSHOTS):
            self.slide_counter += 1
            self.perform_click()
            self.take_screenshot()

            if self.slide_counter > self.MAX_SCREENSHOT_COUNT:
                self.stopped.set()


if __name__ == '__main__':

    app = wx.App(False)
    stopped = Event()
    ss = ScreenShot(stopped)
    app.MainLoop()
    ss.start()
