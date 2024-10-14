import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
import plotly.graph_objects as go


#chargement de données :
try :
    data = pd.read_csv("database.csv",sep=',')
except Exception as e:
    print(f"error lors de l'ouverture du fichier :{e}")
print(data.head())

#nettoyage des données :
#remplacer les colones vides par des 0 pour faciliter les calculs
data = data.replace(['', ' '], 0 )
#analyse des données :
#Diviser les Latitudes et Longitudes en des intervalles de taille 10 pour grouper les régions :
data['groupe_longitude'] = pd.cut(data['Longitude'], bins=range(int(data['Longitude'].min()), int(data['Longitude'].max()) + 10, 10))
data['groupe_latitude'] = pd.cut(data['Latitude'], bins=range(int(data['Latitude'].min()), int(data['Latitude'].max()) + 10, 10))

#convertir les données en str pour appliquer px.scatter:
data['groupe_latitude'] = data['groupe_latitude'].astype(str)
data['groupe_longitude'] = data['groupe_longitude'].astype(str)
#determiner le nombre de tremblement de terre pour chaque région:
groupement =data.groupby(['groupe_latitude','groupe_longitude']).size().reset_index(name='n_Troublement')
#Visualisation

v1= px.scatter(groupement, x='groupe_longitude', y='groupe_latitude',
                 size='n_Troublement', color='n_Troublement',
                 labels={'groupe_longitude':'Longitude', 'groupe_latitude':'Latitude'},
                 title="Variation de Nombre des Tremblements de Terre En Fonction des  Regions ")
v1.show()