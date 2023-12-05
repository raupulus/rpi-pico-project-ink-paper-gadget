import uasyncio
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec
import random


class Display:
    def __init__(self, controller) -> None:

        self.controller = controller

        self.graphics = PicoGraphics(display = DISPLAY_INKY_PACK)
        self.WIDTH, self.HEIGHT = self.graphics.get_bounds()

        self.jpegdec = jpegdec.JPEG(self.graphics)

        self.graphics.set_font("bitmap8")
        self.graphics.set_update_speed(3)
        self.graphics.set_pen(0)
        self.graphics.update()

        self.clear()

    # a handy function we can call to clear the screen
    # display.set_pen(15) is white and display.set_pen(0) is black
    def clear(self):
        self.graphics.set_pen(15)
        self.graphics.clear()
        self.graphics.set_pen(0)

    def draw_rectangle(self, start_x, start_y, end_x, end_y):
        self.graphics.set_pen(0)
        self.graphics.rectangle(start_x,start_y,end_x,end_y)

    def create_frame(self):
        """
        Crea el marco inicial rodeando la pantalla.
        """
        self.graphics.set_pen(0)

        self.graphics.line(0,0,self.WIDTH - 1,0)
        self.graphics.line(0,0,0,self.HEIGHT - 1)
        self.graphics.line(self.WIDTH - 1,0,self.WIDTH -1,self.HEIGHT - 1)
        self.graphics.line(0,self.HEIGHT - 1,self.WIDTH -1,self.HEIGHT - 1)

        self.update()

    def create_top_bar(self):
        print('ENTRA EN CREATE_TOP_BAR')

        # Background
        self.graphics.set_pen(0)
        self.graphics.rectangle(2,2,self.WIDTH - 4, 16)
        self.graphics.update()

        # Wifi
        if self.controller.wifiIsConnected():
            self.jpegdec.open_file("images/wifi-on.jpg")
        else:
            self.jpegdec.open_file("images/wifi-off.jpg")

        self.jpegdec.decode(self.WIDTH - 20, 5, jpegdec.JPEG_SCALE_FULL, dither=False)

        self.graphics.set_pen(15)

        # Hora
        self.graphics.text("16:41", self.WIDTH - 67, 3, scale=2)

    def create_home(self):

        pass
        #self.jpegdec.open_file("images/wifi-white.jpg")
        #self.jpegdec.decode(self.WIDTH - 20, 6, jpegdec.JPEG_SCALE_FULL, dither=True)

        """
        icon_scale = 2
        color_transparent = 15

        self.graphics.load_spritesheet("spritesheet_128x128.rgb332")
        self.graphics.update()
        self.graphics.set_pen(15)

        self.graphics.sprite(0, 0, 4, 3, icon_scale, color_transparent)
        self.graphics.sprite(0, 0, 4, 3, icon_scale)
        self.graphics.sprite(1, 0, 4, 3, icon_scale, color_transparent)
        self.graphics.sprite(2, 0, 4, 3, icon_scale, color_transparent)
        self.graphics.sprite(3, 0, 4, 3, icon_scale, color_transparent)
        self.graphics.sprite(3, 0, 4, 3)
        self.graphics.sprite(0, 0, 50, 60, icon_scale, color_transparent)

        self.graphics.set_pen(0)
        """


    def status_handler(self):
        self.clear()
        self.graphics.set_update_speed(3)
        self.graphics.set_pen(15)
        self.graphics.clear()
        self.graphics.set_pen(0)
        self.graphics.text("Network: {}".format(self.controller.SSID), 10, 10, scale=2)
        self.status_text = "Connecting..."

        ip = None

        self.graphics.text("ESTADOOO CONECTADOOOOOO", 10, 30, scale=2)
        self.graphics.text("IP: {}".format(ip), 10, 60, scale=2)
        self.graphics.update()




    def update(self):
        self.graphics.update()

        """
        # Stream the image data from the socket onto disk in 1024 byte chunks
        # if you're doing something else RAM intensive you might want to use this!
        data = bytearray(1024)
        with open(FILENAME, "wb") as f:
            while True:
                if socket.readinto(data) == 0:
                    break
                f.write(data)
        socket.close()
        """

        """
        jpeg = jpegdec.JPEG(graphics)
        jpeg.open_RAM(data)
        jpeg.decode(0, 0)

        self.graphics.set_pen(15)
        self.graphics.rectangle(0, HEIGHT - 14, WIDTH, 14)

        self.graphics.set_pen(0)
        self.graphics.text(url, 5, HEIGHT - 9, scale=1)

        self.graphics.set_update_speed(1)
        self.graphics.update()
        """

        pass
