#PRUEBA DOS

from machine import Pin, PWM
import utime
import random

# ----------- Pines -----------
# LEDs del juego (matriz 2x2)
leds = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]

# Botones con PULL_UP
botones = [
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP)
]

boton_reinicio = Pin(21, Pin.IN, Pin.PULL_UP)

# Registro de corrimiento para display de 7 segmentos
AB = Pin(14, Pin.OUT)  # Datos
CLK = Pin(5, Pin.OUT)  # Reloj

# Buzzer PWM
buzzer = PWM(Pin(3))

# --- Circuitos Exceso 3 ---
# Entradas simuladas por el valor binario del puntaje
B_pin = Pin(16, Pin.OUT)   # GP16
C_pin = Pin(4, Pin.OUT)    # GP4
D_pin = Pin(15, Pin.OUT)   # GP15

# Bit de habilitaciÃ³n aleatorio
L1_pin = Pin(17, Pin.OUT, pull=Pin.PULL_DOWN)  # GP17 - Habilita el circuito
utime.sleep(0.1)

# Salidas del circuito Exceso 3
led_L2 = Pin(18, Pin.OUT)  # Salida L2
led_L3 = Pin(19, Pin.OUT)  # Salida L3
led_L4 = Pin(20, Pin.OUT)  # Salida L4

# Patrones para display de 7 segmentos (cÃ¡todo comÃºn)
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
    0b00111110,  # b
    0b10011100,  # C
    0b01111010,  # d
    0b10011110,  # E
    0b10001110   # F
]


# ----------- Funciones del Display -----------
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

# ----------- FunciÃ³n lÃ³gica Exceso 3 -----------
def aplicar_exceso3(B_val, C_val, D_val):
    not_C = not C_val
    not_B = not B_val
    not_D = not D_val

    xor_BD = (B_val and not_D) or (not_B and D_val)
    L2_val = (not_C and xor_BD) or (not_B and C_val)
    L3_val = (not_C and not_D) or (C_val and D_val)
    L4_val = not_D

    return int(L2_val), int(L3_val), int(L4_val)

def actualizar_circuito_exceso3(valor_hex):
    bcd_input = valor_hex & 0b111  # Tres LSBs
    B_val = (bcd_input >> 2) & 1
    C_val = (bcd_input >> 1) & 1
    D_val = (bcd_input >> 0) & 1

    B_pin.value(B_val)
    C_pin.value(C_val)
    D_pin.value(D_val)

    L2_val, L3_val, L4_val = aplicar_exceso3(B_val, C_val, D_val)

    led_L2.value(L2_val)
    led_L3.value(L3_val)
    led_L4.value(L4_val)

def apagar_leds_exceso3():
    led_L2.value(0)
    led_L3.value(0)
    led_L4.value(0)
    
    B_pin.value(0)
    C_pin.value(0)
    D_pin.value(0)

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

def sonido_set_completado():
    sonar_buzzer(1500, 0.1)
    utime.sleep(0.05)
    sonar_buzzer(2000, 0.1)

def sonido_victoria():
    for freq in [800, 1200, 1600, 2000]:
        sonar_buzzer(freq, 0.15)
        utime.sleep(0.05)
    sonar_buzzer(1500, 0.3)
    sonar_buzzer(2000, 0.3)

# ----------- Animaciones -----------
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

def animacion_set_completado():
    for _ in range(2):  # Repetir 2 veces
        leds[2].value(1)  # Pin 8 (tercer LED en la lista)
        leds[3].value(1)  # Pin 9 (cuarto LED en la lista)
        utime.sleep(0.2)
        leds[2].value(0)
        leds[3].value(0)
        utime.sleep(0.2)

def animacion_victoria():
    for led in leds:    # Encender LEDs uno por uno
        led.value(1)
        utime.sleep(0.3)
    for _ in range(3): # Parpadeo rÃ¡pido 3 veces
        for led in leds:
            led.value(0)
        utime.sleep(0.2)
        for led in leds:
            led.value(1)
        utime.sleep(0.2)
    for led in leds:
        led.value(0)

# ----------- Funciones del juego -----------
def verificar_nivel(actual, aciertos):
    if actual == 1 and aciertos >= 25:
        return 2  # Avanzado
    elif actual == 2 and aciertos >= 40:
        return 3  # Leyenda
    elif actual == 3 and aciertos >= 60:
        print("Â¡Felicidades, completaste el nivel Leyenda!")
    else:
        return actual

def generar_patron(nivel):
    if nivel in [1, 2]:  
        return [random.randint(0, 3)]
    elif nivel == 3:  
        return random.sample(range(4), random.choice([1, 2]))

def mostrar_patron(patron):
    for i, led in enumerate(leds):
        led.value(1 if i in patron else 0)

def apagar_todos_leds():
    for led in leds:
        led.value(0)

def leer_botones():
    for i, boton in enumerate(botones):
        if boton.value() == 0:
            print(f"✅ Botón {i+1} (GPIO {boton}) PRESIONADO")
            return i
    return -1

# ----------- InicializaciÃ³n -----------
print("Iniciando sistema... Esperando 5 segundos antes de comenzar...")
utime.sleep(5)
print("Â¡Juego iniciado! Nivel 1 - Principiante")

aciertos = 0
nivel = 1
sets_completados = 0
limites = {1: 25, 2: 40}
L1_pin.value(random.getrandbits(1))  # Inicializar L1
ultimo_cambio_L1 = utime.ticks_ms()
intervalo_L1 = random.randint(1000, 1000)  # Primer intervalo aleatorio entre 1-5 segundos

# ----------- Bucle principal -----------
def verificar_reinicio():
    global aciertos, nivel, sets_completados  # ¡Importante!
    if boton_reinicio.value() == 0:
        utime.sleep_ms(50)  # Antirrebote
        if boton_reinicio.value() == 0:
            aciertos = 0
            nivel = 1
            sets_completados = 0
            return True
    return False

while True:
    
    if verificar_reinicio():
        aciertos = 0
        nivel = 1
        sets_completados = 0
        display.update_display(0)
        apagar_leds_exceso3()
        print("¡Juego reiniciado! Nivel 1 - Principiante")
        while boton_reinicio.value() == 0:  # Espera a que suelten el botón
            utime.sleep_ms(100)
        continue  # Saltar al siguiente ciclo del bucle
        # Verificar si es tiempo de cambiar L1
    ahora = utime.ticks_ms()
    if utime.ticks_diff(ahora, ultimo_cambio_L1) >= intervalo_L1:
        L1_pin.value(random.getrandbits(1))
        ultimo_cambio_L1 = ahora
        intervalo_L1 = random.randint(1000, 1000)  # Nuevo intervalo aleatorio
        
        # Activar o desactivar el circuito Exceso 3
        if L1_pin.value() == 1:
            actualizar_circuito_exceso3(sets_completados)
            print("Circuito Exceso 3 ACTIVADO")
        else:
            apagar_leds_exceso3()
            print("Circuito Exceso 3 DESACTIVADO")
            
    patron = generar_patron(nivel)
    mostrar_patron(patron)
    tiempo_limite = {1: 1.0, 2: 0.5, 3: 0.2}[nivel]
    inicio = utime.ticks_ms()
    acierto = False
    while utime.ticks_diff(utime.ticks_ms(), inicio) < tiempo_limite * 1000:
        boton_presionado = leer_botones()
        if boton_presionado != -1:
            acierto = (boton_presionado in patron) if nivel == 3 else (boton_presionado == patron[0])
            break

    apagar_todos_leds()

    if acierto:
        aciertos += 1
        sets_completados_nuevos = aciertos // 5

        if sets_completados_nuevos != sets_completados:
            sets_completados = sets_completados_nuevos

            # Mostrar nÃºmero en display
            display.update_display(sets_completados)

            # Activar o desactivar el circuito Exceso 3
            if L1_pin.value() == 1:
                actualizar_circuito_exceso3(sets_completados)

            # AnimaciÃ³n y sonido de set completado
            animacion_set_completado()
            sonido_set_completado()
            print(f"Set completado! Total: {sets_completados}")

        sonido_acierto()

        nuevo_nivel = verificar_nivel(nivel, aciertos)
        if nuevo_nivel != nivel:
            nivel = nuevo_nivel
            animacion_cambio_nivel()
            sonido_cambio_nivel()
            print(f"Â¡Nivel cambiado! Nuevo nivel: {nivel}")

        print(f"Acierto! Total: {aciertos} - Nivel: {nivel}")

    else:
        aciertos = 0
        sets_completados = 0
        display.update_display(0)
        apagar_leds_exceso3()

        sonido_error()
        animacion_error()
        print("Error! Intenta de nuevo. Aciertos reiniciados a 0.")

    utime.sleep(0.5)