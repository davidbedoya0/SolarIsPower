# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:03:55 2021

@author: crisd
"""
import pandas as pd
from Panel import Panel

class ListaPaneles:
    
    
    def __init__(self, direccion= None):
        if direccion is None : #Se puede crear una lista de paneles con un archivo que siempre estará por defecto
            direccion="paneles.csv"
        self.direccion= direccion
        self.dataframeOrigen=pd.read_csv(direccion, sep=';', decimal=',')
        self.dataframe=self.dataframeOrigen.dropna(how='all')
        self.lista= self.CrearListaPaneles()
    
    def CrearListaPaneles (self):
        dataframe= self.dataframe
        listaPaneles= []
        for i in dataframe.index: 
            datos= dataframe.iloc[i]
            referencia=datos['referencia']
#            fabricante=datos['fabricante']
            Wp= datos['Wp']
            tipoCelda= datos['tipoCelda']
            Vmp=datos['Vmp']
            Imp=datos['Imp']
            Isc=datos['Isc']
            Voc=datos['Voc']
            dimensiones=datos['dimensiones']
            nCeldas= datos['nCeldas']
            Cpmax=datos['Cpmax']
            Cvoc=datos['Cvoc']
            Cisc=datos['Cisc']
            peso=datos['peso']
            costo=datos['costo']
            
            panel= Panel(referencia,Wp,tipoCelda, Vmp, Imp,Isc, Voc, dimensiones, nCeldas, Cpmax,Cvoc,Cisc,peso, costo)
            
            listaPaneles.append(panel)
        return listaPaneles

if __name__ == '__main__':
    pruebaClase= ListaPaneles('paneles.csv')
    listaTest=pruebaClase.lista
    dfTest=pruebaClase.dataframe