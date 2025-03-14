import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Configuración de la API
API_KEY = "BR2vTX6TUpfDnMoGShdhRcsgxxXYb3GiRnDNFhX3"
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

# Función para obtener datos de asteroides
def get_asteroid_data(start_date, end_date):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Fechas para la consulta
start_date = "2023-01-01"
end_date = "2023-01-07"

# Obtener datos
asteroid_data = get_asteroid_data(start_date, end_date)

# Crear lista para almacenar datos procesados
processed_data = []

# Procesar datos
for date in asteroid_data['near_earth_objects']:
    for asteroid in asteroid_data['near_earth_objects'][date]:
        processed_data.append({
            'id': asteroid['id'],
            'name': asteroid['name'],
            'date': date,
            'diameter_min': asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
            'diameter_max': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
            'hazardous': asteroid['is_potentially_hazardous_asteroid'],
            'close_approach_distance': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
            'relative_velocity': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
        })

# Crear DataFrame
df = pd.DataFrame(processed_data)

# Mostrar primeras filas
print("Primeras filas del DataFrame:")
print(df.head())

# Estadísticas básicas
print("\nEstadísticas básicas:")
print(df.describe())

# Gráfico de dispersión: Diámetro vs Distancia de aproximación
fig = px.scatter(df, 
                 x='diameter_max', 
                 y='close_approach_distance',
                 color='hazardous',
                 title='Diámetro vs Distancia de aproximación',
                 labels={'diameter_max': 'Diámetro máximo (km)',
                        'close_approach_distance': 'Distancia de aproximación (km)',
                        'hazardous': 'Potencialmente peligroso'})
fig.show()

# Histograma de velocidades relativas
fig2 = px.histogram(df, 
                   x='relative_velocity',
                   title='Distribución de velocidades relativas',
                   labels={'relative_velocity': 'Velocidad relativa (km/h)'})
fig2.show()

# Cantidad de asteroides por día
asteroids_per_day = df['date'].value_counts().sort_index()
fig3 = px.bar(x=asteroids_per_day.index, 
              y=asteroids_per_day.values,
              title='Cantidad de asteroides por día',
              labels={'x': 'Fecha', 'y': 'Número de asteroides'})
fig3.show()

# Proporción de asteroides peligrosos vs no peligrosos
hazardous_count = df['hazardous'].value_counts()
fig4 = px.pie(values=hazardous_count.values,
              names=hazardous_count.index,
              title='Proporción de asteroides peligrosos vs no peligrosos')
fig4.show()
