import sys  
import json

from pprint import pprint

from googleapiclient import sample_tools
from googleapiclient.http import build_http

import pandas as pd

discovery_doc = "myBusiness_discovery.json"

# GET https://mybusiness.googleapis.com/v4/accounts/account_name/locations/location_name/reviews

def flattenjson( b, delim="__" ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val

def flatlist(items):
    return [flattenjson(item) for item in items]

def location():
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(['sample.py'], "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)
    output = service.accounts().list().execute()

    # print("List of Accounts:\n")
    # print(json.dumps(output, indent=2) + "\n")

    firstAccount = output["accounts"][0]["name"]
    # Get the list of locations for the first account in the list
    # print("List of Locations for Account " + firstAccount)
    locationsList = service.accounts().locations().list(parent=firstAccount).execute()
    locations_all = []

    for each_location in locationsList["locations"]:
        locations_all.append(each_location["name"]) 
        

    
    firstLocation = locationsList["locations"][0]["name"]

    return locations_all  

def reviews(location):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(['sample.py'], "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)
    reviewsApi = service.accounts().locations().reviews()


    for each_location in location: 
        print(each_location)
        request = reviewsApi.list(parent=each_location)
    #reviewsList = request.execute()
    reviews = []

    # pagination
    # https://developers.google.com/api-client-library/python/guide/pagination
    while request is not None:
      response = request.execute()

      # Do something with the activities
      reviews += response["reviews"]

      request = reviewsApi.list_next(request, response) # all pages
      # request = None # first page only

    print(len(reviews))
    return reviews

def export_csv(reviews_dict, dest='reviews.csv'):
    df = pd.DataFrame(flatlist(reviews_dict))
    output = open(dest, 'w', encoding="utf-8")
    output.write(df.to_csv())

def main(argv):
    export_csv(reviews(location()))
    
if __name__ == "__main__":
  main(sys.argv)