'''
Created on 19 Feb 2019

@author: Ciaran
'''

import sqlalchemy as sqla
import requests as req
import pandas as pd
import time
import json

with open('../authentication.txt') as f:
    auth=f.read().split('\n')
    
Key=auth[0]
Contract=auth[1]
URL =auth[2]
LOG =auth[3]
PWD =auth[4]
DB  =auth[5]
TAB =auth[6]
PORT=auth[7]

ENG ="mysql+mysqldb://{0}:{1}@{2}:{3}/{4}".format(LOG,PWD,URL,PORT,DB)

engine = sqla.create_engine(ENG,echo=False)

def scrape_dynamic_data():
    
    response = req.get('https://api.jcdecaux.com/vls/v1/stations?contract={0}&apiKey={1}'.format(Contract,Key))
    Data = pd.DataFrame(response.json())
    
    available_bike_stands = Data['available_bike_stands']
    available_bikes = Data['available_bikes']
    bike_stands = Data['bike_stands']
    last_update = Data['last_update']
    number = Data['number']
    status = Data['status']
    
    print(Data.shape[0])
    
    for i in range(Data.shape[0]):

        SQL = """
        INSERT INTO {0}.{1} (available_bike_stands,
                   available_bikes,
                   bike_stands,
                   last_update,
                   number,
                   status)
        VALUES ({2}, {3}, {4}, {5}, {6}, \"{7}\")
        """.format(
            DB,
            TAB,
            available_bike_stands[i],
            available_bikes[i],
            bike_stands[i],
            last_update[i],
            number[i],
            status[i])

        try: 
            engine.execute(SQL)

        except:
            pass

def continuous_scrape():
    
    while True:
        
        #scrape data and write to RDS DB
        scrape_dynamic_data()

#         dtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         print('{} pieces of Data written to DublinBikesDB.dynamic at {}'.format(counter,dtime))

        # sleep for 5 mins - runtime
        time.sleep(60)
        
continuous_scrape()