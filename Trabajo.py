from enum import Enum
from typing import List

class EstadoTrabajo(Enum):
    NO_INICIADO=1
    PROCESANDO=2
    PROCESADO=3
    TERMINADO=4

class Trabajo:
    
    
    def __init__(self,numeroTrabajo, maquinaActual,estadoTrabajo: EstadoTrabajo,ordenProcesamiento: List[int] ,tiemposProcesamiento: List[int]) -> None:
        self.numeroTrabajo=numeroTrabajo
        self.maquinaActual=maquinaActual
        self.estadoTrabajo=estadoTrabajo
        self.ordenProcesamiento=ordenProcesamiento
        self.tiemposProcesamiento=tiemposProcesamiento
        self.tiemposProcesamientoGuardados=tiemposProcesamiento.copy()
        self.ordenProcesamientoGuardados=ordenProcesamiento.copy()
    
    def __str__(self) -> str:
        
        return f"Trabajo {self.numeroTrabajo} - Maquina Actual: {self.maquinaActual} - Estado: {self.estadoTrabajo} - Maquinas restantes: {self.ordenProcesamiento} - Tiempos maquinas restsantes: {self.tiemposProcesamiento}"