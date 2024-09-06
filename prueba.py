import matplotlib.pyplot as plt
import pandas as pd

# Datos de ejemplo con valores numéricos
df = pd.DataFrame([
    dict(Task="Job A", Start=0, Finish=30, Resource="Alex"),
    dict(Task="Job B", Start=40, Finish=50, Resource="Alex"),
    dict(Task="Job C", Start=20, Finish=40, Resource="Max")
])

# Crear una figura y un eje
fig, ax = plt.subplots(figsize=(10, 6))

# Añadir las barras para cada tarea
for index, row in df.iterrows():
    ax.barh(row['Resource'], row['Finish'] - row['Start'], left=row['Start'], height=0.4, label=row['Task'])

# Añadir etiquetas y título
ax.set_xlabel('Tiempo')
ax.set_title('Gráfico de Gantt con Matplotlib')
ax.set_xlim(0, df['Finish'].max() + 10)  # Ajustar el límite del eje X
ax.legend(title='Tarea')

# Mostrar el gráfico
plt.show()
print(df)