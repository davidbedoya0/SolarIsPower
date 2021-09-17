
import numpy as np

"""

# Descripcion. Calcula la configuracion de las protecciones, el tablero, cableado, 
estructura,sistemas de medicion, adquisicion, tiempo horas hombre y horas 
de ingenieria.

# Inputs 
Limites Potencia
Limites Tension
Limites Corriente
Cantidad de paneles
Configuracion de paneles
Cantidad inversores 
Configuracion inversores

# Outputs
    Cantidad de protecciones
accesoreios protecciones 
Cantidad de tableros
Accesorios Tableros 
    Seleccion de cable
    Cantidad de cable
    Referencia sistema de medicion 
Accesorios sistemas de medicion
Sistema de adquisicion
Accesorios sistema de adquisicion
    Tiempo Horas hombre
Tiempo horas hombre ingenieria
    elementos Estructura
    tuberia


"""

def otherElementsSising():



    return otherElements





"""

# Descripcion: Calcula la proteccion especifica que se necesita en el sistema 
para el lado DC o AC. 

# Inputs: 
Dataframe Protecciones mercado
Corriente salida arreglo paneles
Corriente salida inversores
configuracion



# Outputs: 
Dataframe protecciones necesarias
    tipo
    configuracion

"""

def calculoProtecciones(corrienteSalidaPaneles, corrienteSalidaInversor, proteccionesDF):

    # Breaker Paneles
    breakerDC = buscarProteccionCercana(proteccionesDF, corrienteSalidaPaneles)


    return [proteccionnecesariaDF]


def buscarProteccionCercana(df, i_fail, config):

    # convierte la columna de corriente en un array numpy
    ibreakers = df["corriente"]

    # crea un array con el valor de la corriente del panel
    iPanelArr = [i_fail] * len(ibreakers)

    # calcula la diferencia entre los dos paneles
    diffI = [e1 - e2 for e1, e2 in zip(ibreakers, iPanelArr)]

    #Inicializa las variables de diferencia e indicador
    breakerCercano = 1e6
    iCurr = 1e6
    lowV = 1e6

    # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
    for i, val in enumerate(diffI):
        # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
        if breakerCercano > val and val > 0:
            print(str(config["fases"]) + " AND " + str(df["Polos"][i]) + "\n")
            print(str(config["Tension"]) + " AND " + str(df["Tension"][i]) + "\n")
            if config["fases"] == df["Polos"][i] and config["Tension"] < df["Tension"][i]:
                if df["Tension"][i] < lowV:
                    breakerCercano = diffI[i]
                    lowV = df["Tension"][i]
                    iCurr = i
    
    # Se retorna la referencia de la proteccion mas cercana
    if iCurr == 1e6:
        return "No se encontro Breaker Adecuado"
    else:
        return df["referencia"][iCurr]



"""

# Descripcion: Calcula la cantidad total de cable que es necesaria para el proyecto en 
su lado AC y DC.

# Inputs: 
Dataframe cables mercado
Corriente salida arreglo paneles
Corriente salida inversores
Distancia ubicacion tablero - paneles
Area arreglos paneles solares

# Outputs: 
Dataframe cableado necesarias
    tipo
    configuracion
    distancia

"""

def calculoCableado(
    corrienteSalidaPaneles, 
    corrienteSalidaInversor, 
    cableDF, 
    distanciaTab2Array, 
    areaPV):




    return [cablenecesariaDF]




"""

# Descripcion: selecciona el sistema de medicion de energia

# Inputs: 
Tension AC
Corriente AC 
configuracion AC


# Outputs: 
referenciaMedidor

"""

def seleccionMedidor(
    tensionAC, 
    corrienteAC,
    configuracionAC):


    return [refMedidor]



"""

# Descripcion: Calcula el tiempo total de instalacion del proyecto para un trabajador

# Inputs: 
cantidad Tableros
longitud cableado
cantidad modulos PV 
cantidad inversores


# Outputs: 
Timepo horas Hombre

"""

def tiempoinstalacionTotal(
    cantidadTableros, 
    longitudCableado,
    cantidadModulosPV, 
    cantidadInversores):


    return [tiempoInstalacion]





"""

# Descripcion: Calcula el tipo de estructura y la cantidad necesaria

# Inputs: 
Cantidad de paneles
Tipo de techo (Opcional)
dataframe estructura paneles comerciales
Area arreglo


# Outputs: 
dataframe estructura para paneles proyecto

"""

def tiempoinstalacionTotal(
    cantidadTableros, 
    longitudCableado,
    cantidadModulosPV, 
    cantidadInversores):


    return [estructuraPanelesDF]


    
"""

# Descripcion: Calcula la tuberia necesaria desde el punto 

# Inputs: 
distancia tablero paneles
dataframe Cableado utilizado

# Outputs: 
dataframe tuberia

"""

def tiempoinstalacionTotal(
    distanciaTab2Panels, 
    cableadoutilizadoDF):


    return [estructuraPanelesDF]