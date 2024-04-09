import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from PIL import Image  # Importa la clase Image desde el módulo PIL
import json

# Abre el archivo GeoJSON
with open('Mapa de Accidentalidad Vial Municipio de Medellín 2016.geojson', "r") as read_file:
    data = json.load(read_file)

# Título de la aplicación
st.title("Accidentalidad Municipio de Medellín 2016")

# Introducción
st.write('Se entiende por accidente de tránsito evento, generalmente involuntario, generado al menos por un vehículo en movimiento, que causa daños a '
         'personas y bienes involucrados en él, e igualmente afecta la normal circulación de los vehículos que se movilizan por la vía o vías comprendidas en el ' 
         'lugar o dentro de la zona de influencia del hecho0 (Ley 769 de 2002 - Código Nacional de Tránsito)')
st.subheader('Sistema de consulta de Accidentalidad municipio de Medellín')

# Carga de imagen
image = Image.open('AccV.jpeg')
st.image(image, caption="Accidentes viales")

# Listas para almacenar los datos
La = []
Lo = []
day = []
hour = []
neig = []
dir = []

# Decodificación del archivo en formato JSON
for feature in data['features']:
    coordinates = feature['geometry']['coordinates']
    dia = feature['properties']['dia']
    Hora = feature['properties']['hora']
    barrio = feature['properties']['barrio']
    direccion = feature['properties']['direccion']
    La.append(coordinates[1])
    Lo.append(coordinates[0])
    day.append(dia)
    hour.append(Hora)
    neig.append(barrio)
    dir.append(direccion)

# Slider para seleccionar el número de registros de accidentes a visualizar
nm = st.slider('Selecciona el número de registros de accidentes que deseas visualizar', 5, 30000)

# Construir el DataFrame con los datos obtenidos
dfLa = pd.DataFrame({'lat': La[0:nm]})
dfLo = pd.DataFrame({'lon': Lo[0:nm]})
dfdia = pd.DataFrame({'día': day[0:nm]})
dfhor = pd.DataFrame({'Hora': hour[0:nm]})
dfbarr = pd.DataFrame({'Barrio': neig[0:nm]})
dfdir = pd.DataFrame({'Dirección': dir[0:nm]})
df_g = pd.concat([dfLa, dfLo, dfdia, dfhor, dfdir, dfbarr], axis=1)

# Mostrar la tabla de datos
st.dataframe(df_g)

# Dibujar el mapa utilizando las columnas 'lat' y 'lon'
st.map(df_g)

# Realizar un filtrado de los datos por día y hora
st.subheader('Filtrado por Día y Hora')
option_hour_min = st.selectbox('Selecciona filtro por Hora',
                               ('08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00'),
                               key='1')
option_day = st.selectbox('Selecciona filtro por día', ('LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'))

df_filtrado = df_g.query('día == @option_day and Hora >= @option_hour_min')
st.dataframe(df_filtrado)

try:
    st.metric("Cantidad de Incidentes dentro del filtro", df_filtrado.shape[0])
except:
    pass

st.map(df_filtrado)

# Realizar un filtrado de los datos por barrio
st.subheader('Filtrado por Barrio')
option_barrio = st.selectbox('Selecciona filtro por Barrio',
                             ('La Aguacatala', 'Aranjuez', 'Manrique', 'Robledo'))

df_filtrado_barrio = df_g.query('Barrio == @option_barrio')

st.dataframe(df_filtrado_barrio)

try:
    st.metric("Cantidad de Incidentes en el Barrio seleccionado", df_filtrado_barrio.shape[0])
except:
    pass

st.map(df_filtrado_barrio)

# Realizar un filtrado de los datos por barrio, día y hora
st.subheader('Filtrado por Barrio, Día y Hora')

# Selección de filtro por hora
option_hour_min_filtro = st.selectbox('Selecciona filtro por Hora',
                               ('08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00'),
                               key='2')

# Selección de filtro por día
option_day_filtro = st.selectbox('Selecciona filtro por día', ('LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'))

# Selección de filtro por barrio
option_barrio_filtro = st.selectbox('Selecciona filtro por Barrio',
                             ('La Aguacatala', 'Aranjuez', 'Manrique', 'Robledo'))

# Filtrado del DataFrame
df_filtrado_barrio_dia_hora = df_g.query('Barrio == @option_barrio_filtro and día == @option_day_filtro and Hora >= @option_hour_min_filtro')

# Mostrar el DataFrame filtrado
st.dataframe(df_filtrado_barrio_dia_hora)

# Mostrar la cantidad de incidentes en el filtro
try:
    st.metric("Cantidad de Incidentes en el Filtro", df_filtrado_barrio_dia_hora.shape[0])
except:
    pass

# Mostrar el mapa con los incidentes filtrados
st.map(df_filtrado_barrio_dia_hora)
