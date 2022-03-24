
from bs4 import BeautifulSoup
import requests
import sys
import json


def get_file(first_name ="George", last_name="Washington", page="1"):
    # define search url based on user input
    url = (
        f"https://www.findagrave.com/memorial/search?firstname={first_name}&"
        f"middlename=&lastname={last_name}&birthyear=&birthyearfilter=&"
        "deathyear=&deathyearfilter=&location=&locationId=&memorialid=&mcid=&"
        f"linkedToName=&datefilter=&orderby=b&plot=&page={page}#sr-1075")

    page_HTML = requests.get(url) # HTML from URL

    # successful url request code is 200
    if page_HTML.status_code != 200:
        sys.exit("Connection Failed.") # stop execution and return error

    return page_HTML


def get_info(first_name ="George", last_name="Washington"):
    # get HTML of specified page number
    page = get_file(first_name, last_name, 1)

    # Parse HTML into Beautiful Soup format
    parsed = BeautifulSoup(page.content, "html.parser")

    #Find the div containing the maximum number of pages
    max_page = parsed.find(id = "gotoPage")

    #max_page functions as a dictionary where we can enter the
    #string of any element in the div to find its value
    max_page = max_page["max"]

    #Create a list of all tag with an attribute class "memorial-item"
    #tags act like containers that contain attributes and text
    grave_infos = parsed.find_all(class_ = "memorial-item")

    #select the first item of the list
    grave_info = grave_infos[0]

    #find the text contained within the <i> tag
    name = grave_info.find("i").string

    print(name)
    #TODO: get data for every page in range
    #TODO: try to limit file size

    return max_page #! TEMPORARY


#! TEST
print(get_info())
