import requests
from requests.models import Response
from support_dataprep import *

"""
! ==========================================================
--- TEST SUCCESS
+++ Name: siteFeatures <class>

! description: a class that contains site features and methods 
! to prepare data to start with pv project sizing.

? attributes: 
    contain physical and dimensions info of pv project location,
    electrical basic features and solar radiation features

? methods:
    __init__: construct class
    datavalidation: validate input data before sising project
    cases_vll_ac: convert voltage config data from int to real voltage value data
    cases_config_ac: convert ac config data from int to string data
    getgenerationData: get pvgis data and fill attributes

? another functions:
    support_dataprep: contains support functions contained inside methods

! ==========================================================
"""

class siteFeatures:
    
    distTab_Cont:None              # Distancia del tablero de inversores al contador (float)
    distPv_Tab:None                # Distancia del tablero de inversores a los array (float)
    availableArea:None             # Area disponible (float)
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
    neutral:None                   # presencia de nuetro
    poles:None                     # cantidad de polos en la instalacion

    
    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: __init__
    ! description: construct class sitefeatures
    ? inputs: 
        None

    ? output:
        None
    ! ==========================================================
    """
    def __init__(self, pr, enne, entyp, aconf, volt, coords,
    area = None, dt2c = None, dpv2tab = None, tc = None, btrn = None):

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


    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: datavalidation
    ! description: execute validation function across all inputs
    ? inputs: 
        None

    ? output: 
        success or error flag
    ! ==========================================================
    """
    def datavalidation(self):

        supLim = [1.00001, 1e9, 4, 4, 6, [71, 115], 1e6, 900, 900, 3, 2]
        infLim = [0, 0, -1, -1, -1, [-37, -162], 0, 0, 0, -1, -1 ]
        typeData = [1, 1, 0, 0, 0, 2, 1, 1, 1, 0, 0] # o to int, 1 to float, 2 list of float
        error = ["performance Ratio", "energia necesaria", 
        "unidades de energia", "configuracion AC", 
        "tension", "coordenadas", "area", 
        "distancia del tablero al contador", 
        "distancia de modulos a tablero", 
        "tipo de cubierta", "buitron"]

        flag = validation(self.performanceRatio, 1, supLim[0], infLim[0], error[0] + " invalido ", typeData[0])
        if flag != "SUCCESS": return flag
        flag = validation(self.ener_Need, 1, supLim[1], infLim[1], error[1] + " invalido", typeData[1])
        if flag != "SUCCESS": return flag
        flag = validation(self.ener_Type, 1, supLim[2], infLim[2], error[2] + " invalido", typeData[2])
        if flag != "SUCCESS": return flag
        flag = validation(self.ACConfig, 1, supLim[3], infLim[3], error[3] + " invalido", typeData[3])
        if flag != "SUCCESS": return flag
        flag = validation(self.voltage, 1, supLim[4], infLim[4], error[4] + " invalido", typeData[4])
        if flag != "SUCCESS": return flag
        flag = validation(self.coords, 2, supLim[5], infLim[5], error[5] + " invalido", typeData[5])
        if flag != "SUCCESS": return flag
        if self.availableArea != None:
            flag = validation(self.availableArea, 1, supLim[6], infLim[6], error[6] + " invalido", typeData[6])
            if flag != "SUCCESS": return flag
        if self.availableArea != None:
            flag = validation(self.distTab_Cont, 1, supLim[7], infLim[7], error[7] + " invalido", typeData[7])
            if flag != "SUCCESS": return flag
        if self.availableArea != None:
            flag = validation(self.distPv_Tab, 1, supLim[8], infLim[8], error[8] + " invalido", typeData[8])
            if flag != "SUCCESS": return flag
        if self.availableArea != None:
            flag = validation(self.TipodeCubierta, 1, supLim[9], infLim[9], error[9] + " invalido", typeData[9])
            if flag != "SUCCESS": return flag
        if self.availableArea != None:
            flag = validation(self.buitron, 1, supLim[10], infLim[10], error[10] + " invalido", typeData[10])
            if flag != "SUCCESS": return flag

        return "SUCCESS"

    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: cases_config_ac
    ! description: converts ac config attribute in ac config string 
    ? inputs: 
        None

    ? output: 
        success or error flag
    ! ==========================================================
    """
    def cases_Vll_ac(self):
        # case 0 -> 110 V
        if self.voltage == 0:
            self.voltage = 110
        # case 1 -> 120 V
        elif self.voltage == 1:
            self.voltage = 120
        # case 2 -> 127 V
        elif self.voltage == 2:
            self.voltage = 127
        # case 3 -> 208 V
        elif self.voltage == 3:
            self.voltage = 208
        # case 4 -> 220 V
        elif self.voltage == 4:
            self.voltage = 220
        # case 5 -> 254 V
        elif self.voltage == 5:
            self.voltage = 254

    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: cases_config_ac
    ! description: converts ac config attribute in a well described 
    ! string
    ? inputs: 
        None

    ? output: 
        success or error flag
    ! ==========================================================
    """
    def cases_config_ac(self):
        # case 0 -> 1 fase 1 neutro
        if self.ACConfig == 0:
            self.ACConfig = "P+N"
            self.poles = 1
            self.neutral = 1
        # case 1 -> 2 fases
        if self.ACConfig == 1:
            self.ACConfig = "2P"
            self.poles = 2
            self.neutral = 0
        # case 2 -> 3 fases 
        if self.ACConfig == 2:
            self.ACConfig = "3P"
            self.poles = 3
            self.neutral = 0
        # case 3 -> 3 fases 1 neutro
        if self.ACConfig == 2:
            self.ACConfig = "3P+N"
            self.poles = 3
            self.neutral = 1
     
    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: getgenerationData
    ! description: a function that initialize pvgis get data function 
    ! and organize data into sitefeatures class varible
    ? inputs: 
        none

    ? output: 
        success or error flag
    ! ==========================================================
    """
    def getgenerationData(self):
    
        # Request optimum slope angle from 
        [self.slopeAngleOP, flag] = req_pvgis( self.coords[0], self.coords[1], 0)
        if flag !=  "SUCCESS":
            return flag

        # Request monthly data from all available months from pvgis
        [Data, flag]= req_pvgis(self.coords[0], self.coords[1], 1)
        if flag !=  "SUCCESS":
            return flag
        else:
            [avg, avgHist, maxHist, minHist, flag] = anualAverageHSP(Data)
            self.avgYearHSP = avg
            self.avgHistHSP = avgHist
            self.maxHSP = maxHist
            self.minHSP = minHist

        self.dayDat = []
        for i in range(12):
            # Request daily data from every month from pvgis
            [Data, flag] = req_pvgis(self.coords[0], self.coords[1], 2, i + 1)
            if flag !=  "SUCCESS":
                return flag
            else:
                self.dayDat.append(dailyRad(Data))
        
        aux = 0

        for i in range(len(avg)):
            aux += avg[i][0]
        self.avgHSP = aux / len(avg)
        return "SUCCESS"




