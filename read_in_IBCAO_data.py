# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 08:52:36 2024

@author: Sara Edland Gjøsteen

This script handles the IBCAO V5 100m resolution from 2024.
It puts the raster data in right projection and plots an area of interest. 

In this file area of interest is on the west coast of Spitsbergen, Svalbard Archipelago.
This can be changed into desired area. 

At the end, the script makes a csv file of the area of interest, so the bathymetric data 
can be handled in other scripts without having to read it all in again.  

The scrip plots the section with bathymetric data. 
"""
# Packages
import rioxarray as rio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Opening the tiff file with rioxarray
rds = rio.open_rasterio("C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/ibcao_v5_2024_100m_depth.tiff")

# Removes "band". 
rds = rds.squeeze().drop("band")

# Reproject the data to EPSG:4326 lat/lon
rds_4326 = rds.rio.reproject("EPSG:4326")

# Cutting the data to cover the area of interest.
rds_area = rds_4326.rio.clip_box(minx=7, miny=77.40, maxx=14, maxy=78.3)

# Make a figure for a map
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# Plot the data 
rds_area.plot.imshow(ax=ax, transform=ccrs.PlateCarree(), cmap='terrain', add_colorbar=True)

# Adding features to the plot
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAND)
ax.gridlines(zorder=100, draw_labels=True)

# Setting the extent of the map
ax.set_extent([7, 14, 77.40, 78.3], crs=ccrs.PlateCarree())

plt.title("IBCAO Data Over Isfjorddrenna area, Svalbard in WGS 84 (EPSG:4326)")
plt.show()


#%% This part makes the subarea into a csv file. Run if desired. 
""""
# Convert the xarray to pandas dataframe with the column name "bathymetry" for the depth values. 
df_svalbard = rds_area.to_dataframe(name='bathymetry').reset_index()

# Save as a CSV-fil
file_name = "ibcao_v5_2024_100m_depth_isfjorddrena_area_bathymetry_data_2.csv"
df_svalbard.to_csv(file_name, index=False)

print(f"CSV-fil saved as {file_name}")
"""