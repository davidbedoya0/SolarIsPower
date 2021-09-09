# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 13:19:53 2021

@author: crisd
"""
import pandas as pd


#Se importa la lista de inversores 
inversores_1= pd.read_csv('inversores.csv', sep=';')


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




##Clase: PanelSolar
class PanelSolar():
    def __init__(self, nombre, potencia):
        self.nombre= nombre # Definimos que el atributo nombre, será el nombre asignado
        self.potencia= potencia # Definimos que el atributo potencia, será la potencia asignada






#Metodo para cuando el cálculo es mediante consumos: Tipo de cáculo (1)
def calPotNec (irradiacion, consumoDia, PF):
    """  Función que calcula la potencia pico minima requerida para suministrar la energía de entrada
             ENTRADAS: irradiacon: promedio diaria (kWh-dia/m2)  
              ConsumoDia: Consumo promedio diario (kWh-dia)
              PF: Performance Ratio, valores de 0 a 1."""
    STC= 1000 #Irradiacion estadnar con las que se dan los valores de Wp a los páneles solares
    potNec=consumoDia/(irradiacion*STC*PF) #Energía necesaria para suministrar el consumoDia
    return potNec

def NumPan (energiaNecesaria, refPan):
    numP=energiaNecesaria/refPan
    return numP



"""
def elecciónInversor (numeroPaneles, potenciaReferenciaPanel):
    potenciaSistema= numeroPaneles * potenciaReferenciaPanel
    mejor = inversores['Potencia Nominal'][0]
    for i in inversores.index:
        

"""

