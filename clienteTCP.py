# Import socket module
import socket
import logging
import hashlib
import time
from _thread import *
from threading import Thread
def Main():

    #Initializes the client log
    logging.basicConfig(filename="clientLog.log", level=logging.INFO,
    format = '%(asctime)s %(levelname)-8s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    )
    numt=int(input("Cuantos threads de cliente quiere correr?"))
    for i in range(numt):
        m = hashlib.sha256()
        print("entre al for")
        try:
            thread = Thread(target = threaded, args = (i,m,))
            thread.start()
            thread.join()
        except:
            print("Error al arrancar el thread")


def threaded(i,m):
    print("Entre al threaded")
    start_time=time.time()
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 6666
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    s.connect((host, port))
    print("Thread #%d Ready to receive info ",i)
    logging.info("CLIENTE Thread #%d ready to receive info",i)
    f=open("ctext.txt",'wb')
    while True:
        # message received from server
        data = s.recv(1024)
        #f.write(data)
        if not data:
            print("Termino el envio")
            break
        elif (data.__contains__(b"HASH")):
            logging.info("Found hash")
            index=data.find(b"HASH")
            m.update(data[:index])
            print("Los datos usados son ", data[:index])
            realM=data[index+4:]
            print("Hash recibido ",realM.decode())
            print("Hash creado ",m.hexdigest())
            if m.hexdigest() == realM.decode():
                print("Hash correcto")
                logging.info("CLIENTE hash correcto")
            else:
                print("Hash incorrecto")
                logging.info("CLIENTE hash corrupto ")

        m.update(data)

    logging.info("CLIENTE Tiempo del envio %s",(time.time()-start_time))
    logging.info("---------------------------------------------")
    s.close()

Main()