#!/usr/bin/env python3

import socket
import time
import os
from os import system, name
import random
import pickle

#HOST = input("Introduzca la direccion IP del servidor (192.168.1.135): ")  # El hostname o la IP del servidor
#PORT = input("Intruduzca el puerto de destino (65432): ")  # El puerto que usa el servidor
HOST = "192.168.0.13"
PORT = 65432
buffer_size = 1024
DATA = "Confirm"
BDATA = DATA.encode()

def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')
def MostrarMapa(map):
    for row in map:
        print(" ".join(str(cell) for cell in row))
        print("")
def CheckContinuarJuego(puntos):
    print("Tu puntuacion: ", puntos)
    continuar = input("Deseas intentar de nuevo? (s/n) :")
    if continuar == 'n':
        return False
    return True
def CheckContinuarJuego2(puntos):
    print("Tu puntuacion: ", puntos)
    continuar = input("Deseas empezar nueva partida? (s/n) :")
    if continuar == 'n':
        return False
    return True
def ConnectionTimeExpired(socket):
    print("El servidor tardo mucho en responder de vuelta")
    print("Conexion con ", socket, "terminada")
    time.sleep(5)
    quit()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, int(PORT)))
    StatusJuego = True
    while StatusJuego:
        clear()
        dificultad = input("Selecciona la dificultad (f, d):")
        Bdificultad = pickle.dumps(dificultad)
        print("Enviando mensaje a servidor...")
        TCPClientSocket.sendall(Bdificultad)#la letra "b" transforma la cadena de caracteres a bytes.
        print("Recibiendo datos del servidor...")
        while True:
            buscaminas_mapa = pickle.loads(TCPClientSocket.recv(buffer_size))
            if not buscaminas_mapa:
                break
            #print("Recibido,", repr(buscaminas_mapa), " de", TCPClientSocket.getpeername())
            TCPClientSocket.sendall(BDATA)
            break
        while True:
            mapa_jugador = pickle.loads(TCPClientSocket.recv(buffer_size))
            if not mapa_jugador:
                break
            #print("Recibido,", repr(mapa_jugador), " de", TCPClientSocket.getpeername())
            TCPClientSocket.sendall(BDATA)
            break
        MostrarMapa(mapa_jugador)
        while True:
            while True:
                CheckWon = pickle.loads(TCPClientSocket.recv(buffer_size))
                if not CheckWon:
                    break
                TCPClientSocket.sendall(BDATA)
                break
            print("CheckWon: ", str(CheckWon))
            if CheckWon == False:
                print("Inserta coordenada para excavar: ")
                if dificultad.lower() == 'd':
                    x = input("X (1 a 16): ")
                    if (int(x) < 1 or int(x) > 16):
                        x = 0
                    x = int(x) - 1
                    Bx = pickle.dumps(x)
                    print("Enviando dato x al servidor...")
                    TCPClientSocket.sendall(Bx)
                    while True:
                        print("Dato enviado, esperando confirmacion...")
                        confirmacion = TCPClientSocket.recv(buffer_size)
                        if not confirmacion:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    y = input("Y (1 a 16): ")
                    if (int(y) < 1 or int(y) > 16):
                        y = 0
                    y = int(y) - 1
                    By = pickle.dumps(y)
                    print("Enviando dato y al servidor...")
                    TCPClientSocket.sendall(By)
                    while True:
                        print("Dato enviado, esperando confirmacion...")
                        confirmacion = TCPClientSocket.recv(buffer_size)
                        if not confirmacion:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    clear()
                    while True:
                        print("Recibiendo Mapa actualizado...")
                        mapa_jugador_nuevo = pickle.loads(TCPClientSocket.recv(buffer_size))
                        if not mapa_jugador_nuevo:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    MostrarMapa(mapa_jugador_nuevo)
                else:
                    x = input("X (1 a 9): ")
                    if (int(x) < 1 or int(x) > 9):
                        x = 0
                    y = input("Y (1 a 9): ")
                    if (int(y) < 1 or int(y) > 9):
                        y = 0
                    x = int(x) - 1
                    y = int(y) - 1
                    clear()
                    print("Enviando dato x al servidor...")
                    TCPClientSocket.sendall(pickle.dumps(x))
                    while True:
                        print("Dato enviado, esperando confirmacion...")
                        confirmacion = TCPClientSocket.recv(buffer_size)
                        if not confirmacion:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    print("Enviando dato y al servidor...")
                    TCPClientSocket.sendall(pickle.dumps(y))
                    while True:
                        print("Dato enviado, esperando confirmacion...")
                        confirmacion = TCPClientSocket.recv(buffer_size)
                        if not confirmacion:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    while True:
                        print("Recibiendo Mapa actualizado...")
                        mapa_jugador_nuevo = pickle.loads(TCPClientSocket.recv(buffer_size))
                        if not mapa_jugador_nuevo:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    MostrarMapa(mapa_jugador_nuevo)
                if TCPClientSocket.recv(buffer_size) == "Lost":
                    while True:
                        print("Recibiendo puntaje...")
                        puntos = TCPClientSocket.recv(buffer_size)
                        if not puntos:
                            break
                        TCPClientSocket.sendall(BDATA)
                        break
                    print("Fin del Juego!\n")
                    MostrarMapa(buscaminas_mapa)
                    StatusJuego = CheckContinuarJuego(puntos)
                    break
            else:
                while True:
                    print("Recibiendo puntaje...")
                    puntos = TCPClientSocket.recv(buffer_size)
                    if not puntos:
                        break
                    TCPClientSocket.sendall(BDATA)
                    break
                print("Bien hecho, ganaste!\n")
                MostrarMapa(buscaminas_mapa)
                StatusJuego = CheckContinuarJuego2(puntos)
                break

    #print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
