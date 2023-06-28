"""
Script para cambiar el formato de los archivos de una carpeta para adaptarlos al formato Casava, soportado por Qiime2.
"""

# Imports
import os
import shutil
import gzip
import sys

correo = 'bioknowledgelab@gmail.com'
carpeta = sys.argv[1] #Carpeta donde se encuentran los archivos

def rename_and_compress_files(folder_path):
    """
    Método para renombrar los archivos de la carpeta
    """
    
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(folder_path)
    
    # Iterar sobre cada archivo
    for file_name in files:
        if file_name.endswith("_1.fastq"):
            # Obtener el nombre sin la extensión
            base_name = os.path.splitext(file_name)[0]
            
            # Crear el nuevo nombre de archivo
            new_name = f"{base_name.replace('_1', '')}_00_L001_R1_001.fastq.gz"
            
            # Comprimir el archivo en gzip
            with open(os.path.join(folder_path, file_name), 'rb') as file_in:
                with gzip.open(os.path.join(folder_path, new_name), 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)
            os.remove(os.path.join(folder_path, file_name))            
            print(f"Archivo {file_name} comprimido correctamente.")
        
        elif file_name.endswith("_2.fastq"):
            # Obtener el nombre sin la extensión
            base_name = os.path.splitext(file_name)[0]
            
            # Crear el nuevo nombre de archivo
            new_name = f"{base_name.replace('_2', '')}_00_L001_R2_001.fastq.gz"
            
            # Comprimir el archivo en gzip
            with open(os.path.join(folder_path, file_name), 'rb') as file_in:
                with gzip.open(os.path.join(folder_path, new_name), 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)
            os.remove(os.path.join(folder_path, file_name))
            print(f"Archivo {file_name} comprimido correctamente.")
    
    
    print("Proceso completado.")



# Ejemplo de uso
rename_and_compress_files(carpeta)

