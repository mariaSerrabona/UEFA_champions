# En este fichero se quiere crear un modelo de machine learning en el que se entrene a la red con los datos que tenemos
# y las probabilidades que se van a calcular. De esta forma, al introducir una nueva apuesta, nuestro modelo será lo
#suficientemnete preciso como para que nos estime una probabilidad de acierto.

# como ya hemos visto en la estandarizacion, vamos a preparar la información de los equipos,
#generandola como una lista
import pandas as pd

class modelo():
    def __init__(self, info_equipos, temporadas, Champions, goles_local, goles_visitante):
        self.info_equipos=info_equipos
        self.temporadas=temporadas
        self.Champions=Champions
        self.goles_local=goles_local
        self.goles_visitante=goles_visitante


    def conteo_goles(self):

        self.info_equipos = pd.read_csv ('docs/equipo.csv')

        #Vemos con qué tipo de datos trabajamos
        self.info_equipos = self.info_equipos['Equipo']

        #Convertimos a lista para que pueda ser recorrida
        self.info_equipos=list(self.info_equipos)

        #Establecemos todos los años como una lista para que puedan ser recorridos
        self.temporadas=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
                            ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

        #Ahora, vamos a desarrollar nuestro objetivo, generar una lista completa con todos los equipos
        #y la cantidad de goles que ha marcado, diferenciando las ocaciones en las que ha sido visitante o local

        #diccionario: clave(equipo), valor(goles)
        # muy útil el uso de diccionarios para conservar una clave única (equipo)  y poder acceder a la información de los goles mediante las claves
        self.Champions={}
        #Diccionarios para guardar los goles de cada equipo, diferenciando entre local y visitante
        self.goles_local = {}
        self.goles_visitante = {}
        #Recorremos todos los años
        for temporada in self.temporadas:
            self.Champions[f'{temporada}'] = pd.read_csv('datas/Champions/resultados_'+temporada+'.csv')

        #Importante inicializar los diccionarios de todos los equipos a 0
        for equipo in self.info_equipos:
            self.goles_local[equipo] = 0
            self.goles_visitante[equipo] = 0


        for temporada in self.temporadas:

            for index in range(len(self.Champions[temporada])):
                #hacemos el mismo código para calcular los goles, tanto en local como en visitant

                #Se mete en la temporada de la champions, en la fila del fichero,
                # escogiendo solo la información de la columna Visitante. Si este equipo está en nuestra información
                # de equipos:
                if self.Champions[temporada].iloc[index]['Visitante'] in self.info_equipos:
                    #Entonces añadimos los goles marcados en el partido que se está analizando
                    # a los ya contabilizados del mismo equipo como visitante.
                    self.goles_visitante[self.Champions[temporada].iloc[index]['Visitante']] += int(self.Champions[temporada].iloc[index]['GolesVisitante'])

                #Realizamos lo mismo, pero esta vez con el equipo como Visitante
                if str(self.Champions[temporada].iloc[index]['Local']) in self.info_equipos:
                    self.goles_local[self.Champions[temporada].iloc[index]['Local']] += int(self.Champions[temporada].iloc[index]['GolesLocal'])
            print('Temporada '+ temporada+' realizada')


    def info_equiposGoles(self):
        #Ahora queremos generar un csv en el que figure el equipo y los goles que ha marcado como local.

        #Generamos directamnete un df con la información que nos interesa.
        # Por una parte, tenemos key con el listado de los equipos
        # Luego tenemos que hallar los goles que ha marcado cada equipo como visitante
        # Para realizarlo, recorremos mediante un bucle for los goles visitantes que hemos hallado antes
        #Conseguimos así tener el equipo con sus goles como vistante
        df_goles_visitante = pd.DataFrame([[key, self.goles_visitante[key]] for key in self.goles_visitante.keys()],
                                            columns = ['Equipo Visitante', 'Goles como Visitante'])


        # Hacemos lo mismo pero ahora evaluando cada equipo cuando juega como local
        df_goles_local = pd.DataFrame([[key, self.goles_local[key]] for key in self.goles_local.keys()],
                                            columns = ['Equipo Local', 'Goles como Local'])

        df_goles_local.to_csv('preparacion_datos/goles_local.csv', index=False)
        df_goles_visitante.to_csv('preparacion_datos/goles_vistante.csv', index=False)
        df_conjunto = pd.concat([df_goles_local, df_goles_visitante], axis=1)
        df_conjunto.to_csv('preparacion_datos/goles_cada_equipo.csv', index=False)


def main():
    info_equipos = pd.read_csv ('docs/equipo.csv')

    #Vemos con qué tipo de datos trabajamos
    info_equipos = info_equipos['Equipo']

    #Convertimos a lista para que pueda ser recorrida
    info_equipos=list(info_equipos)

    #Establecemos todos los años como una lista para que puedan ser recorridos
    temporadas=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
                        ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

    #Ahora, vamos a desarrollar nuestro objetivo, generar una lista completa con todos los equipos
    #y la cantidad de goles que ha marcado, diferenciando las ocaciones en las que ha sido visitante o local

    #diccionario: clave(equipo), valor(goles)
    Champions={}
    #Diccionarios para guardar los goles de cada equipo, diferenciando entre local y visitante
    goles_local = {}
    goles_visitante = {}

    creacion_modelo=modelo(info_equipos, temporadas, Champions, goles_local, goles_visitante)
    creacion_modelo.conteo_goles()
    creacion_modelo.info_equiposGoles()


if __name__ == '__main__':
    main()