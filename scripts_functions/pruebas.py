#import pandas as pd
from sizingOtherElements import *
from protectionsDB import proteccionesDC

config = {
    "fases":3, 
    "tension":230, 
    "stack": 4, 
    "vString":200
    }

DCbreak = buscarProteccionCercana(proteccionesDC, 60, config, 1)
print(DCbreak)

ACbreak = buscarProteccionCercana(proteccionesAC, 90, config, 0)
print(ACbreak)

DPSAC = seleccionDPS(config, DPS_AC, 0)
DPSDC = seleccionDPS(config, DPS_DC, 1)
print(DPSDC)
print(DPSAC)





