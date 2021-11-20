# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 15:23:04 2021

@author: crisd
"""

from ConfiguracionInversor import ConfiguracionInversor
from ListaInversores import ListaInversores

class ConfiguracionesInversores:
    
    def __init__(self, potenciaNecesaria, fases ):
        
        #Validacion de argumentos
        assert potenciaNecesaria > 0, "La potencia necesaria ingresada debe ser mayor que 0"
        assert fases in [1,2,3], "Ingrese un numero de fases entre 1 y 3"
        
        self.potenciaNecesaria= potenciaNecesaria
        self.fases=fases
        self.listaInversores= ListaInversores(direccion= "inversores.csv").FiltrarOrganizar(potenciaNecesaria, fases=fases)
        self.configuraciones=self.GenerarConfiguraciones()
        self.seleccion = self.SeleccionarConfiguracionEconomica()
        
        
        
    
    
    def GenerarConfiguraciones (self):
        
        configuraciones= []
        
        for inversor in self.listaInversores.lista:
            configuracion = ConfiguracionInversor(inversor,self.potenciaNecesaria,self.fases,self.listaInversores)
            configuraciones.append(configuracion)
        
        #Organizo las configuraciones por costo ?????
        
        return configuraciones
    
    
    
    def SeleccionarConfiguracionEconomica(self):
        
        listaCostos=[self.configuraciones[i].costo for i in range(len (self.configuraciones))]
        minimo=listaCostos.index(min(listaCostos))
        configMin=self.configuraciones[minimo]
        
        return configMin
    
    
    def SeleccionarConfiguracion (self,codigo): 
        
        listaCodigos=[self.configuraciones[i].codigoInversorPrincipal for i in range(len(self.configuraciones))]
        eleccion= listaCodigos.index(codigo)
        configuracionElegida= self.configuraciones[eleccion]
        self.seleccion = configuracionElegida
        
        
        
        
if __name__ == '__main__':
    pruebaClase= ConfiguracionesInversores(120,3)
    listaInversoresTest=pruebaClase.listaInversores
    
    