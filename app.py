from flask import Flask, request, jsonify, render_template ,make_response
import numpy as np
import requests
from datetime import date
import time
import datetime
import csv
import pandas as pd
import os
app = Flask(__name__)

today =date.today()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/weather',methods =["GET", "POST"])
def weather():
    
    if request.method == "POST":
        city_name = request.form.get("cityname")
        s = request.form.get("s")
        e = request.form.get("e")
        sd = datetime.datetime.strptime(s, '%Y-%m-%d').date()
        ed = datetime.datetime.strptime(e, '%Y-%m-%d').date()

        start_date = abs(sd - today).days
        end_date = abs(ed - today).days

        URL="forecasts/latest"
        url="https://www.weather-forecast.com/locations/"
        
        req = requests.get(f'{url}{city_name}/{URL}')
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(req.content, 'lxml')
        day_name = soup.findAll("div" , {"class":"b-forecast__table-days-name"})
        day_date= soup.findAll("div" , {"class":"b-forecast__table-days-date"})
        
        

        weather_max_temp = soup.find("tr" , {"class":"b-forecast__table-max-temperature js-temp"})
        max_temp_value = weather_max_temp.findAll("span" , {"class":"temp b-forecast__table-value"})
        
        weather_min_temp = soup.find("tr" , {"class":"b-forecast__table-min-temperature js-min-temp"})
        min_temp_value = weather_min_temp.findAll("span" , {"class":"b-forecast__table-value"})
        

        weather_wind = soup.find("tr" , {"class":"b-forecast__table-wind js-wind"})
        wind_value = weather_wind.findAll("text" , {"class":"wind-icon-val"})
        

        rain=soup.find('tr',{'class':"b-forecast__table-rain js-rain"})
        weather_rain=rain.findAll('span',{"class":"rain b-forecast__table-value"})
        
     

        weather_chill = soup.find("tr" , {"class":"b-forecast__table-chill js-chill"})
        chill_val = weather_chill.findAll("span" , {"class":"temp b-forecast__table-value"})
        
      

        weather_humidity = soup.find("tr" , {"class":"b-forecast__table-humidity js-humidity"})
        humidity_val = weather_humidity.findAll("span" , {"class":"b-forecast__table-value"})
        
    
    df = pd.DataFrame()
    with open( city_name + '.csv',mode = 'w') as csv_file:
        fieldnames = ['Days_Name',
                  'Date_Name',
                  'Max_Temp\n[AM,PM,Night]',
                  'Min_Temp\n[AM,PM,Night]',
                  'Wind\n[AM,PM,Night]',
                  'Rain\n[AM,PM,Night]',
                  'Chill\n[AM,PM,Night]',
                  'Humidity\n[AM,PM,Night]',
        ]
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
        for (i,y) in zip(range(start_date,end_date+1),range(0,34,3)):
            #print(y)
            a={
            'Days_Name':str(day_name[i].text),
            'Date_Name':str(day_date[i].text),
            'Max_Temp\n[AM,PM,Night]':[str(max_temp_value[y].text),str(max_temp_value[y+1].text),str(max_temp_value[y+2].text)],
            'Min_Temp\n[AM,PM,Night]':[str(min_temp_value[y].text),str(min_temp_value[y+1].text),str(min_temp_value[y+2].text)],
            'Wind\n[AM,PM,Night]':[str(wind_value[y].text),str(wind_value[y+1].text),str(wind_value[y+2].text)],              
            'Rain\n[AM,PM,Night]':[str(weather_rain[y].text),str(weather_rain[y+1].text),str(weather_rain[y+2].text)],              
            'Chill\n[AM,PM,Night]':[str(chill_val[y].text),str(chill_val[y+1].text),str(chill_val[y+2].text)],              
            'Humidity\n[AM,PM,Night]':[str(humidity_val[y].text),str(humidity_val[y+1].text),str(humidity_val[y+2].text)],              
            
            }
            df = df.append(a, ignore_index = True)
        response =make_response(df.to_csv())
        response.headers["Content-Disposition"] = "attachment; filename="+city_name + '.csv'
        return response
        

if __name__ == "__main__":
    app.run(debug=True)
