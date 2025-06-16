from machine import Pin
import time

# Configurar el pin del botón (pull-down)
boton = Pin(10, Pin.IN, Pin.PULL_DOWN)  # Usamos resistencia interna PULL_DOWN

while True:
    if boton.value() == 1:  # Si el botón se presiona (HIGH)
        print("Estoy siendo presionado")
        time.sleep(0.2)  # Pequeña pausa para evitar rebotes