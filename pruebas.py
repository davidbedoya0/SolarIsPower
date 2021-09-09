# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:11:19 2021

@author: crisd
"""



import pandas as pd
import math
import numpy as np


DatosInversores = {'referencia':['Huawei 20','Huawei 60','Fronius 15','Fronius 10','CPS 30', 'CPS 10'],'nominal_power':[20,60,15,10,30,10],'precio':[11875000,17125000,12950000,9675000,12750000,3000000],'fabricante':['Huawei','Huawei','Fronius','Fronius','CPS','CPS']}
inversores_1= pd.DataFrame(data=DatosInversores)

inversores_2= inversores_1.sort_values('nominal_power')


"""
def FiltAndOrg (dataframe, potenciaRequerida, fabricante_in):
    
    dataframeNuevo=dataframe
    dataframeNuevo['distancia']=pd.Series()
    for i in dataframeNuevo.index:
        distancia= abs (potenciaRequerida -dataframeNuevo['nominal_power'][i])
        dataframeNuevo['distancia'][i]= distancia
        if dataframeNuevo['fabricante'][i]!=fabricante_in and fabricante_in != 'any':
            dataframeNuevo= dataframeNuevo.drop([i],axis=0)
    dataframeNuevo= dataframeNuevo.sort_values('distancia')
    final=max(dataframeNuevo.index)
    vector=np.arange(0,final+1,1)
    dataframeNuevo.index= [vector]
    return dataframeNuevo


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



