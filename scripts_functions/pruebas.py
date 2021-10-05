#import pandas as pd
from sizingOtherElements import *
from ComponentsDB import *

pvModules = {

    #input
    "performanceRatio":[],
    "ener_Need":[],
    #output
    "vArraymax":125,
    "iArray":[12, 26, 38],
    "nArray":2,           #
    "pvModperArray":20,
    "amountPVMod":63,
    "refPVMod":[],
    "iPVMod":[],
    "vPVMod":[],
    "sizePVMod":[2, 1.05, 0.03],
    "areaPVMod":[],
    "araTotSyst":[]
}

solarInverter = {
    #input
    "powerNeed":[],             # Potencia necesaria antes de dimensionamiento (float)
    #output
    "ref":[],                   # Referencias de inversores seleccionados (list of strings)
    "invAmount":[],             # Cantidad por referencia (list of ints)
    "totInvAmount": 2,          # Cantidad total de inversores
    "iInput":[12, 26, 38],      # Entrada de corriente del inversor, (list of floats)
    "polesperInput":[1, 2, 1],  # Cantidad de polos por entrada de corriente (list of ints)
    "vInput":[],                # Tension de entrada (list of floats)
    "iOutput":[54, 90],         # salida de corrientes del inversor, (list of floats)
    "totIoutput": None,         # suma de la corriente de salida (float)
    "vOutput":[200, 75, 40],    # tensiones de salida (list of floats)
    "pOutput":[],               # potencias de salida (list of floats)
    "pInput":[],                # potencias de entrada (list of floats)
    "MPPTusados":[]             # cantidad de MPPT usados por inversor (list of ints)
}

otherElements = {
    "pvWires":[],               # 
    "facilityWires":[],         # 
    "pvProtections":[],         # 
    "facilityProtections":[],   # 
    "pvDPS":[],                 # 
    "facilityDPS":[],           # 
    "meter":[],                 # referencia del medidor y CT si requiere
    "structData":[],            # referencias y cantidades de la estructura
    "pipeData":[],              # referencias, tipo y metraje de la tuberia
    "InstalationData":[],       # 
    "wires":[]                  # Estructura del cableado
}

siteFeatures ={
    "distTab_Cont":3,           # Distancia del tablero de inversores al contador (float)
    "distPv_Tab":15,            # Distancia del tablero de inversores a los array (float)
    "availableArea":[],         # Area disponible (float)
    "HSP":[],                   # Horas solares Pico (float)
    "coords":[],                # Coordenadas del proyecto (list)
    "ACConfig":"3P+N",          # "TAG 3F+N, Cantidad de Fases" (string)
    "TipodeCubierta":1,         # Cubierta Metalica, Teja de Barro, Tipo Suelo(Plancha) (string)
    "cubiertaApta":[],          # Cubierta Apta (la cubierta es apta)(book)
    "buitron":0                # Existencia de buitron (bool)
}

dimensionamiento = {
    "pvModules":pvModules,             # Estructura de modulos solares
    "solarInverter":solarInverter,     # Estructura de la seleccion del inversor
    "siteFeatures":siteFeatures,       # Estructura de las caracteristicas del sitio
    "otherElements":otherElements      # Estructura que almacena la informacion de otros elementos
}



status = otherElementsSising( dimensionamiento, 
    proteccionesAC, 
    proteccionesDC, 
    DPS_AC, 
    DPS_DC, 
    WiresISO,
    WiresDCIso, 
    bdMeters, 
    dbCT, 
    metalicStruct, 
    clayTileStruct, 
    metalicStruct, 
    EMT
    )

