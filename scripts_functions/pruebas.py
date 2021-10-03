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
    "sizePVMod":[],
    "areaPVMod":[2, 1.05, 0.03],
    "araTotSyst":[]
}

solarInverter = {
    #input
    "powerNeed":[],

    #output
    "ref":[],           #referencias de inversores seleccionados
    "invAmount":[],     #cantidad por referencia
    "totInvAmount": 2,  # cantidad total de inversores
    "cost":[], 
    "iInput":[12, 26, 38], 
    "polesperInput":[1, 2, 1], 
    "vInput":[], 
    "iOutput":[54, 90], 
    "totIoutput": None,
    "vOutput":[200, 75, 40], 
    "pOutput":[], 
    "pInput":[], 
    "MPPTusados":[]
}

otherElements = {
    "pvWires":[],               # 
    "facilityWires":[],         # 
    "pvProtections":[],         # 
    "facilityProtections":[],   # 
    "pvDPS":[],                 # 
    "facilityDPS":[],           # 
    "meter":[],                 # 
    "structData":[],            # 
    "pipeData":[],              # 
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
    "TipodeCubierta":1,        # Cubierta Metalica, Teja de Barro, Tipo Suelo(Plancha) (string)
    "cubiertaApta":[],          # Cubierta Apta (la cubierta es apta)(book)
    "buitron":[]                # Existencia de buitron (bool)
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
    metalicStruct
    )

