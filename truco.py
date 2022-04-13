# -*- coding: utf-8 -*-
"""
Created on Abril 5, 2022
version: 0.2

@author: jc
@author: sd
"""

from functools import total_ordering
import random
import os

from scipy import rand


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


class ICUtils():
    def __init__(self) -> None:
        pass

    def randomFromList(self, _list : list):
        index = random.randrange(0, len(_list), 1)
        return _list[index]



class Estadistica():
    p_rondas = list()
    puntos = None




class Mazo():
    def __init__(self) -> None:
        self.__minimo_corte = 0
        
        self.__cartas = [
            "1-oro", "2-oro", "3-oro", "4-oro", "5-oro", 
            "6-oro", "7-oro", "10-oro", "11-oro", "12-oro",
            "1-copa", "2-copa", "3-copa", "4-copa", "5-copa", 
            "6-copa",  "7-copa", "10-copa", "11-copa", "12-copa",
            "1-basto", "2-basto", "3-basto", "4-basto", "5-basto", 
            "6-basto",  "7-basto", "8-basto", "11-basto", "12-basto",
            "1-esapda", "2-esapda", "3-esapda", "4-esapda", "5-esapda", 
            "6-esapda",  "7-esapda", "10-esapda", "11-esapda", "12-esapda"
        ]
        self.mezclar_veces = 2
    @property
    def minimo_corte(self):
        return self.__minimo_corte

    @minimo_corte.setter
    def minimo_corte(self, min_corte):
        self.__minimo_corte = min_corte

    @property
    def mezclar_veces(self):
        return self.__mezlar_veces

    @mezclar_veces.setter
    def mezclar_veces(self, n_veces):
        self.__mezlar_veces = n_veces

    def cortar(self):
        cartas = list()
        n_cartas = len(self.__cartas)
        # estoy considerando tener un corde de mazo 
        # despues de la 5ta carta y antes de la 5ta carta
        # con la propiedad minimo_corte puedo ajustar este parametro
        index = random.randrange(self.minimo_corte, n_cartas-self.minimo_corte, 1)
        corte2 = [self.__cartas[i] for i in range(index , n_cartas) ]
        corte1 = [self.__cartas[i] for i in range(0, index) ]
        self.__cartas = corte2
        self.__cartas += corte1
        return self.__cartas 

    
    # si el parametro _veces es None osea no se asigna toma el valor por defecto
    # si se asigna un valor 
    def mezclar(self, _veces=None):
        n_cartas = len(self.__cartas)
        if _veces:
            _v = _veces
        else:
            _v = self.mezclar_veces
        n_cartas_menor = int(n_cartas/_v)
        sub_mazos = list()
        # corto en los n submazos en n sublistas
        for n in range(_v):
            n_corte = random.randrange(0, n_cartas_menor, 1)
            sub_mazos.insert(0, self.__cartas[0:n_corte] )
            self.__cartas = self.__cartas[n_corte:] 
        sub_mazos.insert(0, self.__cartas)
        #aplano la lista
        self.__cartas = [item for l in sub_mazos for item in l]

    def mezclarSegunIndice(self, _veces=None):
        n_cartas = len(self.__cartas)
        #print(n_cartas)
        _v = self.mezclar_veces
        if _veces:
            _v = _veces
        sub_mazo_pares = list()
        sub_mazo_impares = list()
        mazo_auxiliar = list()
        # cargo la lista de cartas
        for i in range(n_cartas):
            mazo_auxiliar.append(self.__cartas[i])
        for n in range(_v):
            #separo en dos listas del mismo tamanio:
            for i in range(n_cartas):
                if not i%2: # == 0
                    sub_mazo_pares.append(mazo_auxiliar[i])
                else:
                    sub_mazo_impares.append(mazo_auxiliar[i])
            #recombino las listas en una:
            mazo_auxiliar.clear()
            mazo_auxiliar = sub_mazo_impares + sub_mazo_pares
            sub_mazo_pares.clear()
            sub_mazo_impares.clear()
        self.__cartas = mazo_auxiliar
    
    def mazo(self):
        return self.__cartas

    def __str__(self) -> str:
        salida = ""
        i = 1
        for c in self.__cartas:
            salida += c.ljust(15," ") # + "\t"
            if i>7:
                salida += "\n"
                i = 0
            i += 1
        return salida
    
    def sacarCartaDeAbajo(self):
        carta = self.__cartas[-1]
        self.__cartas = self.__cartas[:-1]
        return carta
    


class Truco():
    # tablero
    
    def __init__(self, mazo : Mazo) -> None:
        self.__mazo = mazo
        self.__jugadores = list()
        self.__cartas_mesa = list()


    def obtenerPuntaje(self,carta_agente: str):

        if "12" in carta_agente:
            return 7
        elif "11" in carta_agente:
            return 6
        elif "10" in carta_agente:
            return 5
        elif "1" in carta_agente:
            if "espada" in carta_agente:
                return 14
            elif "basto" in carta_agente:
                return 13
            else:
                return 8
        elif "2" in carta_agente:
            return 9
        elif "3" in carta_agente:
            return 10
        elif "4" in carta_agente:
            return 1
        elif "5" in carta_agente:
            return 2
        elif "6" in carta_agente:
            return 3
        elif "7" in carta_agente:
            if "espada" in carta_agente:
                return 12
            elif "oro" in carta_agente:
                return 11
            else:
                return 4
        else:
            return -10


    def mezclar(self, veces=None):
        self.__mazo.mezclar(veces)
        self.__mazo.mezclarSegunIndice(veces)
    
    def cortarMazo(self):
        self.__mazo.cortar()

    def ponerCartaMesa(self, carta):
        self.__cartas_mesa.append(carta)

    def repartirCartas(self):
        n_jugadores = len(self.__jugadores)
        if n_jugadores >= 2: 
            for c in range( 3 ):
                carta = self.__mazo.sacarCartaDeAbajo()
                self.__jugadores[1].tomarCarta( carta )
                carta = self.__mazo.sacarCartaDeAbajo()
                self.__jugadores[0].tomarCarta( carta )
        else:
            print("Debe asignar los jugadores")

    
    def sumarJugador(self, jugador):
        self.__jugadores.append(jugador)
        

    def listarJugadores(self):
        for j in self.__jugadores:
            print( j.nombre )
            
    def listarCartas(self):
        print (self.__mazo)

    def computarRonda(self, ag0, ag1):
        ganador = None
        cartas_ronda = self.__cartas_mesa[-2:]
        print("Cantidad de cartas sobre la mesa: ",len(self.__cartas_mesa))
        c = cartas_ronda[0]
        p_ag0 = self.obtenerPuntaje( c )
        c = cartas_ronda[1]
        p_ag1 = self.obtenerPuntaje( c )
        if p_ag0 == p_ag1:
            ag0.asignarResultado("E")
            ag1.asignarResultado("E")
        elif p_ag0 > p_ag1:
            ganador = 0
            ag0.asignarResultado("V")
            ag1.asignarResultado("D")
        else:
            ganador = 1
            ag0.asignarResultado("D")
            ag1.asignarResultado("V")
        return ganador
        

    def jugarSimple(self):
        n_jugadores = len(self.__jugadores)
        for n in range(3):
            self.__jugadores[1].mirarMesa(tuple(self.__cartas_mesa))
            carta_jugada = self.__jugadores[1].tirarCarta()
            #carta_jugada.por = self.__jugadores[1].nombre

            #print(f"Carta sobre la mesa: {carta_jugada}, jugado por {carta_jugada.por}")
            self.ponerCartaMesa(carta_jugada)

            self.__jugadores[0].mirarMesa(tuple(self.__cartas_mesa))
            carta_jugada = self.__jugadores[0].tirarCarta()
            #carta_jugada.por = self.__jugadores[0].nombre
            #print(f"Carta sobre la mesa: {carta_jugada}, jugado por {carta_jugada.por}")
            self.ponerCartaMesa(carta_jugada)

            ganador = self.computarRonda(self.__jugadores[0], self.__jugadores[1])
            if ganador == 0:
                jtmp = self.__jugadores[0]
                self.__jugadores[0] = self.__jugadores[1]
                self.__jugadores[1] = jtmp

        print ("Resualtado de las rondas:")
        self.__jugadores[0].mostarResultados()
        self.__jugadores[1].mostarResultados()
        


class Agente():
    def __init__(self, nombre, envio=None, flor=None, mensajes=True) -> None:
        self.__mensajes = mensajes
        if envio != None:
            self.__envio = envio
        if flor != None:
            self.__flor = flor
        self.__nombre = nombre
        self.__mis_cartas = list()
        self.__mi_proxima_jugada = 0
        self.__resultados = list()
        
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, _nombre):
        self.__nombre = _nombre

    def tomarCarta(self, carta):
        self.__mis_cartas.append( carta )
        if (self.__mis_cartas==3):
            self.ordenarMisCartas()

    def ordenarMisCartas(self):
        if self.__mensajes:
            print (f"Mis cartas desordenadas: {self.__mis_cartas}")
        #tope = len
        for j in range(2):
            for i in range(2):
                c = self.__mis_cartas[i]
                pc1 = Truco.obtenerPuntaje(c)
                c = self.__mis_cartas[i+1]
                pc2 = Truco.obtenerPuntaje(c)
                if pc1>pc2:
                    ctmp = self.__mis_cartas[i]
                    self.__mis_cartas[i] = self.__mis_cartas[i+1]
                    self.__mis_cartas[i+1] = ctmp
        if self.__mensajes:
            print (f"Mis cartas ordenadas: {self.__mis_cartas}")
            
    def asignarResultado(self, res):
        self.__resultados.append(res)

    def mostarResultados(self):
        print(f"El resultado de: {self.nombre} es: {self.__resultados}" )

    def mirarMesa(self, cartas_mesa):
        n_cartas = len(cartas_mesa)
        carta = None
        if n_cartas == 0:
            self.__mi_proxima_jugada=1
        elif n_cartas >= 1:
            self.__mi_proxima_jugada = 0


    #def queInmediatoSuperior(self,):


    def tirarCarta(self):
        if self.__mi_proxima_jugada != -1:
            #if len(self.__mis_cartas) == 3:
            if True:
                carta = self.__mis_cartas[self.__mi_proxima_jugada]
                self.__mis_cartas.remove(self.__mis_cartas[self.__mi_proxima_jugada])
                #self.__mi_proxima_jugada = -1
        else:
            if self.__mensajes:
                print("No es mi turno para jugar")
            carta = None
        return carta

    
        

clear()

mazo_cartas = Mazo()
truco = Truco(mazo_cartas)

truco.listarCartas()

# se puede agregar aqui
# truco.sumarJugador( Agente("A1") )
# truco.sumarJugador( Agente("A2") )

truco.cortarMazo()
truco.mezclar(5)
truco.cortarMazo()

truco.listarCartas()

# o aqui
a1 = Agente("A1")
a2 = Agente("A2")
truco.sumarJugador( a1 )
truco.sumarJugador( a2 )

# se considera solo dos jugadores
# se toma el primer jugador que se agrego al juego como el jugador pie
truco.repartirCartas()

truco.jugarSimple()



truco.listarJugadores()






#truco = Truco()
#truco.minimo_corte = 3
#truco.mezclar_veces = 5

#print( truco )

#truco.mezclar()

#print ( truco )


#ag1 = Agente( "Sandro" )

#ag2 = Agente( "Carlos" )

#ag1.listarJugadores()

#truco.listarJugadores()



#print ("Corto el mazo")
#truco.cortar( truco.mazo() )
#print(truco)

#print ("Corto el mazo")
#truco.cortar( truco.mazo() )
#print(truco)
