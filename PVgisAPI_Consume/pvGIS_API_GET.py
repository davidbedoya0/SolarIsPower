import requests
from requests.models import Response
from scripts_functions.APIProcess import *
import time

def pvgisGetData(dimensionamiento):
    
    lat = dimensionamiento["siteFeatures"]["latitude"]
    lon = dimensionamiento["siteFeatures"]["longitude"]
    
    # Request optimum slope angle from 
    [dimensionamiento["siteFeatures"]["slopeAngleOp"], flag] = req_pvgis( lat, lon, 0)
    if flag!= "SUCCESS":
        return flag
    # Request monthly data from all available months from pvgis
    [Data, flag]= req_pvgis(lat, lon, 1)
    if flag!= "SUCCESS":
        return flag
    else:
         [avg, avgHist, maxHist, minHist, flag] = anualAverageHSP(Data)
         dimensionamiento["siteFeatures"]["avgYearHSP"] = avg
         dimensionamiento["siteFeatures"]["avgHistHSP"] = avgHist
         dimensionamiento["siteFeatures"]["maxHSP"] = maxHist
         dimensionamiento["siteFeatures"]["minHSP"] = minHist

    for i in range(12):
        # Request daily data from every month from pvgis
        [Data, flag] = req_pvgis(lat, lon, 2, i + 1)
        if flag!= "SUCCESS":
            return flag
        else:
            dimensionamiento["siteFeatures"]["dayDat"].append(dailyRad(Data))
    
    aux = 0

    for i in range(len(avg)):
        aux += avg[i][0]
    dimensionamiento["siteFeatures"]["avgHSP"] = aux / len(avg)
    return "SUCCESS"
    

"""
Name: req_pvgis
inputs: 
    lat: PV project site latitude
    lon: PV project site longitude
    case: PV tool to get data
    month: *optional parameter when case 2 is selected

output: JSON data of PVGIS API request
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


