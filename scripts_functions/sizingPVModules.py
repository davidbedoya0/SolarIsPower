"""

# Descripcion

# Inputs Outputs

"""

import pandas as pd
import math 
import numpy as np
import re

"""

# Descripcion

# Inputs Outputs

"""


"""DATOS PARA PRUEBAS
ejemploInversor = {'referencia': ['Huawei 20','Huawei 60'], 
                   'cantidad': [2,1],
                   'potenciaNominal':[20,60],# ,[kW], 
                   '#MPPTs' :[ 4 , 6], 
                   'corrienteMppt': [26,22], 
                   'maxInputVoltage':[750,1100],#[V],
                   'maxPvInput': [30000,None],
                   'maxAcOutput':[22000,66000],#[W],
                   'eficiencia': [0.98 , 0.98]}

ejemploPaneles= {'referencia': ['465 Wp Jinko Tiger Mono','535 Jinko Mono'],
                  'Wp': [465,535], 
                  'Vmp':[43.18,40.63],
                  'Imp':[10.8,13.17],
                  'Isc':[11.59,13.79],
                  'Voc':[51.92,49.38],
                  'area':[2.275,2.58],
                  'precio':[488250,561750],
                  'dimensiones': ['2205x1032x35','2274x1174x35']}


DfInversores= pd.DataFrame(data=ejemploInversor)
DfPaneles= pd.DataFrame (data=ejemploPaneles)

"""

def importarPaneles():
    inversores= pd.read_csv('paneles.csv', sep=';', decimal = ",")
    inversores_1=inversores.dropna(how='all') #Se eliminan las filas que tengan todas las columnas como Nan
    return inversores_1


def calPotNec (irradiacion , consumo , PF , EnergiaDiaria: bool = True ,EnergiaMensual:bool = False , EnergiaAnual: bool=False):
    """  Función que calcula la potencia pico minima requerida para suministrar la energía de entrada
    Entradas: irradiacon: promedio diaria (kWh-dia/m2)  
    Consumo: Consumo promedio (kWh-periodoSeleccionado)
    PF: Performance Ratio, valores de 0 a 1.
    
    IMPORTANTE: Por defecto calcula con el periodo de energía diaria. Si se desea utilizar consumo mensual o anual 
                toca hacer uso de las entradas booleanas para indicar que el consumo está en el periodo deseado
    """
    
    if EnergiaMensual:
        potNec=consumo/(irradiacion*30*PF)
    elif EnergiaAnual:
        potNec=consumo/(irradiacion*365*PF)
    else:
        potNec=consumo/(irradiacion*PF)
        
    
    
    return potNec #[kW]



def calNumPaneles (potenciaNecesaria, potenciaReferenciaPanel):
    nPn=math.ceil(potenciaNecesaria/(potenciaReferenciaPanel/1000))
    
    return nPn

def calAreaPaneles (dimensionesPanel, nPn):
    
    dim = re.split('[xX\*]',dimensionesPanel)
    largo= int (dim [0])/1000 #metros
    ancho= int (dim[1])/1000 #metros
    #grueso=int (dim[2])
    areaUnitaria=largo*ancho
    areaTotal= areaUnitaria* nPn
    areaTotal = round (areaTotal,2)
    return areaTotal





def mejorSerie (nPu,nSmax):
    #Entradas: nPu = Numero de paneles utilizados 
    #          nSmax= Numero de paneles en serie maximos soportados por el inversor 
    #Salidas: nS, nP
    vector = np.arange(nSmax, 0, -1)
    for i in vector :
        mod = nPu % i
        if mod ==0:
            nS= i
            nP= nPu/i
            #print (nS, "paneles en serie , y ", nP, " arreglos en paralelo", ", y un total de ", nS*nP)
            return nS, nP


def CantidadPanelesConfig (nPu, nSmax, iMaxI ,Imp,disminuir: bool = False ):
    
    nS, nP = mejorSerie(nPu, nSmax) 
    Ip = nP*Imp
    while nS <=nP or Ip > iMaxI: 
        if disminuir:
            nPu -=1
        else : 
            nPu += 1
        nS, nP = mejorSerie(nPu, nSmax) 
        Ip = nP*Imp
    return nS, nP




def calPanelesSoportados (inversor, panel):
    
    #Información necesaria del panel 
    Voc= panel['Voc'] #Voltaje de circuito abierto
    Imp= panel['Imp'] #Corriente de punto de maxima potencia del panel
    Wp= panel['Wp'] #Potencia pico nominal
    #print ('\n Voltaje de corto circuit Panel:', Voc,  '  , \n Corriente de maxima potencia:  ', Imp,' , \n Potencia pico panel: ', Wp,' \n')
    #Información necesaria del inversor
    maxAcOutput = inversor['MaxAcOutput'] #Maxima potencia de salida del inversor 
    #print ("maxima potencia de salida inversor: ", maxAcOutput)
    maxInputVoltage= inversor['MaxInputVoltage'] #Maximo voltaje de trabajo admitido por el inversor 
    #print ('maximo voltaje de entrada inversor: ', maxInputVoltage)
    
    #ef= inversor['eficiencia'] #Eficiencia Inversor  
    ef=1
    #print ("eficiencia inversor : ", ef)
    #Calculamos la potencia DC maxima convertible por el inversor 
    maxDcInput= (1-ef)*maxAcOutput+maxAcOutput
    #print ("potencia DC maxima convertible por el inversor: ", maxDcInput,'\n')
    #Cálculo de maximo numero de paneles para maxDcInput
    nPmax=math.floor(maxDcInput*1000/Wp)
    #print ('maximo numero de paneles soportados por el inversor: ', nPmax, '\n')
    #Cálculo de maximo numero de paneles en serie 
    nSmax=math.floor(maxInputVoltage/Voc)
    
    #print ("Este inversor soporta máximo ", nPmax ," paneles, con una potencia total de ",nPmax*Wp , "Wp, y ",nSmax," paneles en serie como máximo" )
    return nPmax, nSmax






def configuracionPanelesEnInversor (inversor, panel, nPn): 
        
    
    
    Imp= panel['Imp'] #Corriente de punto de maxima potencia del panel
    iMppt=inversor['corrienteMPPT']
    nMppt= inversor ['#MPPTs']
    iMaxI= iMppt*nMppt
    nPmax, nSmax  = calPanelesSoportados(inversor, panel)
    condicion = nPmax<nPn
    if condicion :
        nPu=nPmax
        nS,nP = CantidadPanelesConfig(nPu, nSmax,iMaxI,Imp,True)
        nPu = nS * nP
    else: 
        nPu=nPn
        nS,nP = CantidadPanelesConfig(nPu,nSmax ,iMaxI,Imp)
    nPn_new=nPn-nPu
    return nS, nP, nPn_new


""" #PRUEBA
#valores sugeridos= de paneles necesarios: 61,62, 125,124

inversorSeleccionadoo= DfInversores.iloc[1]
panelseleccionado= DfPaneles.iloc[1]


PanelesSerie, PanelesParalelo, Restantes = configuracionPanelesEnInversor(inversorSeleccionadoo, panelseleccionado,61)


"""

def ConfigurarSeleccionInversores (potenciaNecesariaEntrada,dataframeInversores, dataframePaneles, seleccionInversores,panel):
    
    potenciaPanel= panel['Wp']
    Vmp= panel['Vmp']
    
    panelesNecesariosEntrada= calNumPaneles (potenciaNecesariaEntrada, potenciaPanel)

    #print ("\n potenciaNecesaria:", potenciaNecesariaEntrada, " , Paneles necesarios: ", panelesNecesariosEntrada)

    inversores = list();nPns= list ();nSs=list ();nPs= list ();potenciaInstalada=list ();voltajeInversores=list()
    voltajeArreglos=list ();arreglo=list();corrientesArreglos=list ();listaTodosInversores=list ();mppts=list();nSeries=list();nPT_lst = list()
    
    for i in seleccionInversores ['configuracion'].keys() :
        cantidad = seleccionInversores['configuracion'][i]
        #print ("\n Inversor: ",i, "\n Numero de inversores de esta referencia necesarios: ", cantidad)
        contador = cantidad
        inversor = dataframeInversores [dataframeInversores['referencia']==i].squeeze()
        while contador > 0 :
            
            nS, nP, nPn_nuevo = configuracionPanelesEnInversor(inversor,panel,panelesNecesariosEntrada)
            #print ( nS, nP, nPn_nuevo)
        
            panelesInversor= nS*nP
            #print ('\n paneles utilizados en este inversor: ', panelesInversor)
            potenciaT = panelesInversor*potenciaPanel
            
            nPanelesArreglo, voltajeArreglo, corrienteArreglo,mppt,listaInversores, nPanelesSerie, nPT= definirArreglo(nS, nP, panel, inversor)
            
            inversores.append(i) ; nPns.append (panelesInversor); nSs.append(nS);nPs.append(nP)
            potenciaInstalada.append(potenciaT);voltajeInversores.append(nS*Vmp)
            
            #arreglo.append(nPanelesArreglo); voltajeArreglos.append(voltajeArreglo)
            #corrientesArreglos.append(corrienteArreglo);listaTodosInversores.append(listaInversores);mppts.append(mppt)
            arreglo+=nPanelesArreglo; voltajeArreglos+=voltajeArreglo;corrientesArreglos+=corrienteArreglo
            listaTodosInversores+=listaInversores;mppts+=mppt; nSeries+=nPanelesSerie; nPT_lst+= nPT
            
            
            panelesNecesariosEntrada = nPn_nuevo
            #print ('\n Cantidad de paneles necesarios restantes: ', panelesNecesariosEntrada)
            contador-=1
        #print ("\n inversor : ",i, ", Cantidad : " , cantidad)
        
    
    
    costoPanel= panel['precio']
    costoTotalPaneles= costoPanel * sum (nPns)
    #print ("\n El costo total de los paneles es de: ", costoTotalPaneles, '\n')
    
    configuracionGeneral = pd.DataFrame({'inversor': inversores,'numeroPaneles': nPns,'Serie':nSs,'Paralelo':nPs, 'potenciaInstalada':potenciaInstalada,'voltajeIn':voltajeInversores})
    configuracionArrays= pd.DataFrame({'inversor':listaTodosInversores, 'mppt':mppts,'panelesUsados':nPT_lst,'PanelesSerie':nSeries,'SeriesEnParalelo':arreglo,'voltajeArreglo': voltajeArreglos,'corrienteArreglo': corrientesArreglos})
    
    return configuracionGeneral, configuracionArrays ,costoTotalPaneles

def definirArreglo(nS,nP, panel, inversor):##Define cuantos MPPTs son necesarios utlizar en el inversor. 
    
    voltajeMaximaPotencia= panel ['Vmp']
    corrienteMaximaPotencia= panel ['Imp']
    voltaje=voltajeMaximaPotencia*nS
    panelesParaleloMaximosMppt=math.floor((inversor['corrienteMPPT']*1.1)/panel['Imp'])
    restantes=nP%panelesParaleloMaximosMppt
    
    nArreglosFull=(nP-restantes)/panelesParaleloMaximosMppt
    
    ultimoArreglo=restantes
    nArreglos=nArreglosFull+1 
    
    
    nPA=list (); nSA = list ();vA = list (); iA= list (); inversores= list ();mppts=list()
    nPTA=list()
    
    #nPA= numero de series de paneles en paralelo en el arreglo; iA= corriente del arreglo ; vA = voltaje arreglo
    contador=nArreglosFull
    mppt=1
    while contador>0:
        nPA.append(panelesParaleloMaximosMppt)
        nSA.append(nS)
        vA.append(voltaje)
        iA.append(panelesParaleloMaximosMppt*corrienteMaximaPotencia)
        inversores.append(inversor['referencia'])
        mppts.append('MPPT '+ str (mppt))
        nPTA.append(nS*panelesParaleloMaximosMppt)
        
        
        mppt+=1
        contador-=1
    if restantes != 0:
        nPA.append(restantes)
        nSA.append(nS)
        vA.append(voltaje)
        iA.append(restantes*corrienteMaximaPotencia)
        inversores.append(inversor['referencia'])
        mppts.append('MPPT '+ str (mppt))
        nPTA.append(nS*restantes)
    

    return nPA, vA, iA, mppts,inversores,nSA, nPTA




'''
dfInversores=importarInversores()
dfPaneles= importarPaneles()
panel= dfPaneles.iloc[8]
inversor = dfInversores.iloc[8]
definirArreglos(10,11, panel, inversor)
'''


'''###DATOS PARA PRUEBAS 



irradiacionEntrada= 4.1
energiaEntrada= 500 #116.9 #kWh-dia
fasesSistema= 3
PF= 0.8316
referenciaPanelElegido = '535 W Jinko Tiger Pro '



dfInversores=importarInversores()
dfPaneles= importarPaneles()

panel = dfPaneles [dfPaneles['referencia']== referenciaPanelElegido].squeeze()

potenciaNecesariaa= calPotNec(irradiacionEntrada,energiaEntrada,PF)

seleccion = seleccionarInversores(potenciaNecesariaa,fasesSistema,dfInversores)
configuracionGeneral, configuracionArreglos , costoss= ConfigurarSeleccionInversores (potenciaNecesariaa, dfInversores, dfPaneles, seleccion, panel)
'''







def configuracionesPosibles (potenciaNecesaria, dfPaneles, dfInversores, seleccionInversores):
    
    referencias = list (); configuraciones = list ();costos= list (); areas = list();numeroPaneles = list ();potenciaInstaladaTotal=list ()
    
    for i in dfPaneles.index:
       referencia= dfPaneles['referencia'][i]
       panel = dfPaneles [dfPaneles['referencia']== referencia].squeeze()
       #print (referencia)
       configuracionGeneral, configuracionArreglos, costo = ConfigurarSeleccionInversores (potenciaNecesaria, dfInversores, dfPaneles, seleccionInversores, panel)
       configuracion = [configuracionGeneral,configuracionArreglos]
       numeroTotalPaneles=sum (configuracion[0]['numeroPaneles'])
       dimensiones= dfPaneles['dimensiones'][i]
       area=calAreaPaneles(dimensiones,numeroTotalPaneles)
       potenciaPanel= dfPaneles['Wp'][i]
       potenciaInstalada= potenciaPanel*numeroTotalPaneles/1000 #kWp
       referencias.append(referencia);configuraciones.append(configuracion);costos.append(costo);areas.append(area);numeroPaneles.append(numeroTotalPaneles); potenciaInstaladaTotal.append(potenciaInstalada)
    
    configuracionesPaneles = pd.DataFrame({'referencia': referencias,'configuracion': configuraciones,'costo':costos,'areaRequerida':areas,'numeroPaneles':numeroPaneles,'potenciaInstalada': potenciaInstaladaTotal})
    
    return configuracionesPaneles



def elegirPanelAutomatico (configuracionesPosiblesResultado ):
    #configuracionesPosiblesResultado: dataframe que devuelve la función configuracionesPosibles
    
    
    #Hacer una prueba que si existen dos elementos iguales en el data frame, sigue seleccionando solo 1 
    
    menorCosto = min (configuracionesPosiblesResultado['costo'])
    seleccion= configuracionesPosiblesResultado[configuracionesPosiblesResultado['costo']==menorCosto]
    
    if len (seleccion)>1:
        menorArea= min(seleccion['areaRequerida'])
        seleccion = seleccion[seleccion['areaRequerida']==menorArea]
        if len(seleccion)>1:
            for i in seleccion.index:
                seleccion=seleccion.loc[i]
                return seleccion

    seleccion= seleccion.squeeze()

    return seleccion



















