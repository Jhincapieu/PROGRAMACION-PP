import networkx as nx
import matplotlib.pyplot as plt


# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos (representando trabajos y máquinas)
G.add_node("T1-O1-M1")  # Trabajo 1, Operación 1, Máquina 1
G.add_node("T1-O2-M2")  # Trabajo 1, Operación 2, Máquina 2
G.add_node("T2-O1-M3")  # Trabajo 2, Operación 1, Máquina 3
G.add_node("T2-O2-M1")  # Trabajo 2, Operación 2, Máquina 1

# Añadir aristas con pesos que representan tiempos de procesamiento
# (Trabajo, Operacion, Maquina) -> siguiente paso
G.add_edge("T1-O1-M1", "T1-O2-M2", weight=5)
G.add_edge("T1-O2-M2", "T2-O1-M3", weight=8)  # Con tiempo de bloqueo
G.add_edge("T2-O1-M3", "T2-O2-M1", weight=3)

# Opcional: mostrar los pesos (tiempos) en las aristas
pos = nx.spring_layout(G)  # Layout para una mejor visualización
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)

# Dibujar los pesos (tiempos de procesamiento o bloqueo) en las aristas
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Mostrar el grafo
plt.title("Grafo de Job Shop con Bloqueo")
plt.show()