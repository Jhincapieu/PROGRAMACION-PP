from enum import Enum

class EstadoMaquina(Enum):
    LIBRE = 1
    OCUPADO = 2
    BLOQUEO= 3

class Maquina:
    
    tiempoProgramable=0
    tiemposTrabajos=[] #la idea es que sean los elementos sean listas [NumeroTrabajo,tiempoInicio,tiempoFin]
     
    
    
    def __init__(self,numeroMaquina,trabajoActual,estadoMaquina: EstadoMaquina,):
        self.numeroMaquina= numeroMaquina
        self.trabajoActual=trabajoActual
        self.estadoMaquina=estadoMaquina
        
    def __str__(self) -> str:
        return f"Maquina {self.numeroMaquina} - Trabajo actual: {self.trabajoActual} - Estado Maquina: {self.estadoMaquina} - Tiempo programable: {self.tiempoProgramable}"    
    