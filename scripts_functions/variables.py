
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
    "ref":[],       #referencias de inversores seleccionados
    "invAmount":[], #cantidad por referencia
    "cost":[], 
    "iInput":[], 
    "vInput":[], 
    "iOutput":[], 
    "vOutput":[], 
    "pOutput":[], 
    "pInput":[]
}

otehrElements = {
    "pvWires":[],
    "facilityWires":[],
    "pvProtections":[],
    "facilityProtections":[],
    "pvDPS":[],
    "facilityDPS":[],
    "meter":[],
    "structData":[],
    "pipeData":[],
    "InstalationData":[]
}

dimensionamiento = {
    pvModules,
    solarInverter

}