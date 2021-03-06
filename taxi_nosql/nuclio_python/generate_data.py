import requests
import os
import json
from decimal import *
from random import *

def handler(context, event):

    # Get the IP and port of the ingestion function from environment variables
    # defined using Nuclio
    INGEST_URL = os.getenv ("INGEST_URL")
    
    # List of GPS coordinates for randomly selected locations
    # TODO: Modify the list, as needed, to use your preferred locations.
    Downtown_London = [-0.1195,51.5033]
    Westminster = [-0.1357,51.4975]
    Oxford_St = [-0.1410,51.5154]
    Heathrow = [-0.4543,51.4700]
    Heathrow_Parking = [-0.4473,51.4599]
    Gatwick =  [0.1821,51.1537]
    Canary_Wharf = [-0.0235,51.5054]
    Locations = [Canary_Wharf,Canary_Wharf,Downtown_London,Westminster,Oxford_St,Oxford_St,Oxford_St,Heathrow,Heathrow_Parking,Gatwick]

    # Get IP and Port of the ingestion function from environment variables defined using Nuclio
    INGEST_URL = os.getenv ("INGEST_URL")

    # Create a session for sending requests for ingestion
    s = requests.Session()
    request_json = {}

    # Generate random driver locations for 1000 drivers and send the data for
    # ingestion
    for x in range (1,1000):
        rnd_driver = randint (1,5000)
        rnd_location = randint (0,9)
        rnd_radius =randint (0,8)
        rnd_long = randint (-rnd_radius,rnd_radius)
        rnd_lat  = randint (-rnd_radius,rnd_radius)
        longitude =  Decimal (Locations[rnd_location][0]) + (Decimal (rnd_long) / Decimal (300))
        latitude = Decimal (Locations[rnd_location][1])  + (Decimal (rnd_lat) / Decimal (300))
        
        #context.logger.info('driver id - '+ str(rnd_driver))

        # Build a JSON request body
        request_json["RecordType"] = "driver"
        request_json["ID"] = rnd_driver
        request_json["longitude"] = str (longitude)
        request_json["latitude"] = str (latitude)
        
        payload = json.dumps(request_json)

        # Send a request to the ingestion function
        res = s.put(INGEST_URL, data=payload)
        if res.status_code != requests.codes.ok:
            context.logger.error("Ingestion of drivers failed with error code :"+str(res.status_code))
            return context.Response(body='Ingestion of driver failed',
                            headers={},
                            content_type='text/plain',
                            status_code=500)
        

   # Generate random location for 1,500 passengers and send for ingestion
    for x in range (1,500):
        rnd_driver = randint (1,5000)
        rnd_location = randint (0,9)
        rnd_radius =randint (0,8)
        rnd_long = randint (-rnd_radius,rnd_radius)
        rnd_lat  = randint (-rnd_radius,rnd_radius)
        longitude =  Decimal (Locations[rnd_location][0]) + (Decimal (rnd_long) / Decimal (300))
        latitude = Decimal (Locations[rnd_location][1])  + (Decimal (rnd_lat) / Decimal (300))
        
        #context.logger.info('passenger id - '+ str(rnd_driver))

        # Build a JSON request body
        request_json["RecordType"] = "passenger"
        request_json["ID"] = rnd_driver
        request_json["longitude"] = str (longitude)
        request_json["latitude"] = str (latitude)
        
        payload = json.dumps(request_json)

        # Send a request to the ingestion function
        res = s.put(INGEST_URL, data=payload)
        
        if res.status_code != requests.codes.ok:
            context.logger.error("Ingestion of passengers failed with error code :"+str(res.status_code))
            return context.Response(body='Ingestion of passengers failed',
                            headers={},
                            content_type='text/plain',
                            status_code=500)

    context.logger.info('End - Generating Data')

    return context.Response(body='Ingestion of drivers and passengers completed successfully',
                            headers={},
                            content_type='text/plain',
                            status_code=200)

