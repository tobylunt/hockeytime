# Scrape hockey birthplaces and basic stats from hockey-reference.com
# code modified from: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

# import libraries
import requests
from bs4 import BeautifulSoup
import csv

# specify the url
#base_url = 
state_url = 'https://www.hockey-reference.com/friv/birthplaces.cgi?country=US&province=&state=AL'

# query the website and return the html to the variable ‘page’
page = requests.get(state_url)
print(page.text[:100])

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.text, 'html.parser')

# cull the multicolumn super-headers (e.g. goalie stats)
for tr in soup.find_all("tr", {'class':'over_header'}): 
    tr.decompose()

# identify table
table = soup.find('table')

# separate table header and table body
thead = soup.find('thead')
tbody = soup.find('tbody')

# find header rows
headers = [header.text for header in thead.find_all('th')]

# data rows
rows = []
for row in tbody.find_all('tr'):
    rows.append([val.text for val in row.find_all(['th','td'])])

# write to csv
with open('output_file.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)

