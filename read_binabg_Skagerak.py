# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:27:33 2024

@author: sarag
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Parametre
Tmin = -1.8
Tmax = 14
Smin = 34.4
Smax = 35.6

folder = r'C:/Users/sarag/OneDrive/Skrivebord/MASTER/Data/Skagerak/Processed_data/Bin_avg'

# Importopsjoner
opts = {
    'skiprows': 237,  # MATLAB bruker 1-basert indeksering
    'delim_whitespace': True,
    'header': None,
    'names':    ["scan", "timeJ", "Lon", "Lat", "P", "T", "C", "DO_V", "Fl", "Turb", "timeS", "S", "DO_ml", "D", "w", "nbin", "flag"],
    'usecols':  ["scan", "timeJ", "Lon", "Lat", "P", "T", "C", "DO_V", "Fl", "Turb", "timeS", "S", "DO_ml", "D", "w", "nbin", "flag"],
}

# Få en liste over filene i mappen
files = [f for f in os.listdir(folder) if f.endswith('_avg.cnv')]

# Prosessere og plotte dataene
for n, filename in enumerate(files, start=0):
    data_path = os.path.join(folder, filename)
    CTD = pd.read_csv(data_path, **opts)
    
    # Filtrere ut data der trykk (P) er større eller lik 3
    I = CTD[CTD['P'] >= 3]

    if not I.empty:
        # Plot 1
        plt.figure(1)
        plt.scatter(I['S'], I['T'], c=I['P'], s=12, cmap='viridis', edgecolor='k', alpha=0.75)
        plt.colorbar(label='Pressure')
        plt.xlabel('Salinity (S)')
        plt.ylabel('Temperature (T)')
        plt.xlim([Smin, Smax])
        plt.ylim([Tmin, Tmax])

        # Plot 2a
        plt.figure(2)
        plt.subplot(121)
        plt.plot(I['S'], I['P'], '.', label=f'Station {n}')
        plt.title(f'S, station: {n}')
        plt.xlabel('Salinity (S)')
        plt.gca().invert_yaxis()

        # Plot 2b
        plt.subplot(122)
        plt.plot(I['T'], I['P'], '.', label=f'Station {n}')
        plt.title(f'T, station: {n}')
        plt.xlabel('Temperature (T)')
        plt.gca().invert_yaxis()

# Justere Layout
plt.figure(2)
plt.tight_layout()
plt.show()

plt.figure(1)
plt.show()
