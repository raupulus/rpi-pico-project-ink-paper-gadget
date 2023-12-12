import uasyncio
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec
import random

class Display:
    WS_ICONS = {
        "cloud_moon_rain": "images/weather-station/day-status-cloud_moon_rain.jpg", # Noche nublada lluviosa
        "cloud_moon": "images/weather-station/day-status-cloud_moon.jpg", # Noche Nublada
        "cloud_rain": "images/weather-station/day-status-cloud_rain.jpg", # Nublado con mucha lluvia
        "cloud_showers_heavy": "images/weather-station/day-status-cloud_showers_heavy.jpg", #Nublado con lluvia
        "cloud_sun_rain": "images/weather-station/day-status-cloud_sun_rain.jpg", # Soleado con lluvia
        "cloud": "images/weather-station/day-status-cloud.jpg", # Nublado
        "sun_cloud": "images/weather-station/day-status-sun_cloud.jpg", # Soleado con algo de nubes
        "sun": "images/weather-station/day-status-sun.jpg", # Soleado
        "thunderstorm": "images/weather-station/day-status-thunderstorm.jpg", # Tormentas
        "wind": "images/weather-station/day-status-wind.jpg", # Viento
    }

    ICONS = {
        "youtube": 'images/youtube.jpg',
        "twitch": 'images/twitch.jpg',
        "twitter": 'images/twitter.jpg',
        "bitcoin": 'images/bitcoin.jpg',
        "printer": 'images/printer.jpg',
        "keyboard": 'images/keyboard.jpg',
    }

    def __init__(self, controller, debug=False) -> None:

        self.DEBUG = debug
        self.controller = controller

        self.graphics = PicoGraphics(display = DISPLAY_INKY_PACK)
        self.WIDTH, self.HEIGHT = self.graphics.get_bounds()

        self.jpegdec = jpegdec.JPEG(self.graphics)

        self.graphics.set_font("bitmap8")
        self.graphics.set_update_speed(2)

        self.clear()

        self.graphics.update()

    # a handy function we can call to clear the screen
    # display.set_pen(15) is white and display.set_pen(0) is black
    def clear(self):
        self.graphics.set_pen(15)
        self.graphics.clear()
        self.graphics.set_pen(0)

    def draw_rectangle(self, start_x, start_y, end_x, end_y, color=0):
        "Dibuja un rectángulo"
        self.graphics.set_pen(color)
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

    def set_top_bar_hour(self, time="00:00"):
        """
        Establece la hora en la barra superior.
        """
        self.graphics.set_pen(15)
        self.graphics.text(time, self.WIDTH - 67, 3, scale=2)

    def set_top_bar_temperature(self, status="sun", temperature=22):
        """
        Establece la temperatura en la barra superior.
        """
        self.jpegdec.open_file(self.WS_ICONS.get(status))
        self.jpegdec.decode(5, 4, jpegdec.JPEG_SCALE_FULL, dither=False)

        self.graphics.set_pen(15)
        self.graphics.text(str(temperature) + "C", 26, 3, scale=2)

    def create_top_bar(self, day_status="sun", temperature=22, time="00:00"):
        """
        Crea la barra superior.
        """
        print('ENTRA EN CREATE_TOP_BAR')

        # Background
        self.graphics.set_pen(0)
        self.graphics.rectangle(2,2,self.WIDTH - 4, 16)
        #self.graphics.update()

        # Wifi
        if self.controller.wifiIsConnected():
            self.jpegdec.open_file("images/wifi-on.jpg")
        else:
            self.jpegdec.open_file("images/wifi-off.jpg")

        self.jpegdec.decode(self.WIDTH - 20, 4, jpegdec.JPEG_SCALE_FULL, dither=False)
        #self.graphics.update()

        #self.graphics.set_pen(15)

        # Weather Station, estado del día y temperatura
        self.set_top_bar_temperature(day_status, temperature)

        # Hora
        self.set_top_bar_hour(time)

    def create_home_card(self, position, icon_name, text):
        """
        Crea una tarjeta en el home.
        """

        # Base para el ancho de la tarjeta.
        card_width = int((self.WIDTH/2) - 2)

        # Altura de la tarjeta en píxeles.
        card_height = 19

        positions = { # [width margin, heigth margin, column]
            1: [2, card_height, 1],
            2: [2, (card_height * 2) + 2, 1],
            3: [2, (card_height * 3) + 4, 1],
            4: [2, (card_height * 4) + 6, 1],
            5: [2, (card_height * 5) + 8, 1],
            6: [card_width + 2, card_height, 2],
        }

        text = str(text)

        position = positions.get(int(position))

        if not position:
            return


        # Creo el marco
        self.graphics.set_pen(0)

        # Superior
        self.graphics.line(position[0], position[1], card_width * position[2], position[1])

        # Izquierda
        self.graphics.line(position[0], position[1], position[0], position[1] + card_height)

        # Inferior
        self.graphics.line(position[0], position[1] + card_height, (card_width * position[2]) + 1, position[1] + card_height)

        # Derecha
        self.graphics.line(card_width * position[2], position[1], (card_width * position[2]) + 1, position[1] + card_height)

        self.jpegdec.open_file(self.ICONS.get(icon_name))
        self.jpegdec.decode(position[0] + 2, position[1] + 3, jpegdec.JPEG_SCALE_FULL, dither=True)

        self.graphics.set_pen(0)

        self.graphics.text(text, position[0] + 30, position[1] + 3, scale=2)

    def create_home(self):
        print("Entra en create_home")
        self.create_home_card(1, "youtube", "16.371")
        self.create_home_card(2, "twitch", "1.583")
        self.create_home_card(3, "twitter", "1.399")
        self.create_home_card(4, "bitcoin", "5.82 khs")
        self.create_home_card(5, "printer", "FINSHED")
        self.create_home_card(6, "keyboard", "99.716")

    def status_handler(self):
        self.clear()
        self.graphics.set_pen(15)
        self.graphics.clear()
        self.graphics.set_pen(0)
        self.graphics.text("Network: {}".format(self.controller.SSID), 10, 10, scale=2)
        self.status_text = "Connecting..."

        ip = None

        self.graphics.text("ESTADOOO CONECTADOOOOOO", 10, 30, scale=2)
        self.graphics.text("IP: {}".format(ip), 10, 60, scale=2)
        self.graphics.update()


    def image_from_sprite(self):
        """
        Establece la imagen desde un sprite.

        TOFIX!!!! -> dinamizar y testear el formato de grises (0-15, 16 tonos)
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

    def update(self):
        """
        Actualiza la información de la pantalla
        """
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
