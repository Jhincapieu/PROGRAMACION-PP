import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
datosGeneral=pd.DataFrame
def importar():
    
    archivo=fd.askopenfilename()
    datos=pd.read_csv(archivo)
    
    print(archivo)
    return datos
datosGeneral=importar()    