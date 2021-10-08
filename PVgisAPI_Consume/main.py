import requests
from requests.models import Response

if __name__ == '__main__':
    url = "https://httpbin.org/get"
    args = {"nombre":"eduardo","curso":"python", "nivel":"intermedio"}
    rspns = requests.get(url, params = args)
    print(rspns.url)
    if rspns.status_code==200:
        print("\n \n")
        #print(rspns.content)
        contenido = rspns.content
        jsonData = rspns.json()
        print(jsonData)
        print(jsonData["origin"])
        

