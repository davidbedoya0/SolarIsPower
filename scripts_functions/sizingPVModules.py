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
    numPaneles=math.ceil(potenciaNecesaria/(potenciaReferenciaPanel/1000))
    
    return numPaneles

def calAreaPaneles (dimensionesPanel, nPaneles):
    dim = re.split('[xX\*]',dimensionesPanel)
    largo= int (dim [0])/1000 #metros
    ancho= int (dim[1])/1000 #metros
    #grueso=[2]
    areaUnitaria=largo*ancho
    areaTotal= areaUnitaria* nPaneles
    areaTotal = round (areaTotal,2)
    return areaTotal





def mejorSerie (nPaneles,nSerieMax):
    #Entradas: nPaneles = Numero de paneles necesarios 
    #          nSerieMax= Numero de paneles en serie maximos soportados por el inversor 
    #Salidas: nPanelesSerie
    vector = np.arange(nSerieMax, 0, -1)
    for i in vector :
        mod = nPaneles % i
        if mod ==0:
            serie = i
            paralelo = nPaneles/i
            #print (serie, "paneles en serie , y ", paralelo, " arreglos en paralelo", ", y un total de ", serie*paralelo)
            return serie , paralelo


def configurarPaneles (nPaneles, nSerieMax, limiteCorriente ,corrientePanel,disminuir: bool = False ):
    
    nSerie, nParalelo = mejorSerie(nPaneles, nSerieMax) 
    corrienteParalelo = nParalelo*corrientePanel
    while nSerie <nParalelo or corrienteParalelo > limiteCorriente: 
        if disminuir:
            nPaneles -=1
        else : 
            nPaneles += 1
        nSerie, nParalelo = mejorSerie(nPaneles, nSerieMax)
        corrienteParalelo = nParalelo*corrientePanel
    return nSerie, nParalelo




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
    maxPan=math.floor(maxDcInput*1000/Wp)
    #print ('maximo numero de paneles soportados por el inversor: ', maxPan, '\n')
    #Cálculo de maximo numero de paneles en serie 
    maxPanSerie=math.floor(maxInputVoltage/Voc)
    
    #print ("Este inversor soporta máximo ", maxPan ," paneles, con una potencia total de ",maxPan*Wp , "Wp, y ",maxPanSerie," paneles en serie como máximo" )
    return maxPan, maxPanSerie






def configuracionPanelesEnInversor (inversor, panel, nPn): #Funcion Final
    
    
    
    Imp= panel['Imp'] #Corriente de punto de maxima potencia del panel
    corrienteMppt=inversor['corrienteMPPT']
    nMppt= inversor ['#MPPTs']
    limiteCorrienteInversor= corrienteMppt*nMppt
    nPsi, nPMaxS  = calPanelesSoportados(inversor, panel)
    condicion = nPsi<nPn
    if condicion :
        nPu=nPsi
        nS,nP = configurarPaneles(nPu, nPMaxS,limiteCorrienteInversor,Imp,True)
        nPu = nS * nP
    else: 
        nPu=nPn
        nS,nP = configurarPaneles(nPu,nPMaxS ,limiteCorrienteInversor,Imp)
    nPn_new=nPn-nPu
    return nS, nP, nPn_new


""" #PRUEBA
#valores sugeridos= de paneles necesarios: 61,62, 125,124

inversorSeleccionadoo= DfInversores.iloc[1]
panelseleccionado= DfPaneles.iloc[1]


PanelesSerie, PanelesParalelo, Restantes = configuracionPanelesEnInversor(inversorSeleccionadoo, panelseleccionado,61)


"""

def configurarArregloInversores (potenciaNecesariaEntrada,dataframeInversores, dataframePaneles, seleccionInversores,panelElegido):
    
    potenciaPanel= panelElegido['Wp']
    
    panelesNecesariosEntrada= calNumPaneles (potenciaNecesariaEntrada, potenciaPanel)
    


    #print ("\n potenciaNecesaria:", potenciaNecesariaEntrada, " , Paneles necesarios: ", panelesNecesariosEntrada)

    inversores = list();nPns= list ();nSs=list ();nPs= list ();potenciaInstalada=list (); voltajeArreglos=list ()
    arreglo=list();corrientesArreglos=list ();listaTodosInversores=list ();mppts=list();nSeries=list();nPT_lst = list()
    
    for i in seleccionInversores ['configuracion'].keys() :
        cantidad = seleccionInversores['configuracion'][i]
        #print ("\n Inversor: ",i, "\n Numero de inversores de esta referencia necesarios: ", cantidad)
        contador = cantidad
        inversor = dataframeInversores [dataframeInversores['referencia']==i].squeeze()
        while contador > 0 :
            
            nS, nP, nPn_nuevo = configuracionPanelesEnInversor(inversor,panelElegido,panelesNecesariosEntrada)
            #print ( nS, nP, nPn_nuevo)
        
            panelesInversor= nS*nP
            #print ('\n paneles utilizados en este inversor: ', panelesInversor)
            potenciaT = panelesInversor*potenciaPanel
            
            nPanelesArreglo, voltajeArreglo, corrienteArreglo,mppt,listaInversores, nPanelesSerie, nPT= definirArreglo(nS, nP, panelElegido, inversor)
            
            inversores.append(i) ; nPns.append (panelesInversor); nSs.append(nS);nPs.append(nP)
            potenciaInstalada.append(potenciaT)
            
            #arreglo.append(nPanelesArreglo); voltajeArreglos.append(voltajeArreglo)
            #corrientesArreglos.append(corrienteArreglo);listaTodosInversores.append(listaInversores);mppts.append(mppt)
            arreglo+=nPanelesArreglo; voltajeArreglos+=voltajeArreglo;corrientesArreglos+=corrienteArreglo
            listaTodosInversores+=listaInversores;mppts+=mppt; nSeries+=nPanelesSerie; nPT_lst+= nPT
            
            
            panelesNecesariosEntrada = nPn_nuevo
            #print ('\n Cantidad de paneles necesarios restantes: ', panelesNecesariosEntrada)
            contador-=1
        #print ("\n inversor : ",i, ", Cantidad : " , cantidad)
        
    
    
    costoPanel= panelElegido['precio']
    costoTotalPaneles= costoPanel * sum (nPns)
    #print ("\n El costo total de los paneles es de: ", costoTotalPaneles, '\n')
    
    configuracionGeneral = pd.DataFrame({'inversor': inversores,'numeroPaneles': nPns,'Serie':nSs,'Paralelo':nPs, 'potenciaInstalada':potenciaInstalada})
    configuracionArreglos= pd.DataFrame({'inversor':listaTodosInversores, 'mppt':mppts,'panelesUsados':nPT_lst,'PanelesSerie':nSeries,'SeriesEnParalelo':arreglo,'voltajeArreglo': voltajeArreglos,'corrienteArreglo': corrientesArreglos})
    
    return configuracionGeneral, configuracionArreglos ,costoTotalPaneles

def definirArreglo(nS,nP, panel, inversor):##Define cuantos MPPTs son necesarios utlizar en el inversor. 
    
    voltajeMaximaPotencia= panel ['Vmp']
    corrienteMaximaPotencia= panel ['Imp']
    voltaje=voltajeMaximaPotencia*nS
    panelesParaleloMaximosMppt=math.floor((inversor['corrienteMPPT']*1.1)/panel['Imp'])
    restantes=nP%panelesParaleloMaximosMppt
    
    nArreglosFull=(nP-restantes)/panelesParaleloMaximosMppt
    
    ultimoArreglo=restantes
    nArreglos=nArreglosFull+1 
    
    
    nParaleloArreglo=list (); nSerieArreglo = list ();voltajeArreglo = list (); corrienteArreglo= list (); inversores= list ();mppts=list()
    panelesTotales=list()
    
    
    contador=nArreglosFull
    mppt=1
    while contador>0:
        nParaleloArreglo.append(panelesParaleloMaximosMppt)
        nSerieArreglo.append(nS)
        voltajeArreglo.append(voltaje)
        corrienteArreglo.append(panelesParaleloMaximosMppt*corrienteMaximaPotencia)
        inversores.append(inversor['referencia'])
        mppts.append('MPPT '+ str (mppt))
        panelesTotales.append(nS*panelesParaleloMaximosMppt)
        
        
        mppt+=1
        contador-=1
    if restantes != 0:
        nParaleloArreglo.append(restantes)
        nSerieArreglo.append(nS)
        voltajeArreglo.append(voltaje)
        corrienteArreglo.append(restantes*corrienteMaximaPotencia)
        inversores.append(inversor['referencia'])
        mppts.append('MPPT '+ str (mppt))
        panelesTotales.append(nS*restantes)
    

    return nParaleloArreglo, voltajeArreglo, corrienteArreglo, mppts,inversores,nSerieArreglo, panelesTotales




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
configuracionGeneral, configuracionArreglos , costoss= configurarArregloInversores (potenciaNecesariaa, dfInversores, dfPaneles, seleccion, panel)
'''







def configuracionesPosibles (potenciaNecesaria, dfPaneles, dfInversores, seleccionInversores):
    
    referencias = list (); configuraciones = list ();costos= list (); areas = list();numeroPaneles = list ();potenciaInstaladaTotal=list ()
    
    for i in dfPaneles.index:
       referencia= dfPaneles['referencia'][i]
       panel = dfPaneles [dfPaneles['referencia']== referencia].squeeze()
       #print (referencia)
       configuracionGeneral, configuracionArreglos, costo = configurarArregloInversores (potenciaNecesaria, dfInversores, dfPaneles, seleccionInversores, panel)
       configuracion = [configuracionGeneral,configuracionArreglos]
       numeroTotalPaneles=sum (configuracion[0]['numeroPaneles'])
       dimensiones= dfPaneles['dimensiones'][i]
       area=calAreaPaneles(dimensiones,numeroTotalPaneles)
       potenciaPanel= dfPaneles['Wp'][i]
       potenciaInstalada= potenciaPanel*numeroTotalPaneles/1000 #kWp
       referencias.append(referencia);configuraciones.append(configuracion);costos.append(costo);areas.append(area);numeroPaneles.append(numeroTotalPaneles); potenciaInstaladaTotal.append(potenciaInstalada)
    
    resultado = pd.DataFrame({'referencia': referencias,'configuracion': configuraciones,'costo':costos,'areaRequerida':areas,'numeroPaneles':numeroPaneles,'potenciaInstalada': potenciaInstaladaTotal})
    
    return resultado



def elegirPanelAutomatico (configuracionesPosiblesResultado ):
    #configuracionesPosiblesResultado: dataframe que devuelve la función configuracionesPosibles
    menorCosto = min (configuracionesPosiblesResultado['costo'])
    seleccion= configuracionesPosiblesResultado[configuracionesPosiblesResultado['costo']==menorCosto]
    seleccion= seleccion.squeeze()
    return seleccion



















