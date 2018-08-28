# Scrape hockey birthplaces and basic stats from hockey-reference.com
# code modified from: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe

# import libraries
#from urlparse import urljoin
import requests
from bs4 import BeautifulSoup

# specify the url
#base_url = 
state_url = 'https://www.hockey-reference.com/friv/birthplaces.cgi?country=US&province=&state=AL'

# query the website and return the html to the variable ‘page’
response = get(state_url)
print(response.text[:100])

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(response.text, 'html.parser')

# cull the multicolumn super-headers (e.g. goalie stats)
for tr in soup.find_all("tr", {'class':'over_header'}): 
    tr.decompose()

# identify table
table = soup.find_all('table')

# split out our table rows
rows = table.find('th')

#
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        print("The value in this cell is %s" % value)

print(type(player_rows))
print(len(player_rows))


# Take out the <div> of name and get its value
name_box = html_soup.find('h1', attrs={'class': 'name'})

# strip() is used to remove starting and trailing
name = name_box.text.strip() 
print name

# get the index price
price_box = soup.find(‘div’, attrs={‘class’:’price’})
price = price_box.text
print price


ONCE ON STATE/COUNTRY PAGE
loop over data-row from 0:no mas
player year_min year_max pos games_played goals assists points plus_minus pen_min games_goalie wins_goalie losses_goalie ties_goalie save_pct goals_against_avg birth_city birth_date death_date
