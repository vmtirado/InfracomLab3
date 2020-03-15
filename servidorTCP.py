# import socket programming library 
import socket

# import thread module 
from _thread import *
import threading
import logging
import hashlib
#print_lock = threading.Lock()

# thread function
# c is the socket object with which connection was made, used to send and receive messages
def threaded(c):
    m = hashlib.sha256()
    print("El archivo que se va a abrir es: ",file)
    with open(file,'rb') as f:
        while True:
            # data received from client
            data= f.read()

            if not data:
                print("Termine de mandar")

                #envio el hash
                h=str(m.hexdigest())
                print("el digest que mando es ",m.hexdigest())
                c.send(("HASH"+h).encode())
                break
            # send back reversed string to client
            print("Mando: ",data)
            m.update(data)
            c.send(data)

     # connection closed
    c.close()


def Main():
    #Initializes the server log
    logging.basicConfig(filename="serverLog.log", level=logging.INFO,
    format = '%(asctime)s %(levelname)-8s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    )
    host = "localhost"
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 6666
    logging.info('Connected to %s on port %s', host,port)
    # Socket del servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port %s", port)

    # put the socket into listening mode 
    s.listen(5)
    print("socket is listening")
    texto=int (input("\n Que texto desea enviar?"
                     "\n 1. 100 mib"
                     "\n 2. 250 mib"))
    if texto==1:
        f="text1.txt"
    else:
        f="text2.txt"
    global file
    file=f
    print("Archivo seleccionado: ",file)
    num_conn= int( input('\n Cuantas conexiones desea recibir?' ))

    print("Esperando conexiones:")

    #Counter with number of conection receibed
    cont=0
    while cont<=num_conn :
        # establish connection with client
        # c is a socket object to send and receive messages
        c, addr = s.accept()
        # lock acquired by client 
        #print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,))
        cont+=1
    s.close()



Main()