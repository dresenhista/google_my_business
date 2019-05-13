
# Pulling Reviews from Google My Business with Python

As a side project at work I wanted to analyze the reasons why our customers (Paybright) give us reviews, either negative or positive.
After stumbling on a few scripts that did not work, I decided it was time to build my own.

## But First
Before we start pulling data we need to be allowed to use the API by Google.
The process is simple but long, basically:
1. Create a project in the Google API Console, just like described in here: https://developers.google.com/my-business/content/prereqs
2. Apply for an access and wait. In this step you do need to have an email from the business you are trying to get access. 
3. Then after you receive the email confirming your access, you need to extract the files as explained in this link https://developers.google.com/my-business/content/basic-setup

I am also following the initial instructions provided in this link on how to use python and GMB
https://developers.google.com/my-business/content/python

Now that you have your token file plus the business information file let's pull the data. You will need to import the libraries below, so make sure you have them installed into Jupyter/Python.




```python
import sys	
import json
from pprint import pprint
from googleapiclient import sample_tools
from googleapiclient.http import build_http
import pandas as pd
import IPython
```


```python
#Business file exported from the API Console project page: 
discovery_doc = "myBusiness_discovery.json"
```

## Now that we are ready
This code will not work on jupyter because of __doc__ and __file__ that are unavailable for, therefore use the sample.py file in this repository.


The business I am working on only has one location, therefore I am returning only the first location, if your business has multiple locations, you might want to change the function below. Instead of calling 
locationsList["locations"][0]["name"] you will have multiple items in the list.

```python
def location():
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    currentNotebook = IPython.notebookname()

    service, flags = sample_tools.init(['Google Reviews.ipynb'], "mybusiness", "v4", __doc__, __file__, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)
    output = service.accounts().list().execute()

    # print("List of Accounts:\n")
    # print(json.dumps(output, indent=2) + "\n")

    firstAccount = output["accounts"][0]["name"]
    # Get the list of locations for the first account in the list
    # print("List of Locations for Account " + firstAccount)
    locationsList = service.accounts().locations().list(parent=firstAccount).execute()
    firstLocation = locationsList["locations"][0]["name"]
    return firstLocation  
```

There are a few things you can do using the API, but I want to pull the users reviews for my business.
Usually Google allows you to pull a page at a time and a page has 200 reviews. The function below allows you to interact through these pages and save all the reviews.:


```python
def reviews(location):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    currentNotebook = IPython.foo.bar.notebookname()
    service, flags = sample_tools.init(['sample.py'], "mybusiness", "v4", __doc__, currentNotebook, scope="https://www.googleapis.com/auth/business.manage", discovery_filename=discovery_doc)

    reviewsApi = service.accounts().locations().reviews()
    request = reviewsApi.list(parent=location)
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
```

The output of the file is a Json format file, so we want to flat it before we load it into a csv.


```python
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
```

Finally we are ready to export it to a csv


```python

def export_csv(reviews_dict, dest='reviews.csv'):
    df = pd.DataFrame(flatlist(reviews_dict))
    output = open(dest, 'w', encoding="utf-8")
    output.write(df.to_csv())
```

and now we call the functions


```python
def main(argv):
    export_csv(reviews(location()))

```

At the end of this project, you should have a reviews.csv file with the json data broken out into columns. 

