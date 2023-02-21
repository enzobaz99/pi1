#importamos las librerias
import pandas as pd                                     #Manejo de Dataframes
from fastapi import FastAPI                             #Implementación de la API
from fastapi.responses import PlainTextResponse         #Output de la información en formato texto
from pandasql import sqldf                              #Consultas sobre dataframes mediante lenguaje SQL

#importamos el dataframe anteriormente generado y en base a eso creamos las funciones
df_plataform = pd.read_csv ("todaslasplataformas_database.csv")

app = FastAPI()

pysqldf = lambda q: sqldf(q, globals())

#tarea Nº1 Película que más duró según año, plataforma y tipo de duración

@app.get(
    "/get_max_duration/{plataforma}/{tipo_duracion}/{anio}",
    response_class=PlainTextResponse,
    tags=["Mayor duración"],
)
def get_max_duration(plataforma: str, tipo_duracion: str, anio: str):
    """
    Esta función calcula cual es la película con mayor duración en minutos o temporadas para ello 
    se requiere ingresar el “año” en el formato AAAA (por ejemplo 2010), 
    el tipo de duración que desean saber (min/season) 
    y la plataforma que deseen (amazon, disney, hulu, netflix), todo esto debe ir en minuscula
    """
    if plataforma == "amazon":
        platafor = "a%"
    elif plataforma == "netflix":
        platafor = "n%"
    elif plataforma == "hulu":
        platafor = "h%"
    elif plataforma == "disney":
        platafor = "d%"
    else:
        return "No ha seleccionado la plataforma"

    query = (
        """SELECT title
        FROM df_plataform
        WHERE id LIKE '"""
        + platafor
        + """'
        AND release_year = '"""
        + anio
        + """'
        AND duration_type = '"""
        + tipo_duracion
        + """'
        AND duration_int = (SELECT MAX(duration_int)
        FROM df_plataform
        WHERE id LIKE '"""
        + platafor
        + """'
        AND release_year = '"""
        + anio
        + """'
        AND duration_type = '"""
        + tipo_duracion
        + """')
        """
    )

    mayorduracion = pysqldf(query)
    return mayorduracion.to_string(index=False, header=False)

#tarea Nº2 Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año

@app.get(
    "/get_score_count/{plataforma}/{score}/{anio}",
    response_class=PlainTextResponse,
    tags=["Cantidad puntaje mínimo"],
)
def get_score_count(plataforma: str, score: str, anio: str):
    """
    Cuenta cantidad de **películas** que superan el score indicado para cierto año y plataforma.
    Requiere el ingreso del **año** en formato AAAA, el **score** como un entero del 0 a 99
    y la **plataforma** (netflix, disney, hulu, amazon)
    """
    if plataforma == "amazon":
        platafor = "a%"
    elif plataforma == "netflix":
        platafor = "n%"
    elif plataforma == "hulu":
        platafor = "h%"
    elif plataforma == "disney":
        platafor = "d%"
    else:
        return "No ha seleccionado la plataforma"

    query = (
        """SELECT COUNT(title)
        FROM df_plataform
        WHERE score > 20 """
        + score
        + """
        AND release_year = """
        + anio
        + """
        AND id LIKE '"""
        + platafor
        + """'
        AND type = "movie" """
    )
    cantidad = pysqldf(query)
    return cantidad.to_string(index=False, header=False)
#tarea Nº3 Cantidad de películas por plataforma

#tarea Nº4 Actor que más se repite según plataforma y año

@app.get(
    "/get_actor/{plataforma}/{keyword}",
    response_class=PlainTextResponse,
    tags=["Contar nombre"],
)
def get_actor(keyword: str, plataforma: str):
    """
    Esta cuenta la cantidad de peliculas que protagoniza un actor.
    requiere el ingreso de una keyword que sera el nombre del actor y la plataforma ingresado en minusculas.

    """
    if plataforma == "amazon":
        plat = "a%"
    elif plataforma == "netflix":
        plat = "n%"
    elif plataforma == "hulu":
        plat = "h%"
    elif plataforma == "disney":
        plat = "d%"
    else:
        return "No ha seleccionado la plataforma entre las opciones posibles"

    query = (
        """SELECT COUNT(cast)
        FROM df_plataform
        WHERE title LIKE '%"""
        + keyword
        + """%'
        AND id LIKE '"""
        + plat
        + """' """
    )
    veces = pysqldf(query)
    return veces.to_string(index=False, header=False)