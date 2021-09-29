
pvModules = {

    #input
    "performanceRatio":[],
    "ener_Need":[],

    #output
    "vArray":[],
    "iArray":[],
    "nArray":[],
    "pvModperArray":[],
    "amountPVMod":[],
    "refPVMod":[],
    "iPVMod":[],
    "vPVMod":[],
    "sizePVMod":[],
    "areaPVMod":[],
    "araTotSyst":[]
}

solarInverter = {
    #input
    "powerNeed":[],

    #output
    "ref":[],           #referencias de inversores seleccionados
    "invAmount":[],     #cantidad por referencia
    "totInvAmount":[],  # cantidad total de inversores
    "cost":[], 
    "iInput":[], 
    "vInput":[], 
    "iOutput":[], 
    "totIoutput":[],
    "vOutput":[], 
    "pOutput":[], 
    "pInput":[]
}

otherElements = {
    "pvWires":[],
    "facilityWires":[],
    "pvProtections":[],
    "facilityProtections":[],
    "pvDPS":[],
    "facilityDPS":[],
    "meter":[],
    "structData":[],
    "pipeData":[],
    "InstalationData":[],
    "wires":[]
}

siteFeatures ={
    "distPv_Tab":[],
    "availableArea":[],
    "HSP":[],
    "coords":[], 
    # ACConfig es un vector que contiene:
    # "TAG 3F+N, Cantidad de Fases"
    "ACConfig":[], 
    "TipodeCubierta":[],
    "cubiertaApta":[],
    "buitron":[]
}

dimensionamiento = {
    pvModules,
    solarInverter,
    siteFeatures

}