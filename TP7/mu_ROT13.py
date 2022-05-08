# Ejercicio 7 - Multiprocessing con Queue.

''''
PROBLEMA:

Escribir un programa que genere dos hijjos utilizando multiprocessing.
Uno de los hijos deberá leer desde stdin texto introducido por el usuario, y deberá escribirlo 
en un pipe (multiprocessing).

El segundo hijo deberá leer desde el pipe el contenido de texto, lo encriptará utilizando 
el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).

El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.
'''

import sys
import os
from multiprocessing import Process, Pipe, Queue
import codecs
import time
import signal


def f(r,w,q,nproc):

    if(nproc == 1):
        #Proceso del H1, LEE DESDE STDIN
        sys.stdin = open(0)
        while True:
            print("Ingrese una linea: ")
            c = sys.stdin.readline()
            w.send(c)
            #H1 LEE lo que le envio encriptado el H2
            time.sleep(1)
            print("El Proceso H1 lee: ",q.get())
    
    if(nproc == 2):
    #Proceso del H2, 
        while True:
            encrypt = codecs.encode(r.recv(), 'rot13')
            q.put(encrypt)
        
    print("Proceso PID %d (%d) terminando..." % (os.getpid(), nproc))


if __name__ == '__main__':
    #Crea el Pipe
    r, w = Pipe()
    #Crea la Cola
    q = Queue()
    #Creacion de los Procesos H1 y H2
    p1 = Process(target=f, args=(r,w,q,1))
    p2 = Process(target=f, args=(r,w,q,2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Bye...")