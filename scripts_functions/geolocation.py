# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:38:37 2021

@author: crisd
"""



import urllib.request, urllib.parse, urllib.error
import json 
import ssl

class geolocalizacion:
    
    def __init__ (self, ubicacion):
        self.ubicacion= ubicacion
        self.data=None
        self.resultadoConsulta=None
        self.direccion= None
        self.ciudad=None
        self.pais= None
        self.latitud=None
        self.longitud=None
        self.geolocalizacion=None
        
        self.obtenerGeolocalizacion()
        
    def obtenerGeolocalizacion (self):
        api_key= 42
        serviceurl= 'http://py4e-data.dr-chuck.net/json?'
        
        #Ignore SSL certificate errors
        ctx=ssl.create_default_context()
        ctx.check_hostname=False
        ctx.verify_mode= ssl.CERT_NONE
        
        address= self.ubicacion
        
        parms= dict()
        parms['address']= address
        parms['key']=api_key
        url=serviceurl + urllib.parse.urlencode(parms) #Retriving this url 
        
        data= urllib.request.urlopen(url,context=ctx).read().decode()
        
        js= json.loads(data)
        
        if not js or 'status' not in js or js['status']!='OK':
            falla='Falla al solicitar datos de geolocalización'
            print(falla)
            self.data=data
            self.resultadoConsulta=falla
            
        
        else:
            self.data=data
            self.resultadoConsulta= js
            
            self.latitud= js['results'][0]['geometry']['location']['lat']
            self.longitud=js['results'][0]['geometry']['location']['lng']
            self.geolocalizacion =str (self.latitud)+","+str(self.longitud)
            self.ciudad= js['results'][0]['formatted_address'].split(',')[1].strip()
            self.pais=js['results'][0]['formatted_address'].split(',')[2].strip()
            self.direccion=js['results'][0]['formatted_address'].split(',')[0].strip()
            
    

if __name__ == '__main__':
    dirTest= input('ingrese ubicacion: ')
    ubicacion = geolocalizacion(dirTest)
    print(ubicacion.direccion,' se encuentra en las coordenadas ', ubicacion.geolocalizacion)