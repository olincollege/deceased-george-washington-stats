
from bs4 import BeautifulSoup
import requests
import sys


def get_file(first_name ="George", last_name="Washington", page="1"):
    # define search url based on user input
    url = (
        f"https://www.findagrave.com/memorial/search?firstname={first_name}&"
        f"middlename=&lastname={last_name}&birthyear=&birthyearfilter=&"
        "deathyear=&deathyearfilter=&location=&locationId=&memorialid=&mcid=&"
        f"linkedToName=&datefilter=&orderby=b&plot=&page={page}#sr-1075")

    site_HTML = requests.get(url) # HTML from URL

    # successful url request code is 200
    if site_HTML.status_code != 200:
        sys.exit("Connection Failed.") # stop execution and return error

    return site_HTML


def get_info(first_name ="George", last_name="Washington"):
    # get HTML of 1st page
    site = get_file(first_name, last_name)

    # Parse HTML into Beautiful Soup format
    parsed = BeautifulSoup(site.content, "html.parser")

    #Find the div containing the maximum number of pages
    max_page = parsed.find(id = "gotoPage")

    #max_page functions as a dictionary where we can enter the
    #string of any element in the div to find its value
    max_page = max_page["max"]

    #TODO: get data for every page in range
    #TODO: try to limit file size

    return max_page #! TEMPORARY


#! TEST
print(get_info())
