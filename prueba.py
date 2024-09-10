import numpy as np

# Crear un valor de tipo np.str_
valor_np_str = np.str_('Trabajo 1 en Maquina 2')

# Convertir np.str_ a cadena de texto estándar de Python
valor_str = str(valor_np_str)

# Verificar el resultado
print("Tipo del valor convertido:", type(valor_str))
print("Valor convertido:", valor_str)
