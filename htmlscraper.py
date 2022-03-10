# Packages to download ahead of time
# requests
# beautifulsoup4

#Load Packages

from bs4 import BeautifulSoup

import requests


def scraper(Firstname,Lastname):

    #Section 1: recording the website page as an .html file

    #Define the url based on user input
    url = (
        f"https://www.findagrave.com/memorial/search?firstname={Firstname}"
        f"&middlename=&lastname={Lastname}&birthyear=&birthyearfilter=&death"
        "year=&deathyearfilter=&location=&locationId=&memorialid=&mcid=&linked"
        "ToName=&datefilter=&orderby=r&plot="
    )

    #produce html file from url of main page
    search_result = requests.get(url)

    #Section 2: Sparsing the html and finding the desired elements

    #Use beautiful soup to parse the html
    parsed = BeautifulSoup(search_result.content, "html.parser")

    #Find the div containing the maximum number of pages
    max_page = parsed.find(id = "gotoPage")

    #max_page functions as a dictionary where we can enter the
    #string of any element in the div to find its value
    max_page = max_page["max"]









    return search_result

#if the requests.get url request is successful its status code will be 200,
# unsuccessful if the status code is 404
if scraper("George", "Washington").status_code is not 200:
    print("Connection to URL Failed")


