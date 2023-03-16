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

@login_required(login_url="/login/")
def index(request):
    response=get_station_data(42809)
    tide=get_tide_data()
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
               'lowtidenightheight':(((json.dumps((tide['tidaldata']['nightlowtideheight']), indent = 4))))

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

