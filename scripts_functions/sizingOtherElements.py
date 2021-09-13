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



# Outputs: 
Dataframe protecciones necesarias
    tipo
    configuracion

"""

def calculoProtecciones(corrienteSalidaPaneles, corrienteSalidaInversor, proteccionesDF):




    return [proteccionnecesariaDF]


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