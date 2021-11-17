

from sizingPVModules import *
from sizingInverters import *
from variables import *


###DATOS PARA PEUEBAS 
irradiacionEntrada=4.8
energiaEntrada= 4.8 #116.9 #kWh-dia
fasesSistema= 1
PF= 0.8316


#def dimensionarSistema (configuracion):
dfInversores=importarInversores()
dfPaneles= importarPaneles()




potenciaNecesaria= calPotNec(irradiacionEntrada,energiaEntrada,PF)

seleccionInversores = seleccionarInversores(potenciaNecesaria,fasesSistema,dfInversores)


configuracionesPaneles = configuracionesPosibles(potenciaNecesaria,dfPaneles, dfInversores,seleccionInversores)

panelElegido = elegirPanelAutomatico (configuracionesPaneles)
#panelEligidoDict = panelElegido.to_dict()




pvModules = {

    #input
    "performanceRatio":PF,        # Eficiencia total del sistema (float)
    "ener_Need":energiaEntrada,               # Energia necesaria a suplir con el sistema (float kWh/dia)
    #output
    #"vArraymax":None,#panelElegido['configuracion']['voltajeArreglo'].tolist (),               # Tension maxima del arreglo de paneles solares (float V)
    #"iArray":iArray,                    # Corriente de cada uno de los array (list of floats A)
    "nArray":len (panelElegido['configuracion'][1]),                  # Cantidad de arrays (int N)
    #"pvModperArray":None,             # Cantidad de modulos por cada array (list of ints N)
    "amountPVMod":int (panelElegido['numeroPaneles']),             # Cantidad total de modulos (int N)
    "refPVMod":panelElegido['referencia'],                # Referencia del panel (string )
    "configuracionGeneral":panelElegido['configuracion'][0],             #dataframe configuracion de paneles en inversores
    'configuracionArrays':panelElegido['configuracion'][1],
    "iPVMod":dfPaneles[dfPaneles['referencia']==panelElegido['referencia']].squeeze()['Imp'], # Corriente de salida del panel seleccionado (float A)
    "vPVMod":dfPaneles[dfPaneles['referencia']==panelElegido['referencia']].squeeze()['Vmp'], # Tension de salida del panel seleccionado (float V)
    "sizePVMod":dfPaneles[dfPaneles['referencia']==panelElegido['referencia']].squeeze()['dimensiones'],   # dimensionaes del panel seleccionado (list of floats mm)
    "areaPVMod":calAreaPaneles(dfPaneles[dfPaneles['referencia']==panelElegido['referencia']].squeeze()['dimensiones'],1),  # area del panel seleccionado (float m2)
    "areaTotSyst":panelElegido['areaRequerida'],                # area total de todos los paneles (float m2)
    'otrasReferencias':configuracionesPaneles,             #
    'pTotalPaneles':sum (list (panelElegido['configuracion'][0]['potenciaInstalada']))#potencia instalada en paneles
    
}





solarInverter = {
    #input
    "powerNeed":potenciaNecesaria,                 # Potencia necesaria antes de dimensionamiento (float kW)
    #output
    "referencias":list (seleccionInversores['configuracion'].keys()),                       # Referencias de inversores seleccionados (list of strings)
    "invAmount":seleccionInversores['configuracion'],                 # Cantidad por referencia (list of ints)
    "totInvAmount": len(panelElegido['configuracion'][0]),           # Cantidad total de inversores (int)
    "iInput":panelElegido['configuracion'][1].loc[:,['inversor','mppt','corrienteArreglo']],                    # Entrada de corriente del inversor, (list of floats)
    "polesperInput":panelElegido['configuracion'][1].loc[:,['inversor','mppt','SeriesEnParalelo']],             # Cantidad de polos por entrada de corriente (list of ints)
    "vInput":panelElegido['configuracion'][0].loc[:,['inversor','voltajeIn']],                    # Tension de entrada (list of floats)
    "iOutput":[ ],                   # salida de corrientes del inversor, (list of floats)
    "totIoutput": None,             # suma de la corriente de salida (float)
    "vOutput":None,                   # tension de salida nominal (list of floats)
    "pOutput":[ ],                   # potencias de salida (list of floats)
    "pInput":panelElegido['configuracion'][0].loc[:,['inversor','potenciaInstalada']],                     # potencias de entrada (list of floats)
    "pTotalInversores":  sum ([dfInversores[dfInversores['referencia']==i].loc[:,'nominal_power'].squeeze() for i in list(seleccionInversores['configuracion'].keys())]) #capacidad de potencia total de los inversores juntos 
}

#    return "SUCCESS"

'''


variables = {'numero1':1,'numero2':'r','resultado':None}

def summa (dictionary):
    dictionary['resultado']= dictionary['numero1'] + dictionary['numero2']
    return 'SUCCESS'

flag = summa(variables)
print (variables['resultado'])


'''


