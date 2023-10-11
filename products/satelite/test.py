import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Definiere die Farben und Intervalle
colors = [
    'lightblue',
    'blue',
    'darkgreen',
    'lightgreen',
    'yellowgreen',
    'brown',
    'yellow',
    'gold',
    'orange',
    'orangered',
    'red',
    'pink',
    'pink',
    'purple',
    'blue'
]

# Erstelle die benutzerdefinierte Colormap
custom_cmap = ListedColormap(colors)

# Erstelle eine Liste von Schwellenwerten für die Farbänderung (Transparenz)
boundaries = [0, 0.1, 0.2, 0.4, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 30.0, 45.0, 75.0, 100.0, 150.0, float('inf')]

# Erstelle die dazugehörigen Werte des Alpha-Kanals (Transparenz)
alphas = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

#custom_cmap.set_under('transparent')  # Vollständig transparent für Werte unter 0

custom_cmap.set_over('blue')  # Vollständig undurchsichtig für Werte über 150

#custom_cmap.set_bad('transparent')  # Vollständig transparent für ungültige Werte

#custom_cmap.set_alpha(alphas)  # Setze die Transparenz
#
# Teste die benutzerdefinierte Colormap
values = np.linspace(0, 200, 100).reshape(10, 10)
plt.imshow(values, cmap=custom_cmap)
plt.colorbar()
plt.show()