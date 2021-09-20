
import numpy as np
from protectionsDB import *
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

def calculoProtecciones(corrienteSalidaPaneles, corrienteSalidaInversor, config):

    # Crea un nuevo dataframe que contendra todas las protecciones necesarias en el sistema
    proteccionnecesariaDF = pd.DataFrame()
    breakerAC = []
    # Calculo de protecciones de salida
    # Recorre la columna de inversores
    for i, iFalla in config["inversores"]["iFalla"]:
        # Breaker Paneles
        breakerAC.append(buscarProteccionCercana(proteccionesAC, iFalla, config, 0))
    
    proteccionesAC["proteccionDC"] = buscarProteccionCercana(proteccionesDC, corrienteSalidaPaneles)
    proteccionesAC["proteccionAC"] = breakerAC
    

    return [proteccionnecesariaDF]


def buscarProteccionCercana(df, i_fail, config, typeBreaker):

    # convierte la columna de corriente en una lista
    ibreakers = df["corriente"]

    # crea un array con el valor de la corriente del panel
    iPanelArr = [i_fail] * len(ibreakers)

    # calcula la diferencia entre los dos paneles
    diffI = [e1 - e2 for e1, e2 in zip(ibreakers, iPanelArr)]

    #Inicializa las variables de diferencia e indicador
    breakerCercano = 1e6
    iCurr = 1e6
    lowV = 1e6

    # CASO DC 
    if typeBreaker == 1: 
        # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
        for i, val in enumerate(diffI):
            # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
            if breakerCercano > val and val > 0:
                if config["fases"] == df["polos"][i] and config["tension"] < df["tension"][i]:
                    if df["tension"][i] < lowV:
                        breakerCercano = diffI[i]
                        lowV = df["tension"][i]
                        iCurr = i
        # Se retorna la referencia de la proteccion mas cercana
        if iCurr!=1e6:
            return (str(config["stack"]) + " X " + str(df["referencia"][iCurr]))
    # CASO AC 
    else:
        # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
        for i, val in enumerate(diffI):
            # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
            if breakerCercano > val and val > 0:
                if config["fases"] == df["polos"][i]:
                        breakerCercano = diffI[i]
                        iCurr = i
        # Se retorna la referencia de la proteccion mas cercana
        if iCurr!=1e6:
            return (str(config["stack"]) + " X " + str(df["referencia"][iCurr]))
        
    
    # Se retorna el mensaje donde se indica que no se encontro la proteccion adecuada
    if iCurr == 1e6:
        return "No se encontro Breaker Adecuado"


def seleccionDPS(config, DPS_DB, DCoAC):
    
    # extrae la tension de operacion de los string del lado DC
    vString = config["vString"]
    # Inicializa la referencia actual y la diferencia de tension
    currREF = ""
    Vdiffant = 1e6
    # recorre la matriz de referencias de DPS buscando el mas cercano que sea superior
    for i, val in enumerate(DPS_DB["tension"]):
        # calcula la diferencia de tension de la referencia con respecto a la tension del string 
        Vdiff = val - vString
        # Se verifica que la diferencia sea positiva y menor a la anterior diferencia
        if Vdiff < Vdiffant and Vdiff > 0:
            if DCoAC == 1:
                # Se almacena la nueva mejor diferencia
                Vdiffant = Vdiff
                # Se almacena la referencia
                currREF = DPS_DB["referencia"][i]
            else:
                if DPS_DB["polos"][i] == config["fases"]:
                    # Se almacena la nueva mejor diferencia
                    Vdiffant = Vdiff
                    # Se almacena la referencia
                    currREF = DPS_DB["referencia"][i]
    # Se retorna la referencia
    return currREF














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