"""

# Descripcion

# Inputs Outputs

"""
import pandas as pd 
import numpy as np
import math

"""

# Descripcion

# Inputs Outputs

"""

"""#DATOS DE PRUEBA 

DatosInversores = {'referencia':['Huawei 25','Huawei 60','Huawei 10','Fronius 15','Fronius 10','CPS 30', 'CPS 10'],'nominal_power':[25,60,10,15,10,30,10],'precio':[11875000,17125000, 8000000 ,12950000,9675000,12750000,3000000],'fabricante':['Huawei','Huawei','Huawei','Fronius','Fronius','CPS','CPS']}
inversores_1= pd.DataFrame(data=DatosInversores)
"""

def filtAndOrg (dataframe, potenciaRequerida, fabricante_in= None, potenciaNominalInversor = None):
    #Los parametros que se incializan como None dan la opción de que sean opcionales
    
    #Incializamos el nuevo dataframe con el ya existente de entrada 
    dataframeNuevo = dataframe.copy()
    
    #Creamos una columna vacía que contenga el atributo "Distancia"
    dataframeNuevo ['distancia'] = pd.Series()
    
    #recorro el nuevo data frame 
    for i in dataframeNuevo.index:
        
        #Sorted by fabricante 
        if fabricante_in is not None and dataframeNuevo['fabricante'][i] != fabricante_in :
            dataframeNuevo=dataframeNuevo.drop([i], axis=0)
            continue
        
        #Sorted by nominal power
        if potenciaNominalInversor is not None and dataframeNuevo['nominal_power'][i] > potenciaNominalInversor:
            dataframeNuevo=dataframeNuevo.drop([i], axis=0)
            continue
        
        #asigno el valor a la columna de 'distancia', la cual contiene la difetencia entre la potencia nominal del inversor y la potencia requerida
        distancia = abs (potenciaRequerida - dataframeNuevo ['nominal_power'][i])
        dataframeNuevo ['distancia'][i] = distancia
    
    #Organizo el nuevo dataframe por la columna 'distancia'
    dataframeNuevo= dataframeNuevo.sort_values ('distancia')
    
    #Re asigno los index para que vayan en orden ascendente de nuevo 
    #ultimoIndexNew= len (dataframeNuevo.index)
    #vector= np.arange(0,ultimoIndexNew,1)
    #dataframeNuevo.index = [vector]
    
    return dataframeNuevo

def calculoPotenciaNuevaNecesaria( potenciaNecesaria, potenciaNominalInversor, costoInversor):
    # recibe
    cantidadInversores = math.floor(potenciaNecesaria / potenciaNominalInversor)
    if(cantidadInversores < 1):
        cantidadInversores = math.ceil(potenciaNecesaria / potenciaNominalInversor)
    potenciaNuevaNecesaria = potenciaNecesaria - cantidadInversores * potenciaNominalInversor
    costoLote = cantidadInversores * costoInversor
    return [potenciaNuevaNecesaria, cantidadInversores, costoLote]



def configInv(referenciaInversor,potenciaRequerida, dataframe, CP,configP=None, Mconfig=None,MT=None):
    """
    Este programa encuentra la mejor configuración para suplir una potencia requerida a partir de un dataframe que contiene los inversores que se pueden utilizar
    Como entrada necesito:la referencia de comienzo de la rama, su costo parcial (CP) y la configuración  (cantidad de inversores)
                        El mejor costo esperado (con el que se comparará las demas configuraciones) (MT)
                        La potencia solicitada
    PARAMETROS: 
    
    CP=Costo Parcial, poner en caso general el costo del primer lote de inversores
    MT=Mejor Total 
    configP= Configuración Parcial (dataframe que coniene los inversores utilizados)
    Mconfig= Mejor Configuración
    referenciaInversor: 
    potenciaRequerida:
    dataframe: dataframe que contiene los inversores y su información 
    
    """

#    print ("Entradas función: \n" , "Referencia Inversor entrada: ",referenciaInversor,"\n", "Potencia requerida entrada: ",potenciaRequerida,"\n","Costo Parcial entrada:",CP, "\n  \n")

    fabricante=dataframe[dataframe['referencia'] == referenciaInversor]['fabricante'].values[0]
    potenciaN=dataframe[dataframe['referencia'] == referenciaInversor]['nominal_power'].values[0]

    #Creo el nuevo data frame con los inversores que pueden complementar a la referencia de entrada para finalalizar la configutación necesaria para completar la potencia requerida
    nuevoDataframe= filtAndOrg(dataframe, potenciaRequerida, fabricante, potenciaN ) 
    
    #Se guarda el Costo parcial y la configuracion de entrada en una constante para luego usarlo dentro del for y reiniciar el CP con CP_p
    CP_p=CP
    configP_p= configP.copy()
    
    epsilon=0
    
    for i in nuevoDataframe.index:
        
        #Reinicio el costo parcial a medida que evalúo otro inversor. El valor del costo parcial con el que se reinicia debe ser el de la configuracion con la que se venía 
        CP=CP_p
        configP= configP_p.copy ()
        
#        print ("CP = " + str(CP)+ "\n  \n")
        #Guardo en esta variable la potencia nominal del inversor i del nuevoDataframe 
        potenciaNominalInversor=nuevoDataframe['nominal_power'][i] 
        
        #Guardo en estas variables el costo y la referencia del inversor i del nuevoDataframe 

        costoInversor=nuevoDataframe['precio'][i]  
        refInvNuevo= nuevoDataframe['referencia'][i]
        inversorNuevo=nuevoDataframe.loc[nuevoDataframe['referencia']==refInvNuevo]
        
#        print ("inversor analizado: ", refInvNuevo, ". Costo Unitario: $" , costoInversor,"\n  \n")
        
        #Se calcula la cantidad necesaria de inversores, la potencia requerida que hace falta y el costo del lote ,,,,,, Salida: potenciaNueva, cantidad inversores, costo. 
        [potenciaNecesariaNueva, CantidadNecesaria, Costo]=calculoPotenciaNuevaNecesaria(potenciaRequerida, potenciaNominalInversor, costoInversor) 
        
#        print ("Para suplir ", potenciaRequerida, "kW con este inversor, se necesitan ", CantidadNecesaria, " Unidades que tienen un costo total de $", Costo,"\n  \n")
        
        CP=CP+Costo #Actualizo el Costo Parcial de la configuración que estoy haciendo con el inversor del nuevoDataframe 
        contador=CantidadNecesaria
        while contador >0:
            configP = configP.append (inversorNuevo)
            contador -=1
#        print ("El costo parcial total de está configuración usando este inversor es de $", CP,"\n  \n")
        
        #Debería también actualizar el string que tenga las referencias utilizadas en la configuración y la cantidad de cada una 
        
        #Si MT aún no ha sido asignado y ya se acabó la configuración, asignar el CP como el nuevo MT 
        if MT is None and potenciaNecesariaNueva <= epsilon:
#            print ("primera configración terminada. Mejor Total asignado a $", CP,"\n  \n")
            MT=CP
            Mconfig=configP.copy()
            
        #Si ya se tiene la potencia requerida y si el costo de esta configuración es menor al mejor total (MT) entonces reemplazar MT y la configuración 
        elif potenciaNecesariaNueva <= epsilon and CP <= MT: 
            
            #ConfigP=MConfig
#            print ("Configuración completada" , "Costo final configuración: $", CP, "; Mejor costo Total (MT): $", MT, ". NUEVA MEJOR CONFIGURACIÓN","\n  \n")
            #Se reemplaza el Mejor total por el Costo Parcial final de la configuración
            MT=CP
            Mconfig=configP.copy()
            
        #Independientemente si ya se acabó la configuración o no, si el costo parcial de la configuración que se está haciendo (CP) es mayor al Mejor Costo, entonces no seguir y evaluar el siguiente inversor del nuevoDataframe
        elif MT is not None and CP>MT: 
#            print ('El costo parcial de esta configuración ya superó al mejor total entonces se descarta',"\n  \n")
            continue
        
        #Si no se ha alcanzado la potencia que se requiere  y el Costo Parcial es menor que el Mejor Costo entonces seguir desarrollando la configuración 
        elif potenciaNecesariaNueva > epsilon: #and CP<MT : 
            MT,Mconfig=configInv(refInvNuevo,potenciaNecesariaNueva,nuevoDataframe,CP, configP,Mconfig,MT)
            
#    print ('La mejor configuración que se encontró tiene un costo de ', MT, "\n  \n")
    
    return MT, Mconfig




""" #TEST 
#valores sugeridos de pruebas: 65, 120

referenciaPrueba='Huawei 60'
configParcial= inversores_1.loc[inversores_1['referencia']== referenciaPrueba]
testConfigCosto, testConfigDatos = configInv (referenciaPrueba, 180, inversores_1, 17125000, configParcial)

"""
