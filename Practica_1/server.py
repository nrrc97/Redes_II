#!/usr/bin/env python3

import socket
import time
import os
from os import system, name
import random
import pickle

HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente
buffer_size = 1024
DATA = "Recibido"
BDATA = DATA.encode()

def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')
def GenerarMapaBuscaMinas(n, k):
    arr = [[0 for row in range(n)] for column in range(n)]
    for num in range(k):
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        arr[y][x] = 'X'

        if (x >= 0 and x <= n-2) and (y >= 0 and y <= n-1):
            if arr[y][x+1] != 'X':
                arr[y][x+1] += 1    #Centro derecho
        if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-1):
            if arr[y][x-1] != 'X':
                arr[y][x-1] += 1    #Centro izquierdo
        if (x >= 1 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x-1] != 'X':
                arr[y-1][x-1] += 1  #Superior izquierdo
        if (x >= 0 and x <= n-2) and (y >= 1 and y <= n-1):
            if arr[y-1][x+1] != 'X':
                arr[y-1][x+1] += 1  #Superior derecho
        if (x >= 0 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x] != 'X':
                arr[y-1][x] += 1    #Superior centro
        if (x >= 0 and x <= n-2) and (y >= 0 and y <= n-2):
            if arr[y+1][x+1] != 'X':
                arr[y+1][x+1] += 1  #Inferior derecho
        if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x-1] != 'X':
                arr[y+1][x-1] += 1  #Inferior izquierdo
        if (x >= 0 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x] != 'X':
                arr[y+1][x] += 1    #Inferior centro
    return arr
def GenerarMapaJugador(n):
    arr = [['-' for row in range(n)] for column in range(n)]
    return arr
def CheckWon(map, k):
    n_holes = 0
    for row in map:
        for cell in row:
            if cell == '-':
                n_holes += 1
                if n_holes != k:
                    return False
    return True
def UpdateMap(map1, map2, x, y):
    if x == -1 and y == -1:
        print("Valores incorrectos, intente de nuevo.")
        Bmapa_jugador = pickle.dumps(map1)
        return Bmapa_jugador
    else:
        map1[y][x] = map2[y][x]
        Bmapa_jugador = pickle.dumps(map1)
        return Bmapa_jugador
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            print("Esperando a recibir datos... ")
            #data = Client_conn.recv(buffer_size)
            dificultad = pickle.loads(Client_conn.recv(buffer_size))
            if not dificultad:
                break
            print("Recibido,", dificultad, "   de ", Client_addr)
            break
        if dificultad == 'd':
            n = 16
            k = 40
            #Bk = pickle.dumps(k)
        else:
            n = 9
            k = 10
            #Bk = pickle.dumps(k)
        clear()
        buscaminas_mapa = GenerarMapaBuscaMinas(n, k)
        Bbuscaminas_mapa = pickle.dumps(buscaminas_mapa)
        mapa_jugador = GenerarMapaJugador(n)
        Bmapa_jugador = pickle.dumps(mapa_jugador)
        puntos = 0

        print("Enviando datos a cliente...")
        Client_conn.sendall(Bbuscaminas_mapa)
        print("Termino de envio datos", Client_conn.recv(buffer_size))
        print("Enviando datos a cliente...")
        Client_conn.sendall(Bmapa_jugador)
        print("Termino de envio datos", Client_conn.recv(buffer_size))

        while True:
            if CheckWon(mapa_jugador, k) == False:
                CW = False
                BCheckWon = pickle.dumps(CW)
                print("Enviando confirmacion al cliente...")
                Client_conn.sendall(BCheckWon)
                print("Termino de envio de confirmacion", Client_conn.recv(buffer_size))
                while True:
                    print("Recibiendo dato x...")
                    x = pickle.loads(Client_conn.recv(buffer_size))
                    print(x)
                    if not x:
                        break
                    print("Recibido, enviando confirmacion...")
                    Client_conn.send(BDATA)
                    break
                while True:
                    print("Recibiendo dato y...")
                    y = pickle.loads(Client_conn.recv(buffer_size))
                    if not y:
                        break
                    print("Recibido, enviando confirmacion...")
                    Client_conn.send(BDATA)
                    break
                ClientMap = UpdateMap(mapa_jugador, buscaminas_mapa, x, y)
                print("Enviando Mapa actualizado al Cliente...")
                Client_conn.sendall(ClientMap)
                puntos += 1

                if (buscaminas_mapa[y][x] == 'X'):
                    GameOver = "Lost"
                    BGM = GameOver.encode()
                    print("Enviando señal de fin del juego...")
                    Client_conn.sendall(BGM)
                    print("Termino de envio de señal", Client_conn.recv(buffer_size))
                    Bpuntos = puntos.encode()
                    print("Enviando puntaje...")
                    Client_conn.sendall(Bpuntos)
                    print("Termino de envio de puntaje", Client_conn.recv(buffer_size))
                    break
            else:
                Bpuntos = puntos.encode()
                print("Enviando puntaje...")
                Client_conn.sendall(Bpuntos)
                print("Termino de envio de puntaje", Client_conn.recv(buffer_size))
                break