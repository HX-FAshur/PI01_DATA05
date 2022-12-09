# Importamos librerias

import pandas as pd
import numpy as np
from fastapi import FastAPI
import Levenshtein

# Cargamos los datos extraidos con EDA.ipynb

catalog =  pd.read_csv('./Exported Data/catalog.csv') # Este es el catalogo con toda la info de los archivos de streaming
actDF = pd.read_csv('./Exported Data/actors.csv') # Esta es la lista de actores
actJunc_DF = pd.read_csv('./Exported Data/actorsjunc.csv') # Esta es la tabla junction en la que esta relacionados que show tuvo que actores
catDF = pd.read_csv('./Exported Data/categories.csv') # Esta es la tabla de categorias
catJunc_DF = pd.read_csv('./Exported Data/categoriesjunc.csv') # Esta es la tabla junction en la que se relaciona las categorias con los shows


app = FastAPI() # Iniciar La API

@app.get("/get_max_duration/{anio}&{plataforma}") # 
async def get_max_duration(anio:int, plataforma:str, tipo:str = 'min'):
    # Máxima duración según tipo de film (película/serie), por plataforma y por año: El request debe ser: get_max_duration(año, plataforma, [min o season])

    platform = str.capitalize(plataforma) # Cambiamos a mayuscula la primera letra de cada palabra. Esto es porque la lista de categorias esta con mayusculas las primeras

    # Filtramos por año, plataforma y tipo

    if tipo == 'min':
        
        subset = catalog[(catalog['release_year'] == anio) & (catalog['platform'] == platform) & (catalog['dtype'] == tipo)] 
    else:
        subset = catalog[(catalog['release_year'] == anio) & (catalog['platform'] == platform) & (catalog['dtype'] != 'min')]

     # Retornamos el primero en la lista de maximos que fue ordenada. 

    return subset[subset['duration'] == subset.duration.max()].title.values[0]


@app.get("/get_count_plataform/{plataforma}")
async def get_count_plataform(plataforma:str):
    # Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)

    plataforma = str.capitalize(plataforma) # Cambiamos a mayuscula la primera letra de cada palabra. Esto es porque la fila de plataformas esta con mayusculas las primeras

    # Buscamos todas las peliculas por plataforma y tomamos la longitud de la lista
    movies = len(catalog[(catalog['platform'] == str.capitalize(plataforma)) & (catalog['dtype'] == 'min')]) 
    # Buscamos todas las series por plataforma y tomamos la longitud de la lista
    series = len(catalog[(catalog['platform'] == str.capitalize(plataforma)) & (catalog['dtype'] != 'min')])

    # Retornamos las longitudes con un poco de arreglos
    return str(plataforma + ': Movies ' + str(movies) + ", Tv Shows " + str(series))


@app.get("/get_listedin/{genero}")
async def get_listedin(genero:str):
    # Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
    
    genero = str.capitalize(genero) # Cambiamos a mayuscula la primera letra de cada palabra. Esto es porque la lista de categorias esta con mayusculas las primeras
    
    if((catDF['categories'].eq(genero)).any()): # Si la categoria requerida esta en la lista de categorias

        catind = catDF[catDF['categories'] == genero].index # Encontramos el indice de la categoria, que se uso como primary key
        shows = catJunc_DF[catJunc_DF['idCategory'] == catind.values[0]].idShow # Usando la tabla junction de shows y peliculas con categorias, buscamos todos los shows y peliculas con ese genero
        subset = pd.DataFrame(catalog.loc[shows.values, 'platform'], columns = ['platform']) # Convertimos la vista encontrada de Serie a Dataframe para accesar mas simple la información

        netflix = len(subset[subset['platform'] == 'Netflix']) # Extraemos la longitud de la lista con filtro Netflix
        hulu = len(subset[subset['platform'] == 'Hulu'])# Extraemos la longitud de la lista con filtro Hulu
        amazon = len(subset[subset['platform'] == 'Amazon']) # Extraemos la longitud de la lista con filtro Amazon     
        disney = len(subset[subset['platform'] == 'Disney']) # Extraemos la longitud de la lista con filtro Disney
        
        dic = {netflix:'Netflix', hulu:'Hulu', amazon:'Amazon Prime', disney:'Disney Plus'} # Creo un diccionario, con los valores como claves
        ans = 'platform: ' + str(dic.get(max(dic))) + ', Cantidad: ' + str(max(dic)) # Creamos la respuesta encontrando el maximo en los diccionarios
    else:
        ans = "None found for Category: " + genero # Si no se encontró en la lista, se le informa al usuario
 
    return ans # retornamos la respuesta adecuada

@app.get("/get_actor/{plataforma}&{anio}")
async def get_actor(plataforma:str, anio:int):
    # Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

    plataforma = str.capitalize(plataforma) # Cambiamos a mayuscula la primera letra de cada palabra. Esto es porque la fila de plataformas esta con mayusculas las primeras

    subset = catalog[(catalog['platform'] == plataforma) & (catalog['release_year'] == anio)].index # Primero filtramos por plataforma y por anio, tomamos los indices que actuan como primary key
    
    mask = [True if id in subset else False for id in actJunc_DF['idShow']] # Creamos una mascara que indica si el id de las peliculas y series estan en el filtro creado antes. 
    
    actorIds = actJunc_DF[mask].idActor # Aplicamos el filtro a la tabla junction para tener solo los actores que aparecian en los shows filtrados y tomamos el id del actor que actua como primary key en la tabla actor (index tambien)
   
    actorcount = actorIds.value_counts()  # Contamos cuantas veces se repite el mismo id de actor en la lista filtrada. Esta funcion tambien ordena de menor a mayor
    
    count = actorcount.tolist()[0] # Transformamos en lista la cuenta y tomamos solo la primera posicion, es decir el de mas apariciones

    id = actorcount.index[0] # tomamos el id solamente del actor con mas apariciones

    # Retornamos la plataforma, la cantidad de apariciones y el nombre del actor, filtrando el nombre por el id en la lista de actores.

    return 'Platform: ' + plataforma + ", cantidad: " + str(count) + ", Actor: " + actDF.loc[id,'actors']


