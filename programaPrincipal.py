import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
from Maquina import Maquina,EstadoMaquina
from Trabajo import Trabajo,EstadoTrabajo
from typing import List
import random

ordenMaquinas=pd.DataFrame
tiemposMaquinas=pd.DataFrame
maquinas: List[Maquina]=[]
trabajos: List[Trabajo]=[]
tiempoProgramable=0
tiemposProgramablesAnteriores=[]
ordenIteracion: List[Maquina]=[]
trabajosProcesados: List[Trabajo]=[]
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

















def algoritmoInicial():
    global maquinas, trabajos, tiempoProgramable
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
        
        print("--------------------INICIANDO ITERACION--------------------")
        

        
        #Iteramos por cada Maquina
        #Buscamos el orden de Iteración de las máquinas, Se pone de ultimo los que tengan tiempo programable
        ordenIteracion=sorted(maquinas, key=lambda m: m.tiempoProgramable,reverse=True)
        trabajosProcesados: List[Trabajo]=[]
        maquinasBloqueadas: List[Maquina]=[]
        #Buscamos los trabajos en estado Procesado que son los que bloquean las máquinas
        for trabajo in trabajos:
            if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO:
                trabajosProcesados.append(trabajo)
        for maquina in maquinas:
            if maquina.estadoMaquina==EstadoMaquina.BLOQUEO:
                maquinasBloqueadas.append(maquina)
        for maquina in ordenIteracion:
            trabajosParaMaquina: List[Trabajo]=[]
            print(f"------------------------------ Revisando Maquina {maquina.numeroMaquina} ------------------------------")
            #Caso en que esté bloqueada la maquina
            print(f"El estado de la máquina es: {maquina.estadoMaquina.name}")
            for elemento in trabajos:
                if elemento.ordenProcesamiento:
                    if elemento.ordenProcesamiento[0]==maquina.numeroMaquina and elemento.estadoTrabajo==EstadoTrabajo.NO_INICIADO:
                        trabajosParaMaquina.append(elemento)
            print(f"Los trabajos que no han empezado y vinen para esta máquina son y no han empezado:")
            
            
            for elemento in trabajosParaMaquina:
                print(elemento.numeroTrabajo)
                
                
            if maquina.estadoMaquina==EstadoMaquina.BLOQUEO:
                for trabajo in trabajosProcesados:
                    #Caso de intercambio
                    if trabajo.ordenProcesamiento[0]==maquina.numeroMaquina:
                        
                        if trabajos[maquina.trabajoActual-1].ordenProcesamiento[0]==trabajo.maquinaActual:
                            maquina1=maquina.numeroMaquina
                            maquina2=trabajo.maquinaActual
                            trabajo1=maquina.trabajoActual
                            trabajo2=trabajo.numeroTrabajo
                            print(f"Caso intercambio entre maquinas {maquina1} y {maquina2}")
                            asignarTrabajo_MaquinaBloq(maquina1,trabajo1,maquina2,trabajo2)
                            
                            break
                    #Caso no intercambio
                    elif trabajo.ordenProcesamiento[0]==maquina.numeroMaquina:
                        print("Caso no intercambio maquina {maquina.numeroMaquina} trabajo {trabajo.numeroTrabajo}")
                        asignarTrabajo_Maquina(maquina.numeroMaquina,trabajo.numeroTrabajo)
                        break
                    
                    
            #Caso no bloqueo
            if maquina.estadoMaquina==EstadoMaquina.LIBRE:
                for trabajo in trabajos:
                    if trabajo.estadoTrabajo==EstadoTrabajo.PROCESADO and trabajo.ordenProcesamiento[0]==maquina.numeroMaquina:
                        maquina1=maquina.numeroMaquina
                        trabajo1=trabajo.numeroTrabajo
                        print(f"Caso no bloqueo mauina {maquina1} trabajo {trabajo1}")

                        asignarTrabajo_Maquina(maquina1,trabajo1)
                        break
                    elif trabajosParaMaquina:
                        print("Caso no hay trabajos procesados, vamos con los no iniciados")
                        #Generamos un numero entre 0 y 1
                        r=random.random()
                        if r<=0.8:
                            #Cogemos un trabajo
                            trab=random.choice(trabajosParaMaquina)
                            maquina1=maquina
                            print(f"Se asignó a la máquina {maquina1.numeroMaquina} el trabajo {trab.numeroTrabajo}")
                            asignarTrabajo_Maquina(maquina1.numeroMaquina,trab.numeroTrabajo)
                            break
            else:
                print("-----------------------------------------------ERROR--------------------------------------------")
                input("Presione una tecla para continuar")
        actializarEstados()
        calcularTiempoProgramable()
        

        #Al final verificamos si sigue pendiente algun trabajo
        contadorPendientes=0
        for trabajo in trabajos:
            if trabajo.estadoTrabajo != EstadoTrabajo.TERMINADO:
                contadorPendientes+=1
        if contadorPendientes==0:
            pendiente=False
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
            
def asignarTrabajo_Maquina(numeroMaquinaAsignar, numeroTrabajoAsignar):
    global tiempoProgramable
    print("ENTRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    
    #----------------------------Maquina nueva----------------------------
    lista=[]
    #estado
    maquinas[numeroMaquinaAsignar-1].estadoMaquina=EstadoMaquina.OCUPADO
    #nuevo tiempo programable
    tprog=maquinas[numeroMaquinaAsignar-1].tiempoProgramable+trabajos[numeroTrabajoAsignar-1].tiemposProcesamiento[0]
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
    maquinas[numeroMaquinaAsignar1-1].estadoMaquina=EstadoMaquina.OCUPADO
    maquinas[numeroMaquinaAsignar2-1].estadoMaquina=EstadoMaquina.OCUPADO
    #nuevo tiempo programable
    tprog1=maquinas[numeroMaquinaAsignar1-1].tiempoProgramable+trabajos[numeroTrabajoAsignar2-1].tiemposProcesamiento[0]
    tprog2=maquinas[numeroMaquinaAsignar2-1].tiempoProgramable+trabajos[numeroTrabajoAsignar1-1].tiemposProcesamiento[0]
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
    
    menortp=None
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
    
    print("Actualizando el estado del sistema")
    print("----------MAQUINAS----------")
    for i in range(len(maquinas)):
        print(maquinas[i])
    print("-------------------")
    print("----------TRABAJOS----------")
    for i in range(len(trabajos)):
        print(trabajos[i])
    print("-------------------")
    for maquina in maquinas:
        if maquina.tiempoProgramable==tiempoProgramable and maquina.tiempoProgramable!=0:
            if not trabajos[maquina.trabajoActual-1].ordenProcesamiento:
                trabajos[maquina.trabajoActual-1].estadoTrabajo=EstadoTrabajo.TERMINADO
                maquinas[maquina.numeroMaquina-1].estadoMaquina=EstadoMaquina.LIBRE
            else:
                maquinas[maquina.numeroMaquina-1].estadoMaquina=EstadoMaquina.BLOQUEO
                trabajos[maquina.trabajoActual-1].estadoTrabajo=EstadoTrabajo.PROCESADO
            
    
    


def main():
    importar()
    crearListas()
    algoritmoInicial()
    print("TERMINADO")
    
main()