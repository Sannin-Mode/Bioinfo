"""
Programa que toma como parámetros dos secuencias con formato SRRxxx_R1.fastq y SRRxxx_R2.fastq
Ejecuta consecutivamente Trim Galore!! y Metaphlan4 para conseguir el análisis metagenómico 
"""
import os
import sys
from os import remove

#Añadimos los archivos declarados como argumentos a las variables
fw_rds = sys.argv[1] #El archivo R1
rv_rds = sys.argv[2] #El archivo R2

#Extraemos el nombre de la secuencia para utilizarla en las salidas y lo formateamos

nombre_extracted = os.path.splitext(fw_rds)[0]
nombre = nombre_extracted[:-3]

#Trim Galore!

os.system("trim_galore -q 20 -j 8 --paired {} {}".format(fw_rds, rv_rds))

#Cambiar nombres de los archivos generados por Trim Galore

trimmed_forward = nombre + "_R1_val_1.fq"
trimmed_reverse = nombre + "_R2_val_2.fq"

#Ejecución de Metaphlan (v4)

os.system("metaphlan {} {} --bowtie2out {}.bowtie2.bz --nproc 8 --input_type fastq --unclassified_estimation > {}_metagenome.txt".format(trimmed_forward,trimmed_reverse,nombre,nombre))
os.system("metaphlan {}.bowtie2.bz --input_type bowtie2out --nproc 8 --unclassified_estimation > {}.txt".format(nombre,nombre))
