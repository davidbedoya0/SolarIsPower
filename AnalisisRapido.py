# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 00:01:09 2021

@author: crisd
"""

import pandas as pd


#Se importa la lista de inversores y se indica que el separador del documento CSV es el punto y coma (;)
inversores_1= pd.read_csv('inversores.csv', sep=';')

#----------Importar lista de paneles?------------


"""
ENTRADAS INICIALES:
    
    -Tipo de instalación (On grid / Off grid / On grid - Híbrido / On grid hibrido con transferencia)
    -Voltaje de alimentación de la carga (12dc,36dc,48dc,120ac,240ac)
    -Lugar de instalación
    -Temperatura Ambiente 
    -Irradiación 
 
    
   -Tipo de cálculo
      (1) Por Consumos (Minimizar costo de inversión, $/kWh):
           -Tipos de entrada de energía: 
               -Promedio Anual [1]
               -Promedio mensual [2]
               -Promedio diaria [3]
               -Cuadro de cargas (Nombre,Potencia promedio,Horas de uso diarias) [4]
               -Valor fáctura (menos preciso de todos. Suponer tarifa de energía)
     
      (2)  Por Área disponible (Maximizar energía producida, minimizar presupuesto)
      (3)  Por Presupuesto (Maximizar energía generada)
"""




##Clase:PanelSolar
class PanelSolar():
    def __init__(self, nombre, potencia):
        self.nombre= nombre # Definimos que el atributo nombre, será el nombre asignado
        self.potencia= potencia # Definimos que el atributo potencia, será la potencia asignada







"""
FUNCIONES
"""

def calEnerNec (irradiacion , consumoMes , PF ):
    """  Función que calcula la potencia pico minima requerida para suministrar la energía de entrada
    Entradas: irradiacon: promedio diaria (kWh-dia/m2)  
    ConsumoDia: Consumo promedio diario (kWh-dia)
    PF: Performance Ratio, valores de 0 a 1."""
    enerNec=consumoMes/(30*irradiacion*1000*PF)
    return enerNec


def calNumPaneles (energiaNecesaria, potenciaReferenciaPanel, areaPanel):
    numPaneles=round(energiaNecesaria/potenciaReferenciaPanel)
    potenciaSistema= numPaneles* potenciaReferenciaPanel
    areaSistema=numPaneles*areaPanel
    return [numPaneles, potenciaSistema,areaSistema]




def eleccionInversor (potenciaSistema): #Elección por inversor mas cercano en potencia a lo necesario
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
    return refmejor

def eleccionInversor2 (potenciaSistema): #Elección de inversor teniendo en cuenta el precio
    inversores_1[]

