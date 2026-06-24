import socket
import threading

HOST = '0.0.0.0'
PORT = 8585
MAX_CLIENTES = 5

def manejar_cliente(conn,addr):
    print(f"[NUEVA CONEXiÓN] {addr} conectado.") 
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            #Responder con eco básico
            conn.sendall(b"PROCESADO: " + data) 
    except ConnectionResetError:
        print(f"[ERROR] Conexión abrupta con {addr}")
    finally:
        conn.close()
        print(f"[DESCONEXIÓN] {addr} finalizó sesión.")

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Evitar el error: address already in use

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(HOST, PORT)
    server.listen(MAX_CLIENTES)  
    print(f"[LISTO] servidor escuchando en el puerto {PORT}")

    while True: 
        conn, addr= server.accept()

        #Hilo principal cuenta como 1, por ende restamos 1 a los clientes activos
        clientes_activos = threading.active_count() - 1

        if clientes_activos < MAX_CLIENTES:
            thread = threading.Thread(target=manejar_cliente, args=(conn,addr))
            thread.start()
            print(f"[HILOS ACTIVOS] CLientes concurrentes: {thread.active_count() - 1}")

        else:
            print(f"[RECHAZADO] conexión {addr} ignorada por saturación. Limite máx {MAX_CLIENTES}")
            try:
                conn.send("[ERROR] Servidor lleno. Intente más tarde.\n".encode())
            except socket.error:
                pass
            finally: 
                conn.close()

if __name__ == "__main__":
    iniciar_servidor()



