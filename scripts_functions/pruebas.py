#import pandas as pd
from sizingOtherElements import *
from ComponentsDB import *

pvModules = {

    #input
    "performanceRatio":[],
    "ener_Need":[],
    #output
    "vArray":[],
    "iArray":[],
    "nArray":[2],
    "pvModperArray":[],
    "amountPVMod":[],
    "refPVMod":[],
    "iPVMod":[],
    "vPVMod":[],
    "sizePVMod":[],
    "areaPVMod":[],
    "araTotSyst":[]
}

solarInverter = {
    #input
    "powerNeed":[],

    #output
    "ref":[],           #referencias de inversores seleccionados
    "invAmount":[],     #cantidad por referencia
    "totInvAmount":[],  # cantidad total de inversores
    "cost":[], 
    "iInput":[], 
    "vInput":[], 
    "iOutput":[54], 
    "totIoutput":[],
    "vOutput":[200], 
    "pOutput":[], 
    "pInput":[], 
    "MPPTusados":[]
    
}

otherElements = {
    "pvWires":[],
    "facilityWires":[],
    "pvProtections":[],
    "facilityProtections":[],
    "pvDPS":[],
    "facilityDPS":[],
    "meter":[],
    "structData":[],
    "pipeData":[],
    "InstalationData":[],     
    "wires":[]                  # Estructura del cableado
}

siteFeatures ={
    "distTab_Cont":[],          # Distancia del tablero de inversores al contador
    "distPv_Tab":[],            # Distancia del tablero de inversores a los array
    "availableArea":[],         # Area disponible 
    "HSP":[],                   # Horas solares Pico 
    "coords":[],                # Coordenadas del proyecto 
    "ACConfig":"3P+N",          # "TAG 3F+N, Cantidad de Fases" 
    "TipodeCubierta":[],        # Cubierta Metalica, Teja de Barro, Tipo Suelo(Plancha)
    "cubiertaApta":[],          # Cubierta Apta (la cubierta es apta)
    "buitron":[]                # Existencia de buitron (bool)
}

dimensionamiento = {
    "pvModules":pvModules,             # Estructura de modulos solares
    "solarInverter":solarInverter,         # Estructura de la seleccion del inversor
    "siteFeatures":siteFeatures,          # Estructura de las caracteristicas del sitio
    "otherElements":otherElements          # Estructura que almacena la informacion de otros elementos
}



status = otherElementsSising( dimensionamiento, 
    proteccionesAC, 
    DPS_AC, 
    proteccionesDC, 
    DPS_DC)

