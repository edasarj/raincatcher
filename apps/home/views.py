# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present SS
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
import json
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
##import mysql.connector as sql
from folium.plugins import TimestampedGeoJson
import pandas as pd
import folium
import datetime
import folium.plugins as plugins
import datetime



@login_required(login_url="/login/")
def index(request):
    response=get_station_data(42809)
    tide=get_tide_data()
    m2=waterloggingmap()
    m=animemap2()
    context = {'segment': 'index','tmax':(((json.dumps((response['forecast'][0]['max']), indent = 4)))),
               'tmin':(((json.dumps((response['forecast'][0]['min']), indent = 4)))),
               'forecast':(((json.dumps((response['forecast'][0]['condition']), indent = 4)))),
               'day1':(((json.dumps((response['forecast'][0]['date']), indent = 4)))),
               'day2':(((json.dumps((response['forecast'][1]['date']), indent = 4)))),
               'day3':(((json.dumps((response['forecast'][2]['date']), indent = 4)))),
               'day4':(((json.dumps((response['forecast'][3]['date']), indent = 4)))),
               'day5':(((json.dumps((response['forecast'][4]['date']), indent = 4)))),
               'day6':(((json.dumps((response['forecast'][5]['date']), indent = 4)))),
               'day7':(((json.dumps((response['forecast'][6]['date']), indent = 4)))),
               'remark1':(((json.dumps((response['forecast'][0]['condition']), indent = 4)))),
               'remark2':(((json.dumps((response['forecast'][1]['condition']), indent = 4)))),
               'remark3':(((json.dumps((response['forecast'][2]['condition']), indent = 4)))),
               'remark4':(((json.dumps((response['forecast'][3]['condition']), indent = 4)))),
               'remark5':(((json.dumps((response['forecast'][4]['condition']), indent = 4)))),
               'remark6':(((json.dumps((response['forecast'][5]['condition']), indent = 4)))),
               'remark7':(((json.dumps((response['forecast'][6]['condition']), indent = 4)))),
               'hightideday':(((json.dumps((tide['tidaldata']['dayhightide']), indent = 4)))),
               'hightidedayheight':(((json.dumps((tide['tidaldata']['dayhightideheight']), indent = 4)))),
               'lowtideday':(((json.dumps((tide['tidaldata']['daymintide']), indent = 4)))),
               'lowtidedayheight':(((json.dumps((tide['tidaldata']['daymintideheight']), indent = 4)))),
               'hightidenight':(((json.dumps((tide['tidaldata']['nighthightide']), indent = 4)))),
               'hightidenightheight':(((json.dumps((tide['tidaldata']['nighthightideheight']), indent = 4)))),
               'lowtidenight':(((json.dumps((tide['tidaldata']['nightlowtide']), indent = 4)))),
               'lowtidenightheight':(((json.dumps((tide['tidaldata']['nightlowtideheight']), indent = 4)))),
               'map': m,
               'map2':m2

               }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
def get_station_data(id):
    URL = 'http://city.imd.gov.in/citywx/city_weather.php?id={}'.format(id)

    response = requests.get(URL, verify=False)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')

    cells = soup.find_all('td')

    max_temp = cells[4].text.strip()
    max_dep = cells[6].text.strip()
    min_temp = cells[8].text.strip()
    min_dep = cells[10].text.strip()
    rh_0830 = cells[14].text.strip()
    rh_1730 = cells[16].text.strip()

    sunrise = cells[20].text.strip()
    sunset = cells[18].text.strip()
    moonrise = cells[24].text.strip()
    moonset = cells[22].text.strip()

    day1_date = cells[31].font.text.strip()
    day1_max = cells[33].font.text.strip()
    day1_min = cells[32].font.text.strip()
    day1_forecast = cells[35].font.text.strip()

    day2_date = cells[36].font.text.strip()
    day2_max = cells[38].font.text.strip()
    day2_min = cells[37].font.text.strip()
    day2_forecast = cells[40].font.text.strip()

    day3_date = cells[41].font.text.strip()
    day3_max = cells[43].font.text.strip()
    day3_min = cells[42].font.text.strip()
    day3_forecast = cells[45].font.text.strip()

    day4_date = cells[46].font.text.strip()
    day4_max = cells[48].font.text.strip()
    day4_min = cells[47].font.text.strip()
    day4_forecast = cells[50].font.text.strip()

    day5_date = cells[51].font.text.strip()
    day5_max = cells[53].font.text.strip()
    day5_min = cells[52].font.text.strip()
    day5_forecast = cells[55].font.text.strip()

    day6_date = cells[56].font.text.strip()
    day6_max = cells[58].font.text.strip()
    day6_min = cells[57].font.text.strip()
    day6_forecast = cells[60].font.text.strip()

    day7_date = cells[61].font.text.strip()
    day7_max = cells[63].font.text.strip()
    day7_min = cells[62].font.text.strip()
    day7_forecast = cells[65].font.text.strip()

    return {
        'temperature': {
            'max': {
                'value': float(max_temp),
                'departure': float(max_dep)
            },
            'min': {
                'value': float(min_temp),
                'departure': float(min_dep)
            }
        },
        'humidity': {
            'morning': float(rh_0830),
            'evening': float(rh_1730)
        },
        'astronomical': {
            'sunrise': sunrise,
            'sunset': sunset,
            'moonrise': moonrise,
            'moonset': moonset
        },
        'forecast': [
            {
                'day': 1,
                'date': day1_date,
                'max': float(day1_max),
                'min': float(day1_min),
                'condition': day1_forecast
            },
            {
                'day': 2,
                'date': day2_date,
                'max': float(day2_max),
                'min': float(day2_min),
                'condition': day2_forecast
            },
            {
                'day': 3,
                'date': day3_date,
                'max': float(day3_max),
                'min': float(day3_min),
                'condition': day3_forecast
            },
            {
                'day': 4,
                'date': day4_date,
                'max': float(day4_max),
                'min': float(day4_min),
                'condition': day4_forecast
            },
            {
                'day': 5,
                'date': day5_date,
                'max': float(day5_max),
                'min': float(day5_min),
                'condition': day5_forecast
            },
            {
                'day': 6,
                'date': day6_date,
                'max': float(day6_max),
                'min': float(day6_min),
                'condition': day6_forecast
            },
            {
                'day': 7,
                'date': day7_date,
                'max': float(day7_max),
                'min': float(day7_min),
                'condition': day7_forecast
            }
        ]
    }

def get_tide_data():
    URL = 'https://www.tide-forecast.com/locations/Calcutta-Garden-Reach-India/tides/latest'

    response = requests.get(URL, verify=False)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')

    cells = soup.find_all('td')

    max_tide_day = cells[1].text.strip()
    max_tide_day_height=cells[2].text.strip()
    min_tide_day = cells[4].text.strip()
    min_tide_day_height = cells[5].text.strip()
    max_tide_night = cells[7].text.strip()
    max_tide_night_height = cells[8].text.strip()
    min_tide_night = cells[10].text.strip()
    min_tide_night_height = cells[11].text.strip()

    #print(max_tide_day)
    return {
        'tidaldata': {
            'dayhightide': max_tide_day,
            'dayhightideheight': max_tide_day_height,
            'daymintide': min_tide_day,
            'daymintideheight': min_tide_day_height,
            'nighthightide': max_tide_night,
            'nighthightideheight': max_tide_night_height,
            'nightlowtide': min_tide_night,
            'nightlowtideheight': min_tide_night_height,
        }
    }
def waterloggingmap():
            # Read the digital elevation  model in longitude, latitude and elevation format.
            DEM = pd.read_csv('boundary.csv', header = None, names = ['longitude','latitude','elevation'])# Set all negative elevations to zero to show that they will be under the mean sea level of zero
            ##DEM=mysqlconnectn()
            DEM.columns = ['longitude','latitude','elevation']
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
            ##context = {'map': m}
            return m
            ##return render(request, 'app_name/rainfall_map.html', context)

##def mysqlconnectn():
##    db_connection = sql.connect(host='localhost', database='water', user='root', password='')
##    db_cursor = db_connection.cursor()
##    db_cursor.execute('SELECT * FROM boundary')

##    table_rows = db_cursor.fetchall()

##    df = pd.DataFrame(table_rows)
##    return df
def animemap():
        # create a map with Folium
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

        # create some geoJSON data with timestamps
        geojson_data = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-122.4194, 37.7749],
                    },
                    'properties': {
                        'title': 'San Francisco',
                        'time': '2023-03-18T12:00:00',
                    },
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-122.4167, 37.7833],
                    },
                    'properties': {
                        'title': 'Fisherman\'s Wharf',
                        'time': '2023-03-18T13:00:00',
                    },
                },
            ],
        }

        # create the TimestampedGeoJson layer
        timestamped_geojson = TimestampedGeoJson(
            data=geojson_data,
            period='PT1H',
            duration='PT1H',
            auto_play=True,
            loop=True,
            max_speed=1,
            loop_button=True,
            date_options='YYYY-MM-DDTHH:MM:SSZ',
            time_slider_drag_update=True,
        )

        # add the TimestampedGeoJson layer to the map
        timestamped_geojson.add_to(m)
        tm=m._repr_html_()

        # render the map
        
        return tm

def animemap2():
    # Import DEM CSV data
    dem_data = pd.read_csv('boundary.csv')
    rainfall =[100,50,30]
    vmin = dem_data['elevation'].min()
    vmean= dem_data['elevation'].mean()
    vmax = dem_data['elevation'].max()# Setup colormap
    colors = ['blue','royalblue', 'navy','pink',  'mediumpurple',  'darkorchid',  'plum',  'm', 'mediumvioletred', 'palevioletred', 'crimson',
             'magenta','pink','red','yellow','orange', 'brown','green', 'darkgreen']
    print(vmean)

    for i in range(0,len(dem_data)):
        for rain in rainfall:
            dem_data.loc[i,'rainfall']=int(dem_data.loc[i,'elevation'])+rain
            dem_data['timestamp']=datetime.datetime.now()+datetime.timedelta(minutes = i)
            

    # Create map
    m = folium.Map([dem_data.latitude.mean(), dem_data.longitude.mean()], zoom_start=12, tiles="OpenStreetMap")

    # Add tile layer
    folium.TileLayer('OpenStreetMap').add_to(m)
    # Create HeatMap layer
    heat_data = dem_data[['latitude', 'longitude', 'elevation']].values.tolist()
    folium.plugins.HeatMap(heat_data, radius=2).add_to(m)
    # Set threshold elevation value
    threshold = vmean



    # Filter data to show areas below threshold elevation value
    waterlogged_data = dem_data[dem_data['elevation'] < threshold][['latitude', 'longitude', 'elevation']].values.tolist()



    # Add Waterlogged areas layer
    folium.FeatureGroup(name='Waterlogged areas').add_to(m)
    folium.plugins.HeatMap(waterlogged_data, radius=2).add_to(m)


    # Define start and end timestamps
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()+datetime.timedelta(minutes = i)


    # Generate GeoJson data for each timestamp
    data = []
    ##m = folium.Map([dem_data.latitude.mean(), dem_data.longitude.mean()], zoom_start=12, tiles="OpenStreetMap")
    for timestamp in pd.date_range(start_date, end_date, freq='M'):
        print(timestamp)
        # Filter data to show areas below threshold elevation value for current timestamp
        filtered_data = dem_data[(dem_data['elevation'] < threshold) & (dem_data['timestamp'] == timestamp)][['latitude', 'longitude', 'elevation']].values.tolist()

        # Create GeoJson data
        geojson_data = {
            'type': 'FeatureCollection',
            'features': [{'type': 'Feature',
                          'geometry': {'type': 'Point', 'coordinates': [d[1], d[0]]},
                          'properties': {'elevation': d[2]}}
                         for d in filtered_data]
        }

        # Add GeoJson data with timestamp
        data.append({
            'times': timestamp.strftime('%Y-%m-%d %H:%M:%S:f'),
            'data': geojson_data
        })

    # Add TimestampedGeoJson layer
##    folium.plugins.TimestampedGeoJson({'type': 'FeatureCollection', 'features': []}, period='P1M',
##                                      add_last_point=True, auto_play=False, loop=False, max_speed=0.5,
##                                      loop_button=True, date_options='YYYY-MM-DD', time_slider_drag_update=True).add_to(m)
##
##    # Add data to TimestampedGeoJson layer
##    folium.LayerControl().add_to(m)
##    # add the TimestampedGeoJson layer to the map
##    ##timestamped_geojson.add_to(m)
##    tm=m._repr_html_()
    timestamped_geojson = TimestampedGeoJson(
        data=data,
        period='PT1H',
        duration='PT1H',
        auto_play=True,
        loop=True,
        max_speed=1,
        loop_button=True,
        date_options='YYYY-MM-DDTHH:MM:SSZ',
        time_slider_drag_update=True,
    )

    # add the TimestampedGeoJson layer to the map
    timestamped_geojson.add_to(m)
    tm=m._repr_html_()

    return tm

