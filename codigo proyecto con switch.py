from machine import Pin, PWM
import utime
import random
 
# ----------- Pines -----------
# LEDs
leds = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
# Botones con PULL_DOWN
botones = [
    Pin(10, Pin.IN, Pin.PULL_DOWN),
    Pin(11, Pin.IN, Pin.PULL_DOWN),
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(13, Pin.IN, Pin.PULL_DOWN)
]
# Switches para selección de nivel (sin pull interno, depende del HW)
switches = [Pin(0, Pin.IN), Pin(1, Pin.IN), Pin(2, Pin.IN)]
#Registro
AB = Pin(14, Pin.OUT)
CLK = Pin(5, Pin.OUT)  
# Buzzer PWM
buzzer = PWM(Pin(3))
# ----------- Variables globales -----------
encendido = False
nivel = 1
aciertos = 0
limites = {1: 5, 2: 12}
secuenciasnumeros = [
    0b11111100,  # 0
    0b01100000,  # 1
    0b11011010,  # 2
    0b11110010,  # 3
    0b01100110,  # 4
    0b10110110,  # 5
    0b10111110,  # 6
    0b11100010,  # 7
    0b11111110,  # 8
    0b11100110,  # 9
    0b11101110,  # A
    0b00111110,  # B
    0b10011100,  # C
    0b01111010,  # D
    0b10011110,  # E
    0b10001110   # F
]
def enviar_bit(bit):
    AB.value(bit)
    CLK.value(1)
    CLK.value(0)
def display_digito(pattern):
    for i in range(8):
        enviar_bit((pattern >> i) & 0x01)
class DisplayController:
    def __init__(self):
        self.current_value = 0
    def update_display(self, value):
        if 0 <= value <= 15:
            display_digito(secuenciasnumeros[value])
display = DisplayController() 
# ----------- Funciones Buzzer -----------
def sonar_buzzer(frecuencia, duracion):
    buzzer.freq(frecuencia)
    buzzer.duty_u16(30000)
    utime.sleep(duracion)
    buzzer.duty_u16(0)
def sonido_acierto():
    sonar_buzzer(1000, 0.1)
def sonido_error():
    sonar_buzzer(300, 0.3)
def sonido_cambio_nivel():
    for freq in [600, 800, 1000, 1200]:
        sonar_buzzer(freq, 0.1)
        utime.sleep(0.05)
# ----------- Animación LEDs -----------
def animacion_cambio_nivel():
    for _ in range(3):
        for led in leds:
            led.value(1)
        utime.sleep(0.2)
        for led in leds:
            led.value(0)
        utime.sleep(0.2)
def animacion_error():
    for _ in range(3):
        leds[0].value(1)
        utime.sleep(0.2)
        leds[0].value(0)
        utime.sleep(0.2)
# ----------- Funciones del juego -----------
def leer_nivel():
    estado_switches = [sw.value() for sw in switches]
    utime.sleep_ms(50)
    if estado_switches[0] == 1:    # Switch 1 (Pin 0)
        return 1  # Principiante
    elif estado_switches[1] == 1:  # Switch 2 (Pin 1)
        return 2  # Avanzado
    elif estado_switches[2] == 1:  # Switch 3 (Pin 2)
        return 3  # Leyenda
    else:
        return 1  # Default: Principiante si ningún switch está activo
def verificar_nivel(actual, aciertos):
    if actual == 1 and aciertos >= limites[1]:
        return 2, 0 
    elif actual == 2 and aciertos >= limites[2]:
        return 3, 0
    else:
        return actual, aciertos
def generar_patron(nivel):
    if nivel in [1, 2]:  
        return [random.randint(0, 3)]
    elif nivel == 3:  
        leds_on = random.sample(range(4), random.choice([1, 2]))
        return leds_on
def mostrar_patron(patron):
    for i, led in enumerate(leds):
        led.value(1 if i in patron else 0)
def apagar_todos_leds():
    for led in leds:
        led.value(0)
def leer_botones():
    for i, boton in enumerate(botones):
        if boton.value() == 1:
            return i
    return -1
# ----------- Bucle principal -----------
print("Iniciando sistema...")
print("¡Juego iniciado! Nivel 1") 
nuevo_nivel, aciertos = verificar_nivel(nivel, aciertos)
while True:
    nivel = leer_nivel()
    print(f"Nivel seleccionado: {nivel}")
    patron = generar_patron(nivel)
    mostrar_patron(patron)
    tiempo_limite = {1: 1.0, 2: 0.5, 3: 0.2}[nivel]
    inicio = utime.ticks_ms()
    acierto = False
    while utime.ticks_diff(utime.ticks_ms(), inicio) < tiempo_limite * 1000:
        boton_presionado = leer_botones()
        if boton_presionado != -1:
            if nivel in [1, 2]:
                acierto = (boton_presionado == patron[0])
            else:
                acierto = (boton_presionado in patron)
            break
    apagar_todos_leds()
    if acierto:
        aciertos += 1
        display.update_display(aciertos // 5)
        sonido_acierto()
        nuevo_nivel = verificar_nivel(nivel, aciertos)
        if nuevo_nivel != nivel:
            nivel = nuevo_nivel
            animacion_cambio_nivel()
            sonido_cambio_nivel()
        print(f"Acierto! Total: {aciertos} - Nivel: {nivel}")
    else:
        sonido_error()
        animacion_error()
        print("Error!")
    utime.sleep(0.5)