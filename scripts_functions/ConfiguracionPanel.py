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
    
    all=[]
    
    def __init__(self, panel:Panel,configuracionesInversores : ConfiguracionesInversores, potenciaNecesaria:float):
        
        
        
        #Inicializar atributos
        self.__configuracionesInversores =  configuracionesInversores
        self.__panel= panel
        self.__potenciaNecesaria= potenciaNecesaria
        
        #Ejecutar Acciones
        ConfiguracionPanel.all.append(self)
        self.__NumeroPanelesNecesarios()
        self.__ConfigurarSeleccionInversores()
        
        
    #Funciones de representación de la instancia
    def __repr__(self): 
        cadena= "<Configuracion utilizando el panel " + self.__panel.referencia+">"
        return cadena
    
    
    #=============Restriccion de atributos a ReadOnly , GETTERS
    @property
    def configuracionesInversores(self):
        return self.__configuracionesInversores
    
    @property
    def panel(self):
        return self.__panel
    
    @property
    def potenciaNecesaria(self):
        return self.__potenciaNecesaria
    
    @property
    def nPanelesNecesarios(self):
        return self.__nPanelesNecesarios
    
    @property
    def configuracionGeneral(self):
        return self.__configuracionGeneral
    
    @property
    def configuracionArrays(self):
        return self.__configuracionArrays
    
    @property
    def nPanelesUsados(self):
        return self.__nPanelesUsados
    
    @property
    def potenciaInstalada(self):
        return self.__potenciaInstalada
    
    @property
    def areaNecesaria(self):
        return self.__areaNecesaria
    
    @property
    def costoPaneles(self):
        return self.__costoPaneles
    
    
    #==================METODOS PRIVADOS
    
    def __NumeroPanelesNecesarios(self):
        panel=self.__panel
        nPn=math.ceil(self.__potenciaNecesaria/(panel.Wp/1000))
        self.__nPanelesNecesarios= nPn
#        return nPn
    
    def __PanelesSoportados(self, inversor: Inversor):
        panel=self.__panel
        #ef= 1 #panel.eficiencia
#        maxDcInput= (1-ef)*inversor.maxPout+inversor.maxPout
        nPmax= math.floor(inversor.maxPout*1000/panel.Wp) #Nmero de paneles soportados
        nSmax=math.floor(inversor.maxVin/panel.Voc) #Numero de paneles en serie soportados 
        
        return nPmax, nSmax
    
    
    def __ConfiguracionGeneralPaneles(self, nPu, nSmax, inversor:Inversor, disminuir:bool=False): #Funciona 
        panel= self.__panel
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
                    nS, nP= self.__ConfiguracionGeneralPaneles(nPu,nSmax, inversor, disminuir)
                else: 
                    return nS, nP
        return nS, nP
    
    
    def __ConfiguracionPanelesEnInversor (self,inversor, nPn): #Esta funcion y __ConfiguracionGeneralPaneles() se podrían unificar 
    
        nPmax ,nSmax = self.__PanelesSoportados(inversor)
        condicion = nPmax <nPn
        if condicion: 
            nPu=nPmax
            nS, nP = self.__ConfiguracionGeneralPaneles(nPu,nSmax,inversor ,True)
            nPu=  nS*nP
        else:
            nPu=nPn
            nS,nP=self.__ConfiguracionGeneralPaneles(nPu,nSmax, inversor, False)
        nPn_new= nPn-nPu
        return nS, nP, nPn_new
    
    

    def __DefinirArreglo (self,nS, nP, inversor:Inversor): ##Define cuantos MPPTs son necesarios utilizar en el inversor
        panel=self.__panel
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
    
    
    def __ConfigurarSeleccionInversores (self):
        
        panel=self.__panel
        nPn= self.__nPanelesNecesarios #Cantidad de paneles necesarios
        
        inversores=[]; nPns=[];nSs=[];nPs=[]; potenciaInstalada=[]; voltajeInversores=[]
        voltajeArreglos=[];nParalelo=[]; corrienteArreglos=[];listaTodosInversores=[];mppts=[];nSeries=[];nPT_list= []
        dfConfiguracionInversores=self.__configuracionesInversores.seleccion.config
        for i in dfConfiguracionInversores.index: #np.arange (len(self.arregloInversores.configuracion)):
            cantidad=dfConfiguracionInversores['Cantidad'][i]
            inversor= dfConfiguracionInversores['Inversor'][i]
            contador=cantidad
            while contador >0:
                nS, nP, nPn_nuevo = self.__ConfiguracionPanelesEnInversor(inversor,nPn)
                panelesInversor=nS*nP#paneles utilizados en este inversor
                potenciaTotal= panelesInversor*panel.Wp
                nPA,nSA,vA, iA, mppt, listaInversores, nPTA =self.__DefinirArreglo(nS,nP , inversor)
                
                #CONFIGURACION GENERAL
                inversores.append(inversor.codigo);nPns.append(panelesInversor);nSs.append(nS); nPs.append(nP)
                potenciaInstalada.append(potenciaTotal);voltajeInversores.append(nS*panel.Vmp)
                
                #CONFIGURACION ARREGLOS
                nParalelo+=nPA;voltajeArreglos+=vA;corrienteArreglos+=iA
                listaTodosInversores+= listaInversores; mppts+=mppt; nSeries+=nSA; nPT_list+=nPTA
                
                nPn= nPn_nuevo #Cantidad de paneles necesarios restantes 
                contador-=1
        self.__nPanelesUsados= sum(nPns)
        self.__potenciaInstalada= self.__nPanelesUsados * self.__panel.Wp
        self.__areaNecesaria = self.__nPanelesUsados * self.__panel.area
        self.__costoPaneles= self.__nPanelesUsados * self.__panel.costo
        self.__configuracionGeneral= pd.DataFrame({'Inversor': inversores, 'Numero de Paneles': nPns, 'Paneles en serie': nSs, 'Series en Paralelo': nPs,
                                            'Potencia Instalada': potenciaInstalada, 'Vin': voltajeInversores})
        self.__configuracionArrays= pd.DataFrame ({'Inversor': listaTodosInversores, 'MPPT': mppts, 'Paneles Usados':nPT_list, 'Paneles en Serie': nSeries, 
                                            'Series en Paralelo':nParalelo, 'Voltaje Arreglo': voltajeArreglos, 'Corriente Arreglo': corrienteArreglos})

    
    #============METODOS PÚBLICOS ---- Setters
    
    
    
    
    
    
    #========== METODO TEST======
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
    
    
    
    