#import pandas as pd
from sizingOtherElements import *
from ComponentsDB import *

pvModules = {

    #input
    "performanceRatio":None,        # Eficiencia total del sistema (float)
    "ener_Need":None,               # Energia necesaria a suplir con el sistema (float kWh/dia)
    #output
    "vArraymax":125,                # Tension maxima del arreglo de paneles solares (float V)
    "iArray":[12, 26, 38],          # Corriente de cada uno de los array (list of floats A)
    "nArray":2,                     # Cantidad de arrays (int N)
    "pvModperArray":[20, 35, 50],   # Cantidad de modulos por cada array (list of ints N)
    "amountPVMod":63,               # Cantidad total de modulos (int N)
    "refPVMod":None,                # Referencia del panel (string )
    "iPVMod":[],                    # Corriente de salida del panel seleccionado (float A)
    "vPVMod":[],                    # Tension de salida del panel seleccionado (float V)
    "sizePVMod":[2, 1.05, 0.03],    # dimensionaes del panel seleccionado (list of floats mm)
    "areaPVMod":[],                 # area del panel seleccionado (float m2)
    "areaTotSyst":[]                # area total de todos los paneles (float m2)
}

solarInverter = {
    #input
    "powerNeed":[],                 # Potencia necesaria antes de dimensionamiento (float kW)
    #output
    "ref":[],                       # Referencias de inversores seleccionados (list of strings)
    "invAmount":[],                 # Cantidad por referencia (list of ints)
    "totInvAmount": 2,              # Cantidad total de inversores (int)
    "iInput":[12, 26, 38],          # Entrada de corriente del inversor, (list of floats)
    "polesperInput":[1, 2, 1],      # Cantidad de polos por entrada de corriente (list of ints)
    "vInput":[],                    # Tension de entrada (list of floats)
    "iOutput":[54, 90],             # salida de corrientes del inversor, (list of floats)
    "totIoutput": None,             # suma de la corriente de salida (float)
    "vOutput":[200, 75, 40],        # tensiones de salida (list of floats)
    "pOutput":[],                   # potencias de salida (list of floats)
    "pInput":[]                     # potencias de entrada (list of floats)
}

otherElements = {
    "pvWires":[],                   # Conductores del lado DC (list [referencias string, metraje float m2])
    "facilityWires":[],             # Conductores del lado AC (list [referencias string, metraje float m2])
    "pvProtections":[],             # breakers lado DC (list[referencia string, cantidad int N])
    "facilityProtections":[],       # breakers lado AC (list[referencia string, cantidad int N])
    "pvDPS":[],                     # DPS lado DC (string)
    "facilityDPS":[],               # DPS lado AC (string)
    "meter":[],                     # referencia del medidor y CT si requiere (list (referencia Medidor, referencia CT))
    "structData":[],                # referencias y cantidades de la estructura (list (referencia, metraje m2))
    "pipeData":[],                  # referencias, tipo y metraje de la tuberia (list (referencia, metraje m2))
    "InstalationData":[],           # Tiempo de instalacion estimado (float)
    "wires":[]                      # Estructura del cableado (list (referencias metraje float m2, referencias metraje float m2))
}

siteFeatures ={
    "distTab_Cont":3,               # Distancia del tablero de inversores al contador (float)
    "distPv_Tab":15,                # Distancia del tablero de inversores a los array (float)
    "availableArea":None,           # Area disponible (float)
    "HSP":None,                     # Horas solares Pico (float)
    "coords":[],                    # Coordenadas del proyecto (list)
    "ACConfig":"3P+N",              # "TAG 3F+N, Cantidad de Fases" (string)
    "TipodeCubierta":1,             # Cubierta Metalica, Teja de Barro, Tipo Suelo(Plancha) (int)
    "cubiertaApta":None,            # Cubierta Apta (la cubierta es apta)(bool) 
    "buitron":0                     # Existencia de buitron (bool)
}

dimensionamiento = {
    "pvModules":pvModules,             # Estructura de modulos solares
    "solarInverter":solarInverter,     # Estructura de la seleccion del inversor
    "siteFeatures":siteFeatures,       # Estructura de las caracteristicas del sitio
    "otherElements":otherElements      # Estructura que almacena la informacion de otros elementos
}


status = otherElementsSising( 
    dimensionamiento, 
    proteccionesAC, proteccionesDC, DPS_AC, DPS_DC, 
    WiresISO, WiresDCIso, 
    bdMeters, dbCT, 
    metalicStruct, clayTileStruct, metalicStruct, 
    EMT
    )

