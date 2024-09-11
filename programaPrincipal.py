import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
from Maquina import Maquina,EstadoMaquina
from Trabajo import Trabajo,EstadoTrabajo
from typing import List
import random
import copy
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import re
import copy
nodoActual=None
mejorMaquinas: List[Maquina]=[]
G:nx.digraph
nodosVisitados=[]
patron = r"Trabajo (\d+) en Maquina (\d+)"
prob=0.8
Cmax=0
ordenMaquinas=pd.DataFrame
tiemposMaquinas=pd.DataFrame
maquinas: List[Maquina]=[]
trabajos: List[Trabajo]=[]
tiempoProgramable=0
tiemposProgramablesAnteriores=[]
ordenIteracion: List[Maquina]=[]
trabajosProcesados: List[Trabajo]=[]
ciclo: List[Maquina]=[]
cicloEncontrado=False
maquinasBloqueadas: List[Maquina]=[]
def importar():
    global ordenMaquinas, tiemposMaquinas
    
    archivo=fd.askopenfilename()
    datos=pd.read_csv(archivo, header=None)
    
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


def asignarTrabajosCiclo(ciclo: List[Maquina]):
    global tiempoProgramable, trabajos,maquinas
    copiaCiclos=copy.deepcopy(ciclo)

    # Verificamos que el ciclo no esté vacío
    if not ciclo:
        print("El ciclo está vacío. No hay trabajos para asignar.")
        return

    # Inicializamos una lista para almacenar la información de los trabajos a asignar
    trabajosAsignar = []

    # Recorremos las máquinas en el ciclo
    for i in range(len(ciclo)-1):
        maquinaAsignar = copiaCiclos[i+1].numeroMaquina
        trabajoAsignar = copiaCiclos[i].trabajoActual
        
        
        
        #Cambiamos el estado de la maquina
        
        maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
        #Cambiamos el trabajo que tiene encima
        maquinas[maquinaAsignar-1].trabajoActual=trabajoAsignar
        
        #Cambiamos el tiempo programable
        if maquinas[maquinaAsignar-1].tiempoProgramable<tiempoProgramable:
            maquinas[maquinaAsignar-1].tiemposTrabajos.append(["Bloqueo",maquinas[maquinaAsignar-1].tiempoProgramable,tiempoProgramable])
        #Añadimos los tiempos
        maquinas[maquinaAsignar-1].tiemposTrabajos.append([trabajoAsignar,tiempoProgramable,tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]])
        
        maquinas[maquinaAsignar-1].tiempoProgramable=tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]
        
        #Cambiamos el estado del trabajo
        trabajos[trabajoAsignar-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
        #Eliminamos elementos
        trabajos[trabajoAsignar-1].tiemposProcesamiento.pop(0)
        trabajos[trabajoAsignar-1].ordenProcesamiento.pop(0)
        
        #Cambiamos el trabajo actual
        trabajos[trabajoAsignar-1].maquinaActual=maquinaAsignar
        
        print(f"El trabajo: {trabajoAsignar} fue asignado a la maquina: {maquinaAsignar}, estaba en la maquina {copiaCiclos[i].numeroMaquina}")


    print("Trabajos asignados correctamente a las máquinas en el ciclo.")

def asignarTrabajosCicloh(ciclo: List[Maquina],camino):
    global tiempoProgramable, trabajos,maquinas
    copiaCiclos=copy.deepcopy(ciclo)

    # Verificamos que el ciclo no esté vacío
    if not ciclo:
        print("El ciclo está vacío. No hay trabajos para asignar.")
        return

    # Inicializamos una lista para almacenar la información de los trabajos a asignar
    trabajosAsignar = []

    # Recorremos las máquinas en el ciclo
    for i in range(len(ciclo)-1):
        maquinaAsignar = copiaCiclos[i+1].numeroMaquina
        trabajoAsignar = copiaCiclos[i].trabajoActual
        
        
        
        #Cambiamos el estado de la maquina
        
        maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
        #Cambiamos el trabajo que tiene encima
        maquinas[maquinaAsignar-1].trabajoActual=trabajoAsignar
        
        #Cambiamos el tiempo programable
        if maquinas[maquinaAsignar-1].tiempoProgramable<tiempoProgramable:
            maquinas[maquinaAsignar-1].tiemposTrabajos.append(["Bloqueo",maquinas[maquinaAsignar-1].tiempoProgramable,tiempoProgramable])
        #Añadimos los tiempos
        maquinas[maquinaAsignar-1].tiemposTrabajos.append([trabajoAsignar,tiempoProgramable,tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]])
        
        maquinas[maquinaAsignar-1].tiempoProgramable=tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]
        
        #Cambiamos el estado del trabajo
        trabajos[trabajoAsignar-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
        #Eliminamos elementos
        trabajos[trabajoAsignar-1].tiemposProcesamiento.pop(0)
        trabajos[trabajoAsignar-1].ordenProcesamiento.pop(0)
        
        #Cambiamos el trabajo actual
        trabajos[trabajoAsignar-1].maquinaActual=maquinaAsignar
        
        print(f"El trabajo: {trabajoAsignar} fue asignado a la maquina: {maquinaAsignar}, estaba en la maquina {copiaCiclos[i].numeroMaquina}")
        camino.append(f'Trabajo {trabajoAsignar} en Maquina {maquinaAsignar}')

    print("Trabajos asignados correctamente a las máquinas en el ciclo.")











        



def algoritmoInicial():
    global maquinas, trabajos, tiempoProgramable,prob, maquinasBloqueadas
    #El bucle sigue hasta que todos los trabajos tengan la etiqueta de Terminados
    pendiente=True
    
    print(f"----------ESTADO INICIAL DEL SISTEMA----------")
    print("MATRIZ INCIAL")
    print(ordenMaquinas)
    print("-------------------")
    print(tiemposMaquinas)
    print("-------------------")
    print("----------MAQUINAS----------")
    for i in range(len(maquinas)):
        print(maquinas[i])
    print("-------------------")
    print("----------TRABAJOS----------")
    for i in range(len(trabajos)):
        print(trabajos[i])
    print("-------------------")
    
    
    
        

    
            
        
                
                
        
        
    
    
    while pendiente:
        
        actializarEstados()
        print("--------------------INICIANDO ITERACION--------------------")
        

        
        #Iteramos por cada Maquina
        #Buscamos el orden de Iteración de las máquinas, Se pone de ultimo los que tengan tiempo programable
        ordenIteracion=sorted(maquinas, key=lambda m: m.tiempoProgramable,reverse=True)
        trabajosProcesados=[]

        maquinasBloqueadas =[]
        
        
        
        
        #Buscamos los trabajos en estado Procesado que son los que bloquean las máquinas
        for trabajo in trabajos:
            if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO:
                trabajosProcesados.append(trabajo)
                
                
                
                
        
                
                
                
                
                

        for maquina in ordenIteracion:
            trabajosParaMaquina: List[Trabajo]=[]
            print(f"------------------------------ Revisando Maquina {maquina.numeroMaquina} ------------------------------")
            #Caso en que esté bloqueada la maquina
            for maquinass in maquinas:
                if maquinass.estadoMaquina==EstadoMaquina.BLOQUEO:
                    maquinasBloqueadas.append(maquinass)
            print(f"El estado de la máquina es: {maquina.estadoMaquina.name}")
            
            for elemento in trabajos:
                if elemento.ordenProcesamiento:
                    if elemento.ordenProcesamiento[0]==maquina.numeroMaquina and elemento.estadoTrabajo==EstadoTrabajo.NO_INICIADO:
                        trabajosParaMaquina.append(elemento)
            print(f"Los trabajos que no han empezado y vinen para esta máquina son:")
            
            
            for elemento in trabajosParaMaquina:
                print(elemento.numeroTrabajo)
                
                
            if maquina.estadoMaquina==EstadoMaquina.BLOQUEO:
                
                
                

                ciclos(maquina,trabajosProcesados)
                            
                        
                        
                        
                        
                if trabajos[maquina.trabajoActual-1].ordenProcesamiento:        
                    #Caso transferencia
                    if maquinas[trabajos[maquina.trabajoActual-1].ordenProcesamiento[0]-1].estadoMaquina==EstadoMaquina.LIBRE and maquina.estadoMaquina==EstadoMaquina.BLOQUEO:
                        
                        print(f"Caso transferencia maquina {maquinas[trabajos[maquina.trabajoActual-1].ordenProcesamiento[0]-1].numeroMaquina} trabajo {maquina.trabajoActual}")
                        asignarTrabajo_Maquina(maquinas[trabajos[maquina.trabajoActual-1].ordenProcesamiento[0]-1].numeroMaquina,maquina.trabajoActual)
                
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
            #Caso no bloqueo
            if maquina.estadoMaquina==EstadoMaquina.LIBRE:
                #for trabajo in trabajos:
                    #if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO and trabajo.ordenProcesamiento[0]==maquina.numeroMaquina:
                        # maquina1=maquina.numeroMaquina
                        # trabajo1=trabajo.numeroTrabajo
                        # print(f"Caso no bloqueo mauina {maquina1} trabajo {trabajo1}")

                        # asignarTrabajo_Maquina(maquina1,trabajo1)
                        # break
                if trabajosParaMaquina:

                    print("Caso no hay trabajos procesados, vamos con los no iniciados")
                    #Generamos un numero entre 0 y 1
                    r=random.random()
                    if r<=prob:
                        #Cogemos un trabajo
                        trab=random.choice(trabajosParaMaquina)
                        maquina1=maquina
                        print(f"Se asignó  el trabajo {trab.numeroTrabajo} a la máquina {maquina1.numeroMaquina}")
                        asignarTrabajo_Maquina(maquina1.numeroMaquina,trab.numeroTrabajo)
                        #input("Presione una tecla para continuar: ")
                        
                        
                else:
                    print("-----------------------------------------------NO SE ASIGNÓ NADA--------------------------------------------")
                    #input("Presione una tecla para continuar: ")
        
        calcularTiempoProgramable()
        

        #Al final verificamos si sigue pendiente algun trabajo
        contadorPendientes=0
        for trabajo in trabajos:
            if trabajo.estadoTrabajo != EstadoTrabajo.TERMINADO:
                contadorPendientes+=1
        if contadorPendientes==0:
            pendiente=False
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
def ciclos(maquina: Maquina,trabajosProcesados):
    #Encontrar los intercambios necesarios
    global  cicloEncontrado, maquinasBloqueadas,maquinas, trabajos
    
    cicloEncontrado=False
    ciclo: List[Maquina]=[]
    maquinaActual=maquina
    #Si los trabajos estan procesados significa que están haciendo bloqueos
    #Maquina incial
    ciclo.append(maquina)
    #Iteramos por todos los trabajos que están haciendo bloqueos
        
    for i in range(len(maquinasBloqueadas)):
        
        if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and trabajos[ciclo[-1].trabajoActual-1] in trabajosProcesados:
            ciclo.append(maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1])
            maquinaActual=maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1]
            if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and ciclo[-1].estadoMaquina==EstadoMaquina.BLOQUEO:
                if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento[0]==maquina.numeroMaquina:
                    ciclo.append(maquina)
                    cicloEncontrado=True
                    break
        else: 
            print("No cumple para intercambio multiple")


    if cicloEncontrado:
        asignarTrabajosCiclo(ciclo)        
          


def ciclosh(maquina: Maquina,trabajosProcesados):
    #Encontrar los intercambios necesarios
    global  cicloEncontrado, maquinasBloqueadas,maquinas, trabajos
    
    cicloEncontrado=False
    ciclo: List[Maquina]=[]
    maquinaActual=maquina
    #Si los trabajos estan procesados significa que están haciendo bloqueos
    #Maquina incial
    ciclo.append(maquina)
    #Iteramos por todos los trabajos que están haciendo bloqueos
        
    for i in range(len(maquinasBloqueadas)):
        
        if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and trabajos[ciclo[-1].trabajoActual-1] in trabajosProcesados:
            ciclo.append(maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1])
            maquinaActual=maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1]
            if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and ciclo[-1].estadoMaquina==EstadoMaquina.BLOQUEO:
                if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento[0]==maquina.numeroMaquina:
                    ciclo.append(maquina)
                    cicloEncontrado=True
                    break
        else: 
            print("No cumple para intercambio multiple")


    return cicloEncontrado                  
          
def cicloshh(maquina: Maquina,trabajosProcesados,camino):
    #Encontrar los intercambios necesarios
    global  cicloEncontrado, maquinasBloqueadas,maquinas, trabajos
    
    cicloEncontrado=False
    ciclo: List[Maquina]=[]
    maquinaActual=maquina
    #Si los trabajos estan procesados significa que están haciendo bloqueos
    #Maquina incial
    ciclo.append(maquina)
    #Iteramos por todos los trabajos que están haciendo bloqueos
        
    for i in range(len(maquinasBloqueadas)):
        
        if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and trabajos[ciclo[-1].trabajoActual-1] in trabajosProcesados:
            ciclo.append(maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1])
            maquinaActual=maquinas[trabajos[maquinaActual.trabajoActual-1].ordenProcesamiento[0]-1]
            if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento and ciclo[-1].estadoMaquina==EstadoMaquina.BLOQUEO:
                if trabajos[ciclo[-1].trabajoActual-1].ordenProcesamiento[0]==maquina.numeroMaquina:
                    ciclo.append(maquina)
                    cicloEncontrado=True
                    break
        else: 
            print("No cumple para intercambio multiple")


    asignarTrabajosCicloh(camino=camino,ciclo=ciclo)          
          
            
def asignarTrabajo_Maquina(numeroMaquinaAsignar, numeroTrabajoAsignar):
    global tiempoProgramable
    
    
    
    #----------------------------Maquina nueva----------------------------
    lista=[]
    #estado
    maquinas[numeroMaquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
    #nuevo tiempo programable
    tprog=tiempoProgramable+trabajos[numeroTrabajoAsignar-1].tiemposProcesamiento[0]
    #Tiempos trabajos
    lista=[numeroTrabajoAsignar,tiempoProgramable,tprog]
    maquinas[numeroMaquinaAsignar-1].tiemposTrabajos.append(lista)
    #tiempoProgramable
    maquinas[numeroMaquinaAsignar-1].tiempoProgramable=tprog
    #Trabajo actual
    maquinas[numeroMaquinaAsignar-1].trabajoActual=numeroTrabajoAsignar
    
    #----------------------------Maquina anterior----------------------------
    if trabajos[numeroTrabajoAsignar-1].maquinaActual!=0:
        #estado
        maquinas[trabajos[numeroTrabajoAsignar-1].maquinaActual-1].estadoMaquina=EstadoMaquina.LIBRE
        #tiempo que estuvo en bloqueo
        
        lista=["Bloqueo",maquinas[trabajos[numeroTrabajoAsignar-1].maquinaActual-1].tiempoProgramable,tiempoProgramable]
        maquinas[trabajos[numeroTrabajoAsignar-1].maquinaActual-1].tiemposTrabajos.append(lista)
        #trabajo actual
        maquinas[trabajos[numeroTrabajoAsignar-1].maquinaActual-1].trabajoActual=0
    
    
    #----------------------------Trabajo----------------------------
    
    #Cambiamos el estado del trabajo
    
    trabajos[numeroTrabajoAsignar-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
    #Maquina actual
    trabajos[numeroTrabajoAsignar-1].maquinaActual=numeroMaquinaAsignar
    #Eliminamos el primer tiempo y el primer elemento en el orden
    trabajos[numeroTrabajoAsignar-1].ordenProcesamiento.pop(0)
    trabajos[numeroTrabajoAsignar-1].tiemposProcesamiento.pop(0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def asignarTrabajo_MaquinaBloq(numeroMaquinaAsignar1, numeroTrabajoAsignar1,numeroMaquinaAsignar2, numeroTrabajoAsignar2):
    global tiempoProgramable
    
    
    
    
    #----------------------------Maquinas----------------------------
    
    #estados
    if maquinas[numeroMaquinaAsignar1-1].estadoMaquina==EstadoMaquina.BLOQUEO:
        maquinas[numeroMaquinaAsignar1-1].estadoMaquina=EstadoMaquina.OCUPADO
    if maquinas[numeroMaquinaAsignar2-1].estadoMaquina==EstadoMaquina.BLOQUEO:
        maquinas[numeroMaquinaAsignar2-1].estadoMaquina=EstadoMaquina.OCUPADO
    #nuevo tiempo programable
    #tprog1=maquinas[numeroMaquinaAsignar1-1].tiempoProgramable+trabajos[numeroTrabajoAsignar2-1].tiemposProcesamiento[0]
    #tprog2=maquinas[numeroMaquinaAsignar2-1].tiempoProgramable+trabajos[numeroTrabajoAsignar1-1].tiemposProcesamiento[0]
    tprog1=tiempoProgramable+trabajos[numeroTrabajoAsignar2-1].tiemposProcesamiento[0]
    tprog2=tiempoProgramable+trabajos[numeroTrabajoAsignar1-1].tiemposProcesamiento[0]
    #Tiempos trabajos
    lista=[numeroTrabajoAsignar2,tiempoProgramable,tprog1]
    maquinas[numeroMaquinaAsignar1-1].tiemposTrabajos.append(lista)
    lista=[numeroTrabajoAsignar1,tiempoProgramable,tprog2]
    maquinas[numeroMaquinaAsignar2-1].tiemposTrabajos.append(lista)
    #tiempoProgramable
    maquinas[numeroMaquinaAsignar1-1].tiempoProgramable=tprog1
    maquinas[numeroMaquinaAsignar2-1].tiempoProgramable=tprog2
    #Trabajo actual
    maquinas[numeroMaquinaAsignar1-1].trabajoActual=numeroTrabajoAsignar2
    maquinas[numeroMaquinaAsignar2-1].trabajoActual=numeroTrabajoAsignar1
    #----------------------------------------------------------------
    if trabajos[numeroTrabajoAsignar1-1].maquinaActual!=0:
        
        #tiempo que estuvo en bloqueo
        lista=["Bloqueo",maquinas[trabajos[numeroTrabajoAsignar1-1].maquinaActual-1].tiempoProgramable,tiempoProgramable]
        maquinas[trabajos[numeroTrabajoAsignar1-1].maquinaActual-1].tiemposTrabajos.append(lista)
        
    if trabajos[numeroTrabajoAsignar2-1].maquinaActual!=0:
        
        #tiempo que estuvo en bloqueo
        lista=["Bloqueo",maquinas[trabajos[numeroTrabajoAsignar2-1].maquinaActual-1].tiempoProgramable,tiempoProgramable]
        maquinas[trabajos[numeroTrabajoAsignar2-1].maquinaActual-1].tiemposTrabajos.append(lista)
        
    
    
    

    #----------------------------Trabajos----------------------------
    
    #Cambiamos el estado del trabajo
    
    trabajos[numeroTrabajoAsignar1-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
    trabajos[numeroTrabajoAsignar2-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
    #Maquina actual
    trabajos[numeroTrabajoAsignar1-1].maquinaActual=numeroMaquinaAsignar2
    trabajos[numeroTrabajoAsignar2-1].maquinaActual=numeroMaquinaAsignar1
    #Eliminamos el primer tiempo y el primer elemento en el orden
    trabajos[numeroTrabajoAsignar1-1].ordenProcesamiento.pop(0)
    trabajos[numeroTrabajoAsignar1-1].tiemposProcesamiento.pop(0)
    trabajos[numeroTrabajoAsignar2-1].ordenProcesamiento.pop(0)
    trabajos[numeroTrabajoAsignar2-1].tiemposProcesamiento.pop(0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                        
def calcularTiempoProgramable():
    global tiempoProgramable, tiemposProgramablesAnteriores,maquinas
    
    
    
    todoslostiempos=[elemento.tiempoProgramable for elemento in maquinas]
    todoslostiempos=sorted(set(todoslostiempos))
    
    #menortp=None
    anterior=tiempoProgramable
    tiempoProgramable=None
    
    for tiempo in todoslostiempos:
        if tiempo not in tiemposProgramablesAnteriores:
            tiempoProgramable=tiempo
            break
    if tiempoProgramable==None:
        tiempoProgramable=anterior+1
    
    tiemposProgramablesAnteriores.append(tiempoProgramable)
    print(f"El Nuevo tiempo programable es: {tiempoProgramable}")
    print(f"Se añade a la lista de tiempos {tiemposProgramablesAnteriores}")
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
def actializarEstados():
    
    global tiempoProgramable, maquinas, trabajos
    
    
    for maquina in maquinas:
        if maquina.tiempoProgramable>=tiempoProgramable and maquina.tiempoProgramable!=0:
            if not trabajos[maquina.trabajoActual-1].ordenProcesamiento:
                trabajos[maquina.trabajoActual-1].estadoTrabajo=EstadoTrabajo.TERMINADO
                maquinas[maquina.numeroMaquina-1].estadoMaquina=EstadoMaquina.LIBRE
                maquinas[maquina.numeroMaquina-1].trabajoActual=0
            else:
                maquinas[maquina.numeroMaquina-1].estadoMaquina=EstadoMaquina.BLOQUEO
                trabajos[maquina.trabajoActual-1].estadoTrabajo=EstadoTrabajo.PROCESADO
                
    print("Actualizando el estado del sistema")
    print("----------MAQUINAS----------")
    for i in range(len(maquinas)):
        print(maquinas[i])
    print("-------------------")
    print("----------TRABAJOS----------")
    for i in range(len(trabajos)):
        print(trabajos[i])
    print("-------------------")
    #input("Presione una tecla para continuar: ")
            

def creacionGraficos(maquinas: List[Maquina]):
    filas = []
    
    for maquina in maquinas:
        for lista in maquina.tiemposTrabajos:
            filas.append({
                "Tarea": lista[0], 
                "Inicio": lista[1], 
                "Fin": lista[2], 
                "Duracion": lista[2] - lista[1],  # Calculamos la duración
                "Maquina": f"Máquina {maquina.numeroMaquina}"  # Etiqueta para las máquinas
            })
    
    # Convertir las columnas Inicio y Fin a tipo int (si ya están en int)
    df = pd.DataFrame(filas)
    print("Datos del DataFrame:")
    print(df)
    graficarGantt(df)
def graficarGantt(df):
    fig = go.Figure()

    # Crear una traza para cada tarea
    for tarea in df['Tarea'].unique():
        df_tarea = df[df['Tarea'] == tarea]
        
        fig.add_trace(go.Bar(
            x=df_tarea['Duracion'],  # La duración de la tarea
            y=df_tarea['Maquina'],   # Las máquinas en el eje Y
            base=df_tarea['Inicio'],  # El inicio de la tarea
            name=str(tarea),
            orientation='h',
            text=df_tarea['Tarea'],  # Mostrar el nombre de la tarea
            textposition='inside',  # Posicionar el texto dentro de la barra
            texttemplate='%{text}'  # Usar el texto directamente sin formato adicional
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title="Unidades de Tiempo",
        yaxis_title="Máquina",
        title="Gráfico de Gantt: Duración de tareas por máquina",
        xaxis=dict(
            type='linear',
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(
            title='Máquina',
            autorange='reversed'
        )
    )
    
    fig.show()




def crearGrafo():
    # Crear un grafo dirigido
    global G
    #plt.ion()
    G = nx.DiGraph()

    # Nodo inicial que representa el nido/hormiguero
    nido = "Nido"
    G.add_node(nido)
    
    # Conectar el nodo inicial a los trabajos iniciales
    for i in range(ordenMaquinas.shape[0]):  # Iterar sobre los trabajos
        primer_maquina = ordenMaquinas.iloc[i, 0]
        nodo_trabajo_inicial = f"Trabajo {i+1} en Maquina {primer_maquina}"
        G.add_edge(nido, nodo_trabajo_inicial)

    # Crear los nodos de los trabajos y las máquinas
    nodos_trabajos = []
    for i in range(ordenMaquinas.shape[0]):
        for j in range(ordenMaquinas.shape[1]):
            nodo = f"Trabajo {i+1} en Maquina {ordenMaquinas.iloc[i, j]}"
            nodos_trabajos.append(nodo)
            G.add_node(nodo)
    
    # Conectar los nodos dentro de cada trabajo respetando la precedencia
    for i in range(ordenMaquinas.shape[0]):
        for j in range(ordenMaquinas.shape[1] - 1):
            trabajo = f"Trabajo {i+1}"
            estado_actual = f"{trabajo} en Maquina {ordenMaquinas.iloc[i, j]}"
            estado_siguiente = f"{trabajo} en Maquina {ordenMaquinas.iloc[i, j+1]}"
            
            # Añadir una arista del estado actual al estado siguiente respetando la precedencia
            G.add_edge(estado_actual, estado_siguiente)

    # Añadir aristas bidireccionales entre nodos que corresponden a la misma máquina
    for j in range(ordenMaquinas.shape[1]):  # Iterar sobre las máquinas
        for i in range(ordenMaquinas.shape[0]):  # Iterar sobre los trabajos
            nodo_origen = f"Trabajo {i+1} en Maquina {ordenMaquinas.iloc[i, j]}"
            for k in range(i + 1, ordenMaquinas.shape[0]):
                nodo_destino = f"Trabajo {k+1} en Maquina {ordenMaquinas.iloc[k, j]}"
                if nodo_origen != nodo_destino:
                    G.add_edge(nodo_origen, nodo_destino)
                    G.add_edge(nodo_destino, nodo_origen)

    # Conectar todos los nodos de un trabajo a todos los nodos de otros trabajos
    for nodo_origen in nodos_trabajos:
        for nodo_destino in nodos_trabajos:
            if nodo_origen != nodo_destino:
                # Extraer información de los trabajos y máquinas
                trabajo_origen, maquina_origen = nodo_origen.split(" en Maquina ")
                trabajo_destino, maquina_destino = nodo_destino.split(" en Maquina ")
                
                # Añadir arista bidireccional entre nodos de trabajos diferentes
                if trabajo_origen != trabajo_destino:
                    G.add_edge(nodo_origen, nodo_destino)
                    G.add_edge(nodo_destino, nodo_origen)

    # Inicializar la feromona en todas las aristas
    for (u, v) in G.edges():
        G[u][v]['feromona'] = 1.0  # Valor inicial de feromona
    
    # Dibujar el grafo
    pos = nx.spring_layout(G)  # Layout del grafo
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=8, font_weight='bold')
    plt.show()
    
    return G

# Asegúrate de definir 'ordenMaquinas' antes de llamar a esta función
def terminado(camino,G):
    sale=False
    nodos=set(G.nodes())
    
    nodosVisitados=set(camino)
    print(nodos)
    print(nodosVisitados==nodos)
    contador=0
    for trab in trabajos:
        if not trab.ordenProcesamiento:
            contador+=1
    if contador==len(trabajos) or nodosVisitados==nodos:
        sale=True
    return sale




















def calcularProbabilidad(hormiga, posiblesSiguientes, feromona, tiempo_ejecucion, alpha, beta, trabajosProcesados,camino):
    global nodosVisitados, nodoActual
    pos=[]
    ciclo=[]
    patron = r"Trabajo (\d+) en Maquina (\d+)"
    
    
    if not posiblesSiguientes:
        return None
    for posibles in posiblesSiguientes:
        coincidencia = re.match(patron, posibles)
    
        if coincidencia:
            trabajo = int(coincidencia.group(1))
            maquina = int(coincidencia.group(2))
        if trabajos[trabajo-1].ordenProcesamiento:
            #Caso traspaso
            if maquinas[maquina-1].estadoMaquina==EstadoMaquina.LIBRE and trabajos[trabajo-1].estadoTrabajo==EstadoTrabajo.PROCESADO and trabajos[trabajo-1].ordenProcesamiento[0]==maquina:
                pos.append(posibles)
            #Caso ciclos o intercambios
            
            elif maquinas[maquina-1].estadoMaquina==EstadoMaquina.BLOQUEO and ciclosh(maquinas[maquina-1],trabajosProcesados) and trabajos[trabajo-1].ordenProcesamiento[0]==maquina:
                pos.append(posibles)
                ciclo.append(posibles)
            #Caso no iniciados
            
            elif trabajos[trabajo-1].estadoTrabajo==EstadoTrabajo.NO_INICIADO and maquinas[maquina-1].estadoMaquina==EstadoMaquina.LIBRE and trabajos[trabajo-1].ordenProcesamiento[0]==maquina:
                pos.append(posibles)
    feromona_nodos = np.array([feromona.get((nodoActual, nodo), 0) for nodo in pos])
    visibilidad_nodos = np.array([
        1 / trabajos[extraer_numero_trabajo(nodo)].tiemposProcesamiento[0] 
        for nodo in pos
    ])
    if pos:
        probabilidad = (feromona_nodos ** alpha) * (visibilidad_nodos ** beta)
        probabilidad /= probabilidad.sum()
        siguiente_nodo = np.random.choice(pos, p=probabilidad)
        coincidencia = re.match(patron, siguiente_nodo)
        if coincidencia:
            trabajo = int(coincidencia.group(1))
            maquina = int(coincidencia.group(2))
        if siguiente_nodo in ciclo:
        
            cicloshh(maquinas[maquina-1],trabajosProcesados,camino)
            if not str(siguiente_nodo) in camino:
                        
                        if str(siguiente_nodo)!= "None":
                            camino.append(str(siguiente_nodo))
                            nodoActual=str(siguiente_nodo)
                            print(nodoActual)
        elif maquinas[maquina-1].estadoMaquina==EstadoMaquina.LIBRE and trabajos[trabajo-1].estadoTrabajo==EstadoTrabajo.PROCESADO:
            
            asignarTrabajo_Maquina(maquina,trabajo)
            if not str(siguiente_nodo) in camino:
                        
                        if str(siguiente_nodo)!= "None":
                            camino.append(str(siguiente_nodo))
                            calcularProbabilidad(hormiga, posiblesSiguientes, nx.get_edge_attributes(G, 'feromona'), tiempoProgramable, 1, 1,trabajosProcesados,camino)
                            nodoActual=str(siguiente_nodo)
                            print(nodoActual)
            
        elif trabajos[trabajo-1].estadoTrabajo==EstadoTrabajo.NO_INICIADO and maquinas[maquina-1].estadoMaquina==EstadoMaquina.LIBRE:
            asignarTrabajo_Maquina(maquina,trabajo)
            if not str(siguiente_nodo) in camino:
                        
                        if str(siguiente_nodo)!= "None":
                            camino.append(str(siguiente_nodo))
                            nodoActual=str(siguiente_nodo)
                            print(nodoActual)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
def extraer_numero_trabajo(texto):
    """
    Extrae el número del trabajo de un texto de la forma "Trabajo x en Maquina y".
    """
    patron = r"Trabajo (\d+) en Maquina"
    coincidencia = re.search(patron, texto)
    
    if coincidencia:
        return int(coincidencia.group(1)) - 1  # Restar 1 si el índice de trabajo empieza desde 0
    else:
        raise ValueError("El texto no tiene el formato esperado")    
    
def actualizarFeromonas(grafo, mejor_cmax, camino, rho=0.1, Q=1.0):
    
    for u, v in grafo.edges:
        grafo[u][v]['feromona'] *= (1 - rho)
    
    # Depósito de feromona en el camino correspondiente al mejor Cmax
    for i in range(len(camino) - 1):
        u, v = camino[i], camino[i+1]
        if grafo.has_edge(u, v):
            # Depósito de feromona proporcional a la calidad de la solución
            grafo[u][v]['feromona'] += Q / mejor_cmax
    return grafo
    
def aco():
    global maquinas, trabajos, Cmax, tiemposProgramablesAnteriores, tiempoProgramable, trabajosProcesados, G, maquinasBloqueadas, mejorMaquinas, nodoActual
    tiemposProgramablesAnteriores=[]
    listaMaqRes=[]
    numeroIteraciones=50
    numeroHormigas=4
    nido = "Nido"
    evaporation_rate = 0.05
    prueba=[]
    alpha=1 
    beta=2
    mejorCamino=None
    for iteracion in range(numeroIteraciones):
        caminosanteriores=[]
        CmaxAnteriores=[]
        tiempo_ejecucion=0
        
        for hormiga in range(numeroHormigas):
            print("--------------------ESTADOS INICIALES--------------------")
            for maq in maquinas:
                maq.estadoMaquina=EstadoMaquina.LIBRE
                maq.tiempoProgramable=0
                maq.tiemposTrabajos=[]
                maq.trabajoActual=0
                print(maq)
            print("--------------------------------------------------------------")
            for trab in trabajos:
                trab.estadoTrabajo=EstadoTrabajo.NO_INICIADO
                trab.maquinaActual=0
                trab.ordenProcesamiento=trab.ordenProcesamientoGuardados.copy()
                trab.tiemposProcesamiento=trab.tiemposProcesamientoGuardados.copy()
                print(trab)
            
            #Iniciamos la hormiga en el hormiguero
            camino=[nido]
            nodoActual=nido
            tiempoProgramable=0
            
            tiemposProgramablesAnteriores=[]
            
            while not terminado(camino,G):
                print("---------------------------EMPIEZA HORMIGA-------------------------")
                actializarEstados()
                trabajosProcesados=[]
                maquinasBloqueadas=[]
                for maquinass in maquinas:
                    if maquinass.estadoMaquina==EstadoMaquina.BLOQUEO:
                        maquinasBloqueadas.append(maquinass)
                for trabajo in trabajos:
                    if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO:
                        trabajosProcesados.append(trabajo)
                posiblesSiguientes=list(G.successors(nodoActual))
                calcularProbabilidad(hormiga, posiblesSiguientes, nx.get_edge_attributes(G, 'feromona'), tiempoProgramable, alpha, beta,trabajosProcesados,camino)
                
                
                calcularTiempoProgramable()
                print(tiempoProgramable)
                
            caminosanteriores.append(camino)
            CmaxAnteriores.append(tiemposProgramablesAnteriores[-1])
            prueba.append(tiemposProgramablesAnteriores[-1])
            
            listaMaqRes.append(copy.deepcopy(maquinas))
        #creacionGraficos(maquinas)
        #mejor_camino = min(caminosanteriores, key=lambda x: evaluar_camino(x, tiempo_ejecucion))
        G=actualizarFeromonas(G, max(CmaxAnteriores), caminosanteriores[CmaxAnteriores.index(max(CmaxAnteriores))], evaporation_rate, Q=2)
        
        if max(CmaxAnteriores)<Cmax:
            aa=listaMaqRes[CmaxAnteriores.index(max(CmaxAnteriores))].copy()
            mejorCaminoT=caminosanteriores[CmaxAnteriores.index(max(CmaxAnteriores))].copy()
            Cmax=copy.deepcopy(max(CmaxAnteriores))
            mejorMaquinas.pop(0)
            mejorMaquinas=copy.deepcopy(aa)
            creacionGraficos(mejorMaquinas)
    
    print(prueba)
    creacionGraficos(mejorMaquinas)
    graficoPrueba(prueba)
    print("Hola")
                
                
def graficoPrueba(datos):
    # Graficar los datos
    plt.plot(range(len(datos)), datos, marker='o')

    # Etiquetas de los ejes
    plt.xlabel('Índice')
    plt.ylabel('Valor')

    # Título del gráfico
    plt.title('Gráfico de datos (Índice vs Valor)')

    # Mostrar el gráfico
    plt.show()
    plt.pause(1)
        
    


    
def main():
    global Cmax, mejorMaquinas
    importar()
    crearListas()
    algoritmoInicial()
    Cmax=tiemposProgramablesAnteriores[-2]
    print(f"Cmax encontrado {Cmax}")
    print("TERMINADO")
    mejorMaquinas=copy.deepcopy(maquinas)
    creacionGraficos(maquinas)
    G=crearGrafo()
    aco()
main()

