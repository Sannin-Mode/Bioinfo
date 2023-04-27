"""
Este script toma como parámetro un archivo tsv que contiene una columna con los nombres de las secuencias (SRR o ERR) y se descarga los archivos fastq.
Posteriormente, extrae el doi del articulo referenciado, y realiza un trimming (con Trim Galore!) y un análisis de abundancia metagenómica mediante Metaphlan (v.4).
Es necesario tener activado el ambiente qiime correspondiente

"""

#imports
import os
import sys
import csv
import zipfile
import pandas as pd
import requests
from Bio import Entrez
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from io import StringIO
import shutil as sh

#Capturamos el archivo que llega por argumento:
archivo_sra = sys.argv[1]
#Creamos archivo qza
os.system(f'qiime tools import --type NCBIAccessionIDs --input-path {archivo_sra} --output-path {archivo_sra}_meta.qza')

with open (archivo_sra, 'r') as archivo:
    #definicion variables
    doi = ''
    cod_proyecto = ''
    name = ''
    archivo = csv.reader(archivo, delimiter='\t')
    for row in archivo:
        if row[0].startswith('S') or row[0].startswith('E'):
            name = row[0]
            print ("SRA: "+ name)

            #Descarga metadatos
            os.system(f'qiime fondue get-metadata --i-accession-ids {archivo_sra}_meta.qza --p-email jmgr@b-kl.eu --o-metadata {name}_metadata.qza --o-failed-runs fail.qza')

            #Capturamos el archivo generado con el fondue:
            archivoZip = f"{name}_metadata.qza"

            #Lo leemos
            with zipfile.ZipFile(archivoZip, 'r') as archivo_zip:
                # Obtener la lista de objetos de archivo dentro del archivo zip (qza)
                objetos = archivo_zip.namelist()
                rutaSra = ''
                ruta = os.path.join(os.getcwd(),os.path.basename(rutaSra))
                
                for ob in objetos:
                    if ob.__contains__("sra-metadata.tsv"):
                        rutaSra = ob
                archivo = archivo_zip.extract(rutaSra)        

            df = pd.read_csv(archivo, sep="\t")
                
            cod_proyecto = df['Bioproject ID']

            cod_proyecto = cod_proyecto[0]

            # Es necesario indicar la dirección de correo electrónico para acceder a la API de Entrez
            Entrez.email = 'jmgr@b-kl.eu'

            # Busqueda en la base de datos de SRA
            handle = Entrez.esearch(db='sra', term=cod_proyecto)

            # Leer los resultados de la busqueda
            record = Entrez.read(handle)

            # Obtener los IDs de los registros asociados al proyecto
            id_list = record['IdList']

            # Obtener los datos de los registros utilizando los IDs
            handle = Entrez.efetch(db='sra', id=','.join(id_list), retmode='xml')


            # Parsear el resultado utilizando ElementTree
            tree = ET.parse(StringIO(handle.read().decode()))


            # Obtener los metadatos del primer registro
            root = tree.getroot()
            experiment = root.find('.//EXPERIMENT')
            title = experiment.find('.//TITLE').text


            # Realizar una consulta a la API de CrossRef
            response = requests.get(f'https://api.crossref.org/works?query.title={title}')

            # Comprobar si la consulta se ha realizado correctamente
            if response.status_code == 200:
                # Obtener los datos del primer resultado de la consulta
                data = response.json()['message']['items'][0]
                
                # Obtener el DOI del artículo
                doi = data['DOI']
                               
            else:
                doi = ''
                print(f'Se ha producido un error al realizar la consulta: {response.status_code}, no se obtuvo doi')

            #Descargamos la secuencia SRA
            os.system ("prefetch --verbose --progress {}".format(name))
            os.system (f'fasterq-dump --threads 8 --split-files --progress {name}')

            #Trim Galore!
            os.system("trim_galore -q 20 -j 8 --paired {}_1.fastq {}_2.fastq".format(name, name))

            #Cambiar nombres de los archivos generados por Trim Galore

            trim_fwd = name + "_1_val_1.fq"
            trim_rev = name + "_2_val_2.fq"

            #Ejecución de Metaphlan (v4)
            print("Metaphlan")

            #Generacion archivo bowtie2
            os.system(f'metaphlan {trim_fwd} {trim_rev} --bowtie2out {name}.bowtie2.bz2 --legacy-output --nproc 8 --input_type fastq > {name}_metagenome.txt')

            #Generacion archivo metagenomica con frecuencia relativa, con salida clásica
            os.system(f'metaphlan {name}.bowtie2.bz2 --input_type bowtie2out --legacy-output --nproc 8 > {name}.tabular')

            #Edicion del .tabular para incluir el doi
            with open(f'{name}.tabular', mode='r') as file:
            
            # Leer el contenido del archivo
                contenido = list(csv.reader(file, delimiter='\t'))
                # Insertar una nueva fila con el texto seleccionado en la segunda posición
                contenido.insert(1, ['doi', doi])
            
            # Abrir el archivo .tabular en modo de escritura
            with open(f'{name}.tabular', mode='w', newline='') as file:
                # Escribir el contenido actualizado en el archivo
                writer = csv.writer(file, delimiter='\t')
                writer.writerows(contenido)

            #Limpieza de la carpeta:
            print("Eliminando archivos temporales")
            extensiones = ['.tabular', '.py', '.tsv', '.qza']

            for root, dirs, files in os.walk('.'):
                for file in files:
                    if not any(file.endswith(extension) for extension in extensiones):
                        os.remove(os.path.join(root, file))
                for file_meta in files:
                    if any(file_meta.endswith("_megatenome.qza")):
                        os.remove(os.path.join(root, file_meta))
                for dir in dirs:
                    if not any(file.endswith(extension) for extension in extensiones):
                        sh.rmtree(os.path.join(root, dir), ignore_errors=True)