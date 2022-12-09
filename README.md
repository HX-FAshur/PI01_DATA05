# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Data Engineering`**</h1>

<div style="text-align: right"> Helio Angel Forero Mora</div>
<hr>

## **Descripción del Proyecto**

La consigna de este proyecto puede ser revisada en el archivo "Proyect Proposal.md". En resumen se solicita disponibilizar, atravez de una API, una base de datos de catalogos de streaming de las plataformas de Netflix, Amazon Prime, Disney Plus y Hulu. 

Los archivos que contienen la información inicial se pueden encontrar en la carpeta Datasets. 

## **Desarrollo del Proyecto**

Los datos se ingestaron y se realizaron los siguientes cambios:

+ Se eliminó la fila de show_id: Esta fila era solo un índice. 

+ Se agregó la columna 'platform' con el nombre de la plataforma al que pertenece la serie o pelicula

+ Se se consolidó en un solo dataframe todos los catalogos. 

+ Se corrigio las filas que tenian la informacion de duración en la fila rating

+ Se completo informacion faltante en las series o peliculas que estaban repetidas en el catalogo completo, teniendo
en cuenta el titulo o la descripción para considerarlas repetidas y considerando si era serie o pelicula para no ingresar informacion erronea

+ Se creo una lista de actores a partir de la columna cast y una lista (junction table) en la que se especifica en 
que actores estuvieron en que serie o pelicula

+ La lista de actores se genero usando la libreria rapidfuzz para comparar la distancia entre palabras en los nombres de los actores para reducir la cantidad de "seudonimos" en la lista de actores. 

+ Se creo una lista de categorias a partir de la columna 'listed_in' y una lista (junction table) en la que se relaciona que categoria(s) tenia que serie o pelicula. 

+ Se exportó el dataframe de los catalogos, la lista de actores y su respectiva lista de union, la lista de categorias y su respectiva lista de union y se colocaron en la carpeta "Exported Data"

Despues de esto, los datos se agregan a la API usando las librerias FastApi y Uvicorn, leyendo los datos de la carpeta "Exported Data" y generando las consultas requeridas. 

Adicionalmente, el proyecto se hizo disponible de forma publica en github (https://github.com/HelioForero/PI01_DATA05/tree/HelioForero/PI01_DATA05) y en una instancia que corre en la nube de Mogenius (https://catalogplatfor-prod-movies-and-shows-catalog-pzd8ie.mo2.mogenius.io/get_actor/netflix&2018)


## **Uso**

La Api cuenta con 4 funciones:

+ Máxima duración según tipo de film (película/serie), por plataforma y por año
    "/get_max_duration/{anio}&{plataforma}?tipo=season" Ejemplo: https://catalogplatfor-prod-movies-and-shows-catalog-pzd8ie.mo2.mogenius.io/get_max_duration/2018&hulu?tipo=min

+ Cantidad de películas y series (separado) por plataforma 
    "/get_count_plataform/{plataforma}" Ejemplo: https://catalogplatfor-prod-movies-and-shows-catalog-pzd8ie.mo2.mogenius.io/get_count_plataform/netflix

+ Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo
    "/get_listedin/{genero}" Ejemplo: https://catalogplatfor-prod-movies-and-shows-catalog-pzd8ie.mo2.mogenius.io/get_listedin/comedy

+ Actor que más se repite según plataforma y año
    "/get_actor/{plataforma}&{anio}" Ejemplo: https://catalogplatfor-prod-movies-and-shows-catalog-pzd8ie.mo2.mogenius.io/get_actor/netflix&2018

    



