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
#distribution des Tremblements de terre par rapport à l'équateur & méridien Greenwich:
#déterminer les regions:
nord_est= data[(data['Latitude'] > 0) & (data['Longitude'] > 0)]
nord_oest = data[(data['Latitude'] > 0) & (data['Longitude'] <0)]
sud_est = data[(data['Latitude'] < 0) & (data['Longitude'] > 0)]
sud_oest = data[(data['Latitude'] < 0) & (data['Longitude'] < 0)]
#calculer le nombre de tremblement par région (n_T *100)/N_totale_T:
x=(len(nord_est)*100)/len(data)
y=(len(nord_oest)*100)/len(data)
z=(len(sud_est)*100)/len(data)
t=(len(sud_oest)*100)/len(data)
#visualisation :
v2 = px.pie(values=[x, y, z, t],
            names=['Nord-Est', 'Nord-Ouest', 'Sud-Est', 'Sud-Ouest'],
            title="Distribution des Tremblements de Terre En <br>Fonction de l'Équateur et du Méridien de Greenwich ",

            color_discrete_sequence=['pink', 'yellow', 'lime', 'orange'])
v2.show()

# Assurer que la colonne 'Date' est en format datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Extraire l'année à partir de la colonne 'Date'
data['Year'] = data['Date'].dt.year

# Distribution des tremblements de terre par année
earthquakes_per_year = data.groupby('Year').size().reset_index(name='n_Troublements')

# Visualisation: Line Plot de tremblements de terre par année
v3 = px.line(earthquakes_per_year, x='Year', y='n_Troublements',
             labels={'Year': 'Année', 'n_Troublements': 'Nombre de Tremblements de Terre'},
             title="Distribution des Tremblements de Terre par Année")

# Ajouter des marqueurs pour chaque point sur la ligne
v3.update_traces(mode='lines+markers')

v3.show()


# Extraire le mois à partir de la colonne 'Date'
data['Month'] = data['Date'].dt.month

# Distribution des tremblements de terre par mois
earthquakes_per_month = data.groupby('Month').size().reset_index(name='n_Troublements')

# Identifier le mois avec le plus grand nombre de tremblements de terre
max_month = earthquakes_per_month.loc[earthquakes_per_month['n_Troublements'].idxmax()]

print(f"Le mois avec le plus grand nombre de tremblements de terre est : Mois {int(max_month['Month'])} avec {int(max_month['n_Troublements'])} tremblements.")

# Visualisation: Histogramme de tremblements de terre par mois
v4 = px.bar(earthquakes_per_month, x='Month', y='n_Troublements',
            labels={'Month': 'Mois', 'n_Troublements': 'Nombre de Tremblements de Terre'},
            title="Distribution des Tremblements de Terre par Mois")

# Ajouter une annotation pour mettre en évidence le mois le plus actif
v4.add_annotation(x=max_month['Month'], y=max_month['n_Troublements'],
                  text=f"Le mois le plus actif ({int(max_month['n_Troublements'])} tremblements)",
                  showarrow=True, arrowhead=2)

v4.show()

