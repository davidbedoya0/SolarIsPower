import math

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
    Cantidad de protecciones
accesoreios protecciones 
Cantidad de tableros
Accesorios Tableros 
    Seleccion de cable
    Cantidad de cable
    Referencia sistema de medicion 
Accesorios sistemas de medicion
Sistema de adquisicion
Accesorios sistema de adquisicion
    Tiempo Horas hombre
    Tiempo horas hombre ingenieria
    elementos Estructura
    tuberia


"""


def otherElementsSising(
    dimensionamiento, 
    dbBRKAC, dbBRKDC, dbDPSAC, dbPSCDC, 
    cableDBAC, cableDBDC, 
    dbMeters, dbCT, 
    metalicStruct, clayTilStruct, soilStruct, 
    pipeDB
    ):
    
    # Se llama la funcion de calculo de protecciones
    flag = calculoProtecciones(dimensionamiento, dbBRKAC, dbBRKDC, dbDPSAC, dbPSCDC)
    if flag == "ERROR":
        return "ERROR"

    # Se llama la funcion de calculo de cableado
    flag = calculoCableado(dimensionamiento, cableDBAC, cableDBDC)
    if flag == "ERROR":
        return "ERROR"
    
    # Se llama la funcion de calculo de la tuberia, sirve con cualquier DB de tuberia
    flag = pipeliComputation( dimensionamiento, cableDBAC, cableDBDC, pipeDB)
    if flag == "ERROR":
        return "ERROR"

    # Se llama la funcion de seleccion del medidor
    flag = seleccionMedidor( dimensionamiento, dbMeters, dbCT)
    if flag == "ERROR":
        return "ERROR"
    
    # Se llama la funcion de dimensionamiento de la estructura
    flag = structureComputation( dimensionamiento, metalicStruct, clayTilStruct, soilStruct)
    if flag == "ERROR":
        return "ERROR"

    return "SUCCESS"


"""
# +++ Descripcion: Calcula la proteccion especifica que se necesita en el sistema 
# +++ para el lado DC o AC. 

# ! Inputs: 
?Dataframe de configuracion
?Base de datos breakers AC
?Base de datos breakers DC
?Base de datos DPS AC
?Base de datos DPS DC

# ! Outputs: 
? bandera success
"""

def calculoProtecciones(dimensionamiento, DB_BKR_AC, DB_BKR_DC, DB_DPS_AC, DB_DPS_DC):

    # Calculo de protecciones de salida
    # Recorre columna de corrientes de inversores para breakers AC
    if type(dimensionamiento["solarInverter"]["iOutput"]) == list:
        rngAC = len( dimensionamiento["solarInverter"]["iOutput"])
    elif type(dimensionamiento["solarInverter"]["iOutput"]) == int:
        rngAC = 1
    if type(dimensionamiento["solarInverter"]["iInput"]) == list:
        rngDC = len( dimensionamiento["solarInverter"]["iInput"])
    elif type(dimensionamiento["solarInverter"]["iInput"]) == int:
        rngDC = 1

    for i in range( rngAC):
        ifail = dimensionamiento["solarInverter"]["iOutput"][i]
        dimensionamiento["otherElements"]["facilityProtections"].append(buscarProteccionCercana( DB_BKR_AC, ifail, 0, 0,dimensionamiento, 0))
        if dimensionamiento["otherElements"]["facilityProtections"][i] == "ERROR":
            return "ERROR protecciones AC"

    # Busca la proteccion para el lado DC
    for i in range(rngDC):
        Vdc = dimensionamiento["solarInverter"]["vOutput"][i]
        Idc = dimensionamiento["solarInverter"]["iInput"][i]
        poles = dimensionamiento["solarInverter"]["polesperInput"][i]
        dimensionamiento["otherElements"]["pvProtections"].append(buscarProteccionCercana(DB_BKR_DC, Idc, Vdc, poles, dimensionamiento, 1))
        if dimensionamiento["otherElements"]["pvProtections"][i] == "ERROR":
            return "ERROR protecciones DC"

    # Dimensionamiento
    dimensionamiento["otherElements"]["facilityDPS"] = seleccionDPS(dimensionamiento, DB_DPS_AC, 0)
    if dimensionamiento["otherElements"]["facilityDPS"] == "ERROR":
        return "ERROR DPS AC"
    
    # Dimensionamiento
    dimensionamiento["otherElements"]["pvDPS"] = seleccionDPS(dimensionamiento, DB_DPS_DC, 1)
    if dimensionamiento["otherElements"]["pvDPS"] == "ERROR":
        return "ERROR DPS DC"

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

def buscarProteccionCercana( df, i_fail, tension, polesperInput, dimensionamiento, typeBreaker):

    # convierte la columna de corriente en una lista
    ibreakers = df["corriente"]

    # crea un array con el valor de la corriente del panel
    iPanelArr = [i_fail] * len(ibreakers)
    typeCon = dimensionamiento["siteFeatures"]["ACConfig"]
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

    # calcula la diferencia entre la corriente de falla y 
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
                if df["polos"][i]==polesperInput and tension < df["tension"][i]:
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
    
    return "SUCCESS"

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
    
    polos = max(config["solarInverter"]["polesperInput"])
    # extrae la tension de operacion maxima de los string del lado DC
    vString = config["pvModules"]["vArraymax"]
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
                if DPS_DB["polos"][i] == polos:
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

    ###### Seleccion de los conductores para el lado DC    ######
    # Crea el array donde se almacenaran las referencias de los conductores
    referencePVWire = []
    referenceACWire = []
    # Se define el factor de sobredimensionamiento
    factOverSizing = 1.25
    # Se extraen las corrientes de cada array de paneles y se sobredimensionan
    curr = [ factOverSizing * element for element in dimensionamiento["pvModules"]["iArray"]]
    
    for j in range(len(curr)):
        [flag, ref, indi] = busquedaComponente(curr[j], cableDBDC, "capCurr", "referencia", "ERROR SELECTING WIRE DC")        
        if flag != "SUCCESS":
            return flag
        else:
            referencePVWire.append(ref)

    ###### Seleccion de los conductores para el lado AC  ######

    # Calcula la corriente de falla
    curr = [ element * factOverSizing for element in dimensionamiento["solarInverter"]["iOutput"]]
    
    for j in range ( len(curr)):

        [flag, ref, indi] = busquedaComponente(curr[j], cableDBAC, "capCurr", "reference", "ERROR SELECTING WIRE AC")        
        if flag != "SUCCESS":
            return flag
        else:
            referenceACWire.append(ref)
        
    if dimensionamiento["siteFeatures"]["distTab_Cont"] != None or dimensionamiento["siteFeatures"]["distPv_Tab"] != None:
        # Calculo cantidad de conductor lado DC

        # Para calcularlo seguimos la siguiente formula
        # PVWireTOTDC = (A + B) * C
        # A -> distancia del tablero a los strings X N Strings X 2
        # B -> Cantidad de Modulos per String X Cantidad strings X anchoMod X 2
        # C -> Factor sobredimensionamiento Normalmente 1.1

        nArray = dimensionamiento["pvModules"]["nArray"]

        A = dimensionamiento["siteFeatures"]["distPv_Tab"] * nArray * 2
        amArr = len(dimensionamiento["pvModules"]["pvModperArray"])
        B = []
        for i in range(amArr):
            B.append(dimensionamiento["pvModules"]["pvModperArray"][i] * nArray * dimensionamiento["pvModules"]["sizePVMod"][1] * 2)

        C = 1.1

        PVWireTOTDC = []
        for i in range(len(B)):
            PVWireTOTDC.append(math.ceil((A + B[i]) * C))

        # Calculo metraje de los conductores lado AC

        # Para calcularlo seguimos la siguiente formula
        # PVWireTOT = cantidad total de inversores * configuracionAC * distanciaInversores_Medidor * C
        
        # Se extrae la configuracion
        typeCon = dimensionamiento["siteFeatures"]["ACConfig"]
        # Se calcula el numero de conductores del lado AC
        [flag, amountWiresAC] = selConfig( typeCon, 0)
        # Se extraer la cantidad de inversores
        nInv = dimensionamiento["solarInverter"]["totInvAmount"]
        # Se extrae la distancia del tablero 
        distInv2Tab = dimensionamiento["siteFeatures"]["distTab_Cont"]
        WireTOTAC = nInv * amountWiresAC * distInv2Tab * 1.1

        dimensionamiento["otherElements"]["pvWires"] = [ referencePVWire, PVWireTOTDC]
        dimensionamiento["otherElements"]["facilityWires"] = [ referenceACWire, WireTOTAC]

    else: 
        WireTOTAC = None
        PVWireTOTDC = None

    return "SUCCESS"

"""

# Descripcion: selecciona el sistema de medicion de energia

# Inputs: 
Tension AC
Corriente AC 
configuracion AC


# Outputs: 
referenciaMedidor

"""

def seleccionMedidor( dimensionamiento, dbMeters, dbCT):

    ref = None
    # Se verifica que existe la corriente total de salida de los inversores
    if dimensionamiento["solarInverter"]["totIoutput"] == None:

        # Se extrae el tamano del vector de corrientes de salida de inversores
        tam = len(dimensionamiento["solarInverter"]["iOutput"])
        # Se inicializa la variable acumuladora
        acumul = 0
        # Se verifica el tamano del vector de corrientes de salida de inversores
        if tam > 0:
            # Se recorre el vector
            for i in range(tam):
                # Se suman todas las corrientes en una variable auxiliar
                acumul += dimensionamiento["solarInverter"]["iOutput"][i]
            # Se almacena la corriente total 
            dimensionamiento["solarInverter"]["totIoutput"] = acumul 

    # Se toma la corriente maxima
    current = dimensionamiento["solarInverter"]["totIoutput"]
    # Se extrae la cantidad de polos del sistema
    # Extrae el tipo de configuracion
    typeCon = dimensionamiento["siteFeatures"]["ACConfig"]
    # Calcula la cantidad de polos de acuerdo a la conexion
    [flag, polos] = selConfig(typeCon, 1)
    if flag != "SUCCESS": return flag
    # Recorre la DB de medidores de acuerdo a los polos
    for ind in range(len(dbMeters["polos"])):
        # Verifica si los polos a medir en el sistema son iguales a los de la referencia
        if polos == dbMeters["polos"][ind]:
            # Verifica si la corriente es menor a 120 para medida directa
            if current < 120 and dbMeters["tipo"][ind] == 1:
                # Almacena la referencia seleccionada del medidor
                ref = dbMeters["referencia"][ind]
                # Escribe la bandera de medida directa
                directa = True
            # Verifica si la corriente es mayor a 120 A para medida semidirecta
            if current > 120 and dbMeters["tipo"][ind] == 0:
                # Almacena la referencia del medidor
                ref = dbMeters["referencia"][ind]
                # Escribe la bandera de medida directa como False
                directa = False

    if ref == None: return "ERROR SELECTING METER"

    ## Seleccion del Transformador de Corriente
    # Verifica si el medidor no es de medida semidirecta
    if directa == False:
        [flag, CT, ind] = busquedaComponente(current, dbCT, "corriente", "referencia", "ERROR SIZING CT")
        if flag != "SUCCESS": return "ERROR SELECTING CT"
    else: CT = "MEDIDA DIRECTA"

    # Se retorna la informacion de la funcion
    dimensionamiento["otherElements"]["meter"] = [ref, CT]
    return "SUCCESS"



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

def tiempoinstalacionTotal(dimensionamiento):

    Horas = [2.5, 4, 1, 4, 3, 3, 3]

    # Sigue la siguiente ecuacion para el calculo 
    # instalationTime = A + B + C + D + E + F
    # A = AreaCubiertaReemplazo * 2.5 hrs
    # B = Cantidadtableros * 4 hrs
    # C = longitudTuberiaExpuesta *  1 hr + longitudTuberiaEnterrada *  4 hr 
    # D = CantidadInversores * 3 hrs
    # E = CantidadModulos * 3 hrs
    # F = CantidadContadores * 3hrs
    
    if dimensionamiento["siteFeatures"]["cubiertaApta"] != 0: 
        if dimensionamiento["siteFeatures"]["TipodeCubierta"] == 0 or dimensionamiento["siteFeatures"]["TipodeCubierta"] == 2: 
            AreaCubiertaReemplazo = dimensionamiento["pvModules"]["areaTotSyst"]
        elif dimensionamiento["siteFeatures"]["TipodeCubierta"] == 1: 
            AreaCubiertaReemplazo = 0
        else:
            return "ERROR CON TIPO DE CUBIERTA"
    else:
        AreaCubiertaReemplazo = 0

    A = AreaCubiertaReemplazo * Horas[0]


    if dimensionamiento["siteFeatures"]["buitron"]==0:
        longitudTuberiaEnterrada = dimensionamiento["siteFeatures"]["distPv_Tab"]
    


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
            dimensionamiento["otherElements"]["structData"] = quantityStructComputation(metalStruct, amMods)
        # Cubierta del tipo teja de barro
        elif cubType == 2:
            dimensionamiento["otherElements"]["structData"] = quantityStructComputation(claytyleStruct, amMods)
        # Cubierta del tipo suelo
        elif cubType == 3:
            dimensionamiento["otherElements"]["structData"] = quantityStructComputation(soilStruct, amMods)
        
        if dimensionamiento["otherElements"]["structData"] == "ERROR":
                return "ERROR"
        else:
            return "SUCCESS"
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
    references = []
    cant = []
    cp = 0

    while amMods_ > 0:

        # Calcula la referencia con la que menos unidades se gastan
        for i in range(len(db["reference"])):
            # Cantidad de modulos que se extraen
            val = db["cantidadModulos"][i]
            # Unidades a extraer
            unidades = math.ceil( amMods_ / val)
            resto = amMods_ % val
  
            if unidades < unidadesAnt:
                unidadesAnt = unidades
                cant_ = unidades
                resto_ = resto
                ind = i
        cp += 1
        if cp > 50:
            return "ERROR"

        references.append(db["reference"][ind])
        cant.append(cant_)
        amMods_ = resto_


    return [references, cant]


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

def pipeliComputation( dimensionamiento, wiresDBAC, wiresDBDC, pipeDB):

    # Calculo del metraje y tipo de tuberia (expuesta, enterrada)
    # Verificamos si existe buitron para uso de IMT
    if dimensionamiento["siteFeatures"]["buitron"] == 0:
        # Calcula la cantidad de tuberias enterradas
        tubEnterrada = dimensionamiento["siteFeatures"]["distPv_Tab"]
        # Calcula la cantidad de tuberias expuestas
        amArr = len(dimensionamiento["pvModules"]["pvModperArray"])
        tubExpuesta = 0
        for i in range(amArr):
            tubExpuesta += dimensionamiento["pvModules"]["pvModperArray"][i] * dimensionamiento["pvModules"]["sizePVMod"][1]
    else:
        # Calcula la cantidad de tuberias enterradas
        tubEnterrada = 0
        tubExp2 = 0
        # Calcula la cantidad de tuberias expuestas
        tubExp1 = dimensionamiento["siteFeatures"]["distPv_Tab"]
        amArr = len(dimensionamiento["pvModules"]["pvModperArray"])
        for i in range(amArr):
            tubExp2 += dimensionamiento["pvModules"]["pvModperArray"][i] * dimensionamiento["pvModules"]["sizePVMod"][1]
        tubExpuesta = tubExp1 + tubExp2

    # Calculo cantidad de conductores por la tuberia
    # Lado DC
    amountWiresDC = dimensionamiento["pvModules"]["nArray"] * 2
    
    # Lado AC
    # Para el lado AC se calcula basado en la cantidad de conductores

    # Se extrae la configuracion de la estructura del dimensionamiento 
    config = dimensionamiento["siteFeatures"]["ACConfig"]
    # Se calcula la cantidad de conductores teniendo en cuenta la configuracion
    [flag, amountWiresAC] = selConfig( config, 0)
    # En caso de no encontrar la cantidad se retorna un ERROR
    if flag != "SUCCESS":
        return flag

    ##########################################################################
    # Calculo de la tuberia
    ##########################################################################

    ###Calculo seccion transversal conductores DC###
    # Se extrae la cantidad de referencias de conductores DC
    dimaux = len(dimensionamiento["otherElements"]["pvWires"][0])
    # Se inicializa la variable de seccion transversal de conductores DC
    seccionAWGDC = 0
    for i in range(dimaux):
        # Se extrae el calibre del conductor DC i
        ind = wiresDBDC["referencia"].index(dimensionamiento["otherElements"]["pvWires"][0][i])
        # Se suman las secciones transversales de los conductores DC
        seccionAWGDC += wiresDBDC["seccion"][ind]
    
    
    ###Calculo seccion transversal conductores AC###
    # Se extrae la cantidad de referencias de conductores AC
    dimaux = len(dimensionamiento["otherElements"]["facilityWires"][0])
    # Se inicializa la variable de seccion transversal de conductores AC
    seccionAWGAC = 0
    for i in range(dimaux):
        ind = wiresDBAC["reference"].index(dimensionamiento["otherElements"]["facilityWires"][0][i])
        # Se suman las secciones transversales de los conductores AC 
        seccionAWGAC += wiresDBAC["seccion"][ind]
    
    # Calcula el calibre optimo si hay dos conductores DC
    if amountWiresDC <= 2: CALWires_DC = seccionAWGDC / 0.31
    # Calcula el calibre optimo si hay mas de dos conductores DC
    else: CALWires_DC = seccionAWGDC / 0.40
    # Calcula el calibre optimo si hay dos conductores AC
    if amountWiresAC <= 2: CALWires_AC = seccionAWGAC / 0.31
    # Calcula el calibre optimo si hay mas de dos conductores AC
    else: CALWires_AC = seccionAWGAC / 0.40

    # Busca la seccion comercial que se acomode a la seccion optima

    [flag, ref, ind] = busquedaComponente(CALWires_DC, pipeDB, "seccion", "referencia", "ERROR SELECTING PIPELINE DC")
    [flag, ref, ind] = busquedaComponente(CALWires_AC, pipeDB, "seccion", "referencia", "ERROR SELECTING PIPELINE AC")
    
    refSeccOptDC = pipeDB["referencia"][ind]
    refSeccOptAC = pipeDB["referencia"][ind]

    return [refSeccOptAC, dimensionamiento["siteFeatures"]["distTab_Cont"],
        refSeccOptDC, tubEnterrada, tubExpuesta]




def selConfig( config, type):
    OP_1 = [4, 3, 2, 2]
    OP_2 = [3, 3, 2, 1]
    OPS = [OP_1, OP_2, OP_1, OP_2]
    ERRORchar = ["ERROR finding AC config to pipelines", "ERROR finding AC config to Protections", 
                "ERROR finding AC config to Wiring", "ERROR finding AC config to Meter"] 

    amountWiresAC = None

    if config == "3P+N": amountWiresAC = OPS[type][0]
    elif config == "3P": amountWiresAC = OPS[type][1]
    elif config == "2P": amountWiresAC = OPS[type][2]
    elif config == "1P": amountWiresAC = OPS[type][3]
    if amountWiresAC == None: return [ERRORchar[type], 0]
    else: return ["SUCCESS", amountWiresAC]


def busquedaComponente(Xval, DB, paramDB_1, paramDB_2, ERROR):

    ref = ERROR

    ind = 1e9
    befDiff = 1e9

    # Busca la seccion comercial que se acomode a la seccion optima
    for i in range(len(DB[paramDB_1])):
        # Calcula la diferencia entre la seccion comercial y la seccion optima
        diff = DB[paramDB_1][i] - Xval
        if diff > 0 and diff < befDiff:
            befDiff = diff
            ind = i

    ref = DB[paramDB_2][ind]

    if ind == 1e9:
        return ["ERROR", None, None]

    return ["SUCCESS", ref, ind]

    