import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.units as munits
import numpy as np
import datetime
import matplotlib.gridspec as gridspec
import metpy.calc as mpcalc
from matplotlib.offsetbox import OffsetImage
import matplotlib.image as mpimg
# Lade das kombinierte Dataset aus der NetCDF-Datei
from PIL import Image
import io
def get_svg_for_synop_code(synop_code):
    # Hier solltest du den Pfad zu deinen SVG-Dateien entsprechend dem Synop-Code erstellen und das SVG als Text zurückgeben
    # Beispiel:
    svg_path = "ressources/symbols/ww_PresentWeather/WeatherSymbol_WMO_PresentWeather_ww_"+str(int(synop_code)).zfill(2)+".svg"
    #with open(svg_path, 'r') as file:
     #   svg_content = file.read()
    return svg_path


def svg_to_image(svg_content):
    # SVG in ein PIL-Bild konvertieren
    svg_io = io.BytesIO(svg_content.encode('utf-8'))
    pil_image = Image.open(svg_io)
    return pil_image


def plot_meteogramm (model="icon", inputpath="", output_path=""):
    combined_ds = xr.open_dataset(inputpath +'meteogramm_'+model+'.nc')

    # Extrahiere die Variablen aus dem Dataset

    # Calculate the total deformation of the flow
    wind_speed = mpcalc.wind_speed(combined_ds.u10, combined_ds.v10)
    #gust_speed = mpcalc.wind_speed(combined_ds.u10, combined_ds.v10)
    # Konvertiere die Zeitstempel in ein pandas DataFrame

    df = combined_ds.to_dataframe()
    print(df.index)
    # Erstelle das Meteogramm mit Matplotlib
    # Erstelle das Meteogramm mit Matplotlib
    #fig, axs = plt.subplots(5, 1, figsize=(10, 15), sharex=True)
    fig = plt.figure(figsize=(12, 7))

    gs0 = gridspec.GridSpec(6, 1, figure=fig)

    gs00 = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=gs0[0])
    gs03 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs0[3])

    ax5 = fig.add_subplot(gs0[5, :])

    ## Pressure anc Rain
    ax5.plot(df.index, df['prmsl'], color='green', linestyle='--')

    ax51 = ax5.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    #ax51.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    ax51.bar(df.index, df["tp"])

    ax5.set_ylabel('Pressure (hPa)', fontsize=12)
    ax5.xaxis.grid(True)

    ax1 = fig.add_subplot(gs0[0, :],sharex=ax5)
    ax11 = fig.add_subplot(gs00[0, :],sharex=ax5)
    ax12 = fig.add_subplot(gs00[1, :],sharex=ax5)
    ax13 = fig.add_subplot(gs00[2, :],sharex=ax5)
    ax14 = fig.add_subplot(gs00[3, :],sharex=ax5)
    ax15 = fig.add_subplot(gs00[4, :],sharex=ax5)
    ax16 = fig.add_subplot(gs00[5, :],sharex=ax5)

    ax2 = fig.add_subplot(gs0[1, :],sharex=ax5)
    ax4 = fig.add_subplot(gs0[3, :],sharex=ax5)
    ax41 = fig.add_subplot(gs03[0, :],sharex=ax5)
    ax42 = fig.add_subplot(gs03[1, :],sharex=ax5)
    ax43 = fig.add_subplot(gs03[2, :],sharex=ax5)
    ax3 = fig.add_subplot(gs0[2, :],sharex=ax5)
    ax6 = fig.add_subplot(gs0[4, :],sharex=ax5)

    for axis in [ax1,ax11,ax12,ax13,ax14,ax15,ax16,ax2,ax3,ax41,ax42,ax43,ax4,ax6]:
        plt.setp(axis.get_xticklabels(), visible=False)

    ## Temperature and dewpoint
    ax3.plot(df.index, df['t2m'], color='red', linestyle='-')
    ax3.set_ylabel('t2m', fontsize=12)
    ax3.plot(df.index, df['t_850'], color='black', linestyle='-')
    ax3.plot(df.index, df['d2m'], color='blue', linestyle='-')
    ax3.xaxis.grid(True)

    ## Wind and Gust speed
    ax2.plot(df.index, wind_speed, color='black')
    ax2.plot(df.index, df['fg10'], color='black')
    ax2.set_ylabel('Windspeed', fontsize=12)
    ax2.xaxis.grid(True)

    ### Cloud coverage
    ax4.xaxis.grid(True)


    ### Significant Weather
    ax6.xaxis.grid(True)
    print(df["WW"])
    #ax6.scatter(df.index, df["WW"], color='black')



    for index, row in df.iterrows():
        synop_code = row["WW"]  # Annahme: Die Spalte "WW" enthält die Synop-Codes
        svg_path = get_svg_for_synop_code(synop_code)
        img = mpimg.imread(svg_path)
        ax6.imshow(img, aspect='auto', extent=(index, index+1, synop_code-0.5, synop_code+0.5), zorder=3)


    ax6.set_ylabel('Windspeed', fontsize=12)


    ## Wind Directions
    ax1.xaxis.grid(True)
    ax16.barbs(df.index, [0]*len(df.index), df['u10'], df['v10'], length=5, pivot='middle')
    ax15.barbs(df.index, [0]*len(df.index), df['u_950'], df['u_950'], length=5, pivot='middle')
    ax14.barbs(df.index, [0]*len(df.index), df['u_850'], df['u_850'], length=5, pivot='middle')
    ax13.barbs(df.index, [0]*len(df.index), df['u_700'], df['u_700'], length=5, pivot='middle')

    ax12.barbs(df.index, [0]*len(df.index), df['u_500'], df['v_500'], length=5, pivot='middle')
    ax11.barbs(df.index, [0]*len(df.index), df['u_300'], df['v_300'], length=5, pivot='middle')

    for axs in [ax11,ax12,ax13,ax14,ax15,ax16,ax41,ax42,ax43]:
        axs.axis("off")

    plt.suptitle("TEST Meteogram")
    ax5.xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Setze den Locator auf alle 6 Stunden
    ax5.xaxis.set_major_formatter(mdates.DateFormatter(' %H \n %d-%m '))  # Formatiere die x-Ticks

    plt.savefig(output_path+"meteogramm_"+model+".png")
#plt.show()

plot_meteogramm (model="icon", inputpath="/mnt/nvmente/CODE/imuk/database/input/meteogram/", output_path="/mnt/nvmente/CODE/imuk/database/output/meteogram/")
#plot_meteogramm (model="icon-eu", inputpath="/mnt/nvmente/CODE/imuk/database/input/meteogram/", output_path="/mnt/nvmente/CODE/imuk/database/output/meteogram/")
#plot_meteogramm (model="icon-d2", inputpath="/mnt/nvmente/CODE/imuk/database/input/meteogram/", output_path="/mnt/nvmente/CODE/imuk/database/output/meteogram/")