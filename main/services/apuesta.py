from main.map import ApuestaSchema
from main.repositories.repositorioapuesta import ApuestaRepositorio
from main.repositories.repositoriocuota import CuotaRepositorio
from abc import ABC
from preparacion_datos.modelo_machine_learning import modelo
import pandas as pd

apuesta_schema = ApuestaSchema()
apuesta_repositorio = ApuestaRepositorio()
cuota_repositorio = CuotaRepositorio()

class ApuestaService:
    #no tenemos constructor de la clase, lo creamos:
    #partimos de la información que se ha sacado en el modelo
    def __init__(self, goles_local, goles_visitante, goles_cada_equipo):
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.goles_cada_equipo = goles_cada_equipo

    def agregar_apuesta(self, apuesta, local, visitante):
        cuota = cuota_repositorio.find_by_partido(apuesta)
        probabilidad = self.set_cuota(cuota, local, visitante)
        apuesta.ganancia = round(apuesta.monto * probabilidad, 2)
        return apuesta_repositorio.create(apuesta)

    def set_cuota(self, cuota, local, visitante):
        if local:
            cuota_local = CuotaLocal()
            probabilidad = cuota_local.calcular_cuota(cuota)
            return probabilidad
        if visitante:
            cuota_visitante = CuotaVisitante()
            probabilidad = cuota_visitante.calcular_cuota(cuota)
            return probabilidad
        cuota_empate = CuotaEmpate()
        probabilidad = cuota_empate.calcular_cuota(cuota)
        return probabilidad

    def obtener_apuesta_por_id(self, id):
        return apuesta_repositorio.find_one(id)

    def obtener_apuestas_ganadas(self):
        return apuesta_repositorio.find_wins()

    def obtener_apuestas(self):
        return apuesta_repositorio.find_all()

class CuotaStrategy(ApuestaService):
    #método para generar una cuota, teniendo en cuenta el equipo que juega como local y el que juega como visitante
    def calcular_cuota(self, cuota, eq_local, eq_visitante ):
        """Calcular probabilidad"""
        #Primer habrá que ver si el equipo está considerado en el modelo
        if eq_local in self.goles_local.index and eq_visitante in self.goles_local.index:
            #at para saber el número exacto de goles que tiene el equipo local que se pasa por parámetro
            cuota_visitante =  self.goles_local.at[eq_visitante, 'Goles como Local'] * self.goles_local.at[eq_local, 'Goles como Visitante']
            cuota_local =  self.goles_local.at[eq_local, 'Goles como Local'] * self.goles_local.at[eq_visitante, 'Goles como Visitante']

            #iniciamos las variables de las probabilidades
            prob_empate=0
            prob_local_gane=0
            prob_visitante_gane=0

            #goles del equipo local
            for i in range(0, 10):
                #Numero de goles del equipo visitante
                for j in range(0, 10):
                    '''
                    Ahora lo que queremos hallar es la probabilidad de que el equipo local meta i goles y que el visitante marque j
                    Para ello, vamos a emplear una distribución de Poisson (halla la probabilidad de que ocurra un evento en un cierto tiempo)
                    mu serán las cuotas correspondientes

                    Por qué usamos Poisson?

                    mide la probabilidad de que un evento ocurra bajo un cierto parámetro (tiempo)
                    los posibles sucesos (que un equipo gane y el otro pierda) son aleatorios y ambos elementos tienen
                    las mismas probabilidades de ganar que de perder
                    mide la probabilidad de variables discretas (por lo tanto, no podemos emplear la normal)
                    '''
                    #se van calculando entonces la probabilidad sucesiva de que queden (1-1), (1-2)...(1-10), (2-1)...(2-10)
                    #de manera sucesiva (se entiende que no se marcarán nunca más de 10 goles)
                    prob_distr_poisson = poisson.pmf(i, cuota_local) * poisson.pmf(j, cuota_visitante)
                    #Si dos equipos tienen la misma probabilidad
                    #Estamos valorando un empate
                    if i == j:
                        prob_empate += prob_distr_poisson

                    #Para i mayor que j, valoramos que el local sea el ganador:
                    elif i > j:
                        prob_local_gane += prob_distr_poisson
                    #En cualquier otro caso, gana el visitante
                    else:
                        prob_visitante_gane += prob_distr_poisson


            #Ahora tenemos que hallar el total de puntos ganado tanto por viistante como por local
            # Si ganas, 3 puntos y si empatas, 1 punto
            puntos_local_ganar=3*prob_local_gane
            puntos_local_empate=prob_empate
            puntos_ganados_local = puntos_local_ganar + puntos_local_empate

            puntos_visitante_ganar= 3*prob_visitante_gane
            puntos_visitante_empate=prob_empate
            puntos_ganados_visitante = puntos_visitante_ganar+ puntos_visitante_empate

            #calculamos la probabilidad de que gane cada equipo (ganeA/ganeA+ganeB)
            prob_local_gane = puntos_ganados_local/(puntos_ganados_local + puntos_ganados_visitante)
            prob_visitante_gane = puntos_ganados_visitante/(puntos_ganados_local + puntos_ganados_visitante)

            #Para poder hallar la probabilidad de empate pensamos,
            #si al suceso seguro le quitamos que ganeA y que ganeB, solo queda que los dos ganen, es decir, un empate
            probabilidad_empate = 1 - prob_local_gane - prob_visitante_gane
            return (puntos_ganados_local, puntos_ganados_visitante)

        #en cualquier otro caso, son 0 puntos para ambos equipos
        else:
            return (0, 0)

class CuotaLocal(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_local
        return probabilidad

class CuotaVisitante(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_visitante
        return probabilidad

class CuotaEmpate(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_empate
        return probabilidad