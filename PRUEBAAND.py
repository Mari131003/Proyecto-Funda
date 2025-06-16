import machine
EntradaA = machine.Pin(4,machine.Pin.OUT)
EntradaB = machine.Pin(15,machine.Pin.OUT)

EntradaA.value(0)
EntradaB.value(0)