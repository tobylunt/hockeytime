# Scrape hockey birthplaces and basic stats from hockey-reference.com
# code modified from: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

# import libraries
import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
import numpy as np
import glob

# specify the url
base_url = 'https://www.hockey-reference.com/friv/birthplaces.cgi'

# get the main index page
main = requests.get(base_url)

# add to beautiful soup
soup = BeautifulSoup(main.text, 'html.parser')

# find the grid with birthplace IDs
grid = soup.find("div", {"id": "div_birthplace"})

# separate out all the links into a list, and the names into another list
links = []
names = []
for link in grid.find_all('a'):
    links += ['https://www.hockey-reference.com/' + link['href']]
    names += [link.string]

# make a directory for individual webpages
newpath = 'tempdata' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    
# query all the individual webpages (states) in a loop
for i in range(0, len(links)):

    # get the place name into a string
    place_spaces = names[i]

    # replace spaces with underscores
    place = place_spaces.replace("\xa0", "_")
    
    # get the url
    link = links[i]
    
    # query the website and return the html to the variable ‘page’
    page = requests.get(link)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.text, 'html.parser')

    # cull the multicolumn super-headers (e.g. goalie stats)
    for tr in soup.find_all('tr', {'class':'over_header'}): 
        tr.decompose()

    # identify table
    table = soup.find('table')

    # separate table header and table body
    thead = soup.find('thead')
    tbody = soup.find('tbody')

    # find header rows 
    headers = [header.text for header in thead.find_all('th')]

    # cull the mid-table reminder headers from the table body
    for tr in tbody.find_all('tr', {'class':'thead'}): 
        tr.decompose()

    # data rows - need to remove "thead rowSum" classes, which are mid-table header rows
    rows = []
    for row in tbody.find_all('tr'):
        rows.append([val.text for val in row.find_all(['th','td'])])

    # write to csv, remove old csv
    with open('tempdata/%s.csv' % place, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

# write in a variable including the state name to all CSVs, and append all. first loop over all files
for filename in os.listdir(newpath):
    
    # read in the csv
    data = pd.read_csv(newpath+'/'+filename, delimiter=',')
    
    # remove the '.csv' and underscores to get the state name
    fn_clean = filename.replace('_',' ')
    fn_clean = fn_clean.replace('.csv','')

    # generate a variable
    data['State'] = fn_clean

    # write out the csv
    data.to_csv(newpath+'/'+filename, index=False)

# get all of our files into an object
all_files = glob.glob(newpath + "/*.csv")

# now append all of them
master = pd.concat((pd.read_csv(f) for f in all_files))
    
# write out the master dataset
data.to_csv('master.csv', index=False)

# tar up the individual state data, just in case
os.system("tar czfv states.tar.gz tempdata/")

# remove the working directory
os.system("rm -rf tempdata/")  
