# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:04:50 2024

@author: Sara Edland Gjøsteen

Plot area of interest (Isfjorddrenna area) with IBCAO data.
"""
#%% Importing packages.
#import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import xarray as xr
#%% Read in data needed.
station_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/Selected_UNISstations_Isfjorddrenna_V1.csv"
ibcao_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/ibcao_v5_2024_100m_depth_isfjorddrena_area_bathymetry_data_2.csv"
hydro_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/CTD_all_1876-2019.nc"

unis_st = pd.read_csv(station_file)
bath = pd.read_csv(ibcao_file)
hd_data = xr.open_dataset(hydro_file, drop_variables=["CALIBRATION"])

lon = unis_st["Longitude decimal degrees N"]
lat = unis_st['Latitude decimal degrees East']
station_name = unis_st['Station name']

lon_hydro = hd_data['LONGITUDE'].values
lat_hydro = hd_data['LATITUDE'].values

def plot_stations_and_bathymetry(unis_data, bath_data):
    # Sett opp projeksjon og figur
    proj = ccrs.Orthographic(0,45)
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': proj})

    # Set extent for the area of Isfjorddrenna
    ax.set_extent([7, 14, 77.40, 78.3], crs=ccrs.PlateCarree())

    # Plotting av stasjonene
    for index, row in unis_data.iterrows():
        lon = row["Longitude decimal degrees N"]
        lat = row['Latitude decimal degrees East']
        station_name = row['Station name']

        ax.scatter(lon, lat, marker="o", transform=ccrs.PlateCarree(), color='red')
        ax.text(lon, lat, station_name, transform=ccrs.PlateCarree(), fontsize=9, ha='right')

    # Konverter bathymetry-data fra csv til et plottbart format (hvis x, y, bathymetry-kolonner finnes)
    if 'x' in bath_data.columns and 'y' in bath_data.columns and 'bathymetry' in bath_data.columns:
        x_vals = bath_data['x']
        y_vals = bath_data['y']
        bath_vals = bath_data['bathymetry']
        
        # Add contour of the different depths
        cs = ax.tricontourf(x_vals, y_vals, bath_vals, levels=20, cmap='Blues_r', transform=ccrs.PlateCarree(), alpha=0.6)
        cbar = fig.colorbar(cs, ax=ax, orientation='vertical', shrink=0.7)
        cbar.set_label('Bathymetry (m)')
        
        # Legg til bakgrunnselementer som land, kystlinje og grenser
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='k', facecolor=cfeature.COLORS['land'])
        ax.add_feature(land_10m, facecolor='burlywood', alpha=0.74)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.gridlines(draw_labels=True)

    # Tittel
    plt.title("UNIS Stations and Bathymetry Contours Over Isfjorddrenna, Svalbard")
    
    return fig, ax

# Kall funksjonen for å plotte dataene
fig, ax = plot_stations_and_bathymetry(unis_st, bath)

# Vis plot
plt.show()
