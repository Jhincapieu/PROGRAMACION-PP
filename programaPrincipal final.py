from operator import index
from traceback import print_tb
from nbformat import current_nbformat_minor
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
import sys
from pandastable import Table

import prueba
alpha=None
beta=None
iteraciones=None
hormigas=None
listasInicialesMaquinas=[]
repite=0
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
        maquinaAnterior=copiaCiclos[i].numeroMaquina
        
        if maquinas[maquinaAnterior-1].estadoMaquina==EstadoMaquina.BLOQUEO:
            maquinas[maquinaAnterior-1].estadoMaquina=EstadoMaquina.LIBRE
        
        
        
        #Cambiamos el estado de las maquinas
        if trabajos[trabajoAsignar-1].ordenProcesamiento[0]==maquinaAsignar:
            
            maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
            maquinas[maquinaAsignar-1].trabajoActual=trabajoAsignar
            trabajos[trabajoAsignar-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
            
            
            
            if maquinas[maquinaAsignar-1].tiempoProgramable<tiempoProgramable:
                maquinas[maquinaAsignar-1].tiemposTrabajos.append(["Bloqueo",maquinas[maquinaAsignar-1].tiempoProgramable,tiempoProgramable])
            tp=tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]
            maquinas[maquinaAsignar-1].tiempoProgramable=tp
            maquinas[maquinaAsignar-1].tiemposTrabajos.append([trabajoAsignar,tiempoProgramable,tp])
            trabajos[trabajoAsignar-1].maquinaActual=maquinaAsignar
            trabajos[trabajoAsignar-1].ordenProcesamiento.pop(0)
            trabajos[trabajoAsignar-1].tiemposProcesamiento.pop(0)
        
        #Maquina anterior si estaba en bloqueo se pone en libre
        if maquinas[maquinaAnterior-1].estadoMaquina==EstadoMaquina.BLOQUEO:
            maquinas[maquinaAnterior-1].estadoMaquina=EstadoMaquina.LIBRE
            maquinas[maquinaAnterior-1].tiemposTrabajos.append(["Bloqueo",maquinas[maquinaAnterior-1].tiempoProgramable],tiempoProgramable)
            maquinas[maquinaAnterior-1].trabajoActual=0
            
        
        
        print(f"El trabajo: {trabajoAsignar} fue asignado a la maquina: {maquinaAsignar}, estaba en la maquina {copiaCiclos[i].numeroMaquina}")
        
        
        if maquinas[maquinaAsignar-1].trabajoActual==0:
            maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.LIBRE
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #     #Cambiamos el estado de la maquina
    #     if trabajos[trabajoAsignar-1].ordenProcesamiento[0]==maquinaAsignar:
    #         maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
    #         #Cambiamos el trabajo que tiene encima
    #         maquinas[maquinaAsignar-1].trabajoActual=trabajoAsignar
        
    #         #Cambiamos el tiempo programable
    #         if maquinas[maquinaAsignar-1].tiempoProgramable<tiempoProgramable:
    #             maquinas[maquinaAsignar-1].tiemposTrabajos.append(["Bloqueo",maquinas[maquinaAsignar-1].tiempoProgramable,tiempoProgramable])
    #         #Añadimos los tiempos
    #         maquinas[maquinaAsignar-1].tiemposTrabajos.append([trabajoAsignar,tiempoProgramable,tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]])
            
    #         maquinas[maquinaAsignar-1].tiempoProgramable=tiempoProgramable+trabajos[trabajoAsignar-1].tiemposProcesamiento[0]
            
    #         #Cambiamos el estado del trabajo
    #         trabajos[trabajoAsignar-1].estadoTrabajo=EstadoTrabajo.PROCESANDO
    #         #Eliminamos elementos
    #         trabajos[trabajoAsignar-1].tiemposProcesamiento.pop(0)
    #         trabajos[trabajoAsignar-1].ordenProcesamiento.pop(0)
            
    #         #Cambiamos el trabajo actual
    #         trabajos[trabajoAsignar-1].maquinaActual=maquinaAsignar
        
    #     print(f"El trabajo: {trabajoAsignar} fue asignado a la maquina: {maquinaAsignar}, estaba en la maquina {copiaCiclos[i].numeroMaquina}")
    #     if maquinas[maquinaAsignar-1].trabajoActual==0:
    #         maquinas[maquinaAsignar-1].estadoMaquina=EstadoMaquina.LIBRE

    # print("Trabajos asignados correctamente a las máquinas en el ciclo.")



        



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
          
          
          
          
def algoritmoInicialMod():
    global maquinas, trabajos, tiempoProgramable,prob, maquinasBloqueadas, listasInicialesMaquinas
    copiaMaquinasIniciales=copy.deepcopy(listasInicialesMaquinas)
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
            for i in listasInicialesMaquinas[maquina.numeroMaquina-1]:
                trabajosParaMaquina.append(trabajos[i-1])
            #for elemento in trabajos:
            #    if elemento.ordenProcesamiento:
            #        if elemento.ordenProcesamiento[0]==maquina.numeroMaquina and elemento.estadoTrabajo==EstadoTrabajo.NO_INICIADO:
            #            trabajosParaMaquina.append(elemento)
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
                for trabajo in trabajos:
                    if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO and trabajo.ordenProcesamiento[0]==maquina.numeroMaquina:
                         maquina1=maquina.numeroMaquina
                         trabajo1=trabajo.numeroTrabajo
                         print(f"Caso no bloqueo maquina {maquina1} trabajo {trabajo1}")

                         asignarTrabajo_Maquina(maquina1,trabajo1)
                         break
                if trabajosParaMaquina and maquina.estadoMaquina==EstadoMaquina.LIBRE:

                    print("Caso no hay trabajos procesados, vamos con los no iniciados")
                    #Generamos un numero entre 0 y 1
                    r=random.random()
                    if r<=prob:
                        #Cogemos un trabajo
                        trab=trabajosParaMaquina[0]
                        listasInicialesMaquinas[maquina.numeroMaquina-1].pop(0)
                        maquina1=maquina
                        print(f"Se asignó  el trabajo {trab.numeroTrabajo} a la máquina {maquina1.numeroMaquina}")
                        asignarTrabajo_Maquina(maquina1.numeroMaquina,trab.numeroTrabajo)
                        #input("Presione una tecla para continuar: ")
                        
                        
                elif maquina.estadoMaquina==EstadoMaquina.LIBRE:
                    print("-----------------------------------------------NO SE ASIGNÓ NADA--------------------------------------------")
                    #input("Presione una tecla para continuar: ")
        
        calcularTiempoProgramableh(copiaMaquinasIniciales)
        

        #Al final verificamos si sigue pendiente algun trabajo
        contadorPendientes=0
        for trabajo in trabajos:
            if trabajo.estadoTrabajo != EstadoTrabajo.TERMINADO:
                contadorPendientes+=1
        if contadorPendientes==0:
            pendiente=False         
          



def llenarProbs(probabilidades,feromonaMaquinas, posiblesInicios,ordenProcesamientoMaquina):   
    global trabajos, maquinas
    camino=[]
    
                    
#def construirInicios(probabilidades,feromonaMaquinas,posiblesInicios,ordenProcesamientoMaquina):
    
#    f
#    camino=[]
    
#    while len(camino)<
    
def calcularProbs(probabilidades,feromonaMaquinas,alpha,beta):
    #SACAR PROBABILIDADES BASADO EN LA FEROMONA Y TIEMPOS DE PROCESAMIENTO
    for proba in range(len(probabilidades)):
        for fila in feromonaMaquinas[proba].index:
            for columna in feromonaMaquinas[proba].columns:
                suma=0
                if fila==columna:
                    probabilidades[proba].loc[fila,columna]=0
                elif columna==0:
                    probabilidades[proba].loc[fila,columna]=0
                elif trabajos[columna-1].estadoTrabajo==EstadoTrabajo.NO_INICIADO:
                    #sumatoria para denominador de la prob
                    for col in feromonaMaquinas[proba].columns:
                        if col!=0:
                            if trabajos[col-1].estadoTrabajo==EstadoTrabajo.NO_INICIADO:
                                suma=suma+((1/trabajos[col-1].tiemposProcesamiento[0]**beta))*(feromonaMaquinas[proba].loc[fila,col]**alpha)
                    probabilidades[proba].loc[fila,columna]=(((1/trabajos[columna-1].tiemposProcesamiento[0])**beta)*(feromonaMaquinas[proba].loc[fila,columna]**alpha))/suma
                    #print(suma)
        print(probabilidades[proba])
        #print("A") 

def seleccionar_camino_con_ajuste(df, nodo_inicial=0):
    # Copia del DataFrame original para modificarlo sin afectar el original
    df_actual = df.copy()

    # Asegurar que todos los valores del DataFrame sean numéricos (forzar conversiones)
    df_actual = df_actual.apply(pd.to_numeric, errors='coerce')

    # Manejar NaNs si es necesario (reemplazar por 0, por ejemplo)
    df_actual = df_actual.fillna(0)

    # Lista para guardar los nodos visitados
    visitados = [nodo_inicial]
    nodo_actual = nodo_inicial
    
    while len(visitados) < len(df.columns):  # Cambiar la condición de parada
        # Obtener las probabilidades del nodo actual
        probabilidades = df_actual.loc[nodo_actual].copy()

        # Convertir las probabilidades a tipo float
        probabilidades = probabilidades.astype(float)
        
        # Eliminar las probabilidades de los nodos ya visitados
        probabilidades[visitados] = 0
        
        # Si todas las probabilidades son cero
        if probabilidades.sum() == 0:
            # Elegir un nodo no visitado arbitrariamente si no hay probabilidades disponibles
            nodos_restantes = [nodo for nodo in df.columns if nodo not in visitados]
            if nodos_restantes:
                siguiente_nodo = np.random.choice(nodos_restantes)
            else:
                break
        else:
            # Normalizar las probabilidades para que sumen 1
            probabilidades /= probabilidades.sum()
            
            # Escoger el siguiente nodo según las probabilidades
            siguiente_nodo = np.random.choice(probabilidades.index, p=probabilidades.values)
        
        # Añadir el siguiente nodo a la lista de visitados
        visitados.append(siguiente_nodo)
        
        # Actualizar las probabilidades del DataFrame, eliminando la fila y columna del nodo seleccionado
        df_actual[siguiente_nodo] = 0
        df_actual.loc[siguiente_nodo] = 0
        
        # Actualizar el nodo actual
        nodo_actual = siguiente_nodo
    
    # Convertir np.int64 a int normales
    visitados = [int(nodo) for nodo in visitados]

    return visitados

def reiniciarEstado():
    global maquinas, trabajos
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
def hormiga():
    global maqiunas,trabajos, tiempoProgramable, tiemposProgramablesAnteriores,Cmax, mejorMaquinas, listasInicialesMaquinas,alpha, beta, iteraciones, hormigas
    pruebaCmax=[]
    listaCaminos={}
    #iteraciones=100
    #hormigas=5
    posiblesInicios: List[Trabajo]=[]
    probabilidades: List[pd.DataFrame]=[]
    feromonaMaquinas: List[pd.DataFrame]=[]
    matricesFeromonas=pd.DataFrame
    feromonaInicial=1
    ordenProcesamientoMaquina=[]
    #alpha=3
    #beta=0.1
    tasaEvaporacion=0.01
    tasaAumento=5
    #Matriz feromona inicial
    reiniciarEstado()
    for maq in maquinas:
        posi=[]
        for trab in trabajos:
            if trab.estadoTrabajo==EstadoTrabajo.NO_INICIADO and trab.ordenProcesamiento[0]==maq.numeroMaquina:
                posi.append(trab)
            
        posiblesInicios.append(copy.deepcopy(posi))
    for s in range(len(maquinas)):
        indices=[]
        columnas=[]
        indices=[trab.numeroTrabajo for trab in posiblesInicios[s]]
        columnas=[trab.numeroTrabajo for trab in posiblesInicios[s]]
        indices.insert(0,0)
        columnas.insert(0,0)
        
        
        matricesFeromonas=pd.DataFrame(index=indices, columns=columnas)
        probabilidades.append(copy.deepcopy(matricesFeromonas))
        #print(matricesFeromonas)
        for fila in matricesFeromonas.index:
            for columna in matricesFeromonas.columns:
                
                if columna==fila:
                    matricesFeromonas.loc[fila,columna]=0
                else:
                    matricesFeromonas.loc[fila,columna]=feromonaInicial
        #print(matricesFeromonas)
        feromonaMaquinas.append(copy.deepcopy(matricesFeromonas))
    calcularProbs(probabilidades,feromonaMaquinas,alpha,beta)
    for i in range(iteraciones):
        listaCmax=[]
        menorCmaxHormiga=sys.maxsize
        listaEstadosMaqiunas=[]
        mejoresIniciales=[]
        for h in range(hormigas):
            reiniciarEstado()
            calcularProbs(probabilidades,feromonaMaquinas,alpha,beta)
            tiempoProgramable=0
            tiemposProgramablesAnteriores=[]
            listasInicialesMaquinas=[]
            for maq in range(len(maquinas)):
                
                camino=seleccionar_camino_con_ajuste(probabilidades[maq], nodo_inicial=0)
                print(camino)
                listasInicialesMaquinas.append(camino[1:])
                print(listasInicialesMaquinas)
                print("a")
            listaInicialesHormiga=copy.deepcopy(listasInicialesMaquinas)
            algoritmoInicialMod()
            Cmaxh=tiemposProgramablesAnteriores[-2]
            print(Cmaxh)
            #MAXIMO LOCAL
            if Cmaxh<menorCmaxHormiga:
                mejoresIniciales=copy.deepcopy(listaInicialesHormiga)
                menorCmaxHormiga=Cmaxh
            listaCmax.append(Cmaxh)
            listaEstadosMaqiunas.append(copy.deepcopy(maquinas))
            pruebaCmax.append(Cmaxh)
        #MAXIMO GLOABL
        if min(listaCmax)<=Cmax:
            #mejoresIniciales=copy.deepcopy(listaInicialesHormiga)
            
            Cmax=min(listaCmax)
            mejorMaquinas=copy.deepcopy(listaEstadosMaqiunas[listaCmax.index(min(listaCmax))])
        texto='\n'.join([' '.join(map(str, sublista))for sublista in mejoresIniciales])
        if  texto in listaCaminos:
            listaCaminos[texto]+=1
        else:
            listaCaminos[texto]=1
        actualizarFeromonas(feromonaMaquinas,mejoresIniciales,menorCmaxHormiga,tasaEvaporacion,tasaAumento)
        
    creacionGraficos(mejorMaquinas)
    graficoPrueba(pruebaCmax)
    print(mejoresIniciales)
    frecuencias_ordenadas = dict(sorted(listaCaminos.items(), key=lambda item: item[1], reverse=True))
    plt.bar(frecuencias_ordenadas.keys(), frecuencias_ordenadas.values())
    plt.title('Frecuencia caminos')
    plt.xlabel('camino')
    plt.ylabel('Frecuencia')
    plt.show()
    print(Cmax)
            
def actualizarFeromonas(feromonaMaquinas,mejoresIniciales,menorCmaxHormiga,tasaEvaporacion,tasaAumento):
    
    for  i in range(len(mejoresIniciales)):
        mejoresIniciales[i].insert(0,0)
    for i in range(len(feromonaMaquinas)):
        feromonaMaquinas[i] = feromonaMaquinas[i].applymap(lambda x: x * (1 - tasaEvaporacion) if x > 0 else x)
        print(feromonaMaquinas[i])
    
        for k in mejoresIniciales:
            if len(k)>1:
                for s in range(len(k)-1):
                    u, v = k[s], k[s+1]
                    if u in feromonaMaquinas[i].index and v in feromonaMaquinas[i].columns:
                        # Depósito de feromona proporcional a la calidad de la solución
                        feromonaMaquinas[i].at[u, v] += tasaAumento / menorCmaxHormiga
                        print(feromonaMaquinas[i])
                        print("a")
    
    
    
def ciclos(maquina: Maquina,trabajosProcesados):
    #if tiempoProgramable==353 or tiempoProgramable==520 or tiempoProgramable==122 or tiempoProgramable==106 or tiempoProgramable==158:
    #    input("A")
    
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
          
           
def asignarTrabajo_Maquina(numeroMaquinaAsignar, numeroTrabajoAsignar):
    global tiempoProgramable
    #if tiempoProgramable==353 or tiempoProgramable==520 or tiempoProgramable==122 or tiempoProgramable==106 or tiempoProgramable==158:
    #    input("A")
    
    
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
    
 

    
                   
def calcularTiempoProgramable():
    global tiempoProgramable, tiemposProgramablesAnteriores,maquinas, repite
    
    
    
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
        repite+=1
        tiempoProgramable=anterior+1
    if tiempoProgramable==None:
        repite+=1
        tiempoProgramable=anterior+1
    if repite>2:
        repite=0
        reiniciarEstado()
        tiempoProgramable=0
        tiemposProgramablesAnteriores=[]
        
    tiemposProgramablesAnteriores.append(tiempoProgramable)
    print(f"El Nuevo tiempo programable es: {tiempoProgramable}")
    print(f"Se añade a la lista de tiempos {tiemposProgramablesAnteriores}")
    
def calcularTiempoProgramableh(copiaMaquinasIniciales):
    global tiempoProgramable, tiemposProgramablesAnteriores,maquinas, repite,listasInicialesMaquinas
    
    
    
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
        repite+=1
        tiempoProgramable=anterior+1
    if repite>3:
        repite=0
        reiniciarEstado()
        tiempoProgramable=0
        tiemposProgramablesAnteriores=[]
        listasInicialesMaquinas=copy.deepcopy(copiaMaquinasIniciales)
        
    tiemposProgramablesAnteriores.append(tiempoProgramable)
    print(f"El Nuevo tiempo programable es: {tiempoProgramable}")
    print(f"Se añade a la lista de tiempos {tiemposProgramablesAnteriores}")
   
   
 
def actializarEstados():
    
    global tiempoProgramable, maquinas, trabajos
    
    #if tiempoProgramable==353 or tiempoProgramable==520 or tiempoProgramable==122 or tiempoProgramable==106 or tiempoProgramable==158:
        #input("pausa")
    for maquina in maquinas:
        if maquina.tiempoProgramable==tiempoProgramable and maquina.tiempoProgramable!=0:
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
    
    creacionGraficos(mejorMaquinas)
    hormiga()
    #G=crearGrafo()
    
    print("TERMINADO")
#main()

import tkinter as tk
from pandastable import Table

class MiAplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz de JobShop")
        self.geometry("1200x800")  # Aumentar el tamaño de la ventana

        # Estilos generales
        self.configure(bg="#f0f0f0")  # Color de fondo

        # Título centrado
        self.label_titulo = tk.Label(self, text="Sistema de JobShop", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.label_titulo.pack(pady=10)

        # Botón para importar datos
        self.boton_importar = tk.Button(self, text="Importar Datos", command=self.importar_datos, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.boton_importar.pack(pady=20)

        # Crear un frame que contiene ambos DataFrames con bordes
        self.frame_dataframes = tk.Frame(self, bg="#f0f0f0")
        self.frame_dataframes.pack(pady=10, expand=True, fill=tk.BOTH)

        # Título y frame para el primer DataFrame (Orden trabajos) con borde
        self.label_orden = tk.Label(self.frame_dataframes, text="Orden trabajos", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.label_orden.grid(row=0, column=0, padx=20, pady=5)
        self.frame_df1 = tk.Frame(self.frame_dataframes, bg="white", highlightbackground="black", highlightthickness=1)
        self.frame_df1.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Título y frame para el segundo DataFrame (Tiempos trabajos) con borde
        self.label_tiempos = tk.Label(self.frame_dataframes, text="Tiempos trabajos", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.label_tiempos.grid(row=0, column=1, padx=20, pady=5)
        self.frame_df2 = tk.Frame(self.frame_dataframes, bg="white", highlightbackground="black", highlightthickness=1)
        self.frame_df2.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        # Configuración para que los DataFrames se expandan correctamente
        self.frame_dataframes.grid_columnconfigure(0, weight=1)
        self.frame_dataframes.grid_columnconfigure(1, weight=1)
        self.frame_dataframes.grid_rowconfigure(1, weight=1)

        # Frame para las variables globales
        self.frame_variables = tk.Frame(self, bg="#f0f0f0")
        self.frame_variables.pack(pady=10)

        # Entradas para las variables globales
        self.label_alpha = tk.Label(self.frame_variables, text="Alpha:", font=("Arial", 12), bg="#f0f0f0")
        self.label_alpha.grid(row=0, column=0, padx=5, pady=5)
        self.entry_alpha = tk.Entry(self.frame_variables)
        self.entry_alpha.grid(row=0, column=1, padx=5, pady=5)

        self.label_beta = tk.Label(self.frame_variables, text="Beta:", font=("Arial", 12), bg="#f0f0f0")
        self.label_beta.grid(row=1, column=0, padx=5, pady=5)
        self.entry_beta = tk.Entry(self.frame_variables)
        self.entry_beta.grid(row=1, column=1, padx=5, pady=5)

        self.label_iteraciones = tk.Label(self.frame_variables, text="Iteraciones:", font=("Arial", 12), bg="#f0f0f0")
        self.label_iteraciones.grid(row=2, column=0, padx=5, pady=5)
        self.entry_iteraciones = tk.Entry(self.frame_variables)
        self.entry_iteraciones.grid(row=2, column=1, padx=5, pady=5)

        self.label_hormigas = tk.Label(self.frame_variables, text="Hormigas:", font=("Arial", 12), bg="#f0f0f0")
        self.label_hormigas.grid(row=3, column=0, padx=5, pady=5)
        self.entry_hormigas = tk.Entry(self.frame_variables)
        self.entry_hormigas.grid(row=3, column=1, padx=5, pady=5)

        # Botón para calcular (colocado debajo de los DataFrames)
        self.boton_calcular = tk.Button(self, text="Empezar Calcular", command=self.calcular, font=("Arial", 12), bg="#FF5722", fg="white", padx=10, pady=5)
        self.boton_calcular.pack(pady=20)

        # Etiqueta para mostrar el resultado de Cmax
        self.label_cmax = tk.Label(self, text="Cmax: --", font=("Arial", 14), bg="#f0f0f0")
        self.label_cmax.pack(pady=10)

        self.df1 = None
        self.df2 = None

    def importar_datos(self):
        # Llama a la función importar para cargar los datos
        importar()

        # Asignar los DataFrames globales a los atributos de la clase
        self.df1 = ordenMaquinas
        self.df2 = tiemposMaquinas

        # Mostrar los DataFrames en los frames correspondientes
        self.mostrar_dataframe(self.df1, self.frame_df1)
        self.mostrar_dataframe(self.df2, self.frame_df2)

    def mostrar_dataframe(self, dataframe, frame):
        # Destruye el contenido anterior del frame si lo hay
        for widget in frame.winfo_children():
            widget.destroy()

        # Muestra el DataFrame con pandastable
        table = Table(frame, dataframe=dataframe)
        table.show()

    def calcular(self):
        # Validar si los campos de entrada están completos
        if not self.entry_alpha.get() or not self.entry_beta.get() or not self.entry_iteraciones.get() or not self.entry_hormigas.get():
            print("Por favor, rellene todos los campos de variables (alpha, beta, iteraciones, hormigas).")
            return

        # Convertir las entradas a valores numéricos
        try:
            global alpha, beta, iteraciones, hormigas
            alpha = float(self.entry_alpha.get())
            beta = float(self.entry_beta.get())
            iteraciones = int(self.entry_iteraciones.get())
            hormigas = int(self.entry_hormigas.get())
        except ValueError:
            print("Por favor, ingrese valores numéricos válidos.")
            return

        if self.df1 is not None and self.df2 is not None:
            print("Realizando cálculos...")

            global Cmax, mejorMaquinas
            crearListas()
            algoritmoInicial()

            # Realizamos el cálculo principal
            Cmax = tiemposProgramablesAnteriores[-2]
            print(f"Cmax encontrado {Cmax}")
            mejorMaquinas = copy.deepcopy(maquinas)

            # Se crea el gráfico y ejecuta el resto del algoritmo
            creacionGraficos(mejorMaquinas)
            hormiga()

            # Actualizamos la etiqueta con el valor de Cmax
            self.label_cmax.config(text=f"Cmax encontrado: {Cmax}")
            print("TERMINADO")

        else:
            print("Por favor, importa los datos primero.")

if __name__ == "__main__":
    app = MiAplicacion()
    app.mainloop()