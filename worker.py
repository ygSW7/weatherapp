import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging

def fetch_data():
    api_token = '94cb87254df829dd'

    url = 'http://api.wunderground.com/api/' + api_token + '/conditions/q/GB/London.json'
    r = requests.get(url).json()
    data = r['current_observation']


    location = data['observation_location']['full'] #city, state and observation location
    weather = data['weather'] # cloud, clear, etc
    wind_str = data['wind_string'] # pretty print version of wind speed and dir
    temp = data['temp_c'] # temperature in Celsius
    humidity = data['relative_humidity'] # humidity with %
    precip = data['precip_today_string'] # displays total precip in inches amd mm
    icon_url = data['icon_url'] # url for weather icon (clear, cloud, rainy, etc)
    observation_time = data['observation_time'] # pretty print of observation time

    #print(r)
    # open DB

    try:
        conn = psycopg2.connect(dbname='weather', user='postgres', host='localhost', password='YGKen-2014')
        print('Opened DB successfully')
    except:
        print(datetime.now(), "Unable to connect the database")
        logging.exception("Unable to open the database")
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # write data to db
    cur.execute("""INSERT INTO station_reading(location, weather, wind_str, temp, humidity, precip, icon_url, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (location, weather, wind_str, temp, humidity, precip, icon_url,observation_time))

    conn.commit()
    cur.close()
    conn.close() # CONNECTION CLOSE

    print("Data Written", datetime.now()) # DATA INSERTION SUCCESSFUL WITH A TIME STAMP

fetch_data()
