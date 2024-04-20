import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from PIL import Image  # Importa la clase Image desde el módulo PIL
import json

# Abre el archivo GeoJSON
with open('pot048_2014_zona_de_influ.geojson', "r") as read_file:
    data = json.load(read_file)

# Título de la aplicación
st.title("Zonas de interés cultural en  Medellín")

# Introducción
st.write('La Cultura hace a las personas, o las personas hacen la cultura, es una relación que no se nos es clara, pero entendemos su existencia y tratamos de mantener la nuestra, pues en un mundo globalizado como el contemporáneo, es difícil mantenerle.')
st.subheader('Sistema de visualización de lugares de interés cultural')

# Carga de imagen
image = Image.open('BT.jpeg')
st.image(image, caption="Accidentes viales")

# Listas para almacenar los datos
La = []
Lo = []
GRUPO = []
SUBGRUPO = []
TIPO = []
NOMBRE = []
DIRECCION = []

# Decodificación del archivo en formato JSON
for feature in data['features']:
    coordinates = feature['geometry']['coordinates']
    grupo = feature['properties']['GRUPO']
    subgrupo = feature['properties']['SUBGRUPO']
    tipo = feature['properties']['TIPO']
    nombre = feature['properties']['NOMBRE']
    direccion = feature['properties']['DIRECCION']
    La.append(coordinates[1])
    Lo.append(coordinates[0])
    GRUPO.append(grupo)
    SUBGRUPO.append(subgrupo)
    TIPO.append(tipo)
    NOMBRE.append(nombre)
    DIRECCION.append(direccion)


# Slider para seleccionar el número de registros de accidentes a visualizar
nm = st.slider('Selecciona el número de registros de accidentes que deseas visualizar', 5, 30000)

# Construir el DataFrame con los datos obtenidos
dfLa = pd.DataFrame({'lat': La[0:nm]})
dfLo = pd.DataFrame({'lon': Lo[0:nm]})
dfgr = pd.DataFrame({'Grupo': grupo[0:nm]})
dfsgr = pd.DataFrame({'Subgrupo': subgrupo[0:nm]})
dftp = pd.DataFrame({'Tipo': tipo[0:nm]})
dfnom = pd.DataFrame({'Nombre': nombre[0:nm]})
dfdir = pd.DataFrame({'Dirección': direccion[0:nm]})
df_g = pd.concat([dfLa, dfLo, dfgr, dfsgr, dftp, dfnom, dfdir], axis=1)

# Mostrar la tabla de datos
st.dataframe(df_g)

# Dibujar el mapa utilizando las columnas 'lat' y 'lon'
st.map(df_g)

# Realizar un filtrado de los datos por día y hora
st.subheader('Filtrado por Grupo')
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
df_filtrado_barrio_dia_hora = dfbarr.query('Barrio == @option_barrio_filtro and día == @option_day_filtro and Hora >= @option_hour_min_filtro')

# Mostrar el DataFrame filtrado
st.dataframe(df_filtrado_barrio_dia_hora)

# Mostrar la cantidad de incidentes en el filtro
try:
    st.metric("Cantidad de Incidentes en el Filtro", df_filtrado_barrio_dia_hora.shape[0])
except:
    pass

# Mostrar el mapa con los incidentes filtrados
st.map(df_filtrado_barrio_dia_hora)
