'''
ERRORES :

- En el segundo nivel se divide el arquero []
- Validacion de ingresar un dato vacio []

'''

# imports
import random

# Funciones
def lecturaArchivo():
    rankings = dict() # { nombre : puntaje, ... }
    try:
        entrada = open("rankings.csv", "rt")
        for linea in entrada:
            linea = linea.strip().split(";")
            nombre = linea[0]
            puntaje = int(linea[1])
            rankings[nombre] = puntaje

    except FileNotFoundError as mensaje:
        print(" No se pudo abrir el archivo.")
    except OSError as mensaje:
        print(" ERROR : " , mensaje)
    finally:
        try:
            entrada.close()
        except NameError:
            pass
    pass

    return rankings

def escrituraArchivo(rankings):
    try:
        archivo = open("rankings.csv", "wt")
        k = 0
        for jugador, puntaje in rankings.items():
            k += 1
            linea = f"{jugador};{str(puntaje)}\n"
            archivo.write(linea)
    except FileNotFoundError as mensaje:
        print(" No se pudo abrir el archivo.")
    except OSError as mensaje:
        print(" ERROR : " , mensaje)
    else:
        print(" Copia finalizada, Lineas copiadas", k)
    finally:
        try:
            archivo.close()
        except NameError:
            pass
    pass

def ordenarDiccionario(rankings):
    rankings = dict(sorted(rankings.items(), key= lambda x: x[1], reverse=True))

def sumarPuntaje(jugador, puntaje, rankings):
    if jugador in rankings.keys():
        rankings[jugador] += puntaje
    else:
        rankings[jugador] = puntaje

def mostrarRanking(ranking):
    if len(rankings) != 0:
        print("\n\t --- RANKING ---")
        for jugador, puntaje in ranking.items():
            print(f" > {jugador} : {puntaje}")
    else:
        print("\n Ranking vacio \n")

def mostrarReglas():
    print()
    print("\t ### BIENVENIDO A PENALTYSHOOTER ###\n \
           \nReglas del juego: \n \
           > Lograr un mayor de 3 goles por nivel, \
teniendo 5 oportunidades. \n \
           > El jugador tendrá diferentes coordenadas para elegir donde patear, \
y el arquero intentará atajarlos. \n \
           > En cada nivel el arquero aumentará \
su tamaño generando más dificultad para el jugador. \
           \n\n\t MUCHA SUERTE Y A GOLEAR!")

def mostrarInicial():
    print()
    print("1. Jugador vs la maquina ")
    print("2. Jugador vs Jugador ")
    print("3. Mostrar Ranking")
    print("4. Salir")

def verificarEleccion():
    eleccion = input("\n> Ingrese que desea jugar : ")
    while eleccion != "1" and eleccion != "2" and eleccion != "3" and eleccion != "4":
        print("\n INGRESASTE UNA ELECCION INVALIDA \n")
        eleccion = input("\n> Ingrese que desea jugar : ")
    return int(eleccion)

def mostrarArco(a):
    lista = []
    k = 0
    for i in range(len(a[0])):
        lista.append(i)
        lista.append("")
    print("   ", *lista,)
    print("  ", " - " * len(a[0]))
    for f in a:
        print(k, end=" ")
        print("|", end="")
        k += 1
        for c in f:
            print(f" {c} ", end="")
        print("|")


def generarArco():
    f = 4 
    c = 6
    m = [ [" "] * c for i in range(f) ]
    return m

def limpiarArco(arco):
    for i in range(len(arco)):
        for j in range(len(arco[0])):
            arco[i][j] = " "

def ingresarBalon(f, c, tabla,arco):
    if arco[f][c] == "x":
        print("\n ATAJADA ")
        tabla.append("X")
    else:
        arco[f][c] = "o"
        print("\n GOOOOOOOOOOOOOOOL ")
        tabla.append("O")

def obtenerMayorCoordenada(coordenadas):
    maximo = 0
    claveMaxima = tuple()
    for clave, valor in coordenadas.items():
        if valor > maximo:
            maximo = valor
            claveMaxima = clave

    return claveMaxima

def ingresarArquero(f, c, arco, arquero):
    for i in range(len(arquero)):
        for k in range(len(arquero[0])):
            arco[f][c] = "x"
            c += 1
        f += 1
        c -= k + 1

def coordenadasArquero(arco, arquero, coordenadas):
    if len(coordenadas) == 0:
        filaI = random.randint(0, len(arco) - len(arquero))
        columnaI = random.randint(0, len(arco[0]) - len(arquero[0]))
        print(" entro al random ")
        ingresarArquero(filaI, columnaI, arco, arquero)
    else:
        print(" entro al IA ")
        f, c = obtenerMayorCoordenada(coordenadas)

        if c >= 5:
            c -= 1
        if f > (len(arco) - len(arquero)):
            print(f, len(arquero), len(arco))
            f -= (len(arquero) - 1)
            print(f)
        ingresarArquero(f, c, arco, arquero)

def agregarCoordenada(fila, columna, coordenadas):

    if (fila, columna) not in coordenadas.keys():
        coordenadas[(fila, columna)] = 1
    else:
        coordenadas[(fila, columna)] += 1

def validarCoordenada():
    fila = input(" Ingrese la fila: ")
    columna = input(" Ingrese la columna: ")

    while not fila.isdigit() or not columna.isdigit(): 
        print("\n Datos invalidos, ingrese numeros \n")
        fila = input(" Ingrese la fila: ")
        columna = input(" Ingrese la columna: ")

    fila = int(fila)
    columna = int(columna)
    return fila, columna

def turno(jugador, tabla, arco, arquero, coordenadas):
    print()
    print(f"\n TURNO DE : {jugador}")
    coordenadasArquero(arco,arquero, coordenadas)
    try:
        fila, columna = validarCoordenada()
        assert fila >= 0 or columna >= 0
        ingresarBalon(fila,columna,tabla,arco)

    except (AssertionError, IndexError):
        print("\nPateaste Afuera!")
        tabla.append("X")

    if fila < len(arco) and columna < len(arco[0]):
        agregarCoordenada(fila, columna, coordenadas)

    mostrarArco(arco)
    limpiarArco(arco)

def jugar(jugador, tabla, arco, arquero, coordenadas):
    puntaje = 0
    patadas = 0
    for i in range(3):
        print(f"\n\t NIVEL : {i + 1}")
        while patadas < 5:
            turno(jugador, tabla, arco, arquero, coordenadas)
            print(f" {tabla} ")
            patadas += 1
        puntaje += (10 * tabla.count("O"))
        print(f"\nPuntaje : {puntaje}")

        if tabla.count("X") >= 3:
            print("\n ERRASTE 3 TIROS, GAME OVER \n")
            break
    
        tabla.clear()
        arquero.append(["x", "x"])
        patadas = 0

    return puntaje

#Programa Principal
arquero = [["x", "x"],["x", "x"]]
arco = generarArco()
mostrarReglas()
mostrarInicial()
mostrarArco(arco)
rankings = lecturaArchivo()
eleccion = verificarEleccion()
# while eleccion != 4:
#     if eleccion == 1:
#         # Codigo de la maquina vs el jugador
#         jugador = input("> Ingrese su nombre : ")
#         tabla = []
#         coordenadas = dict()
#         puntaje = jugar(jugador, tabla, arco, arquero, coordenadas)
#         print(f"\n > Su puntaje actual es : {puntaje}")
#         sumarPuntaje(jugador, puntaje, rankings)

#     elif eleccion == 2:
#         # Codigo de jugador vs jugador
#         # jugador1 = input("> Ingrese su nombre : ")
#         # jugador2 = input("> Ingrese su nombre : ")
#         # tabla1 = []
#         # tabla2 = []
#         # coordenadas1 = dict()
#         # coordenadas2 = dict()
#         pass


#     elif eleccion == 3:
#         mostrarRanking(rankings)

#     ordenarDiccionario(rankings)
#     arquero = [["x", "x"],["x", "x"]]
#     mostrarInicial()
#     eleccion = verificarEleccion()

escrituraArchivo(rankings)


