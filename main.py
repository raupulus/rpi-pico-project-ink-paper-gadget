#from machine import Pin, SPI
import _thread, gc
from time import sleep_ms, sleep, time
from Models.Api import Api
from Models.RpiPico import RpiPico
from Models.Display import Display

# Importo variables de entorno
import env

# Habilito recolector de basura
gc.enable()

# Rpi Pico Model
#controller = RpiPico(ssid=env.AP_NAME, password=env.AP_PASS, debug=env.DEBUG)
controller = RpiPico(debug=env.DEBUG)

#network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
#uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

display = Display(controller=controller)

sleep_ms(10)


# Variables para el manejo de bloqueo con el segundo core
thread_lock = _thread.allocate_lock()
thread_lock_acquired = False

#gc.collect()

def thread0():
    """
    Primer hilo para lecturas y envío de datos a las acciones del segundo hilo.
    """

    # Momento de la última vez que se mostró por pantalla.
    last_show_display_at = time()

    display.create_frame()
    #display.create_top_bar()
    display.create_top_bar("sun_cloud", 19, "17:48")
    display.create_home()
    display.update()

    sleep(30)




def thread1(sensors, wifi_status, voltage):
    """
    Segundo hilo para acciones secundarias.
    """
    pass

while True:
    try:
        thread0()
    except Exception as e:
        if env.DEBUG:
            print('Error: ', e)
    finally:
        if env.DEBUG:
            print('Memoria antes de liberar: ', gc.mem_free())

        gc.collect()

        if env.DEBUG:
            print("Memoria después de liberar:", gc.mem_free())

        sleep(5)
