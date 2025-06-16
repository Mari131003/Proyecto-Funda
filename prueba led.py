from machine import Pin
import time

# Configurar el pin del LED (como salida)
led = Pin(16, Pin.OUT)  # Usamos GPIO15

while True:
    led.value(1)    # Encender LED (HIGH)
    print("LED ENCENDIDO")
    time.sleep(3)   # Esperar 3 segundos
    
    led.value(0)    # Apagar LED (LOW)
    print("LED APAGADO")
    time.sleep(3)   # Esperar otros 3 segundos