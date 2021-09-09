# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 00:48:51 2021

@author: crisd
"""

import pandas as pd
import math

"""
#Se importa la lista de inversores y se indica que el separador del documento CSV es el punto y coma (;)
inversores_1= pd.read_csv('inversores.csv', sep=';')
"""

DatosInversores = {'referencia':['Huawei 20','Huawei 60','Fronius 15','Fronius 10','CPS 30', 'CPS 10'],'nominal_power':[20,60,15,10,30,10],'precio':[11875000,17125000,12950000,9675000,12750000,3000000],'fabricante':['Huawei','Huawei','Fronius','Fronius','CPS','CPS']}
inversores_1= pd.DataFrame(data=DatosInversores)


def eleccionInversor (potenciaSistema): #Elección por inversor mas cercano en potencia a lo necesario (tiene que ser mayor la nominal del inversor a la necesaria para que funcione)
    mejor = inversores_1['nominal_power'][0]
    indexmejor=0
    for i in inversores_1.index:
        actual=inversores_1['nominal_power'][i]
        criterioActual= actual-potenciaSistema
        criterioMejor=mejor-potenciaSistema
        if criterioMejor <0 and criterioActual > 0:
            mejor=actual
            indexmejor=i
        elif criterioActual>0 and criterioActual < criterioMejor:
            mejor=actual
            indexmejor=i
    refmejor=inversores_1['referencia'][indexmejor]
    return [actual, criterioActual,mejor, criterioMejor, refmejor]




def eleccionInversorCeil (potenciaSistema): #Elección de inversor teniendo en cuenta la cantidad de inversores para cumplir la necesidad y luego elegir el de menor precio total (numeroInversores * precioUnitario)
    inversores_1['cantidadNecesaria']=pd.Series() #Se crea vacia la columna que contendrá el numero de inversores necesarios para suplir la Potencia del Sistema
    inversores_1['precioTotal']=pd.Series() #Se crea vacia la columna que contendra el precio total del arreglo de inversores
    menor=0; #Variable que contendrá el precio total menor 
    refmenor=None; #Variable que contendrá la referencia del precio total menor
    for i in inversores_1.index: #Se recorrerá según el tamaño del DataFrame llamado inversores_1
        potenciaInversor=inversores_1['nominal_power'] [i] #
        precioInversor=inversores_1['precio'] [i]
        cantidadNecesaria= math.ceil(potenciaSistema / potenciaInversor)#Se aproxima hacia arriba la cantidad necesaria
        precioTotal=precioInversor * cantidadNecesaria
        inversores_1['cantidadNecesaria'] [i]= cantidadNecesaria
        inversores_1['precioTotal'] [i]= precioTotal
        
        if menor == 0 or precioTotal < menor :
            menor=precioTotal
            refmenor=inversores_1['referencia'] [i]
    return refmenor, precioTotal, cantidadNecesaria

def eleccionInversorFloor (potenciaSistema): #Elección de inversor teniendo en cuenta la cantidad de inversores para cumplir la necesidad y luego elegir el de menor precio total (numeroInversores * precioUnitario)
    inversores_1['cantidadNecesariaFloor']=pd.Series() #Se crea vacia la columna que contendrá el numero de inversores necesarios para suplir la Potencia del Sistema
    inversores_1['precioTotal']=pd.Series() #Se crea vacia la columna que contendra el precio total del arreglo de inversores
    menor=0; #Variable que contendrá el precio total menor 
    refmenor=None; #Variable que contendrá la referencia del precio total menor
    for i in inversores_1.index: #Se recorrerá según el tamaño del DataFrame llamado inversores_1
        potenciaInversor=inversores_1['nominal_power'] [i] #
        precioInversor=inversores_1['precio'] [i]
        cantidadNecesaria= math.floor(potenciaSistema / potenciaInversor)#Se aproxima hacia arriba la cantidad necesaria
        precioTotal=precioInversor * cantidadNecesaria
        inversores_1['cantidadNecesaria'] [i]= cantidadNecesaria
        inversores_1['precioTotal'] [i]= precioTotal
        
        if menor == 0 or precioTotal < menor :
            menor=precioTotal
            refmenor=inversores_1['referencia'] [i]
    return refmenor, precioTotal, cantidadNecesaria




"""
def eleccionInversorArreglo (potenciaSistema): #Elección de inversor utilizando varias referencias de inversores
    inversores_1['cantidadNecesariafloor']=pd.Series() #Se crea vacia la columna que contendrá el numero de inversores necesarios para suplir la Potencia del Sistema
    inversores_1['precioTotal']=pd.Series() #Se crea vacia la columna que contendra el precio total del arreglo de inversores
    inversores_1['']
    potenciaArreglo=0
    while cp = 0:
        for i in inversores_1.index: #Se recorrerá según el tamaño del DataFrame llamado inversores_1
            potenciaInversor=inversores_1['nominal_power'] [i]
            precioInversor=inversores_1['precio'] [i]
            cantidadNecesariaFloor= math.floor(potenciaSistema / potenciaInversor)#Se aproxima hacia arriba la cantidad necesaria
            if cantidadNecesariaFloor==0:
                cantidadNecesariaFloor=1
                inversores_1['cantidadNecesariaFloor'][i]=cantidadNecesariaFloor
        if potenciaArreglo >= potenciaSistema:
            cp=1
"""
def elegirInversor (potenciaSistema, fabricante): #Función que elige el inversor para suplir la potencia restante del arreglo y que cumpla que sea del mismo fabricante 
    
    
    return 1






def eleccionInversorArreglo (potenciaSistema): #Elección de inversor utilizando varias referencias de inversores
    pInicial=potenciaSistema
    cp=0 #Criterio de parada del while. Será 1 cuando la potencia del arreglo calculado sea mayor o ogual a la esperada inicialmente
    inversores_1['ArregloNecesario']=pd.Series() #Se va ir retroalimentando con un String que diga las cantidades y las refernecias de los inversores necesarios 
    inversores_1['precioArreglo']=pd.Series() #Irá acumulando el precio del arreglo
    num=1 #numero de referenciasd de inversores utilizados 
    inversores_1['CantidadNecesariaInversor1']=pd.Series()
    
    while cp==0:
        if num > 1: #Si se usará mas de 1 inversor dentro del arreglo, crear las columnas que contengan la referencia y la cantidad necesaria de ese inversor 
            inversores_1['Inversor'+str(num)]="" #Se incializa vacia esta columna que contendrá la referencia del inversor numero num
            inversores_1['CantidadNecesariaInversor'+str(num)]=""
        for i in inversores_1.index:
            potenciaInversor=inversores_1['nominal_power'] [i]
            
            cantidadNecesariaFloor= math.floor(potenciaSistema / potenciaInversor)
            capacidadArreglo= cantidadNecesariaFloor*potenciaInversor
            potenciaSistema= potenciaSistema-capacidadArreglo
        if potenciaSistema>=pInicial: #Si ya se cubrió la potencia necesaria se detiene el while 
            cp=1
        else:
            num=num+1

