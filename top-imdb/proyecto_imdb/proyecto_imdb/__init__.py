
import os
import re
import requests
from bs4 import BeautifulSoup
import datetime
from collections import Counter
import stat

# Imprime en orde alphanumerico los datos de una carpeta dada.
def elementos(ruta, n=0):
    print(' ' * n + os.path.basename(ruta))

    lista = os.listdir(ruta)
    lista.sort()
    if len(lista)> 500:
      print(' '*(n+2) + 'un monton de archivos')
    else:
      for x in lista:
        ruta_1 = os.path.join(ruta, x)
        if os.path.isdir(ruta_1):
            elementos(ruta_1, n + 2)
        else:
            print(' ' * (n + 2) + os.path.basename(ruta_1))


#Regresa un diccionario con las urls de las peliculas como clave y los valores osn una lista de sus puntajes.
def diccionario_peliculas(lugar):
    peliculas = {}
    directorio = os.getcwd() + '/data/aclImdb/train/' 
    peliculas_url= directorio + 'urls_' + lugar + '.txt'
    for archivo in os.listdir(directorio + lugar):
        match = re.match(r'(\d+)_(\d+)\.txt', archivo)
        n = int(match.group(1))
        puntaje = int(match.group(2))
        with open(peliculas_url, 'r') as archivo:
            lineas = archivo.readlines()
            url = lineas[n - 1].strip().replace('/usercomments','')
            if not url in peliculas.keys():
                peliculas[url] = [puntaje]
            else:
                peliculas[url].append(puntaje)
    return promedio(peliculas)

#Calcula el promedio de las listas.
def promedio(diccionario):
    for pelicula, puntaje in diccionario.items():
        promedio = sum(puntaje) / len(puntaje)  
        diccionario[pelicula] = promedio 
    return diccionario

#Ordena el diccionario de mayor a menor
def ordenar(diccionario):
    return sorted(diccionario.items(), key=lambda item: item[1], reverse=True)

#Regresa una lista con el nombre de las peliculas.
def peliculas():
    peliculas_positivas = dict(ordenar(diccionario_peliculas('pos'))[:10])
    peliculas_negativas = dict(ordenar(diccionario_peliculas('neg'))[-10:])
    return [datos(peliculas_positivas), datos(peliculas_negativas)]

#Busca el nombre de las peliculas usando las urls.
def datos(diccionario):
    peliculas = []
    headers = {'User-Agent': 'Chrome/58.0.3029.110 Safari/537.3 Brave/94.0.4606.61'}
    for url in diccionario.keys():
        respuesta = requests.get(url, headers=headers)
        if respuesta.status_code == 200:
            contenido_html = respuesta.text
            soup = BeautifulSoup(contenido_html, 'html.parser')
            peliculas.append(soup.title.text)
    return peliculas


#Busca la ruta del archivo dado.
def buscar(nombre, ruta = os.getcwd() + '/data'):
    for x in os.listdir(ruta):
        if nombre == x.split('.')[0]:
            return obtener(os.path.join(ruta,x))

    for x in os.listdir(ruta):
        subdir = os.path.join(ruta, x)
        if os.path.isdir(subdir):
            resultado = buscar(nombre, subdir)
            if resultado:
              return resultado


# Obtiene la informacion deseada por la tarea.
def obtener(ruta):
  nombre = ruta.split('/')[-1]
  ruta = ruta
  if os.path.isdir(ruta):
    tipo = 'Directorio'
  else:
    tipo = 'Archivo'
  tamanio = os.path.getsize(ruta)
  gb = int(tamanio / (1024**3))  
  mb = int((tamanio - (gb * (1024**3))) / (1024**2))  
  kb = int((tamanio - (gb * (1024**3)) - (mb * (1024**2))) / 1024)  
  b = int(tamanio - (gb * (1024**3) + mb * (1024**2) + kb * 1024))  

  if tamanio/1024 < 1:
    rep_amena = f'{b} b'
  elif tamanio/(1024**2)<1:
    rep_amena = f'{kb} Kb {b} b'
  elif tamanio/(1024**3)<1:
    rep_amena = f'{mb} Mb {kb} Kb {b} b'
  else:
    rep_amena = f'{gb} Gb {mb} Mb {kb} Kb {b} b'

  permisos = os.stat(ruta).st_mode

  permisos_str = ""
  permisos_str += "r" if permisos & stat.S_IRUSR else "-"
  permisos_str += "w" if permisos & stat.S_IWUSR else "-"
  permisos_str += "x" if permisos & stat.S_IXUSR else "-"
  permisos_str += "r" if permisos & stat.S_IRGRP else "-"
  permisos_str += "w" if permisos & stat.S_IWGRP else "-"
  permisos_str += "x" if permisos & stat.S_IXGRP else "-"
  permisos_str += "r" if permisos & stat.S_IROTH else "-"
  permisos_str += "w" if permisos & stat.S_IWOTH else "-"
  permisos_str += "x" if permisos & stat.S_IXOTH else "-"

  fecha_ultimo_acceso = datetime.datetime.fromtimestamp(os.stat(ruta).st_atime)

  fecha_modificacion = datetime.datetime.fromtimestamp(os.stat(ruta).st_mtime)

  fecha_creacion = datetime.datetime.fromtimestamp(os.stat(ruta).st_ctime)

  for x in [nombre,ruta,tipo,tamanio,rep_amena,permisos_str,fecha_ultimo_acceso,fecha_modificacion,fecha_creacion]:
    print(x)

  if os.path.isfile(ruta):
    if ruta != os.getcwd() + '/data/aclImdb.tar.gz':
      lineas = 0
      palabras = 0
      palabras_unicas = Counter()

      with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            lineas += 1
            palabras_en_linea = linea.split()
            palabras += len(palabras_en_linea)
            palabras_unicas.update(palabras_en_linea)

      print(f"Cantidad de líneas: {lineas}")
      print(f"Cantidad de palabras: {palabras}")
      print(f"Cantidad de palabras únicas: {len(palabras_unicas)}\n")







