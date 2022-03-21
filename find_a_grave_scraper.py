from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd


def get_file(first_name, last_name, page):
    # define search url based on user input
    url = (
        f"https://www.findagrave.com/memorial/search?firstname={first_name}&"
        f"middlename=&lastname={last_name}&birthyear=&birthyearfilter=&"
        "deathyear=&deathyearfilter=&location=&locationId=&memorialid=&mcid=&"
        f"linkedToName=&datefilter=&orderby=r&plot=&page={page}#sr-1075")

    page_HTML = requests.get(url) # HTML from URL

    # successful url request code is 200
    if page_HTML.status_code != 200:
        sys.exit("Connection Failed.") # stop execution and return error

    return page_HTML


def get_info(first_name="George", last_name="Washington"):
    # Define the empty dataframe
    data_table = pd.DataFrame(columns = ["Names", "Birth Year", "Death Year", "Location of Grave"])

    # get HTML of first page
    page = get_file(first_name, last_name, "1")
    # parse HTML into Beautiful Soup format
    parsed = BeautifulSoup(page.content, "html.parser")

    # find the div containing the maximum number of pages and specify the max
    # element in the BeautifulSoup data structure as if it was a dictionary with
    # a key value "max"
    max_page = (parsed.find(id = "gotoPage"))["max"]

    # collect data from all pages
    for page_number in range(int(max_page)):

        # get HTML of specified page number
        page = get_file(first_name, last_name, str(page_number + 1))

        # parse HTML into Beautiful Soup format
        parsed = BeautifulSoup(page.content, "html.parser")

        # each memorial-item is a tag for a grave entry in the database
        # HTML note: tags act like containers that contain attributes and text
        memorial_list = parsed.find_all(class_ = "memorial-item")

        # Iterate through each memorial and only collect useful data
        for memorial_item in memorial_list:
            # double check that first name is George and last name is Washington
            # A blank space after first name eliminates the possibility of names like "Georgette"
            if memorial_item.find("i") is not None and memorial_item.find("i").string is not None and first_name+' ' in memorial_item.find("i").string and ''+ last_name in memorial_item.find("i").string:
                # if it passes all these tests, take the the data from this memorial
                name = memorial_item.find("i").string

                # grave address
                if memorial_item.find("p", attrs = {'class':'addr-cemet'}) is not None:
                    # find the text in <p> with class = addr-cemet
                    grave_address = memorial_item.find("p", attrs = {'class':'addr-cemet'}).string
                else: # skip to next memorial without recording data
                    continue

                # dates of birth and death
                if memorial_item.find(class_ = "birthDeathDates") is not None and "unknown" not in memorial_item.find(class_ = "birthDeathDates").string:
                    # dates of birth/death are stored in class "birthDeathDates"
                    date = memorial_item.find(class_ = "birthDeathDates").string

                    # split birth and death dates
                    birth_death_raw = date.split("–")

                    # clean up date formatting
                    birth_death = ["NA", "NA"]
                    for index, date in enumerate(birth_death_raw):
                        # get rid of letters
                        date = "".join(filter(str.isdigit, date))
                        # as long as the string is greater than 3 charaters (a
                        # month abbreviation) take the last 4 characters (the
                        # year)
                        date = date.strip()
                        if len(date) > 3:
                            date = date[-4:]
                        else: # don't include data, years default to NA
                            break
                        birth_death[index] = date

                    # don't include unknown years, skip to next memorial
                    if birth_death == ["NA", "NA"]:
                        continue

                    birth_year = birth_death[0]
                    death_year = birth_death[1]

                else: # skip to next memorial without recording data
                    continue

                # record scraped data in data frame
                data_table = data_table.append({"Names": name.strip(), "Birth Year": birth_year, "Death Year": death_year, "Location of Grave": grave_address}, ignore_index= True)

    # findagrave.com has quite a few duplicate entries
    data_table = data_table.drop_duplicates(keep="first")

    return data_table
