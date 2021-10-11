

def initProgram(dimensionamiento):

    optACconfig = ["3P+N", "3P", "2P", "1P" ]
    voltageLevel = [110, 120, 127, 208, 220, 230]
    energranul = ["kwh/dia", "kwh/mes", "kwh/año"]
    errText = ["distancia tablero a punto de paneles", 
        "distancia tablero a contador", 
        "area disponible", 
        "cubierta", 
        "buitron"
        ]
    othText = ["inserte la distancia entre el sitio donde se instalara el tablero y los paneles, sino lo sabe inserte -1", 
        "inserte la distancia entre el tablero y el contador, sino inserte -1",
        "inserte el area disponible, sino inserte -1",
        "si su cubierta es en teja de barro 1, metalica 2 o 3 si es una placa, en otro caso inserte -1 ", 
        "inserte 1 si existe buitron para paso de tuberia en la instalacion, sino lo sabe inserte -1"
        ]
    typ = [0, 0, 0, 0, 0]
    iinf = [0, 0, 0, 0, 0]
    isup = [1e9, 1e9, 1e9, 1e9, 1e9]
    fold1 = ["siteFeatures", "siteFeatures", "siteFeatures",  "siteFeatures", "siteFeatures"]
    fold2 = ["distTab_Cont", "distPv_Tab", "availableArea", "cubiertaApta", "buitron"]


    print("Inserte la energia necesaria que desea suplir:  \n")
    sel = float(input())    
    validData(sel, 1e9, 0, 0, [], dimensionamiento, "pvModules", "ener_Need", "seleccion de tension invalida")

    print("Ingrese el numero de acuerdo a la unidad de la energia de entrada: \n")
    for i in range(len(energranul)):
        print(str(i) + ". " +energranul[i] + "\n")
    sel = int(input())
    validData(sel, 1e9, 0, 1, energranul, dimensionamiento, "pvModules", "ener_Type", "seleccion de unidad de energia invalida")

    print("Ingrese la latitud en al cual se encuentra ubicado el proyecto:  \n")
    dimensionamiento["siteFeatures"]["latitude"] = float(input())

    print("Ingrese la longitud en al cual se encuentra ubicado el proyecto :  \n")
    dimensionamiento["siteFeatures"]["longitude"] = float(input())

    print("Ingrese la configuracion AC de la edificacion donde se desarrollara el proyecto:  \n")
    print("Las opciones de configuracion AC son las siguientes:  \n")
    for i in range(len(optACconfig)):
        print(str(i) + ". " +optACconfig[i] + "\n")
    sel = int(input())
    validData(sel, 1e9, 0, 1, optACconfig, dimensionamiento, "siteFeatures", "ACConfig", "seleccion de configuracion invalida")

    print("Inserte el nivel de tension l-n o l-l para bifasica:  \n")
    for i in range(len(voltageLevel)):
        print(str(i) + ". " + str(voltageLevel[i]) + "\n")
    sel = int(input())
    validData(sel, 1e9, 0, 1, voltageLevel, dimensionamiento, "siteFeatures", "voltage","seleccion de tension invalida")

    print("Inserte 1 si desea ingresar informacion detallada de la instalacion")    
    flag = int(input())
    if flag == 1:
        for i in range(len(iinf)):
            data = float(solicitarParam(othText[i], 0))
            if data != -1:            
                flag = validData(data, isup[i], iinf[i], typ[i], [], 
                    dimensionamiento, fold1[i], fold2[i], "dato invalido para" + errText[i])
            else: dimensionamiento[fold1[i]][fold2[i]] = None
        



    return "SUCCESS"



def validData(data, isup, iinf, type, opt, storeVariable, fold1, fold2, error):
    if type == 0:
        if data >= iinf and data < isup:
            storeVariable[fold1][fold2] = data
            return "SUCCESS"
        else: return error
    else:
        if data >= iinf and data < len(opt):
            storeVariable[fold1][fold2] = opt[data]
            return "SUCCESS"
        else: return error


def solicitarParam(text, opt, list = []):
    print(text)
    if opt == 1:
        for i in range( len(list)):
            if type(opt) != str: k = str(list[i]) 
            else: k = list[i]
            print(str(i) + ". " + k)
    return input()
    
    
