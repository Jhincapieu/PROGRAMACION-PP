import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
from Maquina import Maquina,EstadoMaquina
from Trabajo import Trabajo,EstadoTrabajo
from typing import List

ordenMaquinas=pd.DataFrame
tiemposMaquinas=pd.DataFrame
maquinas: List[Maquina]=[]
trabajos: List[Trabajo]=[]
tiempoProgramable=0
def importar():
    
    archivo=fd.askopenfilename()
    datos=pd.read_csv(archivo, header=None)
    global ordenMaquinas, tiemposMaquinas
    ordenMaquinas=datos[0].str.split(expand=True)
    
    
    tiemposMaquinas=datos[1].str.split(expand=True)
    
    
def crearListas():
    
    global maquinas,ordenMaquinas,tiemposMaquinas
    
    
    for i in range(1,ordenMaquinas.shape[1]+1):
        maquina=Maquina(i,0,EstadoMaquina.LIBRE)
        maquinas.append(maquina)
    for i in range(1,ordenMaquinas.shape[0]+1):
        tiempos=[]
        orden=[]
        for s in range(ordenMaquinas.shape[1]):
            tiempos.append(int(tiemposMaquinas.iloc[i-1,s]))
            orden.append(int(ordenMaquinas.iloc[i-1,s]))
        trabajo=Trabajo(i,0,EstadoTrabajo.NO_INICIADO,orden,tiempos)
        trabajos.append(trabajo)

def algoritmoInicial():
    global maquinas, trabajos, tiempoProgramable
    #El bucle sigue hasta que todos los trabajos tengan la etiqueta de Terminados
    pendiente=True
    while pendiente:
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #Al final verificamos si sigue pendiente algun trabajo
        contadorPendientes=0
        for trabajo in trabajos:
            if trabajo.estadoTrabajo != EstadoTrabajo.TERMINADO:
                contadorPendientes+=1
        if contadorPendientes==0:
            pendiente=False
            
            
    


def main():
    importar()
    print(ordenMaquinas)
    print("-------------------")
    print(tiemposMaquinas)
    print("-------------------")
    crearListas()
    for i in range(len(maquinas)):
        print(maquinas[i])
    print("-------------------")
    for i in range(len(trabajos)):
        print(trabajos[i])
    
    for trabajo in trabajos:
        if trabajo.estadoTrabajo==EstadoTrabajo.NO_INICIADO:
            print(trabajo.estadoTrabajo.name)

main()