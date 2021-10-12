from PVgisAPI_Consume.pvGIS_API_GET import *
from scripts_functions.initSizingProgram import *
from scripts_functions.sizingOtherElements import *
from scripts_functions.variables import *
from scripts_functions.ComponentsDB import *
from scripts_functions.readPVandInvDB import *


# Dimensionamiento

flag = initProgram(dimensionamiento)
if flag == "SUCCESS":
    flag = pvgisGetData(dimensionamiento)
    if flag == "SUCCESS":
        flag = configuracionPanelesInversor(dimensionamiento, dfInversores, dfPaneles)
        if flag == "SUCCESS":
            flag = otherElementsSising(dimensionamiento, 
                proteccionesAC, proteccionesDC, DPS_AC, DPS_DC, 
                WiresISO, WiresDCIso,
                bdMeters, dbCT, 
                metalicStruct, clayTileStruct, SoilStruct, 
                IMC)
            if flag != "SUCCESS":
                print(flag)
        else:
            print(flag)
    else: 
        print(flag)
else:
    print(flag)



# Analisis Financiero


# Analisis tributario