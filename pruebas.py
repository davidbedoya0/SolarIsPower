
# +++ inputs
# ? input (opcional)
# ! Outputs

from numpy import empty


class pvProject:
    performanceRatio:None        # +++ Eficiencia total del sistema (float)
    ener_Need:None               # +++ Energia necesaria a suplir con el sistema (float kWh/dia)
    ener_Type:None               # +++ Energia necesaria a suplir con el sistema (float kWh/dia)
    areaTotSyst:None             # ? area total de todos los paneles (float m2)
    powerNeed:None                 # Potencia necesaria antes de dimensionamiento (float kW)

    
class pvArea:

    
    vArraymax:None               # ! Tension maxima del arreglo de paneles solares (float V)
    iArray:None                  # ! Corriente de cada uno de los array (list of floats A)
    nArray:None                  # ! Cantidad de arrays (int N)
    pvModperArray:None           # ! Cantidad de modulos por cada array (list of ints N)
    amountPVMod:None             # ! Cantidad total de modulos (int N)
    configuracionGeneral:None    # ! Cantidad total de modulos (int N)
    configuracionArrays:None     # ! Cantidad total de modulos (int N)        
    refPVMod:None                # ! Referencia del panel (string )
    iPVMod:None                  # ! Corriente de salida del panel seleccionado (float A)
    vPVMod:None                  # ! Tension de salida del panel seleccionado (float V)
    sizePVMod:None               # ! dimensionaes del panel seleccionado (list of floats mm)
    areaPVMod:None               # ! area del panel seleccionado (float m2)
    pTotalPaneles:None           # ! dimensionaes del panel seleccionado (list of floats mm)

    
    


class inverters:

    referencias:None               # Referencias de inversores seleccionados (list of strings)
    invAmount:None                 # Cantidad por referencia (list of ints)
    totInvAmount: None             # Cantidad total de inversores (int)
    iInput:None                    # Entrada de corriente del inversor (list of floats)
    polesperInput:None             # Cantidad de polos por entrada de corriente (list of ints)
    vInput:None                    # Tension de entrada (list of floats)
    iOutput:None                   # salida de corrientes del inversor (list of floats)
    totIoutput: None               # suma de la corriente de salida (float)
    vOutput:None                   # tensiones de salida (list of floats)
    pOutput:None                   # potencias de salida (list of floats)
    pInput:None                    # potencias de entrada (list of floats)
    pTotalInversores:None          # potencias de entrada (list of floats)
    powerNeed:None                 # Potencia necesaria antes de dimensionamiento (float kW)
    referencias:None               # Referencias de inversores seleccionados (list of strings)
    invAmount:None                 # Cantidad por referencia (list of ints)
    totInvAmount: None             # Cantidad total de inversores (int)
    iInput:None                    # Entrada de corriente del inversor (list of floats)
    polesperInput:None             # Cantidad de polos por entrada de corriente (list of ints)
    vInput:None                    # Tension de entrada (list of floats)
    iOutput:None                   # salida de corrientes del inversor (list of floats)
    totIoutput: None               # suma de la corriente de salida (float)
    vOutput:None                   # tensiones de salida (list of floats)
    pOutput:None                   # potencias de salida (list of floats)
    pInput:None                    # potencias de entrada (list of floats)
    pTotalInversores:None          # potencias de entrada (list of floats)

class inventary:
    pvWires:None                   # Conductores del lado DC (list [referencias string metraje float m2])
    facilityWires:None             # Conductores del lado AC (list [referencias string metraje float m2])
    pvProtections:None             # breakers lado DC (list[referencia string cantidad int N])
    facilityProtections:None       # breakers lado AC (list[referencia string cantidad int N])
    pvDPS:None                     # DPS lado DC (string)
    facilityDPS:None               # DPS lado AC (string)
    meter:None                     # referencia del medidor y CT si requiere (list (referencia Medidor referencia CT))
    structData:None                # referencias y cantidades de la estructura (list (referencia metraje m2))
    pipeData:None                  # referencias tipo y metraje de la tuberia (list (referencia metraje m2))
    wires:None                     # Estructura del cableado (list (referencias metraje float m2 referencias metraje float m2))
    pvModulesData:None             # informacion de los modulos solares



class humanResources:
    InstalationData:None           # Tiempo de instalacion estimado (float)
    EngineerTime:None              # Tiempo de dedicacion ingenieria




class siteFeatures:

    distTab_Cont:None              # Distancia del tablero de inversores al contador (float)
    distPv_Tab:None                # Distancia del tablero de inversores a los array (float)
    availableArea:None             # Area disponible (float)
    HSP:None                       # Horas solares Pico (float)
    coords:None                    # Coordenadas del proyecto (list)
    ACConfig:None                  # TAG 3F+N Cantidad de Fases (string)
    TipodeCubierta:None            # Cubierta Metalica Teja de Barro Tipo Suelo(Plancha) (int)
    cubiertaApta:None              # Cubierta Apta (la cubierta es apta)(bool) 
    buitron:None                   # Existencia de buitron (bool)
    azimuthOP:None                 # Azimuth Optimo extraido de PVGIS
    slopeAngleOP:None              # Angulo de inclinacion Optimo
    avgHSP:None                    # promedio HSP de todos los años
    avgYearHSP:None                # promedio de HSP de cada año
    avgHistHSP:None                # Promedio de HSP 
    maxHSP:None                    # Valor máximo de HSP por cada año
    minHSP:None                    # valor mínimo de HSP por cada año
    dayDat:None                    # Data diaria por cada mes
    voltage:None                   # Tension linea neutro existente en la edificacion

    def __init__(self, pr, enne, entyp, aconf, volt, coords,
    area = 0, dt2c=0, dpv2tab=0, tc =0, btrn = 0):
        self.performanceRatio = pr
        self.ener_Need = enne
        self.ener_Type = entyp
        self.ACConfig = aconf
        self.voltage = volt
        self.coords = coords
        self.availableArea = area
        self.distTab_Cont = dt2c
        self.distPv_Tab = dpv2tab
        self.TipodeCubierta = tc
        self.buitron = btrn

    
    
class pvSizing(pvArea, pvProject, inverters, inventary, siteFeatures):
    
    super().__init__(self, pr, enne, entyp, aconf, volt, coords,
            area = 0, dt2c=0, dpv2tab=0, tc =0, btrn = 0)
        


