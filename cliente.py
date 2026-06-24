import socket 

HOST = "127.0.0.1"
PORT = 8585


def iniciar_cliente(): 
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        cliente.connect((HOST, PORT))
        print("Conectado al servidor")

        #
        bienvenida = cliente.recv(1024).decode()
        print(f"Servidor dice: {bienvenida}")

       
        comando = "STATS"
        cliente.send(comando.encode('UTF-8'))

        respuesta = cliente.recv(1024).decode()
        print(f"Respuesta STAT:\n{respuesta}")

    except Exception as e: 
        print(f"Error de conexión: {e}")
    finally:
        cliente.close()

if __name__ == '__main__':
    iniciar_cliente()

