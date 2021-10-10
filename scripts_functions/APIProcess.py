


def assessPVGisData(Data):
    size = len(Data)



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


def dailyRad(Data):
    arr = []
    for i in range (24):
        arr.append( Data[i]["G(i)"])

    return arr