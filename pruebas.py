# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:11:19 2021

@author: crisd
"""


import pandas as pd
import math 
import numpy as np
import time


DatosInversores = {'referencia':['Huawei 20','Huawei 60','Fronius 15','Fronius 10','CPS 30', 'CPS 10'],'nominal_power':[20,60,15,10,30,10],'precio':[11875000,17125000,12950000,9675000,12750000,3000000],'fabricante':['Huawei','Huawei','Fronius','Fronius','CPS','CPS']}
inversores_1= pd.DataFrame(data=DatosInversores)

inversores_2= inversores_1.sort_values('nominal_power')



def FiltAndOrg (dataframe, potenciaRequerida, fabricante_in):
    
    dataframeNuevo=dataframe
    dataframeNuevo['distancia']=pd.Series()
    for i in dataframeNuevo.index:
        if dataframeNuevo['fabricante'][i]!=fabricante_in and fabricante_in != 'any':
            dataframeNuevo= dataframeNuevo.drop([i],axis=0)
            continue
        distancia= abs (potenciaRequerida -dataframeNuevo['nominal_power'][i])
        dataframeNuevo['distancia'][i]= distancia

    dataframeNuevo= dataframeNuevo.sort_values('distancia')
    final=max(dataframeNuevo.index)
    vector=np.arange(0,final+1,1)
    dataframeNuevo.index= [vector]
    return dataframeNuevo



def calculoPotenciaNuevaNecesaria( potenciaNecesaria, potenciaNominalInversor, costoInversor):
    # recibe
    cantidadInversores = math.floor(potenciaNecesaria / potenciaNominalInversor)
    if(cantidadInversores < 1):
        cantidadInversores = math.ceil(potenciaNecesaria / potenciaNominalInversor)
    potenciaNuevaNecesaria = potenciaNecesaria - cantidadInversores * potenciaNominalInversor
    costoLote = cantidadInversores * costoInversor
    return [potenciaNuevaNecesaria, cantidadInversores, costoLote]




"""
def prueba (dataframe, potenciaRequerida, fabricante_in):
    
    dataframeNuevo=dataframe
    dataframeNuevo['distancia']=pd.Series()
    for i in dataframeNuevo.index:
        if dataframeNuevo['fabricante'][i]!=fabricante_in and fabricante_in != 'any':
            dataframeNuevo= dataframeNuevo.drop([i],axis=0)
            continue
        distancia= abs (potenciaRequerida -dataframeNuevo['nominal_power'][i])
        dataframeNuevo['distancia'][i]= distancia

    dataframeNuevo= dataframeNuevo.sort_values('distancia')
    final=max(dataframeNuevo.index)
    vector=np.arange(0,final+1,1)
    dataframeNuevo.index= [vector]
    return final, distancia

"""







"""
dataframe= inversores_1
potenciaRequerida=15
fabricante_in= 'Huawei'


dataframeNuevo=dataframe
dataframeNuevo['distancia']=pd.Series()
for i in dataframeNuevo.index:
    if dataframeNuevo['fabricante'][i]!=fabricante_in and fabricante_in != 'any':
        dataframeNuevo=dataframeNuevo.drop([i],axis=0)
        continue
    distancia= abs (potenciaRequerida -dataframeNuevo['nominal_power'][i])
    dataframeNuevo['distancia'][i]= distancia
DataframeNuevo= dataframeNuevo.sort_values('distancia')
final=max(dataframeNuevo.index)
vector=np.arange(0,final+1,1)
dataframeNuevo.index= [vector]

"""






"""

def cuenta_regresiva(numero):
     numero -= 1
     if numero > 0:
         print (numero)
         time.sleep(1)
         cuenta_regresiva(numero)
     else:
         print ("Boooooooom!")
     print ("Fin de la función", numero)

cuenta_regresiva(5)
"""


def configInv(referenciaInversor,potenciaRequerida, dataframe, CP, MT, ConfigP, MConfig):
    """
    CP=Costo Parcial, poner en caso general el costo del primer lote de inversores
    MT=Mejor Total 
    ConfigP= Configuración Parcial 
    MConfig= Mejor Configuración
    """
    ind_ref=int (dataframe.loc[dataframe['referencia']== referenciaInversor].index.values)
    #CP=CP +dataframe['precio'][ind_ref] #Costo Parcial 
    fabricante=dataframe['fabricante'][ind_ref]
    nuevoDataframe= FiltAndOrg(dataframe, potenciaRequerida, fabricante ) #Debe filtrar también según potenciaNomianl (Dejar solamente los que sean de menor potencia nominal a la referencia de entrada )
    for i in nuevoDataframe.index:
        
        potenciaNominalInversor=nuevoDataframe['nominal_power'][ind_ref]
        costoInversor=nuevoDataframe['precio'][ind_ref]
        
        [potenciaNecesariaNueva, CantidadNecesaria, Costo]=calculoPotenciaNuevaNecesaria(potenciaRequerida, potenciaNominalInversor, costoInversor) #Salida: potenciaNueva, cantidad inversores, costo. 
        CP=CP+Costo
        if potenciaNecesariaNueva <= potenciaRequerida and CP <= MT:
            MT=CP
            
        
        
    
    
    
    return fabricante





