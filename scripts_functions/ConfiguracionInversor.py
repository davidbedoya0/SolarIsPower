# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 23:05:10 2021

@author: crisd
"""
from Inversor import Inversor
from ListaInversores import ListaInversores
import math
import pandas as pd

class ConfiguracionInversor:
    
    def __init__(self, inversor: Inversor, potenciaNecesaria,fases ,listaInversores: ListaInversores= None):
        self.inversor= inversor 
        self.potenciaNecesaria= potenciaNecesaria
        if listaInversores is not None: #Si se ingresa un lista de inversores, se utiliza esa 
            self.listaInversores= listaInversores
        if listaInversores is None: #Si no se utiliza una lista de inversores, se utiliza el CSV de inversores que se tiene por defecto
            self.listaInversores= ListaInversores('inversores.csv')
        self.fases=fases
        self.config, self.costo= self.ConfigurarInversor ()
        self.configCodigos=None
        self._GenerarConfiguracionVisible()
        self.capacidad= self.CapacidadInversores()
        self.codigoInversorPrincipal= inversor.codigo
        
        
        
        
    
    def ConfiguracionParcial(self,potenciaNecesaria=None,inversor:Inversor = None,cantidadInversores=None):
        if inversor is None: #Se puede calcular la configuracion parcial con el inversor principal o con cualquier otro 
            inversor= self.inversor
        if potenciaNecesaria is None : #Se puede calcular la configuracion parcial con la potencia Necesaria principal o con cualquier otra por ejemplo para calcular un segundo inversor ya se ha cambiado la potencia necesaria
            potenciaNecesaria= self.potenciaNecesaria
        if cantidadInversores is None:
            cantidadInversores=math.floor(potenciaNecesaria/inversor.potenciaNominal)
        if cantidadInversores <1:
            cantidadInversores=1
        potenciaNuevaNecesaria=potenciaNecesaria-cantidadInversores*inversor.potenciaNominal
        if potenciaNuevaNecesaria < 0:
            potenciaNuevaNecesaria= 0
        costo=cantidadInversores * inversor.costo
        return potenciaNuevaNecesaria, cantidadInversores, costo
    
    
    def ConfigurarInversor (self, inversor: Inversor=None, listaInversores: ListaInversores =None,potenciaRequerida=None, configL=None, CP=None, Mconfig=None, MT=None):
        inversor= self.inversor
#        print ("inversor analizado: "+ inversor.codigo)
        if potenciaRequerida is None :
            potenciaRequerida=self.potenciaNecesaria
        if inversor is None :
            inversor=self.inversor
        if listaInversores is None:
            listaInversores= self.listaInversores
            
        if CP is None: 
            potenciaRequerida,cantidadInversores, CP= self.ConfiguracionParcial(potenciaRequerida,inversor)
            configL= [[inversor],[cantidadInversores]] #se puede usar inversor, inversor.codigo, inversor.referencia
            if potenciaRequerida == 0 :
                inversores=configL[0]
                cantidades=configL[1]
                configL=pd.DataFrame({'Inversor':inversores, 'Cantidad': cantidades})
                return configL, CP
        listaUsada=listaInversores.FiltrarOrganizar(potenciaRequerida=potenciaRequerida,fabricante=inversor.fabricante, potenciaNominalMax=inversor.potenciaNominal,
                                         fases=self.fases)
        CP_c=CP
        configL_c=[x[:]for x in configL]
        epsilon=0
        for inversorNuevo in listaUsada.lista:
            CP=CP_c
            configL=[x[:]for x in configL_c]
            potenciaNecesariaNueva,cantidadNecesaria, costo= self.ConfiguracionParcial(potenciaRequerida, inversorNuevo)
            CP+=costo
            if inversorNuevo in configL[0]:#se puede usar inversor, inversor.codigo, inversor.referencia
                indexx=configL[0].index(inversorNuevo)#se puede usar inversor, inversor.codigo, inversor.referencia
                configL[1][indexx]+=cantidadNecesaria
            else:
                configL[0].append(inversorNuevo)#se puede usar inversor, inversor.codigo, inversor.referencia
                configL[1].append(cantidadNecesaria)
            if MT is None and potenciaNecesariaNueva <= epsilon:
                MT=CP
                Mconfig=configL
            elif potenciaNecesariaNueva<= epsilon and CP <=MT:
                MT=CP
                Mconfig=configL
            elif MT is not None and CP>MT:
#                print ('Configuracion mas costosa')
                continue
            elif potenciaNecesariaNueva>epsilon:
                Mconfig, MT= self.ConfigurarInversor(inversorNuevo,listaUsada,potenciaNecesariaNueva,configL,CP,Mconfig,MT)
        
#        Mconfig=pd.DataFrame(dict(zip(Mconfig[0],Mconfig[1])))
        inversores=Mconfig[0]
        cantidades=Mconfig[1]
        Mconfig=pd.DataFrame({'Inversor':inversores, 'Cantidad': cantidades})
        return Mconfig, MT
    
    def _GenerarConfiguracionVisible (self):
        config=self.config
        codigos=[]
        cantidades=[]
        for i in config.index:
            codigo= config['Inversor'][i].codigo
            cantidad=config['Cantidad'][i]
            codigos.append(codigo)
            cantidades.append(cantidad)
        df= pd.DataFrame({'Inversor':codigos, 'Cantidad':cantidades})
        self.configCodigos= df
    
    def CapacidadInversores (self): #kW :
        config= self.config
        potencia= 0
        for i in config.index:
            potencia+=config['Inversor'][i].potenciaNominal*config['Cantidad'][i]
        return potencia
        
if __name__ == '__main__':
    inversorTest= ListaInversores("inversores.csv").lista[8]
    pruebaConfiguracionInversor= ConfiguracionInversor (inversorTest,120,3)