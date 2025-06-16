#MODIFICADO pines
from machine import Pin
import utime

# Configuración
botones = [
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP)
]

leds = [
    Pin(6, Pin.OUT),
    Pin(7, Pin.OUT),
    Pin(8, Pin.OUT),
    Pin(9, Pin.OUT)
]

print("Prueba con retroalimentación visual")
print("El LED correspondiente se encenderá al presionar cada botón")

try:
    while True:
        for i, btn in enumerate(botones):
            if not btn.value():
                leds[i].value(1)  # Enciende el LED correspondiente
                print(f"Botón {i} presionado")
                while not btn.value():  # Espera a que se suelte
                    pass
                leds[i].value(0)
                utime.sleep_ms(200)
        utime.sleep_ms(10)
        
except KeyboardInterrupt:
    for led in leds:
        led.value(0)
    print("Prueba terminada")