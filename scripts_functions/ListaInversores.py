# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 20:40:56 2021

@author: crisd
"""
import pandas as pd 
from Inversor import Inversor

class ListaInversores:
    
    def __init__(self,direccion: str = None, lista:list = None , df=None) :
        self.direccion=direccion
        
        if direccion is None :
            direccion= "inversores.csv"
            
        self.dataframeOrigen=pd.read_csv(direccion, sep=';', decimal = ",")
        
        if df is None: #Si no me dan un dataframe como entrada entonces uso el que importo de la direccion y lo filtro
            self.dataframe=self.dataframeOrigen.dropna(how='all') #Se eliminan las filas que tengan todas las columnas como Nan
        if df is not None: #Si me dan el dataframe como entrada uso directamente este
            self.dataframe= df
        if lista is None :  #Si no me dan una lista entonces utilizo el metodo creado para que apartir del dataframe lo cree 
            self.lista= None
            self._CrearListaInversores()
        if lista is not None: #Si me dan un parametro de lista entonces lo utilizo.
            self.lista= lista
#        self.listaFiltrada=None
    
        self.cantidadInversores= len (self.lista)
    
    
    def _CrearListaInversores (self):
        dataframe= self.dataframe
        
        listaInversores= []
        for i in dataframe.index:
            
            datos=dataframe.iloc[i]
            referencia=datos['referencia']
            fabricante=datos['fabricante']
            costo=datos['precio']
            pN=datos['nominal_power']
            maxVin=datos['MaxInputVoltage']
            iMppt=datos['corrienteMPPT']
            iMax=datos['max_Imp_total_limit']
            startVoltage=datos['startVoltage']
            ratedVoltage=datos['ratedVoltage']
            nMppt=datos['#MPPTs']
            maxPout=datos['MaxAcOutput']
            vOut=datos['Output voltage 1']
            fases=datos['phases']
            eficiencia= datos['eficiencia']
            
            inversor= Inversor(referencia,fabricante,costo,pN,maxVin,iMppt,iMax,startVoltage, ratedVoltage,nMppt,maxPout,vOut,fases,eficiencia)
            listaInversores.append(inversor)
            
        self.lista= listaInversores
#        return listaInversores
    
    
    
    
    def FiltrarOrganizar(self,potenciaRequerida, fabricante=None, potenciaNominalMax=None, fases=None):
        
        listaUsada=self.lista #lista de inversores 
#        if potenciaRequerida is None :
#            potenciaRequerida= self.potenciaNecesaria
        if fabricante is not None:
            listaUsada= [inversor for inversor in listaUsada if inversor.fabricante==fabricante]
            if len (listaUsada)<=0: 
                print ('Ningun inversor es del fabricante requerido')
                return None
        if potenciaNominalMax is not None:
            listaUsada=[inversor for inversor in listaUsada if inversor.potenciaNominal<=potenciaNominalMax]
            if len (listaUsada)<=0:
                print ('Ningun inversor cumple con la potencia nominal minima  requerida ')
                return None
        if fases is not None :
            listaUsada=[inversor for inversor in listaUsada if inversor.fases==fases]
            if len (listaUsada)<=0:
                if fases>3 or fases<1 :
                    print ("Ingrese un numero de fases entre 1 y 3")
                else:
                    print ("Fases requeridas: ",fases,'. No hay un inversor con este numero de fases y que cumpla con los demsa requisitos')
                return None
        for inversor in listaUsada:
            inversor.distancia= abs (potenciaRequerida-inversor.potenciaNominal)
        listaUsada=sorted(listaUsada, key=lambda x: x.distancia)
        
        vector=[]
        for i in listaUsada: 
            vector.append(i.referencia)
            
        dfNuevo=self.dataframe[self.dataframe.referencia.isin(vector)]
        nuevaListaInversores= ListaInversores(direccion=self.direccion, lista=listaUsada,df=dfNuevo) #Siempre que cree una ListaInversores esta heredará la dirección del objeto sin filtrar y organizar
        #Lo que estará organizado es el atributo lista, el dataframe no se organiza segun la distancia a la potencia requerida 
        return nuevaListaInversores


if __name__ == '__main__':
    prueba= ListaInversores(direccion='inversoresTest.csv')
    codigoPrueba= prueba.lista[0].codigo
    if type(codigoPrueba) is str: 
        print ('Datos importados correctamente')
    #print (codigoPrueba) #Si imprime un String significa que está bien conectado con la clase Inversor
    pruebaFiltrado=prueba.FiltrarOrganizar(120 ,fabricante="Huaweii") 
    if pruebaFiltrado.cantidadInversores == 9 :
        print ('Filtrado funcionando correctamente')
    
