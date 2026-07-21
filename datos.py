import kagglehub # C01: Kaggle
from pathlib import Path # 03: Pathlib
import pandas as pd # 04: Pandas

# Descarga del dataset a kagglehub
path = Path(
    kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
)

csv_file = next(path.glob("*.csv"))

# Obtener los ficheros csv
print(csv_file)

# Guardar el fichero CSV en una variabla para su manejo (aquí ya se manejaría con pandas "pd")
df = pd.read_csv(csv_file)

print(f"- Total de datos: {len(df)}")
print(f"- Total de columnas: {len(df.columns)}")
print(f"- Info de columnas: ")
print(f" {df.info()}")
print(f"- Hay NULLS en el dataset: {df.isnull().values.any()}")
print(f"- Porcentaje de NULLS por columna{df.isnull().mean() * 100}")
# print(df["track_genre"].value_counts())
# Cuantos generos existen
#print(df["track_genre"].nunique())

# Que generos existen:
#print(df["artists"].unique())

# cuantas filas por genero hay
#print(df["track_genre"].value_counts())
#print(df.nlargest(20, 'popularity')[["artists", "track_name", "popularity"]])

# 1. Obtiene el top de popularidad
top_df = df.nlargest(200, 'popularity')

# 2. Quita duplicados basados en una columna (ej. 'nombre') dejando el primero
resultado = top_df.drop_duplicates(subset=['track_name', 'artists'], keep='first')

print("- Canciones más populares")
print(resultado.nlargest(10, 'popularity')[["artists", "track_name", "popularity", "danceability", "valence"]])
print("")

bottom_df = df.nsmallest(200, 'popularity')
resultado_df = bottom_df.drop_duplicates(subset=['track_name', 'artists'], keep='first')
print("- Canciones menos populares")
print(resultado_df.nsmallest(10, 'popularity')[["artists", "track_name", "popularity", "danceability", "valence"]])
