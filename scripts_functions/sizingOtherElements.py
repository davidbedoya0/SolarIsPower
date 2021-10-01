
"""

# Descripcion. Calcula la configuracion de las protecciones, el tablero, cableado, 
estructura,sistemas de medicion, adquisicion, tiempo horas hombre y horas 
de ingenieria.

# Inputs 
dimensionamiento
base de datos breakers AC
base de datos breakers DC
base de datos DPS AC
base de datos DPS DC

# Outputs
    bandera: SUCCESS o ERROR


"""

def otherElementsSising(
    dimensionamiento, 
    dbBRKAC, 
    dbBRKDC, 
    dbDPSAC, 
    dbPSCDC):

    
    flag = calculoProtecciones(dimensionamiento, dbBRKAC, dbBRKDC, dbDPSAC, dbPSCDC)
    if flag == "ERROR":
        return "ERROR"
    

"""
# Descripcion: Calcula la proteccion especifica que se necesita en el sistema 
para el lado DC o AC. 

# Inputs: 
Dataframe de configuracion
Base de datos breakers AC
Base de datos breakers DC
Base de datos DPS AC
Base de datos DPS DC

# Outputs: 
Dataframe de configuracion actualizado
    Se actualiza el array proteccion AC
    Se actualiza el array proteccion DC
    Se actualiza el string DPS AC
    Se actualiza el string DPS DC
"""

def calculoProtecciones(dimensionamiento, DB_BKR_AC, DB_BKR_DC, DB_DPS_AC, DB_DPS_DC):

    # Calculo de protecciones de salida
    # Recorre columna de corrientes de inversores para breakers AC
    for iFalla in range( len( dimensionamiento["solarInverter"]["iOutput"])):
        dimensionamiento["otherElements"]["facilityProtections"] = buscarProteccionCercana( DB_BKR_AC, iFalla, dimensionamiento, 0)
        if dimensionamiento["otherElements"]["facilityProtections"] == "ERROR":
            return "ERROR"

    # Busca la proteccion para el lado DC
    dimensionamiento["otherElements"]["pvProtections"] = buscarProteccionCercana(DB_BKR_DC, dimensionamiento["solarInverter"]["iOutput"])
    if dimensionamiento["otherElements"]["pvProtections"] == "ERROR":
        return "ERROR"

    # Dimensionamiento
    dimensionamiento["pvDPS"] = seleccionDPS(dimensionamiento, DB_DPS_AC, 0)
    if dimensionamiento["pvDPS"] == "ERROR":
        return "ERROR"
    
    # Dimensionamiento
    dimensionamiento["facilityDPS"] = seleccionDPS(dimensionamiento, DB_DPS_DC, 1)
    if dimensionamiento["facilityDPS"] == "ERROR":
        return "ERROR"

    return "SUCCESS"

"""
# Descripcion: Calcula el breaker para el circuito. Funciona para AC y DC

# Inputs: 
Base de datos de breakers (AC o DC)
Corriente de falla
estructura que contiene la info del dimensionamiento
Tipo de breaker a seleccionar (DC o AC)

# Outputs: 
Referencia o success
"""

def buscarProteccionCercana( df, i_fail, dimensionamiento, typeBreaker):

    # convierte la columna de corriente en una lista
    ibreakers = df["corriente"]

    # crea un array con el valor de la corriente del panel
    iPanelArr = [i_fail] * len(ibreakers)
    typeCon = dimensionamiento["siteFeatures"]["ACConfig"]
    tension = dimensionamiento["solarInverter"]["vOutput"]
    n_string = dimensionamiento["pvModules"]["nArray"]

    if typeCon == "3P+N":
        amountWiresAC = 3
    elif typeCon == "3P": 
        amountWiresAC = 3
    elif typeCon == "2P": 
        amountWiresAC = 2
    elif typeCon == "1P": 
        amountWiresAC = 1
    else:
        return "ERROR"

    # calcula la diferencia entre los dos paneles
    diffI = [e1 - e2 for e1, e2 in zip(ibreakers, iPanelArr)]

    #Inicializa las variables de diferencia e indicador
    breakerCercano = 1e6
    iCurr = 1e6
    lowV = 1e6

    # CASO DC 
    if typeBreaker == 1: 
        # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
        for i, val in enumerate(diffI):
            # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
            if breakerCercano > val and val > 0:
                if amountWiresAC == df["polos"][i] and tension < df["tension"][i]:
                    if df["tension"][i] < lowV:
                        breakerCercano = diffI[i]
                        lowV = df["tension"][i]
                        iCurr = i
        # Se retorna la referencia de la proteccion mas cercana
        if iCurr != 1e6:
            return [df["referencia"][iCurr], n_string]
    # CASO AC 
    else:
        # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
        for i, val in enumerate(diffI):
            # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
            if breakerCercano > val and val > 0:
                if amountWiresAC == df["polos"][i]:
                        breakerCercano = diffI[i]
                        iCurr = i
        # Se retorna la referencia de la proteccion mas cercana
        if iCurr!=1e6:
            return df["referencia"][iCurr]
        
    # Se retorna el mensaje donde se indica que no se encontro la proteccion adecuada
    if iCurr == 1e6:
        return "ERROR"

"""
# Descripcion: selecciona el DPS, es valido para lado DC y AC

# Inputs: 
dimensionamiento: estructura que contiene todas las variables de dimensionamiento
DPS_DB: Base de datos del DPS (valida para DB AC y DC)
DCoAC: variable que indica si el calculo del DPS es AC o DC

# Outputs: 
currRef : retorna la referencia del DPS
"""

def seleccionDPS(config, DPS_DB, DCoAC):
    
    # extrae la tension de operacion de los string del lado DC
    vString = config["vString"]
    # Inicializa la referencia actual y la diferencia de tension
    currREF = ""
    Vdiffant = 1e6
    # recorre la matriz de referencias de DPS buscando el mas cercano que sea superior
    for i, val in enumerate(DPS_DB["tension"]):
        # calcula la diferencia de tension de la referencia con respecto a la tension del string 
        Vdiff = val - vString
        # Se verifica que la diferencia sea positiva y menor a la anterior diferencia
        if Vdiff < Vdiffant and Vdiff > 0:
            if DCoAC == 1:
                # Se almacena la nueva mejor diferencia
                Vdiffant = Vdiff
                # Se almacena la referencia
                currREF = DPS_DB["referencia"][i]
            else:
                if DPS_DB["polos"][i] == config["fases"]:
                    # Se almacena la nueva mejor diferencia
                    Vdiffant = Vdiff
                    # Se almacena la referencia
                    currREF = DPS_DB["referencia"][i]
    # Se retorna la referencias
    if Vdiffant == 1e6:
        return "ERROR"
    else:
        return currREF

"""
# Descripcion: Calcula la cantidad total de cable que es necesaria para el proyecto en 
su lado AC y DC.

# Inputs: 
Dataframe cables mercado
Corriente salida arreglo paneles
Corriente salida inversores
Distancia ubicacion tablero - paneles
Area arreglos paneles solares

# Outputs: 
Dataframe cableado necesarias
    tipo
    configuracion
    distancia
"""

def calculoCableado( dimensionamiento, cableDBAC, cableDBDC):

    factOverSizing = 1.25
    # Se extrae la corriente necesaria
    curr = dimensionamiento["pvModules"]["iArray"] * factOverSizing
    befDiffCurr = 1e9
    # Seleccion de la referencia del conductor para el lado DC
    for i, idx, in cableDBDC["capCurr"]:
        diffCurr = i - curr
        if diffCurr < befDiffCurr and diffCurr > 0:
            befDiffCurr = diffCurr
            ind = idx

    referencePVWire = cableDBDC["capCurr"][ind]

    curr = dimensionamiento["solarInverter"]["iOutput"] * factOverSizing
    befDiffCurr = 1e9
    # Seleccion de la referencia del conductor para el lado AC
    for i, idx, in cableDBAC["capCurr"]:
        diffCurr = i - curr
        if diffCurr < befDiffCurr and diffCurr > 0:
            befDiffCurr = diffCurr
            ind = idx

    referenceACWire = cableDBAC["capCurr"][ind]

    # Calculo cantidad de conductor lado DC

    # Para calcularlo seguimos la siguiente formula
    # PVWireTOTDC = (A + B) * C
    # A -> distancia del tablero a los strings X N Strings X 2
    # B -> Cantidad de Modulos per String X Cantidad strings X anchoMod X 2
    # C -> Factor sobredimensionamiento Normalmente 1.1

    nArray = dimensionamiento["pvModules"]["nArray"]

    A = dimensionamiento["siteFeatures"]["distPv_Tab"] * nArray * 2
    B = dimensionamiento["pvModules"]["pvModperArray"] * nArray * dimensionamiento["pvModules"]["areaPVMod"][1] *2
    C = 1.1

    PVWireTOTDC = (A + B) * C

    # Calculo cantidad de conductor lado AC

    # Para calcularlo seguimos la siguiente formula
    # PVWireTOT = cantidad total de inversores * configuracionAC * distanciaInversores_Medidor * C

    nInv = dimensionamiento["solarInverter"]["totInvAmount"]
    PVWireTOTAC = nInv * dimensionamiento["siteFeatures"]["ACConfig"][1] * 1.1

    return[PVWireTOTAC, referenceACWire, PVWireTOTDC, referencePVWire]

"""

# Descripcion: selecciona el sistema de medicion de energia

# Inputs: 
Tension AC
Corriente AC 
configuracion AC


# Outputs: 
referenciaMedidor

"""

def seleccionMedidor(
    dimensionamiento,
    dbMeters, 
    dbCT):
    current = dimensionamiento["solarInverter"]["totIoutput"]
    polos = dimensionamiento["siteFeatures"]["ACConfig"]["polos"]
    for val, ind in dbMeters[polos]:
        if polos == val:
            if current < 120 and dbMeters["tipo"][ind] == 1:
                ref = dbMeters["referencia"][ind]
                directa = True
            if current > 120 and dbMeters["tipo"][ind] == 0:
                ref = dbMeters["referencia"][ind]
                directa = False

    if directa == False:

        currentdif = 1e9
        for val, ind in dbCT["corriente"]:
            diff = val - current
            if diff > 0 & diff < currentdif:
                if val > current * 1.5:
                    currentdif = diff
                    index = ind
        CT = dbCT["referencia"][index]

    else:
        CT = "MEDIDA DIRECTA"

    return [ref, CT]



"""

# Descripcion: Calcula el tiempo total de instalacion del proyecto para un trabajador

# Inputs: 
cantidad Tableros
longitud cableado
cantidad modulos PV 
cantidad inversores


# Outputs: 
Timepo horas Hombre

"""

def tiempoinstalacionTotal(
    dimensionamiento, 
    longitudCableado,
    cantidadModulosPV, 
    cantidadInversores):

    # Sigue la siguiente ecuacion para el calculo 
    # instalationTime = A + B + C + D + E + F
    # A = AreaCubiertaReemplazo * 2.5 hrs
    # B = Cantidadtableros * 4 hrs
    # C = longitudTuberiaExpuesta *  1 hr + longitudTuberiaEnterrada *  4 hr 
    # D = CantidadInversores * 3 hrs
    # E = CantidadModulos * 4 hrs
    # F = CantidadContadores * 3hrs
    
    if dimensionamiento["siteFeatures"]["cubiertaApta"]==1:
        areaCubiertaReemplazo = 0;
    if dimensionamiento["siteFeatures"]["buitron"]==0:
        longitudTuberiaEnterrada = dimensionamiento["siteFeatures"]["distPv_Tab"]
    

    return [tiempoInstalacion]


"""

# Descripcion: Calcula el tipo de estructura y la cantidad necesaria

# Inputs: 
Cantidad de paneles
Tipo de techo (Opcional)
dataframe estructura paneles comerciales
Area arreglo


# Outputs: 
dataframe estructura para paneles proyecto

"""

def structureComputation(
    dimensionamiento, 
    metalStruct, 
    claytyleStruct,
    soilStruct
    ):

    cubType = dimensionamiento["siteFeatures"]["TipodeCubierta"]
    amMods = dimensionamiento["pvModules"]["amountPVMod"]
    
    if cubType > 0 and cubType < 4:
        # Cubierta del tipo metalica
        if cubType == 1:
            return quantityStructComputation(metalStruct, amMods)
        # Cubierta del tipo teja de barro
        elif cubType == 2:
            return quantityStructComputation(claytyleStruct, amMods)
        # Cubierta del tipo suelo
        elif cubType == 3:
            return quantityStructComputation(soilStruct, amMods)
    else:
        return "ERROR"


"""
# Descripcion: Calcula la cantidad total de cable que es necesaria para el proyecto en 
su lado AC y DC.

# Inputs: 
Dataframe cables mercado
Corriente salida arreglo paneles
Corriente salida inversores
Distancia ubicacion tablero - paneles
Area arreglos paneles solares

# Outputs: 
Dataframe cableado necesarias
    tipo
    configuracion
    distancia
"""

def quantityStructComputation(db, amMods):
    amMods_ = amMods
    unidadesAnt = 1e9
    i = 0
    k = 0
    references = []
    unidades = []

    while amMods_ > 0:

        val = db["cantidadModulos"][i]
        unidades = val / amMods_
        resto = val % amMods_

        if unidades < unidadesAnt:

            unidadesAnt = unidades
            amMods_ = resto
            references[k] = db["reference"][i]
            unidades[k] = unidades
            k =+ 1
        i += 1

    return [references]


"""

# Descripcion: Calcula la tuberia necesaria desde el punto 

# Inputs: 
Estructura de dimensionamiento
Base de datos cableado AC
Base de datos cableado DC
Base de datos tuberia

# Outputs: 
dataframe tuberia

"""

def pipeliComputation(
    dimensionamiento, 
    wiresDBAC, 
    wiresDBDC,
    pipeDB
    ):

    # Calculo del metraje y tipo de tuberia (expuesta, enterrada)
    # Verificamos si existe buitron para uso de IMT
    overSize = 1.2
    if dimensionamiento["siteFeatures"]["buitron"]==0:
        tubEnterrada = dimensionamiento["siteFeatures"]["distPv_Tab"]
        tubExpuesta = dimensionamiento["pvModules"]["pvModperArray"]*dimensionamiento["pvModules"]["sizePVMod"][1]
    else:
        tubEnterrada = 0
        tubExp1 = dimensionamiento["siteFeatures"]["distPv_Tab"]
        tubExp2 = dimensionamiento["pvModules"]["pvModperArray"]*dimensionamiento["pvModules"]["sizePVMod"][1]
        tubExpuesta = tubExp1 + tubExp2

    # Calculo cantidad de conductores por la tuberia
    # Lado DC
    amountWiresDC = dimensionamiento["pvModules"]["nArray"]*2
    
    # Lado AC
    # Para el lado AC se tiene en cuenta una cantidad de conductores igual a 
    # la configuracion del sistema

    config = dimensionamiento["siteFeatures"]["ACConfig"]

    if config == "3P+N":
        amountWiresAC = 4
    elif config == "3P": 
        amountWiresAC = 3
    elif config == "2P": 
        amountWiresAC = 2
    elif config == "1P": 
        amountWiresAC = 2

    # Calculo de la tuberia
    # conversion de AWG a mm2

    ind = wiresDBAC["reference"].index(dimensionamiento["otherElements"]["pvWires"])
    # Se extrae el calibre
    seccionAWGDC = wiresDBAC["seccion"][ind]
    seccionAWGAC = wiresDBDC["seccion"][ind]
    # Calculo seccion optima del tubo
    
    if amountWiresDC == 2:
        seccionOptimaDC = seccionAWGDC / 31
    else:
        seccionOptimaDC = seccionAWGDC / 40

    if amountWiresAC == 2:
        seccionOptimaAC = seccionAWGAC / 31
    else:
        seccionOptimaAC = seccionAWGAC / 40

    seccionOpt = 1e9
    # Buscar seccion 
    for val, ind in pipeDB["seccion"]:
        diff = val - seccionOptimaAC
        if diff > 0 and diff < seccionOpt:
            seccionOpt = pipeDB["seccion"][ind]
            indopt = ind

    refSeccOptAC = pipeDB["referencia"][ind]
            
    for val, ind in pipeDB["seccion"]:
        diff = val - seccionOptimaDC
        if diff > 0 and diff < seccionOpt:
            seccionOpt = pipeDB["seccion"][ind]
            indopt = ind

    refSeccOptDC = pipeDB["referencia"][ind]

    return [refSeccOptAC, dimensionamiento["siteFeatures"]["distTab2Cont"],
        refSeccOptDC, tubEnterrada, tubExpuesta]



