import kagglehub # C01: Kaggle
from pathlib import Path # 03: Pathlib
import pandas as pd # 04: Pandas
import math
from utils import *


# Descarga del dataset a kagglehub
path = Path(
    kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
)

csv_file = next(path.glob("*.csv"))

# Obtener los ficheros csv
# print(csv_file)

# Guardar el fichero CSV en una variabla para su manejo (aquí ya se manejaría con pandas "pd")
df = pd.read_csv(csv_file)

# Eliminación de canciones repetidas
data = df.drop_duplicates(subset=['track_name', 'artists'], keep='first')




print(f"{GREEN_B}SPOTIFY ANALYSIS{RESET} ✨")
print(f"{YELLOW_BI}Spotify Tracks Dataset posee datos del año 2022 👈{RESET}")
print(f"{YELLOW_I}Canciones analisadas:{RESET} {YELLOW_B}{len(data)}{RESET} \n")


# 1 ------------
# ¿Qué género tiene la mayor popularidad promedio?
print(f"{PINK}¿Qué género tiene la mayor popularidad promedio?{RESET}")
most_popular_genre = data.groupby('track_genre')['popularity'].mean()
# print(f"{most_popular_genre.nlargest(10)}")

contador = 1
for genero, promedio in most_popular_genre.nlargest(5).items():
    print(f"{contador}. {genero}: {promedio:.2f}")
    contador += 1

# 2 ------------
# ¿Las canciones explícitas son, en promedio, más populares?
print(f"\n{PINK}¿Las canciones explícitas son, en promedio, más populares?{RESET}")

# Explicitas
explicit = data[data['explicit'] == True]
average_explicit = explicit['popularity'].mean()

# No explicitas
no_explicit = data[data['explicit'] == False]
average_no_explicit = no_explicit['popularity'].mean()

print(f"- Popularidad de canciones explicitas: {math.trunc(average_explicit * 100)  / 100}%")
print(f"- Popularidad de canciones no explicitas: {math.trunc(average_no_explicit * 100)  / 100}%")


# 3 ------------
#¿Las canciones más largas suelen ser más populares?

# LIMIAR DURACIÓN MÁXIMA
# Hay canciones que tienen una duración de más de 10 minutos, superior a esto se consideraran datos "atipicos"

limit_minute = 10
limit_ms = limit_minute * 60000

# C05: Coeficiente de Correlación de Pearson
print(f"\n{PINK}¿Las canciones más largas suelen ser más populares?{RESET}")

# Calcular la correlación entre las 2  columnas
data_duration_limit = data[data['duration_ms'] <= limit_ms]
correlacion = data_duration_limit['duration_ms'].corr(data['popularity'])

# Con formato :.2f: Redondea y corta a 2 decimales (formatear números flotantes (con decimales) y controlar cuántos decimales)
print(f"Coeficiente de correlación: {correlacion:.2f}")

# C06: Correlación moderada
if correlacion > 0.3:
    print("R: Sí, las canciones más largas tienden a ser más populares")
elif correlacion < -0.3:
    print("R: No, de hecho, las canciones más cortas son las más populares")
else:
    print("R: La duración no influye en la popularidad de la cación")



# 4 ------------    
# ¿Qué artistas tienen el mayor promedio de popularidad?
print(f"\n{PINK}¿Qué artistas tienen el mayor promedio de popularidad?{RESET}")
print(f"{YELLOW_I}No tiene en cuenta las colaboraciones, solo canciones de artista individuales{RESET}")

# Quitar los artistas como colaboraciones (ejemp: Sam Smith;Kim Petras // Bizarrap;Quevedo // etc)
# ~: operador de negación lógica en Pandas
individual = data[~data['artists'].str.contains(';', na=False)]

popular_artists = individual.groupby('artists')['popularity'].mean()

contador = 1
for artista, promedio in popular_artists.nlargest(5).items():
    print(f"{contador}. {artista}: {promedio:.2f}")
    contador += 1




# 5 ------------  
# ¿Existe relación entre danceability y popularity?
print(f"\n{PINK}¿Existe relación entre {RESET}{PINK_B}danceability{RESET} {PINK}y{RESET} {PINK_B}popularity{RESET}{PINK}?{RESET}")
relation = data['danceability'].corr(data['popularity'])

print(f"Coeficiente de correlación: {relation:.2f}")

# C06: Correlación moderada
if relation > 0.3:
    print("R: Sí, las canciones con más 'danceability' tienden a ser más populares")
elif relation < -0.3:
    print("R: No, de hecho, las canciones con menos 'danceability' son las más populares")
else:
    print("R: La 'danceability' no influye en la popularidad de la cación")



# 6 ------------  
# ¿Los géneros con mayor energy también tienen mayor tempo?
print(f"\n{PINK}¿Los géneros con mayor energy también tienen mayor tempo?{RESET}")