

from sizingPVModules import *
from sizingInverters import *


###DATOS PARA PEUEBAS 
irradiacionEntrada= 4.6
energiaEntrada= 500 #116.9 #kWh-dia
fasesSistema= 3
PF= 0.8316



dfInversores=importarInversores()
dfPaneles= importarPaneles()




potenciaNecesaria= calPotNec(irradiacionEntrada,energiaEntrada,PF)

seleccionInversores = seleccionarInversores(potenciaNecesaria,fasesSistema,dfInversores)


configuracionesPaneles = configuracionesPosibles(potenciaNecesaria,dfPaneles, dfInversores,seleccionInversores)

panelElegido = elegirPanelAutomatico (configuracionesPaneles)
panelEligidoDict = panelElegido.to_dict()




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
    'otrasReferencias':configuracionesPaneles             #
    
}





solarInverter = {
    #input
    "powerNeed":potenciaNecesaria,                 # Potencia necesaria antes de dimensionamiento (float kW)
    #output
    "ref":[],                       # Referencias de inversores seleccionados (list of strings)
    "invAmount":[],                 # Cantidad por referencia (list of ints)
    "totInvAmount": None,           # Cantidad total de inversores (int)
    "iInput":[],                    # Entrada de corriente del inversor, (list of floats)
    "polesperInput":[],             # Cantidad de polos por entrada de corriente (list of ints)
    "vInput":[],                    # Tension de entrada (list of floats)
    "iOutput":[],                   # salida de corrientes del inversor, (list of floats)
    "totIoutput": None,             # suma de la corriente de salida (float)
    "vOutput":None,                   # tension de salida nominal (list of floats)
    "pOutput":[],                   # potencias de salida (list of floats)
    "pInput":[]                     # potencias de entrada (list of floats)
}



'''




variables = {'numero1':1,'numero2':'r','resultado':None}

def summa (dictionary):
    dictionary['resultado']= dictionary['numero1'] + dictionary['numero2']
    return 'SUCCESS'

flag = summa(variables)
print (variables['resultado'])


'''


