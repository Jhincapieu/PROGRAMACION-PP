import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Matrices de orden de máquinas y tiempos de procesamiento
ordenMaquinas = pd.DataFrame([
    [2, 1, 3],
    [3, 2, 1],
    [2, 3, 1]
])

tiemposProcesamiento = pd.DataFrame([
    [5, 6, 1],
    [4, 3, 6],
    [2, 3, 2]
])

# Parámetros ACO
FEROMONA_INICIAL = 1.0  # Valor inicial de feromona en todas las aristas
EVAPORACION = 0.1       # Tasa de evaporación de la feromona
DEPOSITO_FEROMONA = 1.0 # Cantidad de feromona depositada por las hormigas

def crearGrafo():
    # Crear un grafo dirigido
    G = nx.DiGraph()

    # Agregar un nodo inicial que conecte a todos los primeros trabajos
    nodo_inicial = "Nodo Inicial"
    G.add_node(nodo_inicial)

    # Crear las conexiones dentro de cada trabajo respetando la precedencia (aristas dirigidas)
    for i in range(ordenMaquinas.shape[0]):  # Iterar sobre los trabajos
        trabajo = f"Trabajo {i+1}"
        maquina_primera = ordenMaquinas.iloc[i, 0]  # Obtener la primera máquina de cada trabajo
        estado_primero = f"{trabajo} en Maquina {maquina_primera}"
        
        # Conectar el nodo inicial al primer estado de cada trabajo
        G.add_edge(nodo_inicial, estado_primero, pheromone=FEROMONA_INICIAL)

        for j in range(ordenMaquinas.shape[1] - 1):  # Iterar sobre las máquinas en el orden dado
            maquina_actual = ordenMaquinas.iloc[i, j]
            maquina_siguiente = ordenMaquinas.iloc[i, j+1]
            
            estado_actual = f"{trabajo} en Maquina {maquina_actual}"
            estado_siguiente = f"{trabajo} en Maquina {maquina_siguiente}"
            
            # Agregar una arista dirigida del estado actual al estado siguiente
            G.add_edge(estado_actual, estado_siguiente, pheromone=FEROMONA_INICIAL)

    # Conectar trabajos diferentes, permitiendo que las hormigas exploren otras rutas
    for i in range(ordenMaquinas.shape[0]):
        for j in range(ordenMaquinas.shape[1]):
            trabajo_origen = f"Trabajo {i+1} en Maquina {ordenMaquinas.iloc[i, j]}"
            for k in range(ordenMaquinas.shape[0]):
                if i != k:  # Evitar conexión dentro del mismo trabajo
                    trabajo_destino = f"Trabajo {k+1} en Maquina {ordenMaquinas.iloc[k, 0]}"  # Conexión al primer estado de otro trabajo
                    G.add_edge(trabajo_origen, trabajo_destino, pheromone=FEROMONA_INICIAL)

    return G

# Función para actualizar las feromonas en el grafo
def actualizarFeromonas(G, caminos_hormigas):
    # Evaporación de feromonas
    for u, v, data in G.edges(data=True):
        data['pheromone'] *= (1 - EVAPORACION)
    
    # Depósito de feromonas basado en los caminos de las hormigas
    for camino in caminos_hormigas:
        for u, v in zip(camino[:-1], camino[1:]):  # Recorrer pares consecutivos del camino
            if G.has_edge(u, v):
                G[u][v]['pheromone'] += DEPOSITO_FEROMONA

# Dibujar el grafo con las feromonas representadas
def dibujarGrafo(G):
    pos = nx.spring_layout(G)  # Layout del grafo
    feromonas = nx.get_edge_attributes(G, 'pheromone')
    
    # Dibujar nodos y aristas
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=8, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=feromonas)
    
    plt.show()

# Ejemplo de ejecución
G = crearGrafo()
dibujarGrafo(G)

# Simulación de caminos de hormigas (ejemplo de 2 caminos)
caminos_hormigas = [
    ["Trabajo 1 en Maquina 2", "Trabajo 1 en Maquina 1", "Trabajo 2 en Maquina 3"],
    ["Trabajo 3 en Maquina 2", "Trabajo 3 en Maquina 3", "Trabajo 1 en Maquina 1"]
]

# Actualizar feromonas en función de los caminos de las hormigas
actualizarFeromonas(G, caminos_hormigas)
dibujarGrafo(G)
