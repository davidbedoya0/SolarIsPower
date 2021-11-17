# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:36:57 2021

@author: crisd
"""
import pandas as pd 
import numpy as np 
import math
from Panel import Panel 
from ListaPaneles import ListaPaneles
from ConfiguracionesInversores import ConfiguracionesInversores
from Inversor import Inversor


class ConfiguracionPanel:
    
    
    def __init__(self, panel:Panel,configuracionesInversores : ConfiguracionesInversores, potenciaNecesaria):
        
#        if direccion is None :
#            direccion= 'paneles.csv'
#        self.listaPaneles = ListaPaneles(direccion)
        self.configuracionesInversores =  configuracionesInversores
        self.panel= panel
        self.potenciaNecesaria= potenciaNecesaria
        self.nPanelesNecesarios = self.NumeroPanelesNecesarios()
        self.configuracionGeneral=None
        self.configuracionArrays=None
        self.panelesUsados=None
        self.potenciaInstalada=None 
        self.ConfigurarSeleccionInversores()
        self.areaNecesaria = self.panelesUsados * self.panel.area
        self.costoPaneles= self.panelesUsados * self.panel.costo

        
        
        
        
    def NumeroPanelesNecesarios(self):
        panel=self.panel
        nPn=math.ceil(self.potenciaNecesaria/(panel.Wp/1000))
        return nPn
    
    def panelesSoportados(self, inversor: Inversor):
        panel=self.panel
        #ef= 1 #panel.eficiencia
#        maxDcInput= (1-ef)*inversor.maxPout+inversor.maxPout
        nPmax= math.floor(inversor.maxPout*1000/panel.Wp) #Nmero de paneles soportados
        nSmax=math.floor(inversor.maxVin/panel.Voc) #Numero de paneles en serie soportados 
        
        return nPmax, nSmax
    
    
    def ConfiguracionGeneralPaneles(self, nPu, nSmax, inversor:Inversor, disminuir:bool=False): #Funciona 
        panel= self.panel
        vector=np.arange (nSmax, 0,-1)
        for i in vector: 
            mod=nPu%i
            if mod ==0:
                nS=i
                nP=nPu/i
                Ip=nP*panel.Imp
                if nS<=nP or Ip> inversor.iMax:
                    if disminuir:
                        nPu-=1
                    else:
                        nPu+=1
                    nS, nP= self.ConfiguracionGeneralPaneles(nPu,nSmax, inversor, disminuir)
                else: 
                    return nS, nP
        return nS, nP
    
    
    def ConfiguracionPanelesEnInversor (self,inversor, nPn): #Esta funcion y ConfiguracionGeneralPaneles() se podrían unificar 
    
        nPmax ,nSmax = self.panelesSoportados(inversor)
        condicion = nPmax <nPn
        if condicion: 
            nPu=nPmax
            nS, nP = self.ConfiguracionGeneralPaneles(nPu,nSmax,inversor ,True)
            nPu=  nS*nP
        else:
            nPu=nPn
            nS,nP=self.ConfiguracionGeneralPaneles(nPu,nSmax, inversor, False)
        nPn_new= nPn-nPu
        return nS, nP, nPn_new
    
    

    def definirArreglo (self,nS, nP, inversor:Inversor): ##Define cuantos MPPTs son necesarios utilizar en el inversor
        panel=self.panel
        voltaje= panel.Vmp * nS
        nPanelesMaxPerMppt= math.floor (inversor.iMppt*1.1/panel.Imp)#numero de paneles maximos por mppt
        nPr=nP%nPanelesMaxPerMppt #numero de paralelo restantes. 
        nMpptsFull=(nP-nPr)/nPanelesMaxPerMppt #numero de Mppts que tienen el numero de maximo de series en paralelo.
        
        nPA=[]; nSA=[];vA=[];iA=[];inversores=[];mppts=[];nPTA=[];paneles=[]
        #nPA= numero de series en paralelo en el arreglo; iA= corriente del arreglo; vA= voltaje arreglo, nPTA= numero de paneles totales arreglo
        contador= nMpptsFull
        mppt=1
        while contador>0:
            nPA.append(nPanelesMaxPerMppt)
            nSA.append(nS)
            vA.append(voltaje)
            iA.append(nPanelesMaxPerMppt*panel.Imp)
            inversores.append(inversor.codigo)
            paneles.append(panel.referencia)
            mppts.append('MPPT'+str(mppt))
            nPTA.append(nS*nPanelesMaxPerMppt)
            mppt+=1
            contador-=1
        if nPr !=0:
            nPA.append(nPr)
            nSA.append(nS)
            vA.append(voltaje)
            iA.append(nPr*panel.Imp)
            inversores.append(inversor.codigo)
            paneles.append(panel.referencia)
            mppts.append('MPPT'+str(mppt))
            nPTA.append(nS*nPr)
        resultado=pd.DataFrame({'Inversor': inversores,'MPPT': mppts,'Panel': paneles,'NumeroPanelesTotal': nPTA, 'Numero de Paneles en Serie': nSA, 
                   'Numero Series En Paralelo': nPA, 'Voltaje Arreglo': vA, 'Corriente Arreglo': iA})
        inversor.paneles=resultado
        
        return  nPA, nSA, vA, iA,mppts, inversores, nPTA
    
    
    def ConfigurarSeleccionInversores (self):
        
        panel=self.panel
        nPn= self.nPanelesNecesarios #Cantidad de paneles necesarios
        
        inversores=[]; nPns=[];nSs=[];nPs=[]; potenciaInstalada=[]; voltajeInversores=[]
        voltajeArreglos=[];nParalelo=[]; corrienteArreglos=[];listaTodosInversores=[];mppts=[];nSeries=[];nPT_list= []
        dfConfiguracionInversores=self.configuracionesInversores.seleccion.config
        for i in dfConfiguracionInversores.index: #np.arange (len(self.arregloInversores.configuracion)):
            cantidad=dfConfiguracionInversores['Cantidad'][i]
            inversor= dfConfiguracionInversores['Inversor'][i]
            contador=cantidad
            while contador >0:
                nS, nP, nPn_nuevo = self.ConfiguracionPanelesEnInversor(inversor,nPn)
                panelesInversor=nS*nP#paneles utilizados en este inversor
                potenciaTotal= panelesInversor*panel.Wp
                nPA,nSA,vA, iA, mppt, listaInversores, nPTA =self.definirArreglo(nS,nP , inversor)
                
                #CONFIGURACION GENERAL
                inversores.append(inversor.codigo);nPns.append(panelesInversor);nSs.append(nS); nPs.append(nP)
                potenciaInstalada.append(potenciaTotal);voltajeInversores.append(nS*panel.Vmp)
                
                #CONFIGURACION ARREGLOS
                nParalelo+=nPA;voltajeArreglos+=vA;corrienteArreglos+=iA
                listaTodosInversores+= listaInversores; mppts+=mppt; nSeries+=nSA; nPT_list+=nPTA
                
                nPn= nPn_nuevo #Cantidad de paneles necesarios restantes 
                contador-=1
        self.panelesUsados= sum(nPns)
        self.potenciaInstalada= self.panelesUsados * self.panel.Wp
        self.configuracionGeneral= pd.DataFrame({'Inversor': inversores, 'Numero de Paneles': nPns, 'Paneles en serie': nSs, 'Series en Paralelo': nPs,
                                            'Potencia Instalada': potenciaInstalada, 'Vin': voltajeInversores})
        self.configuracionArrays= pd.DataFrame ({'Inversor': listaTodosInversores, 'MPPT': mppts, 'Paneles Usados':nPT_list, 'Paneles en Serie': nSeries, 
                                            'Series en Paralelo':nParalelo, 'Voltaje Arreglo': voltajeArreglos, 'Corriente Arreglo': corrienteArreglos})
#        return configuracionGeneral, configuracionArrays, costoTotalPaneles
    
    
    def TestConfiguracion (self):
        print ("HAZ LA FUNCIÓNNNN!!!")
        #El voltaje de cada MPPT cumple con los requerimientos del inversor?
        #La corriente de cada MPPT cumple con los requisitos del inversor?
        #Utilizo el numero de MPPTS adecuado? utilizo mas de los que debería???
        #Crear criterios para saber si tengo una buena configuración
        
        #Esta funcion debe asignar el valor a un atributo booleano de la clase la cual indica si existen advertencias o errores 
        #También debe asignar un arreglo con las distintas advertencias 
        



if __name__ == '__main__':
    potenciaNecesariaTest=120
    fasesTest=3
    panelTest= ListaPaneles('paneles.csv').lista[13]
    configuracionesInversoresTest= ConfiguracionesInversores(potenciaNecesariaTest, fasesTest)
    configuracionSeleccionadaTest=configuracionesInversoresTest.seleccion
    
    
    configuracionPanelTest= ConfiguracionPanel(panelTest,configuracionesInversoresTest, potenciaNecesariaTest)
    listaInversores= configuracionesInversoresTest.listaInversores.dataframe
    
    
    
    