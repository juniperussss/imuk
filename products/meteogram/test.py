import matplotlib.pyplot as plt
import numpy as np
import datetime

# Beispiel Daten für Windgeschwindigkeiten
dates = [datetime.datetime(2024, 3, 15, 12),
         datetime.datetime(2024, 3, 16, 12),
         datetime.datetime(2024, 3, 17, 12)]
wind_speeds = [10, 15, 20]  # Beispiel Windgeschwindigkeiten in m/s

# Beispielwindrichtungen in Grad
wind_directions = [180, 225, 270]  # Beispiel Windrichtungen in Grad

# Umwandlung der Windrichtungen in Vektoren für barbs()
u = wind_speeds * np.sin(np.deg2rad(wind_directions))
v = wind_speeds * np.cos(np.deg2rad(wind_directions))

# Erstellen des Plots
fig, ax = plt.subplots()

# Plotten der Barb-Visualisierung
ax.barbs(dates, [0]*len(dates), u, v, length=7, pivot='middle')

# Einstellungen für die Achsen
ax.set_yticks([])
ax.set_xlabel('Datum')
ax.set_ylabel('Windgeschwindigkeit (m/s)')

# Datumsformatierung für die x-Achse
ax.xaxis_date()
plt.xticks(rotation=45)

# Titel setzen
plt.title('Windgeschwindigkeiten über die Zeit')

# Anzeige des Plots
plt.show()