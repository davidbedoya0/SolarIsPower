# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:38:37 2021

@author: crisd
"""



import urllib.request, urllib.parse, urllib.error
import json 
import ssl

class Geolocalizacion:
    
    def __init__ (self, ubicacion):
        
        #Inicializar parametros
        self.__ubicacion= ubicacion
        
        #Ejecutar Acciones
        self.ObtenerGeolocalizacion()
        
        
    #=============Restriccion de atributos a ReadOnly , GETTERS
    @property
    def ubicacion(self):
        return self.__ubicacion
    
    @property
    def data(self):
        return self.__data
    
    @property
    def resultado(self):
        return self.__resultado
    
    @property
    def direccion(self):
        return self.__direccion
    
    @property
    def ciudad(self):
        return self.__ciudad
    
    @property
    def pais(self):
        return self.__pais
    
    @property
    def latitud(self):
        return self.__latitud
    
    @property
    def longitud(self):
        return self.__longitud
        
    #=====Metodos Privados
    def __ObtenerGeolocalizacion (self):
        api_key= 42
        serviceurl= 'http://py4e-data.dr-chuck.net/json?'
        
        #Ignore SSL certificate errors
        ctx=ssl.create_default_context()
        ctx.check_hostname=False
        ctx.verify_mode= ssl.CERT_NONE
        
        address= self.__ubicacion
        
        parms= dict()
        parms['address']= address
        parms['key']=api_key
        url=serviceurl + urllib.parse.urlencode(parms) #
        
        data= urllib.request.urlopen(url,context=ctx).read().decode()
        
        js= json.loads(data)
        
        if not js or 'status' not in js or js['status']!='OK':
            falla='Falla al solicitar datos de geolocalización'
            print(falla)
            self.__data=data
            self.__resultado=falla
            
        
        else:
            self.__data=data
            self.__resultado= js
            
            self.__latitud= js['results'][0]['geometry']['location']['lat']
            self.__longitud=js['results'][0]['geometry']['location']['lng']
            self.__geolocalizacion =str (self.latitud)+","+str(self.longitud)
            self.__ciudad= js['results'][0]['formatted_address'].split(',')[1].strip()
            self.__pais=js['results'][0]['formatted_address'].split(',')[2].strip()
            self.__direccion=js['results'][0]['formatted_address'].split(',')[0].strip()
            
    

if __name__ == '__main__':
    dirTest= input('ingrese ubicacion: ')
    ubicacion = Geolocalizacion(dirTest)
    print(ubicacion.direccion,' se encuentra en las coordenadas ', ubicacion.geolocalizacion)