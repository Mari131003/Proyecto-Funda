import machine
import utime

AB = machine.Pin(14, machine.Pin.OUT)  
CLK = machine.Pin(5, machine.Pin.OUT)  

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
        self.current_digit = 0
        self.last_change = utime.ticks_ms()
        self.change_interval = 2000  # 3 segundos en milisegundos
    
    def update(self):
        """Actualiza el display si ha pasado el tiempo suficiente"""
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, self.last_change) >= self.change_interval:
            self.current_digit = (self.current_digit + 1) % 16
            display_digito(secuenciasnumeros[self.current_digit])
            self.last_change = current_time
    
    def set_digito(self, digit):
        """Fuerza un dígito específico"""
        self.current_digit = digit % 16
        display_digito(secuenciasnumeros[self.current_digit])
        self.last_change = utime.ticks_ms()

def main():
    display = DisplayController()
    while True:
        # Actualiza el display (no bloqueante)
        display.update() 

if __name__ == "__main__":
    main()