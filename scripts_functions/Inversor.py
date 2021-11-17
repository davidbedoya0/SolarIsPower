# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 20:41:37 2021

@author: crisd
"""

class Inversor :
    
    def __init__(self,referencia, fabricante, costo, pN,maxVin,iMppt,iMax,startVoltage,ratedVoltage,nMppt,maxPout,vOut, fases, eficiencia):
        self.referencia=referencia
        self.fabricante=fabricante
        self.costo=costo
        self.potenciaNominal=pN
        self.maxVin=maxVin
        self.iMppt=iMppt
        self.iMax= iMax #
        self.startVoltage=startVoltage
        self.ratedVoltage=ratedVoltage
        self.nMppt= nMppt
        self.maxPout=maxPout
        self.vOut= vOut
        self.fases=fases
        self.eficiencia=eficiencia
        self.codigo = fabricante.upper().strip()+"_"+str(int(pN))+"F"+str(int(fases))
        self.distancia=None
        self.potenciaNecesariaConfiguracion=None
        self.costoConfiguracion=None
        self.configuracion=None
    
    def __str___(self):
        return self.codigo
    
    
 