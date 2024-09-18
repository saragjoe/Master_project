# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:32:42 2024

@author: sarag

I want to find out what section I want to focus on first. 
"""
#%%
#import packages.
#import os
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

#%%
# Read in datafile with all the unis stations.
#data = pd.read_csv("C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/UNISstations_selected.csv")

data = pd.read_excel("C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/UNISstations_selected_2.xlsx")

#%%
# To filter the UNIS stations in a certain section
filtered_data = data[(data["Longitude decimal degrees N"] >= 7.5) & 
                     (data["Longitude decimal degrees N"] <= 13.6) &
                     (data['Latitude decimal degrees East'] >= 77.5) & 
                     (data['Latitude decimal degrees East'] <= 78.5)]
#%%
# Change "data" to "filtered_data" if you are using the csv file with all stations. 
# If the file only contains the stations of interest, use "data"
lon = data["Longitude decimal degrees N"]
lat = data['Latitude decimal degrees East']
station_name = data['Station name']

def plot_stations(data):
    # Making a function to plot the stations
    proj = ccrs.Orthographic(0,45)
    land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='k', facecolor=cfeature.COLORS['land'])
    
    # Setting the figure
    fig, ax = plt.subplots(figsize=(7,7),subplot_kw=dict(projection=proj), ncols=1, nrows = 1)
    
    # Giving the extent of the plot so it covers Svalbard.
    ax.set_extent([8, 14, 77.55, 78.15], ccrs.PlateCarree())
    
    # Adding land boarders and color them in.
    ax.add_feature(land_10m, facecolor='burlywood', alpha=0.74 )
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=.5)
    # Add the grid to the map. 
    ax.gridlines(zorder=100, draw_labels=True)
    
    # Plot the position of each station.
    for index, row in data.iterrows():
        ax.scatter(row["Longitude decimal degrees N"], row['Latitude decimal degrees East'], 
                   marker="o", transform=ccrs.PlateCarree(), label=row['Station name'], color='teal')
        ax.text(row['Longitude decimal degrees N'], row['Latitude decimal degrees East'], row['Station name'],
               transform=ccrs.PlateCarree(), fontsize=9, ha='right')
    
    return fig, ax
    
fig, ax = plot_stations(filtered_data)

#%%
# Make a csv file with the selected stations.
#selected_stations = filtered_data.copy()

# Optionally, save the filtered DataFrame to a new CSV file
#selected_stations.to_csv("C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/0911_Selected_UNISstations.csv", index=False)


