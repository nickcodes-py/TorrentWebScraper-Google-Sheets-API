import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests


##################################
# Google Sheets API
##################################

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('spartan-concord-245721-111434f4cb2e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("PythonProjectSheet")
worksheet = wks.worksheet('A worksheet')
list_of_lists = worksheet.get_all_values()
#Print out spreadsheet
def AllValues():
    for x in list_of_lists:
        print(x)


##################################
# Web Scraper
##################################

#Replace this with appropriate category to scrap (Movies : 201 , Games : 400, Gucci : 500 )

page = requests.get('https://uj3wazyk5u4hnvtk.onio.icu/top/201')
soup = BeautifulSoup(page.content, 'html.parser')

tags = soup.find('table', {'id': 'searchResult'})

downlinks = []     #List for all download links
filetitles = []    #List for all names of file
# For extracting the Magnet Links
for magnetlinks in tags.find_all('a', {'title': 'Download this torrent using magnet'}):
    downlinks.append(magnetlinks.get('href'))

# For extracting the names of Movies
for title in tags.find_all('a', {'class': 'detLink'}):
    filetitles.append(title.get('title'))


##################################
# Sending Out Data to Spreadsheet
##################################


#Printing Name Data to Spreadsheet
cell_list = worksheet.range('A1:A100')
x=0
for cell in cell_list:
    cell.value = filetitles[x]
    x = x+1

# Update in batch
worksheet.update_cells(cell_list)

#Printing Link Data to Spreadsheet
cell_list = worksheet.range('B1:B100')
z=0
for cell in cell_list:
    cell.value = downlinks[z]
    z = z+1

# Update in batch
worksheet.update_cells(cell_list)