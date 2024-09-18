# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:04:50 2024

@author: Sara Edland Gjøsteen

Plot area of interest (Isfjorddrenna area) with IBCAO data.
"""
#%% Importing packages.
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

#%% Read in data needed.
station_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/Selected_UNISstations_Isfjorddrenna_V1.csv"
ibcao_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/ibcao_v5_2024_100m_depth_isfjorddrena_area_bathymetry_data_2.csv"
hydro_file = "C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/CTD_all_1876-2019.nc"

unis_st = pd.read_csv(station_file)
bath = pd.read_csv(ibcao_file)
hd_data = xr.open_dataset(hydro_file, drop_variables=["CALIBRATION"])

#%%
# Extract the longitude and latitude values from the UNIS HD file. 
lon_hydro = hd_data['LONGITUDE'].values
lat_hydro = hd_data['LATITUDE'].values

# Making a dataframe which takes the longitude and latitude of all the points in UNIS HD and then
# counts how many times there is a measurement at that exact point. 
hydro_df = pd.DataFrame({'Longitude': lon_hydro, 'Latitude': lat_hydro})
counts = hydro_df.groupby(['Longitude', 'Latitude']).size().reset_index(name='Count')

#%% Function for plotting bathymetry, the frequency of UNIS HD and thed UNIS Stations. 
def plot_stations_bathymetry_freq(unis_data, bath_data, freq_data):
    # Set projection and figure. 
    proj = ccrs.Orthographic(0,45)
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': proj})

    # Set extent for the area of Isfjorddrenna
    ax.set_extent([7, 14, 77.4, 78.3], crs=ccrs.PlateCarree())

    # Converting the bathymetric values which are given as x,y coordinates in the csv file, into longitude and latitude variables.
    if 'x' in bath_data.columns and 'y' in bath_data.columns and 'bathymetry' in bath_data.columns:
        x_vals = bath_data['x']
        y_vals = bath_data['y']
        bath_vals = bath_data['bathymetry']
        
        # Add contour of the different depths
        cs = ax.tricontourf(x_vals, y_vals, bath_vals, 
                            levels=20, 
                            cmap='Blues_r', 
                            vmax = 0,
                            transform=ccrs.PlateCarree(), 
                            alpha=0.6)
        
        cbar = fig.colorbar(cs, ax=ax, orientation='vertical', shrink=0.7)
        cbar.set_label('Bathymetry (m)')
        
    # Add features to the map: coastline, land, gridlines. 
    land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='k', facecolor=cfeature.COLORS['land'])
    ax.add_feature(land_10m, facecolor='burlywood', alpha=0.74)
    ax.add_feature(cfeature.COASTLINE)
    ax.gridlines(draw_labels=True)

    # Plot frekvensbasert scatter
    scatter = ax.scatter(freq_data['Longitude'], freq_data['Latitude'], 
                         s=freq_data['Count']*2,  # Size of amount of measurements based on how many points. 
                         c=freq_data['Count'],    # Color of the scatter point is dependent on how many measurements recorded.
                         cmap='Set1',  
                         alpha=0.7, 
                         vmax = 170,
                         transform=ccrs.PlateCarree())
    
    # Plot the UNIS stations.
    for index, row in unis_data.iterrows():
        lon = row["Longitude decimal degrees N"]
        lat = row['Latitude decimal degrees East']
        station_name = row['Station name']

        ax.scatter(lon, lat, marker="o", transform=ccrs.PlateCarree(), color='aqua')
        ax.text(lon, lat, station_name, transform=ccrs.PlateCarree(), fontsize=9, ha='right')
    
    # Add the colour bar which represents the frequency of measurements. 
    cbar = fig.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7)
    cbar.set_label('Number of Measurements')

    # Title
    plt.title("UNIS Stations, Bathymetry, and Measurement Frequencies in Isfjorddrenna, Svalbard")

    return fig, ax

fig, ax = plot_stations_bathymetry_freq(unis_st, bath, counts)

plt.show()
