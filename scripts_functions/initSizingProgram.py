

def initProgram(dimensionamiento):

    optACconfig = ["3P+N", "3P", "2P", "1P" ]
    voltageLevel = [110, 120, 127, 208, 220, 230]
    energranul = ["kwh/dia", "kwh/mes", "kwh/año"]

    print("Inserte la energia necesaria que desea suplir:  \n")
    dimensionamiento["pvModules"]["ener_need"] = float(input())
    if dimensionamiento["pvModules"]["ener_need"] < 0:
        print("valor de energia invalido")
        return "ERROR"
    print("Ingrese el numero de acuerdo a la unidad de la energia de entrada: \n")
    for i in range(len(energranul)):
        print(str(i) + ". " +energranul[i] + "\n")
    sel = int(input())
    if sel >= 0 and sel < len(energranul):
        dimensionamiento["siteFeatures"]["enerUnit"] = energranul[sel]
    else:
        print("seleccion de unidad de energia invalida")
        return "ERROR"

    print("Ingrese la latitud en al cual se encuentra ubicado el proyecto:  \n")
    dimensionamiento["siteFeatures"]["latitude"] = float(input())

    print("Ingrese la longitud en al cual se encuentra ubicado el proyecto :  \n")
    dimensionamiento["siteFeatures"]["longitude"] = float(input())

    print("Ingrese la configuracion AC de la edificacion donde se desarrollara el proyecto:  \n")
    print("Las opciones de configuracion AC son las siguientes:  \n")
    for i in range(len(optACconfig)):
        print(str(i) + ". " +optACconfig[i] + "\n")
    sel = int(input())
    if sel >= 0 and sel < len(optACconfig):
        dimensionamiento["siteFeatures"]["ACConfig"] = optACconfig[sel]
    else:
        print("seleccion de configuracion invalida")
        return "ERROR"

    print("Inserte el nivel de tension l-n o l-l para bifasica:  \n")
    for i in range(len(voltageLevel)):
        print(str(i) + ". " + str(voltageLevel[i]) + "\n")
    sel = int(input())
    if sel >= 0 and sel < len(voltageLevel):
        dimensionamiento["siteFeatures"]["voltage"] = voltageLevel[sel]
    else:
        print("seleccion de tension invalida")
        return "ERROR"

    return ["SUCCESS", dimensionamiento]

