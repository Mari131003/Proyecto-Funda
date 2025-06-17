import machine
import network # para el WiFi
import socket
from time import sleep

########## Configuración de la red ##########

ssid = "pocof3"  #nombre de la red
password = "tec2025252" #contraseña de la red

########## Función para conectar a la red WiFi ##########
def connectToWifi():
    try:
        wlan = network.WLAN(network.STA_IF) #crea la interfaz para la conexión
        wlan.active(True)
        wlan.connect(ssid, password) 
        while wlan.isconnected() == False: 
            print('Esperando la conexion...')
            sleep(1)
        picoIp = wlan.ifconfig()[0] #obtiene la ip asignada a la raspy
        print('Conectado exitosamente a la ip: ' + str(picoIp))
    except:
        print('Algo salio mal. Intente nuevamente')
        
########## Función para conectar al server ##########
def connectToPC():
        
    server_address = ('192.168.85.182', 8001) #Dir del server 
    messageToConfirm = "Hola, este mensaje es enviado desde la raspy :)"  

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un socket TCP/IP
        print("socket creado")
       
        client_socket.connect(server_address)  # Conectarse al servidor
        print("conexion exitosa")
        
        client_socket.sendall(messageToConfirm.encode()) # Enviar los datos
        
        while True:
            # Esperar respuesta del servidor
            response = client_socket.recv(1024) # Recibe hasta 1024 bytes de datos
            print("Respuesta del servidor:", response.decode())
            
            ###########################################################
        
    except Exception as e:
        print("Error de conexión:", e)
        
    finally:
        client_socket.close() # Cerrar el socket
          
########## Llamar a la función de conexion wifi ##########
connectToWifi()

########## Llamar a la función de conexion con el server ##########
connectToPC()


  