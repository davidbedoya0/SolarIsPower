import math
from support_inventary import *
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
class inventary:
    pvWires:None                   # Conductores del lado DC (list [referencias string metraje float m2])
    facilityWires:None             # Conductores del lado AC (list [referencias string metraje float m2])
    pvProtections:None             # breakers lado DC (list[referencia string cantidad int N])
    facilityProtections:None       # breakers lado AC (list[referencia string cantidad int N])
    pvDPS:None                     # DPS lado DC (string)
    facilityDPS:None               # DPS lado AC (string)
    meter:None                     # referencia del medidor y CT si requiere (list (referencia Medidor referencia CT))
    CT:None
    structData:None                # referencias y cantidades de la estructura (list (referencia metraje m2))
    pipeData:None                  # referencias tipo y metraje de la tuberia (list (referencia metraje m2))
    sizewireDC:None
    wireRefDC:None
    sizewireAC:None
    wireRefAC:None
    pipelRefDC:None
    pipelSizeDC:None
    pipelRefAC:None
    pipelSizeAC:None
    pvModulesData:None             # informacion de los modulos solares
    auxiliarData:None

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

    def calculoProtecciones(self, DB_BKR_AC, DB_BKR_DC, DB_DPS_AC, DB_DPS_DC, 
    aconf, vstring, polos, i_input, i_output, v_input, pol_pr_in):
    

        if type(i_output) == list:
            rngAC = len( i_output)
        elif type(i_output) == int:
            rngAC = 1
        if type(i_input) == list:
            rngDC = len( i_input)
        elif type(i_input) == int:
            rngDC = 1

        for i in range( rngAC):
            ifail = i_output[i]
            self.facilityProtections.append(self.buscarProteccionCercana( DB_BKR_AC, ifail, 0, 0, 0, aconf))
            if self.facilityProtections[i] == "ERROR":
                return "ERROR protecciones AC"

        # Busca la proteccion para el lado DC
        for i in range(rngDC):
            Vdc = v_input[i]
            Idc = i_input[i]
            poles = pol_pr_in[i]
            self.pvProtections.append(self.buscarProteccionCercana(DB_BKR_DC, Idc, Vdc, poles, 1, aconf))
            if self.pvProtections[i] == "ERROR":
                return "ERROR protecciones DC"

        # Dimensionamiento
        self.facilityDPS = self.seleccionDPS(DB_DPS_AC, 0, vstring, polos)
        if self.facilityDPS == "ERROR":
            return "ERROR DPS AC"
        
        # Dimensionamiento
        self.pvDPS = self.seleccionDPS(DB_DPS_DC, 1, vstring, polos)
        if self.pvDPS == "ERROR":
            return "ERROR DPS DC"

        return ["success"]

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

    def buscarProteccionCercana( db_bkr, i_fail, tension, polesperInput, typeBreaker, amountWiresAC):

        #Inicializa las variables de diferencia e indicador
        breakerCercano = 1e6
        iCurr = 1e6
        lowV = 1e6
        
        # convierte la columna de corriente en una lista
        ibreakers = db_bkr["corriente"]
        # crea un array con el valor de la corriente del panel
        iPanelArr = [i_fail] * len(ibreakers)    
        # calcula la diferencia entre la corriente de falla y 
        diffI = [e1 - e2 for e1, e2 in zip(ibreakers, iPanelArr)]

        # CASO DC 
        if typeBreaker == 1: 
            # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
            for i, val in enumerate(diffI):
                # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
                if breakerCercano > val and val > 0:
                    if db_bkr["polos"][i] == polesperInput and tension < db_bkr["tension"][i]:
                        if db_bkr["tension"][i] < lowV:
                            breakerCercano = diffI[i]
                            lowV = db_bkr["tension"][i]
                            iCurr = i
            # Se retorna la referencia de la proteccion mas cercana
            if iCurr != 1e6:
                return ["SUCCESS", db_bkr["referencia"][iCurr]]
        # CASO AC 
        else:
            # Se recorre el vector diffI buscando el valor mas cercano a cero positivo
            for i, val in enumerate(diffI):
                # Se actualiza la diferencia mas pequena y mayor a 0 y el indice
                if breakerCercano > val and val > 0:
                    if amountWiresAC == db_bkr["polos"][i]:
                            breakerCercano = diffI[i]
                            iCurr = i
            # Se retorna la referencia de la proteccion mas cercana
            if iCurr!=1e6:
                return db_bkr["referencia"][iCurr]
            
        # Se retorna el mensaje donde se indica que no se encontro la proteccion adecuada
        if iCurr == 1e6:
            return "ERROR"
        
        return "SUCCESS"
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
    def seleccionDPS(DPS_DB, DCoAC, vString, polos):
        
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
    def calculoCableado( self, cableDBAC, cableDBDC, ifailArrDC, ifailArrAC, dt2c, dt2pv, nArray, pvMpArr, sizpvMod, aconf, nInv, dinv2t):

        ###### Seleccion de los conductores para el lado DC    ######
        # Se define el factor de sobredimensionamiento
        factOverSizing = 1.25
        # Se extraen las corrientes de cada array de paneles y se sobredimensionan
        curr = [ factOverSizing * element for element in ifailArrDC]
        
        for j in range(len(curr)):
            [flag, ref, indi] = busquedaComponente(curr[j], cableDBDC, "capCurr", "referencia", "ERROR SELECTING WIRE DC")        
            if flag != "SUCCESS":
                return flag
            else:
                self.wireRefDC.append(ref)

        ###### Seleccion de los conductores para el lado AC  ######

        # Calcula la corriente de falla
        curr = [ element * factOverSizing for element in ifailArrAC]
        
        for j in range ( len(curr)):

            [flag, ref, indi] = busquedaComponente(curr[j], cableDBAC, "capCurr", "reference", "ERROR SELECTING WIRE AC")        
            if flag != "SUCCESS":
                return flag
            else:
                self.wireRefAC.append(ref)
            
        if dt2c != None and dt2pv != None:
            # Calculo cantidad de conductor lado DC

            # Para calcularlo seguimos la siguiente formula
            # PVWireTOTDC = (A + B) * C
            # A -> distancia del tablero a los strings X N Strings X 2
            # B -> Cantidad de Modulos per String X Cantidad strings X anchoMod X 2
            # C -> Factor sobredimensionamiento Normalmente 1.1

            A = dt2pv * nArray * 2
            amArr = len(pvMpArr)
            B = []
            for i in range(amArr):
                B.append(pvMpArr[i] * nArray * sizpvMod * 2)

            C = 1.1 # factor de sobredimensionamiento
            self.sizewireDC = []
            for i in range(len(B)):
                self.sizewireDC.append(math.ceil((A + B[i]) * C))

            # Calculo metraje de los conductores lado AC
            # PVWireTOT = cantidad total de inversores * configuracionAC * distanciaInversores_Medidor * C
            # Se calcula el numero de conductores del lado AC
            [flag, amountWiresAC] = selConfig( aconf, 0)
            # Se extrae la distancia del tablero 
            self.sizewireAC = nInv * amountWiresAC * dinv2t * 1.1
        else: 
            self.sizewireDC = None
            self.sizewireAC = None
        return "SUCCESS"
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
    def seleccionMedidor(self, aconf, totIoutput, dbMeters, dbCT):

        # Se toma la corriente maxima
        current = totIoutput
        # Se extrae la cantidad de polos del sistema
        # Extrae el tipo de configuracion
        typeCon = aconf
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
            [flag, CurTrf, ind] = busquedaComponente(current, dbCT, "corriente", "referencia", "ERROR SIZING CT")
            if flag != "SUCCESS": return "ERROR SELECTING CT"
        else: CurTrf = "MEDIDA DIRECTA"

        self.CT = CurTrf
        self.meter = ref

        return "SUCCESS"
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
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: structureComputation
    ! description: Select the structure for pvmodules accoding to 
    ! roof features. 
    ? inputs: 
        metalStruct: db of pv modules structures to type metalic roof
        claytileStruct: db of pv modules structures to type claytyle roof
        soilStruct: db of pv modules structures to type soil roof
        cubType: Type of roof.
        amMods: Amount of modules to intall in the project

    ? output:
        None
    ! ==========================================================
    """
    def structureComputation(self, metalStruct, claytyleStruct, soilStruct, cubType, amMods):
        
        if cubType > 0 and cubType < 4:
            # Cubierta del tipo metalica
            if cubType == 1:
                [flag, self.structRef, self.StructCant] = quantityStructComputation(metalStruct, amMods)
            # Cubierta del tipo teja de barro
            elif cubType == 2:
                [flag, self.structRef, self.StructCant] = quantityStructComputation(claytyleStruct, amMods)
            # Cubierta del tipo suelo
            elif cubType == 3:
                [flag, self.structRef, self.StructCant] = quantityStructComputation(soilStruct, amMods)
            
            if flag == "ERROR": return "ERROR"
            else: return "SUCCESS"
        else: return "ERROR"
    
    """
    ! ==========================================================
    --- TEST SUCCESS
    +++ Name: pipeliComputation
    ! description: Select the pipeline references and the size 
    ! for each reference
    ? inputs: 
        wiresDBAC: DBconductoresAC
        wiresDBDC: DBconductoresAC
        pipeDB: base de datos de tuberias
        aconf: string con la configuracion AC
        buitron: disponibilidad de buitron para canalizaciones en la instalacion
        dpv2t: distancia modulos a tablero
        pvModpA: cantidad de modulos por array
        sizpvMod: ancho de los modulos PV
        nArr: Cantidad de arrays

    ? output:
        None: success or error flag
    ! ==========================================================
    """
    def pipeliComputation(self, wiresDBAC, wiresDBDC, pipeDB, aconf, buitron, dpv2t, pvModpA, sizpvMod, nArr):

        # ? Calculo del metraje segun la tuberia (expuesta, enterrada)
        # ! Se verifica si existe buitron
        if buitron == 0:
            # Calcula la cantidad de tuberias enterradas
            self.pipelRefAC = dpv2t
            # Calcula la cantidad de tuberias expuestas
            amArr = len(pvModpA)
            self.pipelRefDC = 0
            for i in range(amArr):
                self.pipelRefDC += pvModpA[i] * sizpvMod
        else:
            # Calcula la cantidad de tuberias enterradas
            self.pipelRefAC = 0
            tubExp2 = 0
            # Calcula la cantidad de tuberias expuestas
            tubExp1 = dpv2t
            amArr = len(sizpvMod)
            for i in range(amArr):
                tubExp2 += pvModpA[i] * sizpvMod
            self.pipelRefDC = tubExp1 + tubExp2

        # Calculo cantidad de conductores por la tuberia
        # Lado DC
        amountWiresDC = nArr * 2
        
        # Lado AC
        # Para el lado AC se calcula basado en la cantidad de conductores

        # Se calcula la cantidad de conductores teniendo en cuenta la configuracion
        [flag, amountWiresAC] = selConfig( aconf, 0)
        # En caso de no encontrar la cantidad se retorna un ERROR
        if flag != "SUCCESS": return flag
        # Se extrae la cantidad de referencias de conductores DC
        dimaux = len(self.sizewireDC)
        # Se inicializa la variable de seccion transversal de conductores DC
        seccionAWGDC = 0
        for i in range(dimaux):
            # Se extrae el calibre del conductor DC i
            ind = wiresDBDC["referencia"].index(self.wireRefDC[i])
            # Se suman las secciones transversales de los conductores DC
            seccionAWGDC += wiresDBDC["seccion"][ind]
        
        ###Calculo seccion transversal conductores AC###
        # Se extrae la cantidad de referencias de conductores AC
        dimaux = len(self.wireRefAC)
        # Se inicializa la variable de seccion transversal de conductores AC
        seccionAWGAC = 0
        for i in range(dimaux):
            ind = wiresDBAC["reference"].index(self.wireRefAC[i])
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
        [flag, self.pipelRefDC, ind] = busquedaComponente(CALWires_DC, pipeDB, "seccion", "referencia", "ERROR SELECTING PIPELINE DC")
        [flag, self.pipelRefAC, ind] = busquedaComponente(CALWires_AC, pipeDB, "seccion", "referencia", "ERROR SELECTING PIPELINE AC")
        
        return "SUCCESS"
    