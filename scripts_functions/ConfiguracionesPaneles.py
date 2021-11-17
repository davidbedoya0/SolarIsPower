# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 00:41:58 2021

@author: crisd
"""
import pandas as pd
from ConfiguracionPanel import ConfiguracionPanel
from ListaPaneles import ListaPaneles
from ConfiguracionesInversores import ConfiguracionesInversores

class ConfiguracionesPaneles: 
    
    def __init__ (self, configuracionesInversores: ConfiguracionesInversores, potenciaNecesaria, fases ):
        self.configuracionesInversores = configuracionesInversores
        self.potenciaNecesaria = potenciaNecesaria
        self.fases = fases
        self.listaPaneles = ListaPaneles ("paneles.csv")
        self.configuraciones=None
        self.dfConfiguraciones=None
        self.CrearConfiguraciones()
        
        
    def CrearConfiguraciones (self):
        
        configuraciones= []
        dfConfiguraciones= pd.DataFrame(columns=['Panel', 'Costo', 'Area Requerida','Potencia Instalada', 'Configuracion'])
        for panel in self.listaPaneles.lista: 
            configuracion= ConfiguracionPanel(panel,self.configuracionesInversores,self.potenciaNecesaria)
            configuraciones.append(configuracion)
            dfConfiguraciones=dfConfiguraciones.append({'Panel':panel.referencia,
                                                      'Costo':"${:,.0f}".format(configuracion.costoPaneles),
                                                      'Area Requerida':configuracion.areaNecesaria ,
                                                      'Potencia Instalada':configuracion.potenciaInstalada,
                                                      'Configuracion': configuracion.configuracionArrays}, ignore_index=True)
        self.configuraciones= configuraciones
        self.dfConfiguraciones= dfConfiguraciones
        
        
        


if __name__ == '__main__':
    
    pN_test=120
    f_test=3
    
    CI_test= ConfiguracionesInversores(pN_test,f_test)
    CP_test=ConfiguracionesPaneles(CI_test,pN_test,f_test)