# En este fichero se quiere crear un modelo de machine learning en el que se entrene a la red con los datos que tenemos
# y las probabilidades que se van a calcular. De esta forma, al introducir una nueva apuesta, nuestro modelo será lo
#suficientemnete preciso como para que nos estime una probabilidad de acierto.

# como ya hemos visto en la estandarizacion, vamos a preparar la información de los equipos,
#generandola como una lista
import pandas as pd

info_equipos = pd.read_csv ('docs/equipo.csv')

#Vemos con qué tipo de datos trabajamos
info_equipos = info_equipos['Equipo']

#Convertimos a lista para que pueda ser recorrida
info_equipos=list(info_equipos)

#Establecemos todos los años como una lista para que puedan ser recorridos
años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]