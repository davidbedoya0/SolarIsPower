"""
! ==========================================================
--- TEST SUCCESS
+++ Name: annualAverageHSP
! description: extract data and compute max, min, monthly and 
! historical HSP from a location.
? inputs: 
    data: a dictionary that contains solar radiation record

? output: 
    avgAnual: anual average HSP from start year until last data bases year
    avgHist: historical HSP from all pvgis database
    maxHistMonth: max HSP for each month
    minHistMOnth: min HSP for each month
    flag: success or error flag

! ==========================================================
"""

def anualAverageHSP(Data):

    i = 0
    k = 1
    acumHS = 0
    size = len(Data)
    curr_Year = Data[0]["year"]
    avgAnualHSP = []
    sumMonth = []
    avgHistMonth = []
    MaxHistMonth = []
    MinHistMonth = []

    for i in range(12):
        avgHistMonth.append(0)
        MaxHistMonth.append(0)
        MinHistMonth.append(1e9)
        sumMonth.append(0)

    i = 0
    MinHistMonth[Data[i]["month"] - 1] = Data[i]["H(h)_m"]

    while i < size:
        
        sumMonth[Data[i]["month"] - 1] += 1
        avgHistMonth[Data[i]["month"] - 1] += Data[i]["H(h)_m"]
        if MaxHistMonth[Data[i]["month"] - 1] < Data[i]["H(h)_m"]:
            MaxHistMonth[Data[i]["month"] - 1] = Data[i]["H(h)_m"]
        if MinHistMonth[Data[i]["month"] - 1] > Data[i]["H(h)_m"]:
            MinHistMonth[Data[i]["month"] - 1] = Data[i]["H(h)_m"]
        
        if curr_Year == Data[i]["year"]:
            acumHS += Data[i]["H(h)_m"]
            k += 1

        else:
            avgAnualHSP.append([ acumHS / k, curr_Year])
            curr_Year = Data[i]["year"]
            k = 1
            acumHS = 0
        i += 1

    avgAnualHSP.append([ acumHS / k, curr_Year])
    acumHS = 0

    for i in range(12):
        avgHistMonth[i] = avgHistMonth[i]/(sumMonth[i] + 1)

    return[avgAnualHSP, avgHistMonth, 
        MaxHistMonth, MinHistMonth, "SUCCESS"]

"""
! ==========================================================
--- TEST SUCCESS
+++ Name: dailyRad
! description: extract data from pvgis daily struct
? inputs: 
    data: a dictionary that contains solar daily radiation record

? output: 
    arr: a list that contains daily radiation info

! ==========================================================
"""

def dailyRad(Data):
    arr = []
    for i in range (24):
        arr.append( Data[i]["G(i)"])

    return arr




"""
! ==========================================================
--- TEST SUCCESS
+++ Name: validation
! description: a function that validate by value and data type 
! the pvsizing input data
? inputs: 
    data: data to validate
    levar: len of data input
    datcomp_Sup: lowest limit to compare with input data
    datcomp_Inf: highest limit to compare with input data
    error: string to return in case of a validation error
    typedata: indicates type of variable (0 -> int, 1 -> float/int, 2 -> list(float/int))

? output: 
    success or error flag
! ==========================================================
"""
def validation(data, lenvar, datcomp_Sup, datcomp_Inf, error, typeData):
    
    # comprobacion de limites superior e inferior de la entrada
    if lenvar > 1:
        for i in range(lenvar):
            if data[i] >= datcomp_Sup[i] or data[i] <= datcomp_Inf[i]:                
                return error
    else:
        if data >= datcomp_Sup or data <= datcomp_Inf:                
            return error

    # verificacion del tipo de dato
    if typeData == 0:
        if type(data) != int:
            return error
    elif typeData == 1:
        if type(data) != float:
            if type(data) != int:
                return error
    elif typeData == 2:
        for i in range(lenvar):
            if type(data[i]) != float:
                if type(data[i]) != int:
                    return error
    return "SUCCESS"

        
"""
! ==========================================================
--- TEST SUCCESS
+++ Name: req_pvgis
! description: a function that get data from pvgis
? inputs: 
    lat: PV project site latitude
    lon: PV project site longitude
    case: PV tool to get data
    month: *optional parameter when case 2 is selected

? output: 
    success or error flag
! ==========================================================
"""

def req_pvgis(lat, lon, case, month = 15):

    if case == 2 and (month < 1 or month > 12 or type(month)!=int):
        return ["ERROR: invalid month to send request to pvgis", 0]
    
    if lat < -37 or lat > 71:
        return ["ERROR: ivalid latitud data", 0]
    
    if lon < -162 or lon > 115:
        return ["ERROR: invalid longitud data", 0]

    if case == 0: # azimuth
        args = {"lat" : lat, "lon" : lon, "peakpower" : 1, "loss" : 14,
            "optimalinclination" : 1, "outputformat" : "json"}
    elif case == 1: # monthly rad
        args = {"lat" : lat, "lon" : lon, "horirrad" : 1, "outputformat" : "json"}
    elif case == 2: # daily rad
        args = {"lat" : lat, "lon" : lon, "month" : month, "outputformat" : "json", 
            "global":1}

    tools = [
        "PVcalc", 
        "MRcalc", 
        "DRcalc"]

    url = "https://re.jrc.ec.europa.eu/api/"
    url = url + tools[case]

    rspns = requests.get(url, args)
    if rspns.status_code == 200:
        Data = rspns.json()
        if case == 0:
            return [Data["inputs"]["mounting_system"]["fixed"]["slope"], "SUCCESS"]
        if case == 1:
            return [Data["outputs"]["monthly"], "SUCCESS"]
        if case == 2:
            return [Data["outputs"]["daily_profile"], "SUCCESS"]
    else: 
        return ["ERROR: Data is correct but " + tools[case] +" API don't work", 0]