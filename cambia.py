import os
from shutil import rmtree

directorio="."

for nombre_archivo in os.listdir(directorio):
    if nombre_archivo.endswith('_1.fastq'):
        numero = nombre_archivo.split('_')[0]
        os.rename(os.path.join(directorio, nombre_archivo), os.path.join(directorio, numero, 'R1.fastq'))
    elif nombre_archivo.endswith('_2.fastq'):
        numero = nombre_archivo.split('_')[0]
        os.rename(os.path.join(directorio, nombre_archivo), os.path.join(directorio, numero, 'R2.fastq'))
    if os.path.isdir(nombre_archivo):
        rmtree(nombre_archivo)