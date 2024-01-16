import requests
import zipfile
import os 
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.gridspec as gridspec

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import locale
locale.setlocale(locale.LC_TIME, 'de_DE')
oldcwd=os.getcwd()

newcwd = oldcwd +"/products" +"/soundings"
os.chdir(newcwd)

class  sounding:
    def __init__(self,stationid="00368",stationname="Bergen", precision="high",windplot=True ,date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)):
        self.stationid=stationid
        self.precision =precision
        self.date =date
        self.stationname=stationname
        self.wind_plot=windplot
        return
    def request(self):
        stationid=self.stationid
        if self.precision == "low":
            r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/radiosondes/low_resolution/recent/punktwerte_aero_'+stationid+'_akt.zip')
        else:
            r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/radiosondes/high_resolution/recent/sekundenwerte_aero_'+stationid+'_akt.zip')

        if r.status_code != 200:
            raise Exception("Data can't be requested: ",r.status_code)
        else:
            with open("temp.zip", "wb") as file:
                file.write(r.content)

            with zipfile.ZipFile("temp.zip", "r") as zip_ref:
                zip_ref.extractall("sounding_data")

            files= glob("sounding_data/*"+stationid+"*")
            os.rename(files[0], 'sounding_data/sounding_'+stationid+'.txt')
        return

    def image(self):
        stationid=self.stationid
        df= pd.read_csv("sounding_data/sounding_"+stationid+".txt", delimiter=";")
        gewuenschtes_datum = pd.to_datetime(self.date, format='%Y-%m-%d %H:%M:%S')
        print(gewuenschtes_datum)
      
        if self.precision == "low":
            df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')
            df = df[df['MESS_DATUM'] == gewuenschtes_datum]
            df['AEDD'] = df['AEDD'].replace(-999, 0) # Set missing winddirections to 0 to prevent overflow
            p = df['AEP'].values * units.hPa
            T = df['AET'].values * units.degC
            Td = df['AETD'].values * units.degC
            wind_speed = df['AEFF'].values * units.meter / (units.second)#units.knots
            wind_dir = df['AEDD'].values * units.degrees
        else:
            stepsize=20
            df['BEZUGSDATUM_SYNOP'] = pd.to_datetime(df['BEZUGSDATUM_SYNOP'], format='%Y%m%d%H')
            df = df[df['BEZUGSDATUM_SYNOP'] == gewuenschtes_datum]
            df['AE_DD'] = df['AE_DD'].replace(-999, 0) # Set missing winddirections to 0 to prevent overflow
            p = df['AE_P'].values * units.hPa
            T = df['AE_TT'].values * units.degC
            Td = df['AE_TD'].values * units.degC
            p_w = df['AE_P'][::stepsize].values * units.hPa
            wind_speed = df['AE_FF'][::stepsize].values * units.knots
            wind_dir = df['AE_TD'][::stepsize].values * units.degrees
            
        u, v = mpcalc.wind_components(wind_speed, wind_dir)
        
        print(df.head())
        fig = plt.figure(figsize=(12.8,7.2))
        if self.wind_plot==True:
            gs = gridspec.GridSpec(1, 8, figure=fig)  # 3/4 für den Hauptplot, 1/4 für den Nebenplot
            ax1 = fig.add_subplot(gs[1:7])
            ax2 = fig.add_subplot(gs[7:8])
            skew = SkewT(fig,rotation=30,subplot=ax1, aspect="auto")
        else:
            
        #add_metpy_logo(fig, 115, 100)
            skew = SkewT(fig, rotation=45)

        # Plot the data using normal plotting functions, in this case using
        # log scaling in Y, as dictated by the typical meteorological plot.
        skew.ax.set_ylim(1000, 100)
        skew.ax.set_xlim(-40, 60)
        skew.plot(p, T, 'r')
        skew.plot(p, Td, 'g')
        if self.precision == "high":
            skew.plot_barbs(p_w, u, v, length=5, y_clip_radius=0)#,sizes={'height':0.2})
        else:
            skew.plot_barbs(p, u, v)

        # Set some better labels than the default
        skew.ax.set_xlabel(f'Temperature ({T.units:~P})')
        skew.ax.set_ylabel(f'Pressure ({p.units:~P})')

        # Calculate LCL height and plot as black dot. Because `p`'s first value is
        # ~1000 mb and its last value is ~250 mb, the `0` index is selected for
        # `p`, `T`, and `Td` to lift the parcel from the surface. If `p` was inverted,
        # i.e. start from low value, 250 mb, to a high value, 1000 mb, the `-1` index
        # should be selected.
        lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
        skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

        # Calculate full parcel profile and add to plot as black line
        prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
        skew.plot(p, prof, 'k', linewidth=2)

        # Shade areas of CAPE and CIN
        skew.shade_cin(p, T, prof, Td)
        skew.shade_cape(p, T, prof)

        # An example of a slanted line at constant T -- in this case the 0
        # isotherm
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

        # Add the relevant special lines
        skew.plot_dry_adiabats()
        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()

        if self.wind_plot == True:
            # Erstellen Sie einen Subplot für den Windgeschwindigkeitsverlauf
            wind_profile_subplot = ax2#fig.add_subplot(122)  # Ändern Sie die Zahlen je nach Bedarf

            # Plot des Windgeschwindigkeitsverlaufs
            wind_profile_subplot.plot(df['AE_FF'].values, df['AE_P'], 'b', linewidth=2)
            wind_profile_subplot.set_ylim(100, 1000)
            wind_profile_subplot.set_xlim(0, 100)  # Passen Sie die x-Limits an

            # Weitere Anpassungen für den Windprofilplot
            wind_profile_subplot.set_xlabel(f'Windgeschwindigkeit ({wind_speed.units:~P})')
            #wind_profile_subplot.set_ylabel(f'Pressure ({p.units:~P})')
            wind_profile_subplot.invert_yaxis()


        # Add Box under the plot
        #box_props = dict(width=10, boxstyle="round,pad=0.3", edgecolor="blue", facecolor="lightyellow")
        #skew.ax.text(0., -0.1, "text", #transform=skew.ax.transAxes,# va='center', ha='center',
         #   bbox=box_props)


        # Show the plot+
        plt.tight_layout()
        plt.savefig("sounding_"+stationid+".png")
        #plt.show()
        return
    def image_box(self):
        stationid= self.stationid
        image = Image.open("sounding_"+stationid+".png")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("../../ressources/fonts/liberation/LiberationMono-Bold.ttf", 20)  # Hier können Sie die Schriftart und Größe anpassen

        # Koordinaten für den Kasten und Text festlegen
        box_x = 0
        box_y = 0.95*image.height
        box_width = image.width
        box_height = 40
        text = "Hier ist eine Erklärung"
        meausurement = "Messung TEMP " 
        stationname = self.stationname
        stationidi = "("+self.stationid+")"
        time = pd.to_datetime(self.date, format='%Y-%m-%d %H:%M:%S')
        time = time.strftime('%H UTC, %A %d.%m %Y')
        print(len(time))


        # Hintergrundkasten zeichnen
        draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill="white", outline="black")

        # Text im Kasten zeichnen
        draw.text((box_x + 10, box_y + 10), meausurement + stationname+ stationidi, fill="black", font=font)
        draw.text(((0.8- (0.0029*len(time)))*(box_x + box_width), box_y + 10), time, fill="black", font=font)
        # Bild mit Kasten speichern
        image.save("sounding_"+stationid+"_box.png")


        return


bergen=sounding(stationid="00368", date="2023-10-28 00:00:00", stationname="Bergen",windplot=True)
bergen.request()
bergen.image()
bergen.image_box()


