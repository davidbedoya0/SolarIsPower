# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:38:25 2021

@author: crisd
"""
import re

class Panel:
    
    
    def __init__(self, referencia, Wp, tipoCelda, Vmp, Imp, Isc, Voc, dimensiones, 
                 nCeldas, Cpmax, Cvoc, Cisc,peso, costo,proveedor=None, datasheet=None ):
        
        self.referencia=referencia
        self.Wp= Wp
        self.tipoCelda=tipoCelda
        self.Vmp=Vmp
        self.Imp=Imp
        self.Isc=Isc
        self.Voc=Voc
        self.dimensiones=dimensiones
        self.nCeldas=nCeldas
        self.Cpmax=Cpmax
        self.Cvoc=Cvoc
        self.Cisc=Cisc
        self.peso=peso
        self.costo=costo
        self.area=self.AreaPanel()
        self.proveedor=proveedor
        self.datasheet=datasheet
        
    def AreaPanel(self,dimensiones=None):
        if dimensiones is None :
            dimensiones= self.dimensiones
        dimensiones= re.split('[xX\*]',dimensiones)
        largo= int (dimensiones[0])/1000
        ancho=int (dimensiones[1])/1000
        alto=int (dimensiones[2])/1000
        areaPanel=largo*ancho
        return areaPanel