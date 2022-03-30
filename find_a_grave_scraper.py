"""
Helper functions to scrape findagrave.com
"""
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_file(first_name, last_name, page):
    """
    Gets the raw HTML from a specified page of findagrave.com.

    Args:
        first_name: A string representing the first name of the person to search
        last_name: A string representing the last name of the person to search
        page: A string representing the page number of findagrave.com to scrape

    Returns:
        The raw HTML of the scraped page
    """
    # define search url based on user input
    url = (
        f'https://www.findagrave.com/memorial/search?firstname={first_name}&'
        f'middlename=&lastname={last_name}&birthyear=&birthyearfilter=&'
        'deathyear=&deathyearfilter=&location=&locationId=&memorialid=&mcid=&'
        f'linkedToName=&datefilter=&orderby=r&plot=&page={page}#sr-1075')

    page_html = requests.get(url) # HTML from URL

    # successful url request code is 200
    if page_html.status_code != 200:
        sys.exit('Connection Failed.') # stop execution and return error

    return page_html


def collect_birth_and_death(memorial_item):
    """
    Separate and clean up years of birth and death if they exist.

    Args:
        memorial_item: container representing a grave in the database

    Returns:
        A list containing the birth and death year
    """
    if memorial_item.find(class_ = 'birthDeathDates') is not None and\
    'unknown' not in memorial_item.find(class_ = 'birthDeathDates').string:
        # dates of birth/death are stored in class 'birthDeathDates'
        date = memorial_item.find(class_ = 'birthDeathDates').string
        # split birth and death dates
        birth_death_raw = date.split('–')

        # clean up date formatting, set default null list to write over
        birth_death = ['NA', 'NA']
        for index, date in enumerate(birth_death_raw):
            # get rid of letters
            date = "".join(filter(str.isdigit, date))
            # as long as the string is greater than 3 charaters (a
            # month abbreviation) take the last 4 characters (the year)
            date = date.strip()
            if len(date) > 3:
                date = date[-4:]
            else: break # don't include data, years default to NA
            birth_death[index] = date
    else: birth_death = ['NA', 'NA'] # birth and death years not known
    return birth_death


def scrape_memorials(memorial_list,first_name='George',last_name='Washington'):
    """
    Processes the data from each grave entry and adds it to the dataframe.

    Args:
        memorial_list: list containing all graves in database
        first_name: optional string representing first name. Defaults to George
        last_name: optional string representing first name. Defaults to
        Washington

    Returns:
        A dataframe with processed data for every George Washington.
    """
    # Define the empty dataframe
    data_table = pd.DataFrame(columns = ['Names',
                                         'Birth Year',
                                         'Death Year',
                                         'Location of Grave'])
    for memorial_item in memorial_list:
        # double check that the memorial has a name
        if memorial_item.find('i') is None\
        or memorial_item.find('i').string is None:
            continue # skip to next memorial without recording data

        # double check for the name George Washington
        if first_name+' ' in memorial_item.find('i').string\
        and ' '+ last_name in memorial_item.find('i').string:
            # collect the exact name (including title and/or middle name)
            name = memorial_item.find('i').string
        else: continue # skip to next memorial without recording data

        # check for and get grave address
        if memorial_item.find('p', attrs = {'class':'addr-cemet'}) is not None:
            # find the text in <p> with class = addr-cemet
            grave_address = memorial_item.find('p', attrs={'class':'addr-cemet'}).string
        else: continue # skip to next memorial without recording data

        # dates of birth and death
        birth_death = collect_birth_and_death(memorial_item)
        if birth_death == ['NA', 'NA']:
            continue # don't include unknown years, skip to next memorial

        # add scraped data to the data frame
        data_table = data_table.append({'Names': name.strip(),
                                        'Birth Year': birth_death[0],
                                        'Death Year': birth_death[1],
                                        'Location of Grave': grave_address},
                                        ignore_index= True)
    return data_table


def collect_and_sort_data(first_name='George', last_name='Washington'):
    """
    Scrape through all pages with relevant results and organize the data from
    each grave into a dataframe.

    Args:
        first_name: optional string representing first name. Defaults to George
        last_name: optional string representing first name. Defaults to
        Washington

    Returns:
        A dataframe with the final processed data for every George Washington.
    """
    # get HTML of first page
    page = get_file(first_name, last_name, '1')
    # parse HTML into Beautiful Soup format
    parsed = BeautifulSoup(page.content, 'html.parser')

    # find the max page number
    max_page = (parsed.find(id = 'gotoPage'))['max']

    # collect data from all pages
    memorial_list = []
    for page_number in range(int(max_page)):
        # get HTML of specified page number
        page = get_file(first_name, last_name, str(page_number + 1))
        # parse HTML into Beautiful Soup format
        parsed = BeautifulSoup(page.content, 'html.parser')
        # each memorial-item is a tag for a grave entry in the database
        memorial_list.extend(parsed.find_all(class_ = 'memorial-item'))

    # Iterate through each memorial and collect useful data
    data_table = scrape_memorials(memorial_list)

    # findagrave.com has some duplicate entries, only keep the first occurrence
    data_table = data_table.drop_duplicates(keep='first')

    return data_table
