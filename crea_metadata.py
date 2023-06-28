"""
Script que toma un archivo csv o tsv, guarde los valores en un dataframe, y cree un archivo de metadatos en formato tsv
Debe tener la siguiente estructura: Sample_ID (el código SRA), Age, Gender, BMI, GroupID, Disease, Stage (sano = 0, enfermo = 1), y la posiblidad de agregar mas columnas si se estima)
"""


from Bio import Entrez #Se activa si lo ejecutamos en entorno Qiime
import sys, os, re
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np

ruta_actual = os.getcwd()

listado_columnas = ['Sample_ID',"Disease","Stage","Age","Gender","BMI","Smoker","Diet"]

archivo_csv = sys.argv[1] #Capturamos el archivo tsv
nombre = os.path.splitext(archivo_csv)[0]

df = pd.read_csv(archivo_csv) #Creamos un dataframe con la tabla





def seleccionar_col(dataframe, columnas):
    """
    Función para seleccionar una serie de columnas en el archivo de
    metadatos, y crear un nuevo dataframe con los datos extraídos
    """
    
    nuevo_dataframe = pd.DataFrame(columns=columnas) #Se crea un Dataframe en blanco para ir agregando los valores

    for _ in dataframe["Sample_ID"].to_list():
    
        if "Sample_ID" in dataframe.columns:
            nuevo_dataframe["Sample_ID"] = dataframe["Sample_ID"]
        else:
            nuevo_dataframe["Sample_ID"] = "not_exists"
        
        #Se coloca en la columna "Disease" el nombre de la enfermedad, que viene determinada por el archivo de metadatos original
        nuevo_dataframe["Disease"] = nombre

        if "Disease" in dataframe.columns:
            nuevo_dataframe["Stage"] = dataframe["Disease"].apply(lambda x: 1 if x == nombre else 0)
        else:
            nuevo_dataframe["Stage"] = "not_exists"
        
        if "Age" in dataframe.columns:
            nuevo_dataframe["Age"] = dataframe["Age"]
        else:
            nuevo_dataframe["Age"] = "not_exists"
        
        if "Gender" in dataframe.columns:
            nuevo_dataframe["Gender"] = dataframe["Gender"]
        else:
            nuevo_dataframe["Gender"] = "not_exists"
        
        if "BMI" in dataframe.columns:
            nuevo_dataframe["BMI"] = dataframe["BMI"]
        else:
            nuevo_dataframe["BMI"] = "not_exists"
        
        if "Smoker" in dataframe.columns:
            nuevo_dataframe["Smoker"] = dataframe["Smoker"]
        else:
            nuevo_dataframe["Smoker"] = "not_exists"
        
        if "Diet" in dataframe.columns:
            nuevo_dataframe["Diet"] = dataframe["Diet"]
        else:
            nuevo_dataframe["Diet"] = "not_exists"

    
    nuevo_dataframe = nuevo_dataframe.dropna(subset=['Sample_ID'])
    nuevo_dataframe = nuevo_dataframe.set_index("Sample_ID")
    nuevo_dataframe["Age"] = nuevo_dataframe["Age"].astype(int)


    return nuevo_dataframe    
    


nuevo_df = seleccionar_col(df, listado_columnas)
nuevo_df.to_csv(f"{nombre}_metadata.tsv", sep="\t")

