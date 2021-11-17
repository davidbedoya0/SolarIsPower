import math

"""
    ! ==========================================================
    --- TEST NOT SUCCESS
    +++ Name: SelConfig
    ! description: construct class sitefeatures
    ? inputs: 
        config: string with the configuration
        type: type of comparison

    ? output:
        flag: success or error flag message
        amountWiresAC: amount of wires that carry out power in the AC system
    ! ==========================================================
    """

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

    """
    ! ==========================================================
    --- TEST NOT SUCCESS
    +++ Name: busquedaComponentes
    ! description: construct class sitefeatures
    ? inputs: 
        Xval: valor a buscar
        DB: base de datos
        paramDB_1: parametro 1 en la DB
        paramDB_2: parametro 2 en la DB
        ERROR: error a retornar en caso de no encontrar el valor

    ? output:
        None
    ! ==========================================================
    """

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


    return ["SUCCESS", references, cant]