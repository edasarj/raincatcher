import folium
import branca
from folium import plugins
from scipy.interpolate import griddata
import geojsoncontour
import scipy as sp
import scipy.ndimage
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def waterloggingmap():
            # Read the digital elevation  model in longitude, latitude and elevation format.
            DEM = pd.read_csv('boundary.csv', header = None, names = ['longitude','latitude','elevation'])# Set all negative elevations to zero to show that they will be under the mean sea level of zero
            DEM.drop(DEM.head(1).index, inplace=True)# delete the first row that contain labels 'x,y,z'
            DEM = DEM.replace(',','.', regex=True).astype(float) # set data type to float, they were saved as strings
            vmin = DEM['elevation'].min() 
            vmax = DEM['elevation'].max()# Setup colormap
            colors = ['blue','royalblue', 'navy','pink',  'mediumpurple',  'darkorchid',  'plum',  'm', 'mediumvioletred', 'palevioletred', 'crimson',
                     'magenta','pink','red','yellow','orange', 'brown','green', 'darkgreen']
            levels = len(colors)
            cm     = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)# Convertion from dataframe to array
            x = np.asarray(DEM.longitude.tolist())
            y = np.asarray(DEM.latitude.tolist())
            z = np.asarray(DEM.elevation.tolist()) # Make a grid
            x_arr          = np.linspace(np.min(x), np.max(x), 500)
            y_arr          = np.linspace(np.min(y), np.max(y), 500)
            x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)
             
            # Grid the elevation (Edited on March 30th, 2020)
            z_mesh = griddata((x, y), z, (x_mesh, y_mesh), method='linear')
             
            # Use Gaussian filter to smoothen the contour
            sigma = [5, 5]
            z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='constant')
             
            # Create the contour
            contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, alpha=0.5, colors=colors, linestyles='None', vmin=vmin, vmax=vmax)


            # Convert matplotlib contourf to geojson
            geojson = geojsoncontour.contourf_to_geojson(
                contourf=contourf,
                min_angle_deg=3.0,
                ndigits=5,
                stroke_width=1,
                fill_opacity=0.1)
            # Set up the map placeholdder
            geomap1 = folium.Map([DEM.latitude.mean(), DEM.longitude.mean()], zoom_start=12, tiles="OpenStreetMap")
            folium.GeoJson(
                geojson,
                style_function=lambda x: {
                    'color':     x['properties']['stroke'],
                    'weight':    x['properties']['stroke-width'],
                    'fillColor': x['properties']['fill'],
                    'opacity':   0.5,
                }).add_to(geomap1)
             
            # Add the colormap to the folium map for legend
            cm.caption = 'waterlogging'
            geomap1.add_child(cm)
             
            # Add the legend to the map
            plugins.Fullscreen(position='bottomleft', force_separate_button=True).add_to(geomap1)
            #geomap1.save('prediction.html')

            m = geomap1._repr_html_()
            context = {'map': m}
            return render(request, 'app_name/rainfall_map.html', context)
