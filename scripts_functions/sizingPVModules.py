"""

# Descripcion

# Inputs Outputs

"""

import pandas as pd
import math 
import numpy as np

"""

# Descripcion

# Inputs Outputs

"""


"""DATOS PARA PRUEBAS
ejemploInversor = {'referencia': ['Huawei 20','Huawei 60'], 
                   'cantidad': [2,1],
                   'potenciaNominal':[20,60],# ,[kW], 
                   '#MPPTs' :[ 4 , 6], 
                   'corrienteMppt': [26,22], 
                   'maxInputVoltage':[750,1100],#[V],
                   'maxPvInput': [30000,None],
                   'maxAcOutput':[22000,66000],#[W],
                   'eficiencia': [0.98 , 0.98]}

ejemploPaneles= {'referencia': ['465 Wp Jinko Tiger Mono','535 Jinko Mono'],
                  'Wp': [465,535], 
                  'Vmp':[43.18,40.63],
                  'Imp':[10.8,13.17],
                  'Isc':[11.59,13.79],
                  'Voc':[51.92,49.38],
                  'area':[2.275,2.58],
                  'precio':[488250,561750],
                  'dimensiones': ['2205x1032x35','2274x1174x35']}


DfInversores= pd.DataFrame(data=ejemploInversor)
DfPaneles= pd.DataFrame (data=ejemploPaneles)

"""





def mejorSerie (nPaneles,nSerieMax):
    #Entradas: nPaneles = Numero de paneles necesarios 
    #          nSerieMax= Numero de paneles en serie maximos soportados por el inversor 
    #Salidas: nPanelesSerie
    vector = np.arange(nSerieMax, 0, -1)
    for i in vector :
        mod = nPaneles % i
        if mod ==0:
            serie = i
            paralelo = nPaneles/i
            print (serie, "paneles en serie , y ", paralelo, " arreglos en paralelo", ", y un total de ", serie*paralelo)
            return serie , paralelo
        

def configurarPaneles (nPaneles, nSerieMax, limiteCorriente ,corrientePanel,disminuir: bool = False ):
    
    nSerie, nParalelo = mejorSerie(nPaneles, nSerieMax) 
    corrienteParalelo = nParalelo*corrientePanel
    while nSerie <nParalelo or corrienteParalelo > limiteCorriente: 
        if disminuir:
            nPaneles -=1
        else : 
            nPaneles += 1
        nSerie, nParalelo = mejorSerie(nPaneles, nSerieMax)
        corrienteParalelo = nParalelo*corrientePanel
    return nSerie, nParalelo



def calPanelesSoportados (inversor, panel):
    
    #Información necesaria del panel 
    Voc= panel['Voc'] #Voltaje de circuito abierto
    Imp= panel['Imp'] #Corriente de punto de maxima potencia del panel
    Wp= panel['Wp'] #Potencia pico nominal
    
    #Información necesaria del inversor
    maxAcOutput = inversor['maxAcOutput'] #Maxima potencia de salida del inversor 
    maxInputVoltage= inversor['maxInputVoltage'] #Maximo voltaje de trabajo admitido por el inversor 
    
    ef= inversor['eficiencia'] #Eficiencia Inversor 
    
    #Calculamos la potencia DC maxima convertible por el inversor 
    maxDcInput= (1-ef)*maxAcOutput+maxAcOutput
    
    #Cálculo de maximo numero de paneles para maxDcInput
    maxPan=math.floor(maxDcInput/Wp)
    
    #Cálculo de maximo numero de paneles en serie 
    maxPanSerie=math.floor(maxInputVoltage/Voc)
    
    print ("Este inversor soporta máximo ", maxPan ," paneles, con una potencia total de ",maxPan*Wp , "Wp, y ",maxPanSerie," paneles en serie como máximo" )
    return maxPan, maxPanSerie






def configuracionPanelesEnInversor (inversor, panel, nPn): #Funcion Final
    
    Imp= panel['Imp'] #Corriente de punto de maxima potencia del panel
    corrienteMppt=inversor['corrienteMppt']
    nMppt= inversor ['#MPPTs']
    limiteCorrienteInversor= corrienteMppt*nMppt
    nPsi, nPMaxS  = calPanelesSoportados(inversor, panel)
    condicion = nPsi<nPn
    if condicion :
        nPu=nPsi
        nS,nP = configurarPaneles(nPu, nPMaxS,limiteCorrienteInversor,Imp,True)
    else: 
        nPu=nPn
        nS,nP = configurarPaneles(nPu,nPMaxS ,limiteCorrienteInversor,Imp)
    nPn_new=nPn-nPu
    return nS, nP, nPn_new


""" #PRUEBA
#valores sugeridos= de paneles necesarios: 61,62, 125,124

inversorSeleccionadoo= DfInversores.iloc[1]
panelseleccionado= DfPaneles.iloc[1]


PanelesSerie, PanelesParalelo, Restantes = configuracionPanelesEnInversor(inversorSeleccionadoo, panelseleccionado,61)


"""

