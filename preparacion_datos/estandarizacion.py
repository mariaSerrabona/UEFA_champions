# En este archivo lo que se pretende es realizar una estandarización de los datos de los que disponemos:

#Por una parte tenemos la información de los partidos, la de los equipos, así como la de los resultados de todos los partidos
#en los últimos 20 años.

#Nuestro objetivo va a ser generar una información completa en la que figuren todos los equipos con la suma
#de los goles que se han marcado siendo local y siendo visitante. De esta manera, lo que vamos a conseguir es
#poder hallar las probabilidades de que se acierte una apuesta, calculando así las cuotas.


#En esta sección se van a estadaridar todos los nombres de todos los partidos. De esta forma, generaremos una clave única (el equipo)
#Con distintos valores (los goles), queremos así eliminar caulquier tipo de impureza en el nombre (tildes, mayúsculas ...).

import pandas as pd
import sys
sys.path.append('../')

info_equipos = pd.read_csv('/Users/mariaperez-serrabona/UEFA_champions/docs/equipo.csv')

#vamos a ver que todos en todos los casos, los equipos se nombren igual
info_equipos['Equipo'].unique()

#tenemos que cargar todos los partidos de los últimos 20 años en un bucle
# creamos entonces una lista con todos los años

años = ["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

#Si nos fijamos en la información dentro de datas, vemos que hay ligeras diferencias en el deletro de un mismo equipo

todos_equipos = info_equipos['Equipo']
#Convertimos a lista para que pueda ser recorrida
todos_equipos = list(todos_equipos)

#Normalizamos los nombres de los equipos
for año in años:
    df_partidos_anual=pd.read_csv(f'/Users/mariaperez-serrabona/UEFA_champions/datas/Champions/resultados_{año}.csv')
    #como ya hemos dicho, la clave es el equipo y el valor serán los goles
    diccionario={}
    for nombre in df_partidos_anual.Local.unique():
        lista=str(nombre).lower().split()
        if 'inter' in lista:
            diccionario[nombre]='Internazionale'
        for equipo in todos_equipos:
            if str(equipo).lower() in lista:
                diccionario[nombre]=str(equipo)
        if 'manchester' in lista:
            if 'united' in lista:
                diccionario[nombre]='Man. United'
            elif 'city' in lista:
                diccionario[nombre]='Man. City'
        elif 'lille' in lista:
            diccionario[nombre]='LOSC'
        elif 'París' in lista:
            diccionario[nombre]='Paris'
        elif 'sporting' in lista:
            if 'portugal' in lista:
                diccionario[nombre]='Sporting CP'
        elif 'donetsk' in lista:
            diccionario[nombre]='Shakhtar Donetsk'
        elif 'real' in lista:
            if 'madrid' in lista:
                diccionario[nombre]='Real Madrid'
        elif 'young' in lista:
            diccionario[nombre]='Young Boys'
    for nombre in diccionario:
        #se guarda el nombre como se infica sin diferencias tanto como si es local como si es visitantye
        df_partidos_anual['Local'] = df_partidos_anual['Local'].replace(nombre,diccionario[nombre])
        df_partidos_anual['Visitante'] = df_partidos_anual['Visitante'].replace(nombre,diccionario[nombre])

    #se vuelve a guardar la información para poder trabajr sobre ella
    #Ya tenemos la información organizara para poder hacer predicciones sobre ella, analizando los goles que se han marcado como visitante y como local
    df_partidos_anual.to_csv(f'/Users/mariaperez-serrabona/UEFA_champions/datas/Champions/DatosBuenos/Informaciónresultados{año}.csv',index=False)

#Normalizamos los nombres de los equipos para que no haya diferncias en el deletreo
def NormalizacionNombres(palabra:str):
    palabra=palabra.lower()
    palabra=palabra.replace("ç","c")
    palabra=palabra.replace("á","a")
    palabra=palabra.replace("é","e")
    palabra=palabra.replace("í","i")
    palabra=palabra.replace("ó","o")
    palabra=palabra.replace("ö","o")
    palabra=palabra.replace("ú","u")
    palabra=palabra.replace("ü","u")
    return palabra