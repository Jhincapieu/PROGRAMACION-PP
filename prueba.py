from enum import Enum
from typing import List

class EstadoTrabajo(Enum):
    NO_INICIADO = 1
    PROCESANDO = 2
    PROCESADO = 3
    TERMINADO = 4

class EstadoMaquina(Enum):
    LIBRE = 1
    OCUPADA = 2
    BLOQUEO = 3

class Trabajo:
    def _init_(self, numeroTrabajo, maquinaActual, estadoTrabajo: EstadoTrabajo, ordenProcesamiento: List[int], tiemposProcesamiento: List[int]) -> None:
        self.numeroTrabajo = numeroTrabajo
        self.maquinaActual = maquinaActual
        self.estadoTrabajo = estadoTrabajo
        self.ordenProcesamiento = ordenProcesamiento
        self.tiemposProcesamiento = tiemposProcesamiento
        self.tiemposProcesamientoGuardados = tiemposProcesamiento.copy()
        self.ordenProcesamientoGuardados = ordenProcesamiento.copy()

class Maquina:
    def _init_(self, numeroMaquina, estadoMaquina: EstadoMaquina, trabajoActual: int = None) -> None:
        self.numeroMaquina = numeroMaquina
        self.estadoMaquina = estadoMaquina
        self.trabajoActual = trabajoActual

def asignarTrabajo_MaquinaBloq(maquina1, trabajo1, maquina2, trabajo2):
    # Implementa la lógica para intercambiar trabajos entre máquinas bloqueadas.
    # Ejemplo básico:
    maquinas[maquina1 - 1].trabajoActual = trabajo2
    maquinas[maquina2 - 1].trabajoActual = trabajo1
    print(f"Intercambio realizado entre Maquina {maquina1} y Maquina {maquina2}")

# Detección y manejo de ciclos
def detectar_ciclo(maquinas, trabajos):
    visitado = set()
    stack = set()

    def dfs(maquina):
        if maquina in stack:  # Ciclo detectado
            return [maquina]
        if maquina in visitado:
            return None
        
        visitado.add(maquina)
        stack.add(maquina)

        trabajo = trabajos[maquina.trabajoActual - 1]
        if trabajo.ordenProcesamiento:
            siguiente_maquina = trabajo.ordenProcesamiento[0] - 1
            if maquinas[siguiente_maquina].estadoMaquina == EstadoMaquina.BLOQUEO:
                ciclo = dfs(maquinas[siguiente_maquina])
                if ciclo:
                    ciclo.append(maquina)
                    return ciclo

        stack.remove(maquina)
        return None

    for maquina in maquinas:
        if maquina.estadoMaquina == EstadoMaquina.BLOQUEO:
            ciclo = dfs(maquina)
            if ciclo:
                ciclo.reverse()  # Opcional: Para empezar desde el origen
                return ciclo
    return None

# Ejemplo de uso con una lista de maquinas y trabajos
maquinas = [
    Maquina(1, EstadoMaquina.BLOQUEO, 1),
    Maquina(2, EstadoMaquina.BLOQUEO, 2),
    Maquina(3, EstadoMaquina.BLOQUEO, 3),
]

trabajos = [
    Trabajo(1, 1, EstadoTrabajo.PROCESANDO, [2], [10]),
    Trabajo(2, 2, EstadoTrabajo.PROCESANDO, [3], [20]),
    Trabajo(3, 3, EstadoTrabajo.PROCESANDO, [1], [30]),
]

ciclo = detectar_ciclo(maquinas, trabajos)
if ciclo:
    print(f"Ciclo detectado: {[maquina.numeroMaquina for maquina in ciclo]}")
    for i in range(len(ciclo)):
        maquina1 = ciclo[i].numeroMaquina
        maquina2 = ciclo[(i + 1) % len(ciclo)].numeroMaquina
        trabajo1 = maquinas[maquina1 - 1].trabajoActual
        trabajo2 = maquinas[maquina2 - 1].trabajoActual
        asignarTrabajo_MaquinaBloq(maquina1, trabajo1, maquina2, trabajo2)