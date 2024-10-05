Python

Todo lo que haremos sera con terminal bash.

1. Lo primero que haremos es abir la linea de comando la ubicación de nuestro proyecto, para ellos sera usando el comando cd.

2. Cuando nos encontremos en el directorio escribiremos el comando python3 -m venv <nombre_entorno> para crear un entrono virtual.

3. Ahora es necesario activar el entorno usando el comando source <nombre_entorno>/bin/activate, instalamos los modulos necesarios con el comando pip install -r requiremnets.txt.

4. Abrimos el archivo tarea.ipynb, seleccionamos el kernel de nuestro entorno y ejecutamos todo.


CMD

Igualmente todo se hará con bash

1. Abrimos nuestra terminal y buscamos donde deseamos descargar el archivo aclImdb_v1.tar.gz, de preferencia en este mismo repositorio dentro de la carpeta "CMD/A-02"

2. Con el comando curl -O https://ai.stanford.edu/%7Eamaas/data/sentiment/aclImdb_v1.tar.gz podemos descargar el archivo.

3. Como el archivo que descargamos está comprimido, para ello usamos el comando tar -xvf aclImdb_v1.tar.gz.

4. Nos movemos al directorio "./aclImdb/train".

5. Usando el siguiente comando podemos obtener los puntajes negativos ls neg | awk -F'[_ .]' '{print $2}' > puntaje_negativo.txt.

6. De manera analoga conseguimos los resultados positivos ls pos | awk -F'[_ .]' '{print $2}' > puntaje_positivo.txt.

7. Utilizemos el comando sed 's/\usercomments$//' urls_neg.txt > urls_negativo.txt para modificar el archivo llamado urls_neg.txt eliminando la parte de la cadena usercomments al final de las líneas.

8. Es igual para los positivos sed 's/\usercomments$//' urls_pos.txt > urls_positivo.txt.

9. A continuacion usando el comando paste urls_negativo.txt puntaje_negativo.txt > critica_negativo.txt combinar los dor archivos anteriores.

10. Para la parte positiva el comando es paste urls_positivo.txt puntaje_positivo.txt > critica_positivo.txt

11. Para crear el archvo que va a contener las 10 peores peliculas, escribimos el comando awk '{critica_negativo[$1]+=$2; count[$1]++} END {for (url in critica_negativo) print url, critica_negativo[url]/count[url]}' critica_negativo.txt | sort -k2 -n | head -n 10 > peores_peliculas.txt, lo que hace el comando anterior es hacer un promedio de todos los puntajes que tienen el mismo url, despues lo ordena de mayor a menor a mayor y despues toma los primeros 10.

12. De forma similar el comando awk '{critica_positio[$1]+=$2; count[$1]++} END {for (url in critica_positivo) print url, critica_positivo[url]/count[url]}' critica_positivo.txt | sort -k2 -n | tail -n 10 > mejores_peliculas.txt, e lo mismo que el paso 11.