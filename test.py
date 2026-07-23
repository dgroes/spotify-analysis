import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from pathlib import Path
import pandas as pd
from utils import *

limite_minutos = 40
limite_ms = limite_minutos * 60000

# Descarga del dataset a kagglehub
path = Path(
    kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
)

csv_file = next(path.glob("*.csv"))

# Guardar el fichero CSV en una variable para su manejo
df = pd.read_csv(csv_file)

# Eliminación de canciones repetidas y filtrado de duración máxima
data_normal = df.drop_duplicates(subset=['track_name', 'artists'], keep='first')
data = data_normal[data_normal['duration_ms'] <= limite_ms].copy() # .copy() evita advertencias de Pandas

# --- ANÁLISIS EN TERMINAL ---
print(f"\n{PINK}¿Las canciones más bailables suelen ser más populares?{RESET}")

# Calcular la correlación entre bailabilidad y popularidad
correlacion = data['danceability'].corr(data['popularity'])

# Mostrar coeficiente formateado a 2 decimales
print(f"Coeficiente de correlación: {correlacion:.2f}")

# Interpretación estadística adaptada a 'danceability'
if correlacion > 0.3:
    print("R: Sí, las canciones más bailables tienden a ser más populares")
elif correlacion < -0.3:
    print("R: No, de hecho, las canciones menos bailables son las más populares")
else:
    print("R: La bailabilidad no influye de forma directa en la popularidad de la canción")

# --- GENERACIÓN DEL GRÁFICO ---
# Configurar el estilo y crear el gráfico de dispersión con línea de tendencia
plt.figure(figsize=(10, 6))
sns.regplot(
    data=data, 
    x='danceability',         # Cambiado a danceability
    y='popularity', 
    scatter_kws={'alpha': 0.3, 'color': 'gray'}, 
    line_kws={'color': 'red', 'linewidth': 2}
)

# Personalización del gráfico con los nuevos títulos y etiquetas
plt.title('¿Las canciones más bailables son más populares?')
plt.xlabel('Bailabilidad (Danceability 0.0 - 1.0)')
plt.ylabel('Popularidad (0-100)')
plt.grid(True, alpha=0.3)

# Mostrar el gráfico en pantalla
plt.show()
