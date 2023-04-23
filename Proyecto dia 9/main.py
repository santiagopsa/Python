from datetime import datetime
import os
from pathlib import Path
import re
import time

print('\n')
print('-'*100)
print('Fecha de búsqueda: '+str(datetime.now().strftime('%m/%d/%Y'))+'\n')
print('ARCHIVO\t\t\tNRO. SERIE')
print('-------\t\t\t----------')
startingpath=Path('G:\\','Mi unidad','Python projects','Proyecto dia 9','Mi_Gran_Directorio')
counter=0
tiempo_inicial=time.time()
for root,folder,file in os.walk(startingpath):
    #print(file)
    if file != []:
        for f in file:
            current_path=root
            #print(current_path)
            temp_file=open(Path(current_path,f)).read()
            #print(temp_file)
            regex=re.search(r'[N](\w{3})[-](\d{5})',temp_file)
            if regex != None:
                print(regex.group()+'\t\t'+f)
                counter += 1
                #print(f)
tiempo_final=time.time()
print(f'Se han encontrado {counter} valores')
print(f'El tiempo de busqueda fue de {tiempo_final-tiempo_final} segundos')

